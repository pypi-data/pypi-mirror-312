from __future__ import annotations

from typing import Union, Tuple, Any
import re
import numbers
from functools import total_ordering
from dataclasses import dataclass

@dataclass(frozen=True)
class VersionInfo:
    """Immutable container for version information."""
    major: int
    minor: int
    micro: int = 0

    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to tuple representation."""
        return (self.major, self.minor, self.micro)

@total_ordering
class BaseVersion:
    """Abstract base class for version implementations."""
    
    def __init__(self) -> None:
        self._version_info: VersionInfo

    @property
    def version_info(self) -> VersionInfo:
        """Get version information."""
        return self._version_info

    @property
    def major(self) -> int:
        """Major version number."""
        return self._version_info.major

    @property
    def minor(self) -> int:
        """Minor version number."""
        return self._version_info.minor

    @property
    def micro(self) -> int:
        """Micro (patch) version number."""
        return self._version_info.micro

    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to tuple representation."""
        return self._version_info.to_tuple()

    @classmethod
    def _validate_integers(cls, *values: Any) -> None:
        """Validate that all values are positive integers."""
        if not all(isinstance(v, int) and v >= 0 for v in values):
            raise ValueError("Version components must be non-negative integers")

    @classmethod
    def cast(cls: Type[T], other: Any) -> T:
        """Cast a value to a Version instance.
        
        Parameters
        ----------
        other : Any
            Value to cast to Version
            
        Returns
        -------
        T
            Version instance of the same class
            
        Raises
        ------
        TypeError
            If the value cannot be cast to a Version
        """
        if isinstance(other, cls):
            return other
        if isinstance(other, BaseVersion):
            return cls(other.to_tuple())
        try:
            return cls(other)
        except (ValueError, TypeError) as e:
            raise TypeError(
                f"Cannot cast {type(other).__name__} to {cls.__name__}"
            ) from e

    def __eq__(self, other: object) -> bool:
        """Compare versions for equality."""
        other_version = self.__class__.cast(other)
        return self.to_tuple() == other_version.to_tuple()

    def __lt__(self, other: object) -> bool:
        """Compare if this version is less than another."""
        other_version = self.__class__.cast(other)
        return self.to_tuple() < other_version.to_tuple()

    def __hash__(self) -> int:
        """Hash the version based on its tuple representation."""
        return hash(self.to_tuple())

class Version(BaseVersion):
    """A class to represent and compare package versions.

    This class handles version numbers in multiple formats:
    - String: "major.minor.micro" or "major.minor"
    - Tuple: (major, minor, micro) or (major, minor)
    - Version: another Version instance
    - VersionInfo: a VersionInfo instance

    Parameters
    ----------
    version : Union[str, Tuple[int, ...], Version, VersionInfo]
        The version information in one of the supported formats.

    Raises
    ------
    ValueError
        If the version format is invalid or contains invalid values
    TypeError
        If the version input is of an unsupported type
    """

    _VERSION_PATTERN = re.compile(r'^\d+(\.\d+){1,2}$')

    def __init__(
        self,
        version: Union[str, Tuple[int, ...], Version, VersionInfo]
    ) -> None:
        """Initialize a Version instance."""
        super().__init__()
        
        if isinstance(version, str):
            self._version_info = self._parse_version_string(version)
        elif isinstance(version, tuple):
            self._version_info = self._parse_version_tuple(version)
        elif isinstance(version, Version):
            self._version_info = version.version_info
        elif isinstance(version, VersionInfo):
            self._version_info = version
        else:
            raise TypeError(
                f"Version must be a string, tuple, Version, or VersionInfo instance, "
                f"not {type(version).__name__}"
            )

    @classmethod
    def _parse_version_string(cls, version: str) -> VersionInfo:
        """Parse a version string into VersionInfo.

        Parameters
        ----------
        version : str
            Version string in the format "x.y.z" or "x.y"

        Returns
        -------
        VersionInfo
            Parsed version information

        Raises
        ------
        ValueError
            If the version string format is invalid
        """
        if not cls._VERSION_PATTERN.match(version):
            raise ValueError(
                "Invalid version string format. Expected 'x.y.z' or 'x.y'"
            )

        try:
            parts = [int(part) for part in version.split('.')]
        except ValueError as e:
            raise ValueError("Version components must be valid integers") from e

        cls._validate_integers(*parts)
        
        if len(parts) == 2:
            return VersionInfo(parts[0], parts[1])
        return VersionInfo(*parts)

    @classmethod
    def _parse_version_tuple(cls, version: Tuple[int, ...]) -> VersionInfo:
        """Parse a version tuple into VersionInfo.

        Parameters
        ----------
        version : Tuple[int, ...]
            Version tuple in the format (x, y, z) or (x, y)

        Returns
        -------
        VersionInfo
            Parsed version information

        Raises
        ------
        ValueError
            If the tuple format is invalid
        """
        if not (2 <= len(version) <= 3):
            raise ValueError("Version tuple must have 2 or 3 elements")

        cls._validate_integers(*version)

        return VersionInfo(*version) if len(version) == 3 else VersionInfo(version[0], version[1])

    def __repr__(self) -> str:
        """Return a detailed string representation."""
        return f"{self.__class__.__name__}{self.to_tuple()}"

    def __str__(self) -> str:
        """Return a string representation."""
        return f"{self.major}.{self.minor}.{self.micro}"


class ROOTVersion(Version):
    """Class representing a ROOT version number.

    Handles version numbers in multiple formats:
    - Integer: 60000 (represents 6.00.00)
    - String: "6.20/04" or "6.20.04"
    - Tuple: (6, 20, 4)
    - Version/ROOTVersion: another version instance
    - VersionInfo: a VersionInfo instance

    Examples
    --------
    >>> ROOTVersion(60000)
    ROOTVersion(6, 0, 0)
    >>> ROOTVersion('6.20/04')
    ROOTVersion(6, 20, 4)
    >>> ROOTVersion((6, 20, 4))
    ROOTVersion(6, 20, 4)
    """

    _ROOT_VERSION_PATTERN = re.compile(
        r"(?P<major>\d+)\.(?P<minor>\d+)[./](?P<micro>\d+)"
    )

    def __init__(
        self,
        version: Union[int, str, Tuple[int, ...], Version, VersionInfo]
    ) -> None:
        """Initialize a ROOTVersion instance."""
        if isinstance(version, numbers.Integral):
            self._version_info = self._parse_version_int(version)
        else:
            super().__init__(version)

    @classmethod
    def _parse_version_int(cls, version: int) -> VersionInfo:
        """Parse an integer version number.

        Parameters
        ----------
        version : int
            Version number in format XYYZZ (X.YY.ZZ)

        Returns
        -------
        VersionInfo
            Parsed version information

        Raises
        ------
        ValueError
            If the version number is invalid
        """
        if version < 10000:
            raise ValueError(f"{version} is not a valid ROOT version integer")

        major = version // 10000
        minor = (version // 100) % 100
        micro = version % 100

        cls._validate_integers(major, minor, micro)
        return VersionInfo(major, minor, micro)

    @classmethod
    def _parse_version_string(cls, version: str) -> VersionInfo:
        """Parse a ROOT version string.

        Parameters
        ----------
        version : str
            Version string in format "X.YY/ZZ" or "X.YY.ZZ"

        Returns
        -------
        VersionInfo
            Parsed version information

        Raises
        ------
        ValueError
            If the version string format is invalid
        """
        match = cls._ROOT_VERSION_PATTERN.match(version)
        if not match:
            raise ValueError(f"'{version}' is not a valid ROOT version string")

        parts = [int(match.group(name)) for name in ('major', 'minor', 'micro')]
        cls._validate_integers(*parts)
        return VersionInfo(*parts)

    def __str__(self) -> str:
        """Return the ROOT-style string representation."""
        return f"{self.major}.{self.minor:02d}/{self.micro:02d}"

    def to_int(self) -> int:
        """Convert to ROOT integer version format.

        Returns
        -------
        int
            Version as integer in format XYYZZ
        """
        return self.major * 10000 + self.minor * 100 + self.micro