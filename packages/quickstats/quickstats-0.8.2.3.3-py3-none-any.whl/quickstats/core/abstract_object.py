"""
Base class providing output and verbosity control functionality.

This module defines the AbstractObject class which serves as a base for objects
requiring configurable verbosity and output handling.
"""

from __future__ import annotations

from typing import Any, ClassVar, Optional, Union, Type

from .decorators import hybridproperty
from .io import Verbosity, VerbosePrint


class AbstractObject:
    """
    Base class with verbosity control and standard output management.
    
    This class provides a foundation for objects that need configurable
    output verbosity and standardized output handling. It maintains both
    class-level and instance-level output controls.

    Parameters
    ----------
    verbosity : Optional[Union[int, str, Verbosity]]
        Verbosity level for output control. If None, uses class default.
    **kwargs : Any
        Additional keyword arguments for subclasses.

    Attributes
    ----------
    stdout : VerbosePrint
        Output handler with verbosity control.

    Examples
    --------
    >>> class MyObject(AbstractObject):
    ...     def process(self):
    ...         self.stdout.info("Processing...")
    ...
    >>> obj = MyObject(verbosity="DEBUG")
    >>> obj.stdout.debug("Debug message")
    [DEBUG] Debug message
    """

    # Class-level default output handler
    _class_stdout: ClassVar[VerbosePrint] = VerbosePrint(Verbosity.INFO)

    def __init__(
        self,
        verbosity: Optional[Union[int, str, Verbosity]] = None,
        **kwargs: Any
    ) -> None:
        """
        Initialize AbstractObject with specified verbosity.

        Parameters
        ----------
        verbosity : Optional[Union[int, str, Verbosity]]
            Verbosity level for output control
        **kwargs : Any
            Additional keyword arguments for subclasses
        """
        self._stdout: Optional[VerbosePrint] = None
        self.set_verbosity(verbosity)
        super().__init__()

    @hybridproperty
    def stdout(cls) -> VerbosePrint:
        """Get class-level output handler."""
        return cls._class_stdout

    @stdout.instance
    def stdout(self) -> VerbosePrint:
        """Get instance-level output handler."""
        return getattr(self, '_stdout', self.__class__._class_stdout)

    @property
    def debug_mode(self) -> bool:
        """
        Check if debug mode is enabled.

        Returns
        -------
        bool
            True if current verbosity is set to DEBUG
        """
        return self.stdout.verbosity == Verbosity.DEBUG

    def set_verbosity(
        self,
        verbosity: Optional[Union[int, str, Verbosity]]
    ) -> None:
        """
        Change output verbosity level.

        This method detaches the instance from the class-level output handler
        and creates a new instance-specific handler with the specified verbosity.

        Parameters
        ----------
        verbosity : Optional[Union[int, str, Verbosity]]
            New verbosity level. If None, uses class default.

        Examples
        --------
        >>> obj = AbstractObject()
        >>> obj.set_verbosity("DEBUG")
        >>> obj.debug_mode
        True

        Raises
        ------
        ValueError
            If verbosity level is invalid
        """
        if verbosity is not None:
            # Create new VerbosePrint instance
            # VerbosePrint constructor validates verbosity
            self._stdout = VerbosePrint(verbosity)
        else:
            # Use class-level stdout
            self._stdout = None

    @classmethod
    def set_default_verbosity(
        cls,
        verbosity: Union[int, str, Verbosity]
    ) -> None:
        """
        Set default verbosity for all new instances.

        This method changes the class-level default verbosity which affects
        all instances using the class-level handler.

        Parameters
        ----------
        verbosity : Union[int, str, Verbosity]
            New default verbosity level

        Examples
        --------
        >>> AbstractObject.set_default_verbosity("DEBUG")
        >>> obj = AbstractObject()  # Will use DEBUG level
        """
        cls._class_stdout = VerbosePrint(verbosity)

    def copy_verbosity_from(self, other: AbstractObject) -> None:
        """
        Copy verbosity settings from another instance.

        Parameters
        ----------
        other : AbstractObject
            Instance to copy verbosity from

        Examples
        --------
        >>> obj1 = AbstractObject(verbosity="DEBUG")
        >>> obj2 = AbstractObject()
        >>> obj2.copy_verbosity_from(obj1)
        >>> obj2.debug_mode
        True
        """
        if not hasattr(other, '_stdout') or other._stdout is None:
            # Other instance uses class-level stdout
            self._stdout = None
        else:
            # Copy instance-level stdout
            self._stdout = other.stdout.copy()

    def __getstate__(self) -> dict:
        """
        Support for pickling.

        Returns
        -------
        dict
            State dictionary for pickling
        """
        state = self.__dict__.copy()
        if hasattr(self, '_stdout') and self._stdout is not None:
            # Only store verbosity level if instance has custom stdout
            state['_verbosity_level'] = self._stdout.verbosity
            state.pop('_stdout', None)
        return state

    def __setstate__(self, state: dict) -> None:
        """
        Support for unpickling.

        Parameters
        ----------
        state : dict
            State dictionary from pickling
        """
        verbosity_level = state.pop('_verbosity_level', None)
        self.__dict__.update(state)
        
        # Recreate VerbosePrint instance if needed
        if verbosity_level is not None:
            self._stdout = VerbosePrint(verbosity_level)
        else:
            self._stdout = None