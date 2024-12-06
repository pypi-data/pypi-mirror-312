from typing import Optional, Union, Dict, List, Tuple, Sequence, Any
import re
from itertools import repeat
from contextlib import contextmanager

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import matplotlib.colors as mcolors
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.artist import Artist
from matplotlib.patches import Patch, Rectangle, Polygon
from matplotlib.lines import Line2D
from matplotlib.container import Container, ErrorbarContainer
from matplotlib.image import AxesImage
from matplotlib.text import Text
from matplotlib.collections import (
    Collection,
    PolyCollection,
    LineCollection,
    PathCollection,
)
from matplotlib.ticker import (
    Locator,
    MaxNLocator,
    AutoLocator,
    AutoMinorLocator,
    ScalarFormatter,
    Formatter,
    LogFormatterSciNotation,
)
from matplotlib.legend_handler import (
    HandlerLineCollection,
    HandlerPathCollection,
)

from quickstats import DescriptiveEnum
from quickstats.core import mappings as mp
from . import template_styles


class ResultStatus(DescriptiveEnum):
    """
    Enumeration for different result statuses with descriptions and display texts.

    Attributes
    ----------
    description : str
        A description of the result status.
    display_text : str
        The display text associated with the result status.
    """

    FINAL = (0, "Finalised results", "")
    INT = (1, "Internal results", "Internal")
    WIP = (2, "Work in progress results", "Work in Progress")
    PRELIM = (3, "Preliminary results", "Preliminary")
    OPENDATA = (4, "Open data results", "Open Data")
    SIM = (5, "Simulation results", "Simulation")
    SIMINT = (6, "Simulation internal results", "Simulation Internal")
    SIMPRELIM = (7, "Simulation preliminary results", "Simulation Preliminary")

    def __new__(cls, value: int, description: str = "", display_text: str = ""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.display_text = display_text
        return obj


class NumericFormatter(ScalarFormatter):
    """
    Custom numeric formatter for matplotlib axis ticks.

    It adjusts the formatting of tick labels for integer values with an absolute magnitude less than
    1000 to display as integers without decimal places (e.g., 5 instead of 5.0). This enhances the
    readability of tick labels for small integer values.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [100, 200, 300])
    >>> ax.yaxis.set_major_formatter(NumericFormatter())
    """

    def __call__(self, x: float, pos: Optional[int] = None) -> str:
        original_format = self.format
        if x.is_integer() and abs(x) < 1e3:
            self.format = re.sub(r"1\.\d+f", r"1.0f", self.format)
        result = super().__call__(x, pos)
        self.format = original_format
        return result


class LogNumericFormatter(LogFormatterSciNotation):
    def __call__(self, x: float, pos: Optional[int] = None) -> str:
        result = super().__call__(x, pos)
        # result = result.replace('10^{1}', '10').replace('10^{0}', '1')
        return result


class CustomHandlerLineCollection(HandlerLineCollection):
    def create_artists(
        self,
        legend,
        orig_handle: Any,
        xdescent: float,
        ydescent: float,
        width: float,
        height: float,
        fontsize: float,
        trans: transforms.Transform,
    ) -> List[Line2D]:
        """
        Create artists for the legend entry.

        Parameters
        ----------
        legend : matplotlib.legend.Legend
            The legend instance.
        orig_handle : Any
            The original plot handle.
        xdescent : float
            The amount by which the legend box is shifted horizontally.
        ydescent : float
            The amount by which the legend box is shifted vertically.
        width : float
            The width of the legend box.
        height : float
            The height of the legend box.
        fontsize : float
            The fontsize in pixels.
        trans : matplotlib.transforms.Transform
            The transform for positioning the artist.

        Returns
        -------
        artists : list of matplotlib.lines.Line2D
            A list of Line2D artists to draw in the legend.
        """
        artists = super().create_artists(
            legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans
        )
        # Adjust line height to center in legend
        for artist in artists:
            artist.set_ydata([height / 2.0, height / 2.0])
        return artists


class CustomHandlerPathCollection(HandlerPathCollection):
    def create_artists(
        self,
        legend,
        orig_handle: Any,
        xdescent: float,
        ydescent: float,
        width: float,
        height: float,
        fontsize: float,
        trans: transforms.Transform,
    ) -> List[Collection]:
        """
        Create artists for the legend entry.

        Parameters
        ----------
        legend : matplotlib.legend.Legend
            The legend instance.
        orig_handle : Any
            The original plot handle.
        xdescent : float
            The amount by which the legend box is shifted horizontally.
        ydescent : float
            The amount by which the legend box is shifted vertically.
        width : float
            The width of the legend box.
        height : float
            The height of the legend box.
        fontsize : float
            The fontsize in pixels.
        trans : matplotlib.transforms.Transform
            The transform for positioning the artist.

        Returns
        -------
        artists : list of matplotlib.collections.Collection
            A list of Collection artists to draw in the legend.
        """
        artists = super().create_artists(
            legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans
        )
        # Modify the path collection offsets to center the markers in the legend
        for artist in artists:
            offsets = np.array([[width / 2.0, height / 2.0]])
            artist.set_offsets(offsets)
        return artists


CUSTOM_HANDLER_MAP = {
    LineCollection: CustomHandlerLineCollection(),
    PathCollection: CustomHandlerPathCollection(),
}

AXIS_LOCATOR_MAP = {"auto": AutoLocator, "maxn": MaxNLocator}


def handle_has_label(handle: Artist) -> bool:
    """
    Check if the artist handle has a label.

    Parameters
    ----------
    handle : matplotlib.artist.Artist
        The artist handle to check.

    Returns
    -------
    has_label : bool
        True if the artist has a label that should be displayed in the legend.
    """
    try:
        label = handle.get_label()
        has_label = bool(label) and not label.startswith("_")
    except AttributeError:
        has_label = False
    return has_label


def ratio_frame(
    logx: bool = False,
    logy: bool = False,
    logy_lower: Optional[bool] = None,
    styles: Optional[Union[Dict[str, Any], str]] = None,
    analysis_label_options: Optional[Union[Dict[str, Any], str]] = None,
    prop_cycle: Optional[List[str]] = None,
    prop_cycle_lower: Optional[List[str]] = None,
    figure_index: Optional[int] = None,
) -> Tuple[Axes, Axes]:
    """
    Create a ratio plot frame with shared x-axis.

    Parameters
    ----------
    logx : bool, default False
        Set x-axis to logarithmic scale.
    logy : bool, default False
        Set y-axis of the main plot to logarithmic scale.
    logy_lower : bool, optional
        Set y-axis of the lower plot to logarithmic scale. Defaults to `logy` value.
    styles : dict or str, optional
        Style configurations for the plot.
    analysis_label_options : dict or str, optional
        Options for drawing analysis labels.
    prop_cycle : list of str, optional
        Color cycle for the main plot.
    prop_cycle_lower : list of str, optional
        Color cycle for the lower plot.
    figure_index : int, optional
        Index of the figure to use.

    Returns
    -------
    ax_main : matplotlib.axes.Axes
        The main plot axes.
    ax_ratio : matplotlib.axes.Axes
        The ratio plot axes.
    """
    if figure_index is None:
        plt.clf()
    else:
        plt.figure(figure_index)
    styles = template_styles.parse(styles)
    gridspec_kw = {
        "height_ratios": styles["ratio_frame"]["height_ratios"],
        "hspace": styles["ratio_frame"]["hspace"],
    }
    _, (ax_main, ax_ratio) = plt.subplots(
        nrows=2, ncols=1, gridspec_kw=gridspec_kw, sharex=True, **styles["figure"]
    )

    if logx:
        ax_main.set_xscale("log")
        ax_ratio.set_xscale("log")

    if logy_lower is None:
        logy_lower = logy

    if logy:
        ax_main.set_yscale("log")

    if logy_lower:
        ax_ratio.set_yscale("log")

    ax_main_styles = mp.concat(
        (styles["axis"], {"x_axis_styles": {"labelbottom": False}})
    )
    format_axis_ticks(
        ax_main,
        x_axis=True,
        y_axis=True,
        xtick_styles=styles["xtick"],
        ytick_styles=styles["ytick"],
        **ax_main_styles,
    )
    format_axis_ticks(
        ax_ratio,
        x_axis=True,
        y_axis=True,
        xtick_styles=styles["xtick"],
        ytick_styles=styles["ytick"],
        **styles["axis"],
    )

    if analysis_label_options is not None:
        draw_analysis_label(
            ax_main, text_options=styles["text"], **analysis_label_options
        )

    if prop_cycle is not None:
        ax_main.set_prop_cycle(prop_cycle)

    if prop_cycle_lower is None:
        prop_cycle_lower = prop_cycle

    if prop_cycle_lower is not None:
        ax_ratio.set_prop_cycle(prop_cycle_lower)

    return ax_main, ax_ratio


def single_frame(
    logx: bool = False,
    logy: bool = False,
    styles: Optional[Union[Dict[str, Any], str]] = None,
    analysis_label_options: Optional[Union[Dict[str, Any], str]] = None,
    prop_cycle: Optional[List[str]] = None,
    figure_index: Optional[int] = None,
) -> Axes:
    """
    Create a single plot frame.

    Parameters
    ----------
    logx : bool, default False
        Set x-axis to logarithmic scale.
    logy : bool, default False
        Set y-axis to logarithmic scale.
    styles : dict or str, optional
        Style configurations for the plot.
    analysis_label_options : dict or str, optional
        Options for drawing analysis labels.
    prop_cycle : list of str, optional
        Color cycle for the plot.
    figure_index : int, optional
        Index of the figure to use.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The plot axes.
    """
    if figure_index is None:
        plt.clf()
    else:
        plt.figure(figure_index)
    styles = template_styles.parse(styles)
    _, ax = plt.subplots(nrows=1, ncols=1, **styles["figure"])

    if logx:
        ax.set_xscale("log")
    if logy:
        ax.set_yscale("log")

    format_axis_ticks(
        ax,
        x_axis=True,
        y_axis=True,
        xtick_styles=styles["xtick"],
        ytick_styles=styles["ytick"],
        **styles["axis"],
    )

    if analysis_label_options is not None:
        draw_analysis_label(ax, text_options=styles["text"], **analysis_label_options)

    if prop_cycle is not None:
        ax.set_prop_cycle(prop_cycle)

    return ax


def suggest_markersize(nbins: int) -> float:
    """
    Suggest a marker size based on the number of bins.

    Parameters
    ----------
    nbins : int
        Number of bins.

    Returns
    -------
    markersize : float
        Suggested marker size.
    """
    bin_max = 200
    bin_min = 40
    size_max = 8
    size_min = 2
    if nbins <= bin_min:
        return size_max
    elif bin_min < nbins <= bin_max:
        return ((size_min - size_max) / (bin_max - bin_min)) * (
            nbins - bin_min
        ) + size_max
    else:
        return size_min


def format_axis_ticks(
    ax: Axes,
    x_axis: bool = True,
    y_axis: bool = True,
    major_length: int = 16,
    minor_length: int = 8,
    spine_width: int = 2,
    major_width: int = 2,
    minor_width: int = 1,
    direction: str = "in",
    label_bothsides: bool = False,
    tick_bothsides: bool = False,
    labelsize: Optional[int] = None,
    offsetlabelsize: Optional[int] = None,
    x_axis_styles: Optional[Dict[str, Any]] = None,
    y_axis_styles: Optional[Dict[str, Any]] = None,
    xtick_styles: Optional[Dict[str, Any]] = None,
    ytick_styles: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Format the axis ticks and spines.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes to format.
    x_axis : bool, default True
        Whether to format the x-axis.
    y_axis : bool, default True
        Whether to format the y-axis.
    major_length : int, default 16
        Length of major ticks.
    minor_length : int, default 8
        Length of minor ticks.
    spine_width : int, default 2
        Width of the axis spines.
    major_width : int, default 2
        Width of major ticks.
    minor_width : int, default 1
        Width of minor ticks.
    direction : str, default 'in'
        Direction of ticks ('in', 'out', 'inout').
    label_bothsides : bool, default False
        Whether to label ticks on both sides of the axes.
    tick_bothsides : bool, default False
        Whether to draw ticks on both sides of the axes.
    labelsize : int, optional
        Font size of tick labels.
    offsetlabelsize : int, optional
        Font size of offset text labels.
    x_axis_styles : dict, optional
        Additional styles for x-axis ticks.
    y_axis_styles : dict, optional
        Additional styles for y-axis ticks.
    xtick_styles : dict, optional
        Styles for x-axis tick formatting.
    ytick_styles : dict, optional
        Styles for y-axis tick formatting.

    Returns
    -------
    None
    """
    if x_axis:
        if ax.get_xaxis().get_scale() != "log":
            ax.xaxis.set_minor_locator(AutoMinorLocator())
        x_styles = {
            "labelsize": labelsize,
            "labeltop": label_bothsides,
            # "labelbottom": True,
            "top": tick_bothsides,
            "bottom": True,
            "direction": direction,
        }
        if x_axis_styles is not None:
            x_styles.update(x_axis_styles)
        ax.tick_params(
            axis="x",
            which="major",
            length=major_length,
            width=major_width,
            **x_styles,
        )
        ax.tick_params(
            axis="x",
            which="minor",
            length=minor_length,
            width=minor_width,
            **x_styles,
        )

    if y_axis:
        if ax.get_yaxis().get_scale() != "log":
            ax.yaxis.set_minor_locator(AutoMinorLocator())
        y_styles = {
            "labelsize": labelsize,
            "labelleft": True,
            # "labelright": label_bothsides,
            "left": True,
            "right": tick_bothsides,
            "direction": direction,
        }
        if y_axis_styles is not None:
            y_styles.update(y_axis_styles)
        ax.tick_params(
            axis="y",
            which="major",
            length=major_length,
            width=major_width,
            **y_styles,
        )
        ax.tick_params(
            axis="y",
            which="minor",
            length=minor_length,
            width=minor_width,
            **y_styles,
        )

    for spine in ax.spines.values():
        spine.set_linewidth(spine_width)

    set_axis_tick_styles(ax.xaxis, xtick_styles)
    set_axis_tick_styles(ax.yaxis, ytick_styles)

    # Handle offset labels
    if offsetlabelsize is None:
        offsetlabelsize = labelsize

    x_offset_text = ax.xaxis.get_offset_text()
    if x_offset_text.get_text():
        x_offset_text.set_fontsize(offsetlabelsize)
        ax.xaxis.labelpad += x_offset_text.get_fontsize()

    y_offset_text = ax.yaxis.get_offset_text()
    if y_offset_text.get_text():
        y_offset_text.set_fontsize(offsetlabelsize)
        ax.yaxis.labelpad += y_offset_text.get_fontsize()

    if (x_offset_text.get_text() or y_offset_text.get_text()) and not isinstance(
        plt.gca(), plt.Subplot
    ):
        plt.tight_layout()


def set_axis_tick_styles(
    axis: Axis, styles: Optional[Dict[str, Any]] = None
) -> None:
    """
    Set styles for axis ticks.

    Parameters
    ----------
    axis : matplotlib.axis.Axis
        The axis to set styles for.
    styles : dict, optional
        Styles to apply to the axis ticks.

    Returns
    -------
    None
    """
    if styles is None:
        return

    fmt = styles.get("format")
    if fmt is not None:
        if isinstance(fmt, str):
            if fmt == "numeric":
                formatter = (
                    LogNumericFormatter()
                    if axis.get_scale() == "log"
                    else NumericFormatter()
                )
            else:
                raise ValueError(f"unsupported format string: '{fmt}'")
        elif isinstance(fmt, Formatter):
            formatter = fmt
        else:
            raise ValueError(f"invalid formatter: {fmt}")
        axis.set_major_formatter(formatter)

    if axis.get_scale() == "log":
        return

    locator = axis.get_major_locator()
    locator_type = type(locator)
    new_locator = AXIS_LOCATOR_MAP.get(
        styles.get("locator", "").lower(), locator_type
    )()
    locator_params = {
        param: styles[param]
        for param in getattr(new_locator, "default_params", [])
        if param in styles
    }
    if locator_params:
        new_locator.set_params(**locator_params)
    axis.set_major_locator(new_locator)


def centralize_axis(
    ax: Axes, which: str = "y", ref_value: float = 0, padding: float = 0.1
) -> None:
    """
    Centralize the axis around a reference value.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axis to be centralized.
    which : str, optional
        The axis to centralize. 'x' for x-axis, 'y' for y-axis. Default is 'y'.
    ref_value : float, optional
        The reference value around which the axis will be centralized. Default is 0.
    padding : float, optional
        The padding applied around the data to create space. Default is 0.1.

    Example
    -------
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [2, 4, 6])
    >>> centralize_axis(ax, which='y', ref_value=3)
    """
    if which not in {"x", "y"}:
        raise ValueError('axis to centralize must be either "x" or "y"')

    get_scale = ax.get_xscale if which == "x" else ax.get_yscale
    get_lim = ax.get_xlim if which == "x" else ax.get_ylim
    set_lim = ax.set_xlim if which == "x" else ax.set_ylim

    if get_scale() == "log":
        raise ValueError("cannot centralize on a logarithmic axis")

    lim = get_lim()
    delta = max(abs(ref_value - lim[0]), abs(lim[1] - ref_value))
    pad = (lim[1] - lim[0]) * padding if padding else 0.0
    new_lim = (ref_value - delta - pad, ref_value + delta + pad)
    set_lim(*new_lim)


def parse_transform(target: Optional[str] = None,
                    ax: Optional = None) -> Optional[transforms.Transform]:
    """
    Parse a string into a Matplotlib transform.

    Parameters
    ----------
    target : Optional[str], default: None
        The string representation of the transformation target.
        Possible values: 'figure', 'axis', 'data', or an empty string.

        - 'figure': Transform relative to the figure.
        - 'axis': Transform relative to the axes.
        - 'data': Transform relative to the data coordinates.
        - None or '': Returns None.

    Returns
    -------
    transform : Optional[transforms.Transform]
        The corresponding transformation object. Returns None if the input is None or an empty string.

    Examples
    --------
    >>> transform_figure = parse_transform('figure')
    >>> transform_data = parse_transform('data')
    """
    if target == "figure":
        fig = plt.gcf()
        if fig is None:
            raise ValueError("no current figure available for 'figure' transform")
        return fig.transFigure
    elif target == "axis":
        if not ax:
            ax = plt.gca()
        if ax is None:
            raise ValueError("no current axis available for 'axis' transform")
        return ax.transAxes
    elif target == "data":
        if not ax:
            ax = plt.gca()        
        ax = plt.gca()
        if ax is None:
            raise ValueError("no current axis available for 'data' transform")
        return ax.transData
    elif not target:
        return None
    else:
        raise ValueError(f"invalid transform target: '{target}'")


def create_transform(
    transform_x: str = "axis", transform_y: str = "axis"
) -> transforms.Transform:
    """
    Create a composite transformation from two string representations of transformations.

    Parameters
    ----------
    transform_x : str, optional
        The string representation of the transformation for the x-direction.
    transform_y : str, optional
        The string representation of the transformation for the y-direction.

    Returns
    -------
    transform : matplotlib.transforms.Transform
        The composite transformation object.

    Examples
    --------
    >>> combined_transform = create_transform('axis', 'data')
    """
    transform = transforms.blended_transform_factory(
        parse_transform(transform_x), parse_transform(transform_y)
    )
    return transform


def get_artist_dimension(artist: Artist, transform='axis') -> Tuple[float, float, float, float]:
    """
    Get the dimensions of an artist's bounding box in axis coordinates.

    This function calculates the dimensions (x-min, x-max, y-min, y-max) of an artist's
    bounding box in axis coordinates based on the provided artist.

    Parameters
    ----------
    artist : matplotlib.artist.Artist
        The artist for which dimensions need to be calculated.

    Returns
    -------
    xmin, xmax, ymin, ymax : float
        The calculated dimensions of the artist's bounding box in axis coordinates.

    Example
    -------
    >>> from matplotlib.patches import Rectangle
    >>> rectangle = Rectangle((0.2, 0.3), 0.4, 0.4)
    >>> xmin, xmax, ymin, ymax = get_artist_dimension(rectangle)
    """
    axis = artist.axes or plt.gca()
    artist.figure.canvas.draw()

    # Get the bounding box of the artist in display coordinates
    bbox = artist.get_window_extent()

    # Transform the bounding box to axis coordinates
    if transform is not None:
        transform = parse_transform(transform, ax=axis)
        bbox = bbox.transformed(transform.inverted())
    xmin, ymin = bbox.xmin, bbox.ymin
    xmax, ymax = bbox.xmax, bbox.ymax

    return xmin, xmax, ymin, ymax

def draw_hatches(
    axis: Axes, ymax: float, height: float = 1.0, **styles
) -> None:
    """
    Draw hatches on the axis.

    Parameters
    ----------
    axis : matplotlib.axes.Axes
        The axis to draw on.
    ymax : float
        Maximum y-value for the hatches.
    height : float, default 1.0
        Height of the hatches.
    **styles
        Additional style arguments for the hatches.

    Returns
    -------
    None
    """
    y_values = np.arange(0, height * ymax, 2 * height) - height / 2
    transform = create_transform(transform_x="axis", transform_y="data")
    for y in y_values:
        axis.add_patch(
            Rectangle((0, y), 1, 1, **styles, zorder=-1, transform=transform)
        )


# Special text formatting patterns
special_text_patterns = {
    r"\\bolditalic\{(.*?)\}": {"weight": "bold", "style": "italic"},
    r"\\italic\{(.*?)\}": {"style": "italic"},
    r"\\bold\{(.*?)\}": {"weight": "bold"},
}
special_text_regex = re.compile(
    "|".join(f"({pattern})" for pattern in special_text_patterns.keys())
)


def draw_text(
    axis: Axes,
    x: float,
    y: float,
    text_str: str,
    transform_x: str = "axis",
    transform_y: str = "axis",
    **styles,
) -> Tuple[float, float, float, float]:
    """
    Draw text on the axis with special font styles.

    Parameters
    ----------
    axis : matplotlib.axes.Axes
        The axis to draw on.
    x : float
        X-coordinate for the text.
    y : float
        Y-coordinate for the text.
    text_str : str
        The text string to draw.
    transform_x : str, default 'axis'
        Coordinate transform for x.
    transform_y : str, default 'axis'
        Coordinate transform for y.
    **styles
        Additional style arguments for the text.

    Returns
    -------
    xmin, xmax, ymin, ymax : float
        The dimensions of the drawn text.
    """
    with change_axis(axis):
        transform = create_transform(transform_x, transform_y)
        components = special_text_regex.split(text_str)
        current_x = x
        xmin = None
        for component in components:
            if component and special_text_regex.match(component):
                for pattern, font_styles in special_text_patterns.items():
                    match = re.match(pattern, component)
                    if match:
                        txt = axis.text(
                            current_x,
                            y,
                            match.group(1),
                            transform=transform,
                            **styles,
                            **font_styles,
                        )
                        break
            else:
                txt = axis.text(current_x, y, component, transform=transform, **styles)
            xmin_, current_x, ymin, ymax = get_artist_dimension(txt)
            if xmin is None:
                xmin = xmin_
    return xmin, current_x, ymin, ymax


def draw_multiline_text(
    axis: Axes,
    x: float,
    y: float,
    text_str: str,
    dy: float = 0.01,
    transform_x: str = "axis",
    transform_y: str = "axis",
    **styles,
) -> None:
    """
    Draw multiline text on the axis.

    Parameters
    ----------
    axis : matplotlib.axes.Axes
        The axis to draw on.
    x : float
        Starting x-coordinate for the text.
    y : float
        Starting y-coordinate for the text.
    text_str : str
        The multiline text string, separated by "//".
    dy : float, default 0.01
        Vertical spacing between lines.
    transform_x : str, default 'axis'
        Coordinate transform for x.
    transform_y : str, default 'axis'
        Coordinate transform for y.
    **styles
        Additional style arguments for the text.

    Returns
    -------
    None
    """
    lines = text_str.split("//")
    for line in lines:
        _, _, y, _ = draw_text(
            axis,
            x,
            y,
            line,
            transform_x=transform_x,
            transform_y=transform_y,
            **styles,
        )
        y -= dy
        transform_x, transform_y = "axis", "axis"


@contextmanager
def change_axis(axis: Axes):
    """
    Temporarily change the current axis to the specified axis within a context.

    Parameters
    ----------
    axis : matplotlib.axes.Axes
        The axis to which the current axis will be temporarily changed.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> fig, axes = plt.subplots(1, 2)
    >>> with change_axis(axes[0]):
    ...     plt.plot([1, 2, 3], [4, 5, 6])
    ...     plt.title('First Axis')
    """
    current_axis = plt.gca()
    plt.sca(axis)
    try:
        yield
    finally:
        plt.sca(current_axis)


def draw_analysis_label(
    axis: Axes,
    loc: Tuple[float, float] = (0.05, 0.95),
    fontsize: float = 25,
    status: Union[str, ResultStatus] = "int",
    energy: Optional[str] = None,
    lumi: Optional[str] = None,
    colab: Optional[str] = "ATLAS",
    main_text: Optional[str] = None,
    extra_text: Optional[str] = None,
    dy: float = 0.02,
    dy_main: float = 0.01,
    transform_x: str = "axis",
    transform_y: str = "axis",
    vertical_align: str = "top",
    horizontal_align: str = "left",
    text_options: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Draw analysis label and additional texts on a given axis.

    This function allows you to add standardized analysis labels and additional text
    annotations to a Matplotlib axis. It supports special text formatting and multiline text.

    Parameters
    ----------
    axis : matplotlib.axes.Axes
        Axis to be drawn on.
    loc : tuple of float, default = (0.05, 0.95)
        The location of the analysis label and additional texts in axis coordinates.
    fontsize : float, default = 25
        Font size of the analysis label and the status label.
    status : str or ResultStatus, default = 'int'
        Display text for the analysis status. Certain keywords can be used to automatically
        convert to the corresponding built-in status texts (see `ResultStatus`).
    energy : str, optional
        Display text for the center-of-mass energy. A prefix of "$\\sqrt{s} = $" will be
        automatically appended to the front of the text.
    lumi : str, optional
        Display text for the luminosity. It will be displayed as is.
    colab : str, optional
        Display text for the collaboration involved in the analysis. It will be
        bolded and italicized.
    main_text : str, optional
        Main text to be displayed before the collaboration text. A new line
        can be added by using a double slash, i.e., "//". Use the "\\bolditalic{<text>}"
        keyword for bold-italic styled text.
    extra_text : str, optional
        Extra text to be displayed after energy and luminosity texts. A new line
        can be added by using a double slash, i.e., "//". Use the "\\bolditalic{<text>}"
        keyword for bold-italic styled text.
    dy : float, default = 0.02
        Vertical separation between each line of the sub-texts in axis coordinates.
    dy_main : float, default = 0.01
        Vertical separation between each line of the main texts in axis coordinates.
    transform_x : str, default = 'axis'
        Coordinate transform for the x location of the analysis label.
    transform_y : str, default = 'axis'
        Coordinate transform for the y location of the analysis label.
    vertical_align : str, default = 'top'
        Vertical alignment of the analysis label.
    horizontal_align : str, default = 'left'
        Horizontal alignment of the analysis label.
    text_options : dict, optional
        A dictionary specifying additional styles for drawing texts.

    Notes
    -----
    - You can use special formatting in your text strings:
        - Use "\\bolditalic{<text>}" for bold and italic text.
        - Use "\\italic{<text>}" for italic text.
        - Use "\\bold{<text>}" for bold text.
    - To add a new line within `main_text` or `extra_text`, use "//" to split lines.
    - The `status` parameter accepts predefined status codes from the `ResultStatus` enum,
      or you can provide a custom string.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> draw_analysis_label(
    ...     ax,
    ...     main_text="\\bolditalic{CMS} Preliminary",
    ...     energy="13 TeV",
    ...     lumi="35.9 fb$^{-1}$",
    ...     extra_text="Work in progress",
    ... )
    """
    try:
        status_text = ResultStatus.parse(status).display_text
    except:
        status_text = status

    with change_axis(axis):
        x_pos, y_pos = loc
        main_texts = []
        if main_text is not None:
            main_texts.extend(main_text.split("//"))
        if colab is not None:
            # Add collaboration and status text
            colab_text = r"\bolditalic{" + colab + "}  " + status_text
            main_texts.append(colab_text)
        for text_line in main_texts:
            _, _, y_pos, _ = draw_text(
                axis,
                x_pos,
                y_pos,
                text_line,
                fontsize=fontsize,
                transform_x=transform_x,
                transform_y=transform_y,
                horizontalalignment=horizontal_align,
                verticalalignment=vertical_align,
            )
            y_pos -= dy_main
            transform_x, transform_y = "axis", "axis"

    # Draw energy and luminosity labels as well as additional texts
    elumi_text_parts = []
    if energy is not None:
        elumi_text_parts.append(r"$\sqrt{s} = $" + energy)
    if lumi is not None:
        elumi_text_parts.append(lumi)
    elumi_text = ", ".join(elumi_text_parts)

    all_texts = []
    if elumi_text:
        all_texts.append(elumi_text)

    if extra_text is not None:
        all_texts.extend(extra_text.split("//"))

    if text_options is None:
        text_options = {}

    for text_line in all_texts:
        _, _, y_pos, _ = draw_text(
            axis,
            x_pos,
            y_pos - dy,
            text_line,
            **text_options,
        )
        y_pos -= dy


def is_edgy_polygon(handle: Polygon) -> bool:
    """
    Check if a legend handle represents a polygon with only edges and no fill.

    Parameters
    ----------
    handle : matplotlib.patches.Polygon
        The legend handle to be checked.

    Returns
    -------
    bool
        True if the provided legend handle represents an edgy polygon (only edges, no fill).
        False if the provided legend handle does not meet the criteria of an edgy polygon.

    Examples
    --------
    >>> from matplotlib.patches import Polygon
    >>> polygon_handle = Polygon([(0, 0), (1, 1), (2, 0)], edgecolor='black', fill=False)
    >>> is_edgy_polygon(polygon_handle)
    True
    """
    if not isinstance(handle, Polygon):
        return False

    edgecolor = handle.get_edgecolor()
    if np.all(edgecolor == 0):
        return False

    if handle.get_fill():
        return False

    return True


def resolve_handle_label(handle: Any, raw: bool = False) -> Tuple[Any, str]:
    """
    Resolve the artist handle and label for the legend.

    Parameters
    ----------
    handle : Any
        The artist handle.
    raw : bool, default False
        If True, return the raw handle and label.

    Returns
    -------
    handle : Any
        The resolved artist handle.
    label : str
        The label associated with the handle.
    """
    if raw:
        label = getattr(handle, "get_label", lambda: "_nolegend_")()
        return handle, label

    if isinstance(handle, Container):
        label = handle.get_label()
        if not label or label.startswith("_"):
            return resolve_handle_label(handle[0])
    elif isinstance(handle, (list, tuple)):
        return resolve_handle_label(handle[0])
    elif hasattr(handle, "get_label"):
        label = handle.get_label()
    else:
        raise RuntimeError("unable to extract label from the handle")

    return handle, label


def remake_handles(
    handles: List[Any],
    polygon_to_line: bool = True,
    fill_border: bool = True,
    line2d_styles: Optional[Dict[str, Any]] = None,
    border_styles: Optional[Dict[str, Any]] = None,
) -> List[Any]:
    """
    Remake legend handles for better representation.

    Parameters
    ----------
    handles : list
        List of artist handles.
    polygon_to_line : bool, default True
        Convert polygon edges to lines in the legend.
    fill_border : bool, default True
        Add a border to filled patches in the legend.
    line2d_styles : dict, optional
        Styles for Line2D objects.
    border_styles : dict, optional
        Styles for border rectangles.

    Returns
    -------
    new_handles : list
        List of remade artist handles.
    """
    new_handles = []
    for handle in handles:
        subhandles = handle if isinstance(handle, (list, tuple)) else [handle]
        new_subhandles = []
        for subhandle in subhandles:
            if polygon_to_line and is_edgy_polygon(subhandle):
                line_styles = line2d_styles or {}
                subhandle = Line2D(
                    [],
                    [],
                    color=subhandle.get_edgecolor(),
                    linestyle=subhandle.get_linestyle(),
                    label=subhandle.get_label(),
                    **line_styles,
                )
            new_subhandles.append(subhandle)
            if fill_border and isinstance(subhandle, PolyCollection):
                border_style = border_styles or {}
                border_handle = Rectangle(
                    (0, 0), 1, 1, facecolor="none", **border_style
                )
                new_subhandles.append(border_handle)
        if isinstance(handle, Container):
            kwargs = {"label": handle.get_label()}
            if isinstance(handle, ErrorbarContainer):
                kwargs.update(
                    {"has_xerr": handle.has_xerr, "has_yerr": handle.has_yerr}
                )
            new_handle = type(handle)(tuple(new_subhandles), **kwargs)
        else:
            new_handle = (
                new_subhandles[0] if len(new_subhandles) == 1 else tuple(new_subhandles)
            )
        new_handles.append(new_handle)
    return new_handles


def isolate_contour_styles(styles: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Converts keyword arguments for contour or contourf to a list of
    styles for each contour level, ensuring that styles are consistently applied
    across different levels.

    Parameters
    ----------
    styles : dict
        Dictionary of keyword arguments passed to contour or contourf.

    Returns
    -------
    list of dict
        A list of dictionaries, each corresponding to the styles for one contour level.

    Raises
    ------
    ValueError
        If the lengths of the sequences for different styles are inconsistent.
    """
    # Map input style names to matplotlib properties
    style_key_map = {
        "linestyles": "linestyle",
        "linewidths": "linewidth",
        "colors": "color",
        "alpha": "alpha",
    }

    # Extract relevant styles from the input dictionary
    relevant_styles = {
        new_name: styles[old_name]
        for old_name, new_name in style_key_map.items()
        if old_name in styles
    }

    # Determine the size (length) of each style property
    sizes = []
    for style_value in relevant_styles.values():
        if isinstance(style_value, Sequence) and not isinstance(style_value, str):
            sizes.append(len(style_value))
        else:
            sizes.append(1)

    if not sizes:
        return repeat({})

    # Check for consistent sizes (if multiple sequences are provided)
    unique_sizes = np.unique([size for size in sizes if size != 1])
    if len(unique_sizes) > 1:
        raise ValueError("contour styles have inconsistent sizes.")

    # Get the maximum size (this will determine the number of contour levels)
    max_size = max(sizes)

    # If all styles are scalar, repeat the same dictionary
    if max_size == 1:
        return repeat(relevant_styles)

    # Create a list of dictionaries, each corresponding to a contour level
    list_styles = []
    for i in range(max_size):
        level_styles = {
            key: value if sizes[idx] == 1 else value[i]
            for idx, (key, value) in enumerate(relevant_styles.items())
        }
        list_styles.append(level_styles)

    return list_styles


def get_axis_limits(
    ax: Axes,
    xmin: Optional[float] = None,
    xmax: Optional[float] = None,
    ymin: Optional[float] = None,
    ymax: Optional[float] = None,
    ypadlo: Optional[float] = None,
    ypadhi: Optional[float] = None,
    ypad: Optional[float] = None,
) -> Tuple[List[float], List[float]]:
    """
    Calculate new axis limits with optional padding.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes to calculate limits for.
    xmin : float, optional
        Minimum x-limit.
    xmax : float, optional
        Maximum x-limit.
    ymin : float, optional
        Minimum y-limit.
    ymax : float, optional
        Maximum y-limit.
    ypadlo : float, optional
        Lower y-padding as a fraction of the data range.
    ypadhi : float, optional
        Upper y-padding as a fraction of the data range.
    ypad : float, optional
        Symmetric y-padding as a fraction of the data range.

    Returns
    -------
    xlim : list of float
        Calculated x-limits.
    ylim : list of float
        Calculated y-limits.
    """
    xlim = list(ax.get_xlim())
    ylim = list(ax.get_ylim())

    # Update x-limits if provided
    if xmin is not None:
        xlim[0] = xmin
    if xmax is not None:
        xlim[1] = xmax

    # Check conflicting padding values
    if ypad is not None and ypadhi is not None:
        raise ValueError("cannot set both `ypad` and `ypadhi`.")

    # If ypad is set, use it for upper padding
    if ypad is not None:
        ypadhi = ypad

    # Determine the lower and upper paddings
    if ypadhi is not None or ypadlo is not None:

        ypad_lo = ypadlo or 0
        ypad_hi = ypadhi or 0

        if not (0 <= ypad_lo <= 1):
            raise ValueError("`ypadlo` must be between 0 and 1.")
        if not (0 <= ypad_hi <= 1):
            raise ValueError("`ypadhi` must be between 0 and 1.")

        # Logarithmic scale adjustment
        if ax.get_yaxis().get_scale() == "log":
            if ylim[0] <= 0:
                raise ValueError("ymin must be positive in a logscale plot")
            new_ymin = ylim[1] / (ylim[1] / ylim[0]) ** (1 + ypad_lo)
            new_ymax = ylim[0] * (ylim[1] / ylim[0]) ** (1 + ypad_hi)
        else:
            # Linear scale adjustment
            y_range = ylim[1] - ylim[0]
            new_ymin = ylim[0] - y_range * ypad_lo / (1 - ypad_lo - ypad_hi)
            new_ymax = ylim[1] + y_range * ypad_hi / (1 - ypad_lo - ypad_hi)

        # Apply padding only if the corresponding value is set
        if ypad_lo:
            ylim[0] = new_ymin
        if ypad_hi:
            ylim[1] = new_ymax

    # Override y-limits if explicitly provided
    if ymin is not None:
        ylim[0] = ymin
    if ymax is not None:
        ylim[1] = ymax

    # Return the calculated xlim and ylim values
    return xlim, ylim


def is_transparent_color(color: Union[str, Tuple, List, None]) -> bool:
    """
    Checks if the input color is transparent.

    Parameters
    ----------
    color : Union[str, tuple, list, None]
        The color to check.

    Returns
    -------
    bool
        True if the color is transparent, False otherwise.

    Raises
    ------
    ValueError
        If the input color is not valid or cannot be converted to an RGBA format.
    """
    if color is None:
        raise ValueError("color cannot be None")

    try:
        # Convert the input color to an RGBA tuple
        rgba = mcolors.to_rgba(color)
        # The fourth element (alpha) indicates transparency, return True if alpha is 0
        return rgba[3] == 0
    except ValueError as e:
        raise ValueError(f"invalid color format: {color}") from e


def get_artist_colors(
    artist: Artist, index: int = 0
) -> Dict[str, Optional[Any]]:
    """
    Retrieves color information from a Matplotlib artist.

    Parameters
    ----------
    artist : matplotlib.artist.Artist
        A Matplotlib artist object (e.g., Line2D, Patch, Collection, etc.).
    index : int, optional
        The index to use if the artist contains multiple children (default is 0).

    Returns
    -------
    colors : dict
        A dictionary containing the relevant color properties depending on the type of artist.

    Raises
    ------
    TypeError
        If the input is not a valid `Artist` object.
    IndexError
        If the provided index is out of bounds for the artist's children.
    """
    colors = {}

    # If artist is a container, get the child artist at the specified index
    if isinstance(artist, Container):
        children = artist.get_children()
        if not children:
            raise IndexError("artist has no children")
        if index >= len(children):
            raise IndexError(
                f"index {index} out of bounds for artist with {len(children)} children"
            )
        artist = children[index]

    # Ensure the object is still an artist after resolving any containers
    if not isinstance(artist, Artist):
        raise TypeError("provided object is not a valid Matplotlib Artist")

    # For Collection objects (e.g., scatter plots)
    if isinstance(artist, Collection):
        facecolors = artist.get_facecolor()
        edgecolors = artist.get_edgecolor()
        colors["facecolor"] = (
            facecolors[index] if len(facecolors) > index else None
        )
        colors["edgecolor"] = (
            edgecolors[index] if len(edgecolors) > index else None
        )

    # For Line2D objects (e.g., lines)
    elif isinstance(artist, Line2D):
        colors["color"] = artist.get_color()
        colors["markerfacecolor"] = artist.get_markerfacecolor()
        colors["markeredgecolor"] = artist.get_markeredgecolor()

    # For Patch objects (e.g., rectangles, polygons, circles)
    elif isinstance(artist, Patch):
        colors["facecolor"] = artist.get_facecolor()
        colors["edgecolor"] = artist.get_edgecolor()

    # For Image objects (e.g., imshow)
    elif isinstance(artist, AxesImage):
        colors["cmap"] = artist.get_cmap()

    # For Text objects
    elif isinstance(artist, Text):
        colors["textcolor"] = artist.get_color()

    return colors

# for converting axis size
def convert_size(size_str: str) -> float:
    if size_str.endswith('%'):
        return float(size_str.strip('%')) / 100
    else:
        return float(size_str)