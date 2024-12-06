from typing import Optional, Union, Dict, List, Tuple, Callable, Sequence, Any
from collections import defaultdict
from itertools import cycle
from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.artist import Artist

from quickstats import AbstractObject, NamedTreeNode
from quickstats.core import mappings as mp
from quickstats.utils.common_utils import insert_periodic_substr
from quickstats.maths.statistics import HistComparisonMode

from . import template_styles, template_analysis_label_options
from .core import PlotFormat, ErrorDisplayFormat
from .colors import (
    ColorType,
    ColormapType,
    get_color_cycle,
    get_cmap,
)
from .template import (
    single_frame,
    ratio_frame,
    format_axis_ticks,
    centralize_axis,
    draw_multiline_text,
    resolve_handle_label,
    get_axis_limits,
    CUSTOM_HANDLER_MAP,
)


class AbstractPlot(AbstractObject):
    """
    A base class for creating plots with customizable styles, colors, labels, and annotations.

    Attributes
    ----------
    COLOR_MAP : Dict[str, ColorType]
        A class-level default color map.
    COLOR_CYCLE : str
        The default color cycle name.
    LABEL_MAP : Dict[str, str]
        A class-level default label map.
    STYLES : Dict[str, Any]
        A class-level default styles dictionary.
    CONFIG : Dict[str, Any]
        A class-level default configuration dictionary.
    """

    COLOR_MAP: Dict[str, ColorType] = {}
    COLOR_CYCLE: str = "default"
    LABEL_MAP: Dict[str, str] = {}
    STYLES: Dict[str, Any] = {}
    CONFIG: Dict[str, Any] = {
        "xlabellinebreak": 50,
        "ylabellinebreak": 50,
        "ratio_line_styles": {
            "color": "gray",
            "linestyle": "--",
            "zorder": 0,
        },
        'draw_legend': True
    }

    def __init__(
        self,
        color_map: Optional[Dict[str, ColorType]] = None,
        color_cycle: Optional[ColormapType] = None,
        label_map: Optional[Dict[str, str]] = None,
        styles: Optional[Union[Dict[str, Any], str]] = None,
        config: Optional[Dict[str, Any]] = None,
        styles_map: Optional[Dict[str, Union[Dict[str, Any], str]]] = None,
        config_map: Optional[Dict[str, Dict[str, Any]]] = None,
        analysis_label_options: Optional[Union[str, Dict[str, Any]]] = None,
        figure_index: Optional[int] = None,
        verbosity: Optional[Union[int, str]] = "INFO",
    ):
        """
        Initialize the AbstractPlot object with customizable options.

        Parameters
        ----------
        color_map : Optional[Dict[str, ColorType]], default None
            A dictionary mapping labels to colors.
        color_cycle : Optional[ColormapType], default None
            The color cycle to use for plots.
        label_map : Optional[Dict[str, str]], default None
            A dictionary mapping internal labels to display labels.
        styles : Optional[Union[Dict[str, Any], str]], default None
            Global styles to apply to the designated artists of the plot.
        config : Optional[Dict[str, Any]], default None
            Configuration parameters for the plot.
        styles_map : Optional[Dict[str, Union[Dict[str, Any], str]]], default None
            Target-specific styles to update the existing style.
        config_map : Optional[Dict[str, Dict[str, Any]]], default None
            Target-specific configuration parameters to update the existing config.
        analysis_label_options : Optional[Union[str, Dict[str, Any]]], default None
            Options for the analysis label.
        figure_index : Optional[int], default None
            The index of the figure to use.
        verbosity : Optional[Union[int, str]], default "INFO"
            The verbosity level.

        Returns
        -------
        None
        """
        super().__init__(verbosity=verbosity)

        self.color_map = color_map
        self.set_color_cycle(color_cycle)
        self.label_map = label_map
        self.styles_map = styles
        self.update_styles_map(styles_map)
        self.config_map = config
        self.update_config_map(config_map)
        self.analysis_label_options = analysis_label_options

        self.reset()
        self.figure_index = figure_index
        

    @property
    def color_map(self) -> NamedTreeNode:
        """
        Get the color map as a NamedTreeNode.

        Returns
        -------
        NamedTreeNode
            The color map.
        """
        return self._color_map

    @color_map.setter
    def color_map(self, value: Optional[Dict[str, ColorType]] = None):
        """
        Set the color map, combining class-level defaults with the provided value.

        Parameters
        ----------
        value : Optional[Dict[str, ColorType]], default None
            A dictionary mapping labels to colors.

        Returns
        -------
        None
        """
        data = mp.merge_classattr(type(self), 'COLOR_MAP', copy=True)
        data &= value
        self._color_map = NamedTreeNode.from_mapping(data)

    @property
    def label_map(self) -> NamedTreeNode:
        """
        Get the label map as a NamedTreeNode.

        Returns
        -------
        NamedTreeNode
            The label map.
        """
        return self._label_map

    @label_map.setter
    def label_map(self, value: Optional[Dict[str, str]] = None):
        """
        Set the label map, combining class-level defaults with the provided value.

        Parameters
        ----------
        value : Optional[Dict[str, str]], default None
            A dictionary mapping internal labels to display labels.

        Returns
        -------
        None
        """
        data = mp.merge_classattr(type(self), 'LABEL_MAP', copy=True)
        data &= value
        self._label_map = NamedTreeNode.from_mapping(data)

    @property
    def config(self) -> Dict[str, Any]:
        """
        Get the configuration dictionary.

        Returns
        -------
        Dict[str, Any]
            The configuration dictionary.
        """
        return self._config_map.data

    @property
    def config_map(self) -> NamedTreeNode:
        """
        Get the configuration map as a NamedTreeNode.

        Returns
        -------
        NamedTreeNode
            The configuration map.
        """
        return self._config_map

    @config_map.setter
    def config_map(self, value: Optional[Dict[str, Any]] = None):
        """
        Set the configuration map, combining class-level defaults with the provided value.

        Parameters
        ----------
        value : Optional[Dict[str, Any]], default None
            A dictionary of configuration parameters.

        Returns
        -------
        None
        """
        data = mp.merge_classattr(type(self), 'CONFIG', copy=True)
        data &= value
        self._config_map = NamedTreeNode(data=data)

    @property
    def styles(self) -> Dict[str, Any]:
        """
        Get the styles dictionary.

        Returns
        -------
        Dict[str, Any]
            The styles dictionary.
        """
        return self._styles_map.data

    @property
    def styles_map(self) -> NamedTreeNode:
        """
        Get the styles map as a NamedTreeNode.

        Returns
        -------
        NamedTreeNode
            The styles map.
        """
        return self._styles_map

    @styles_map.setter
    def styles_map(self, value: Optional[Union[str, Dict[str, Any]]] = None):
        """
        Set the styles map, combining global and class-level defaults with the provided value.

        Parameters
        ----------
        value : Optional[Union[str, Dict[str, Any]]], default None
            Styles for the plot.

        Returns
        -------
        None
        """
        # build from global default
        data = template_styles.get()
        data &= mp.merge_classattr(type(self), 'STYLES', copy=True,
                                   parse=template_styles.parse)
        data &= template_styles.parse(value)
        self._styles_map = NamedTreeNode(data=data)

    @property
    def analysis_label_options(self) -> Optional[Dict[str, Any]]:
        """
        Get the analysis label options.

        Returns
        -------
        Optional[Dict[str, Any]]
            The analysis label options.
        """
        return self._analysis_label_options

    @analysis_label_options.setter
    def analysis_label_options(self, value: Optional[Union[str, Dict[str, Any]]] = None):
        """
        Set the analysis label options.

        Parameters
        ----------
        value : Optional[Union[str, Dict[str, Any]]], default None
            Options for the analysis label.

        Returns
        -------
        None
        """
        if value is None:
            self._analysis_label_options = None
        else:
            self._analysis_label_options = template_analysis_label_options.parse(
                value
            )

    def update_styles_map(
        self, data: Optional[Dict[str, Union[Dict[str, Any], str]]] = None
    ) -> None:
        """
        Update the styles map with additional styles.

        Parameters
        ----------
        data : Optional[Dict[str, Union[Dict[str, Any], str]]], default None
            Additional styles to update.

        Returns
        -------
        None
        """
        if data is None:
            return
        for key, value in data.items():
            self._styles_map[key] = value

    def update_config_map(self, data: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        """
        Update the configuration map with additional configurations.

        Parameters
        ----------
        data : Optional[Dict[str, Dict[str, Any]]], default None
            Additional configuration parameters to update.

        Returns
        -------
        None
        """
        if data is None:
            return
        for key, value in data.items():
            self._config_map[key] = value

    def get_domain_styles(
        self,
        domain: Optional[str] = None,
        copy: bool = True
    ) -> Dict[str, Any]:
        styles = self.styles_map.get(domain, {})
        if copy:
            styles = deepcopy(styles)
        return defaultdict(dict, styles)

    def get_domain_label(
        self,
        name: str,
        domain: Optional[str] = None,
        fallback: bool = False
    ) -> Optional[str]:
        full_domain = self.label_map.format(domain, name)
        if full_domain not in self.label_map:
            if fallback:
                return self.label_map.get(name, None)
            return None
        return self.label_map.get(full_domain, None)

    def add_point(
        self,
        x: float,
        y: float,
        label: Optional[str] = None,
        name: Optional[str] = None,
        styles: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add a point to the plot.

        Parameters
        ----------
        x : float
            The x-coordinate of the point.
        y : float
            The y-coordinate of the point.
        label : Optional[str], default None
            The label for the point.
        name : Optional[str], default None
            The name for the point in the legend.
        styles : Optional[Dict[str, Any]], default None
            Style options for the point.

        Raises
        ------
        RuntimeError
            If a point with the same name is already added.

        Returns
        -------
        None
        """
        if label is not None and name is None:
            name = label
        if name is not None:
            if name in self.legend_order:
                raise RuntimeError(f"point redeclared with the same name: {name}")
        point = {"x": x, "y": y, "label": label, "name": name, "styles": styles}
        self.points.append(point)

    def reset_points(self) -> None:
        """
        Reset the list of points.

        Returns
        -------
        None
        """
        self.points = []

    def add_annotation(self, text: str, **kwargs) -> None:
        """
        Add an annotation to the plot.

        Parameters
        ----------
        text : str
            The text of the annotation.
        **kwargs
            Additional keyword arguments for the annotation.

        Returns
        -------
        None
        """
        annotation = {"text": text, **kwargs}
        self.annotations.append(annotation)

    def reset_annotations(self) -> None:
        """
        Reset the list of annotations.

        Returns
        -------
        None
        """
        self.annotations = []

    def set_color_cycle(
        self, color_cycle: Optional[Union[List[str], str, "ListedColormap"]] = None
    ) -> None:
        """
        Set the color cycle for the plot.

        Parameters
        ----------
        color_cycle : Optional[Union[List[str], str, ListedColormap]], default None
            The color cycle to use.

        Returns
        -------
        None
        """
        if color_cycle is None:
            color_cycle = self.COLOR_CYCLE
        self.cmap = get_cmap(color_cycle)
        self.color_cycle = cycle(self.cmap.colors)

    def reset_color_cycle(self) -> None:
        """
        Reset the color cycle to the beginning.

        Returns
        -------
        None
        """
        self.color_cycle = cycle(self.cmap.colors)

    def get_colors(self) -> List[str]:
        """
        Get the list of colors from the current color cycle.

        Returns
        -------
        List[str]
            The list of colors.
        """
        return get_color_cycle(self.cmap).by_key()["color"]

    def get_default_legend_order(self) -> List[str]:
        """
        Get the default legend order.

        Returns
        -------
        List[str]
            The default legend order.
        """
        return []

    def reset_legend_data(self) -> None:
        """
        Reset the legend data and order.

        Returns
        -------
        None
        """
        self.legend_data = NamedTreeNode()
        self.legend_order = self.get_default_legend_order()

    def get_handle(self, domain: str) -> Optional[Any]:
        """
        Get the legend handle for a given domain.

        Parameters
        ----------
        domain : str
            The domain to retrieve the handle for.

        Returns
        -------
        Optional[Any]
            The legend handle.
        """
        return self.legend_data.get(domain, {}).get("handle", None)

    def update_legend_handles(
        self, handles: Dict[str, Any], domain: Optional[str] = None, raw: bool = False
    ) -> None:
        """
        Update the legend handles.

        Parameters
        ----------
        handles : Dict[str, Any]
            A dictionary mapping names to handles.
        domain : Optional[str], default None
            The domain to update.
        raw : bool, default False
            Whether to use raw handles without processing.

        Returns
        -------
        None
        """
        for name, handle in handles.items():
            if name is None:
                key = domain
            else:
                key = self.legend_data.format(domain, name) if domain else name
            handle, label = resolve_handle_label(handle, raw=raw)
            self.legend_data[key] = {"handle": handle, "label": label}

    def add_legend_decoration(
        self, decorator: Artist, targets: List[str], domain: Optional[str] = None
    ) -> None:
        """
        Add a decorator (an Artist) to legend handles.

        Parameters
        ----------
        decorator : Artist
            The decorator artist to add to the legend entries.
        targets : List[str]
            The list of target legend entries to decorate.
        domain : Optional[str], default None
            The domain of the targets.

        Returns
        -------
        None
        """
        if domain is not None:
            targets = [self.legend_data.format(domain, target) for target in targets]
        for target in targets:
            data = self.legend_data.get(target, None)
            if data is None:
                continue
            handle = data["handle"]
            if isinstance(handle, (list, tuple)):
                new_handle = (*handle, decorator)
            else:
                new_handle = (handle, decorator)
            data["handle"] = new_handle

    def get_legend_handles_labels(
        self, domains: Optional[Union[List[str], str]] = None
    ) -> Tuple[List[Any], List[str]]:
        """
        Get the legend handles and labels.

        Parameters
        ----------
        domains : Optional[Union[List[str], str]], default None
            The domains to retrieve handles and labels for.

        Returns
        -------
        Tuple[List[Any], List[str]]
            The handles and labels.
        """
        if domains is None:
            domains = [None]
        elif isinstance(domains, str):
            domains = [domains]

        handles: List[Any] = []
        labels: List[str] = []

        for name in self.legend_order:
            for domain in domains:
                key = self.legend_data.format(domain, name) if domain else name
                data = self.legend_data.get(key, None)
                if data is None:
                    continue
                handle, label = data["handle"], data["label"]
                if label.startswith("_"):
                    continue
                handles.append(handle)
                labels.append(label)
        return handles, labels

    def get_labelled_legend_domains(self):
        result = []
        for domain in self.legend_data.domains:
            data = self.legend_data.get(domain)
            if data['label'].startswith('_'):
                continue
            result.append(domain)
        return result

    def reset_metadata(self) -> None:
        self.reset_legend_data()
        
    def reset(self) -> None:
        self.reset_metadata()
        self.reset_annotations()
        self.reset_points()

    def draw_frame(self, ratio: bool = False, **kwargs) -> plt.Axes:
        """
        Draw the plot frame.

        Parameters
        ----------
        ratio : bool, default False
            Whether to draw a ratio plot frame.
        **kwargs
            Additional keyword arguments for the frame method.

        Returns
        -------
        plt.Axes
            The matplotlib axes object.
        """
        frame_method = ratio_frame if ratio else single_frame
        ax = frame_method(
            styles=self.styles,
            prop_cycle=get_color_cycle(self.cmap),
            analysis_label_options=self.analysis_label_options,
            figure_index=self.figure_index,
            **kwargs,
        )

        self.figure = plt.gcf()
        return ax

    def draw_annotations(self, ax: plt.Axes) -> None:
        """
        Draw annotations on the plot.

        Parameters
        ----------
        ax : plt.Axes
            The axes to draw annotations on.

        Returns
        -------
        None
        """
        for options in self.annotations:
            options = mp.concatenate((self.styles["annotation"], options), copy=True)
            ax.annotate(**options)

    def draw_points(self, ax: plt.Axes) -> None:
        """
        Draw points on the plot.

        Parameters
        ----------
        ax : plt.Axes
            The axes to draw points on.

        Returns
        -------
        None
        """
        for point in self.points:
            styles = mp.concat((self.styles.get("point"), point.get("styles")))
            handle = ax.plot(
                point["x"],
                point["y"],
                label=point["label"],
                **styles,
            )
            name = point.get('name')
            if name is not None:
                self.update_legend_handles({name: handle[0]})
                self.legend_order.append(name)

    def draw_axis_labels(
        self,
        ax: plt.Axes,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        xlabellinebreak: Optional[int] = None,
        ylabellinebreak: Optional[int] = None,
        combined_styles: Optional[Dict[str, Any]] = None,
        title: Optional[str] = None,
    ) -> None:
        """
        Draw axis labels and title.

        Parameters
        ----------
        ax : plt.Axes
            The axes to set labels on.
        xlabel : Optional[str], default None
            The x-axis label.
        ylabel : Optional[str], default None
            The y-axis label.
        xlabellinebreak : Optional[int], default None
            The character limit for line breaks in the x-axis label.
        ylabellinebreak : Optional[int], default None
            The character limit for line breaks in the y-axis label.
        combined_styles : Optional[Dict[str, Any]], default None
            Combined styles for labels.
        title : Optional[str], default None
            The plot title.

        Returns
        -------
        None
        """
        if combined_styles is None:
            combined_styles = self.styles
        if xlabel is not None:
            if xlabellinebreak is not None and xlabel.count("$") < 2:
                xlabel = insert_periodic_substr(xlabel, xlabellinebreak)
            ax.set_xlabel(xlabel, **combined_styles["xlabel"])
        if ylabel is not None:
            if ylabellinebreak is not None and ylabel.count("$") < 2:
                ylabel = insert_periodic_substr(ylabel, ylabellinebreak)
            ax.set_ylabel(ylabel, **combined_styles["ylabel"])
        if title is not None:
            ax.set_title(title, **self.styles["title"])

    def draw_text(
        self,
        ax: plt.Axes,
        text: str,
        x: float,
        y: float,
        dy: float = 0.05,
        transform_x: str = "axis",
        transform_y: str = "axis",
        **kwargs,
    ) -> None:
        """
        Draw multiline text on the plot.

        Parameters
        ----------
        ax : plt.Axes
            The axes to draw text on.
        text : str
            The text to draw.
        x : float
            The x-coordinate.
        y : float
            The y-coordinate.
        dy : float, default 0.05
            Vertical spacing between lines.
        transform_x : str, default "axis"
            Coordinate transform for x.
        transform_y : str, default "axis"
            Coordinate transform for y.
        **kwargs
            Additional style arguments for the text.

        Returns
        -------
        None
        """
        styles = mp.concat((self.styles["text"], kwargs))
        draw_multiline_text(
            ax,
            x,
            y,
            text,
            dy=dy,
            transform_x=transform_x,
            transform_y=transform_y,
            **styles,
        )

    def draw_axis_components(
        self,
        ax: plt.Axes,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        ylim: Optional[Tuple[float, float]] = None,
        xlim: Optional[Tuple[float, float]] = None,
        xticks: Optional[List[float]] = None,
        yticks: Optional[List[float]] = None,
        xticklabels: Optional[List[str]] = None,
        yticklabels: Optional[List[str]] = None,
        combined_styles: Optional[Dict[str, Any]] = None,
        title: Optional[str] = None,
    ) -> None:
        """
        Draw axis labels, ticks, and other components.

        Parameters
        ----------
        ax : plt.Axes
            The axes to draw on.
        xlabel : Optional[str], default None
            The x-axis label.
        ylabel : Optional[str], default None
            The y-axis label.
        ylim : Optional[Tuple[float, float]], default None
            The y-axis limits.
        xlim : Optional[Tuple[float, float]], default None
            The x-axis limits.
        xticks : Optional[List[float]], default None
            The x-axis tick positions.
        yticks : Optional[List[float]], default None
            The y-axis tick positions.
        xticklabels : Optional[List[str]], default None
            The x-axis tick labels.
        yticklabels : Optional[List[str]], default None
            The y-axis tick labels.
        combined_styles : Optional[Dict[str, Any]], default None
            Combined styles for axis components.
        title : Optional[str], default None
            The plot title.

        Returns
        -------
        None
        """
        if combined_styles is None:
            combined_styles = self.styles
        self.draw_axis_labels(
            ax,
            xlabel,
            ylabel,
            xlabellinebreak=self.config["xlabellinebreak"],
            ylabellinebreak=self.config["ylabellinebreak"],
            combined_styles=combined_styles,
            title=title,
        )

        format_axis_ticks(
            ax,
            **combined_styles["axis"],
            xtick_styles=combined_styles["xtick"],
            ytick_styles=combined_styles["ytick"],
        )

        if ylim is not None:
            ax.set_ylim(*ylim)
        if xlim is not None:
            ax.set_xlim(*xlim)
        if xticks is not None:
            ax.set_xticks(xticks)
        if yticks is not None:
            ax.set_yticks(yticks)
        if xticklabels is not None:
            ax.set_xticklabels(xticklabels)
        if yticklabels is not None:
            ax.set_yticklabels(yticklabels)

    def set_axis_range(
        self,
        ax: plt.Axes,
        xmin: Optional[float] = None,
        xmax: Optional[float] = None,
        ymin: Optional[float] = None,
        ymax: Optional[float] = None,
        ypadlo: Optional[float] = None,
        ypadhi: Optional[float] = None,
        ypad: Optional[float] = None,
    ) -> None:
        """
        Set the axis range with optional padding.

        Parameters
        ----------
        ax : plt.Axes
            The axes to set range on.
        xmin : Optional[float], default None
            Minimum x-limit.
        xmax : Optional[float], default None
            Maximum x-limit.
        ymin : Optional[float], default None
            Minimum y-limit.
        ymax : Optional[float], default None
            Maximum y-limit.
        ypadlo : Optional[float], default None
            Lower y-padding as a fraction of the data range.
        ypadhi : Optional[float], default None
            Upper y-padding as a fraction of the data range.
        ypad : Optional[float], default None
            Symmetric y-padding as a fraction of the data range.

        Returns
        -------
        None
        """
        xlim, ylim = get_axis_limits(
            ax,
            xmin=xmin,
            xmax=xmax,
            ymin=ymin,
            ymax=ymax,
            ypadlo=ypadlo,
            ypadhi=ypadhi,
            ypad=ypad,
        )
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)

    @staticmethod
    def close_all_figures() -> None:
        """
        Close all matplotlib figures.

        Returns
        -------
        None
        """
        plt.close("all")

    def decorate_comparison_axis(
        self,
        ax: plt.Axes,
        xlabel: str = "",
        ylabel: str = "",
        mode: Union[HistComparisonMode, str, Callable] = "ratio",
        ylim: Optional[Sequence[float]] = None,
        ypad: Optional[float] = 0.1,
        draw_ratio_line: bool = True,
    ) -> None:
        """
        Decorate a comparison axis (e.g., ratio or difference plot).

        Parameters
        ----------
        ax : plt.Axes
            The axes to decorate.
        xlabel : str, default ""
            The x-axis label.
        ylabel : str, default ""
            The y-axis label.
        mode : Union[HistComparisonMode, str, Callable], default "ratio"
            The comparison mode.
        ylim : Optional[Sequence[float]], default None
            The y-axis limits.
        ypad : Optional[float], default 0.1
            Padding for centralization.
        draw_ratio_line : bool, default True
            Whether to draw the ratio line.

        Returns
        -------
        None
        """
        if ylim is not None:
            ax.set_ylim(ylim)
        do_centralize_axis = ylim is None
        if not callable(mode):
            mode = HistComparisonMode.parse(mode)
            if mode == HistComparisonMode.RATIO:
                if do_centralize_axis:
                    centralize_axis(ax, which="y", ref_value=1, padding=ypad)
                if draw_ratio_line:
                    ax.axhline(1, **self.config["ratio_line_styles"])
                if not ylabel:
                    ylabel = "Ratio"
            elif mode == HistComparisonMode.DIFFERENCE:
                if do_centralize_axis:
                    centralize_axis(ax, which="y", ref_value=0, padding=ypad)
                if draw_ratio_line:
                    ax.axhline(0, **self.config["ratio_line_styles"])
                if not ylabel:
                    ylabel = "Difference"
            else:
                # For unrecognized modes, do not set ylabel
                pass
        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)

    def draw_legend(
        self,
        ax: plt.Axes,
        handles: Optional[List[Any]] = None,
        labels: Optional[List[str]] = None,
        handler_map: Optional[Dict[Any, Any]] = None,
        domains: Optional[Union[List[str], str]] = None,
        **kwargs,
    ) -> None:
        """
        Draw the legend on the plot.

        Parameters
        ----------
        ax : plt.Axes
            The axes to draw the legend on.
        handles : Optional[List[Any]], default None
            The legend handles.
        labels : Optional[List[str]], default None
            The legend labels.
        handler_map : Optional[Dict[Any, Any]], default None
            A mapping of types to legend handlers.
        domains : Optional[Union[List[str], str]], default None
            The domains to include in the legend.
        **kwargs
            Additional keyword arguments for the legend.

        Returns
        -------
        None
        """
        if handles is None and labels is None:
            handles, labels = self.get_legend_handles_labels(domains)
        if not handles:
            return
        if handler_map is None:
            handler_map = {}
        handler_map = {**CUSTOM_HANDLER_MAP, **handler_map}
        styles = {**self.styles["legend"], **kwargs}
        styles["handler_map"] = handler_map
        ax.legend(handles, labels, **styles)

    def stretch_axis(
        self,
        ax: plt.Axes,
        xlim: Optional[Tuple[float, float]] = None,
        ylim: Optional[Tuple[float, float]] = None,
    ) -> None:
        """
        Stretch the axis limits to include new ranges.

        Parameters
        ----------
        ax : plt.Axes
            The axes to adjust.
        xlim : Optional[Tuple[float, float]], default None
            New x-axis limits to include.
        ylim : Optional[Tuple[float, float]], default None
            New y-axis limits to include.

        Returns
        -------
        None
        """
        if xlim is not None:
            xlim_curr = ax.get_xlim()
            ax.set_xlim(min(xlim[0], xlim_curr[0]), max(xlim[1], xlim_curr[1]))
        if ylim is not None:
            ylim_curr = ax.get_ylim()
            ax.set_ylim(min(ylim[0], ylim_curr[0]), max(ylim[1], ylim_curr[1]))

    def finalize(self, ax: plt.Axes) -> None:
        """
        Finalize the plot by drawing points and annotations.

        Parameters
        ----------
        ax : plt.Axes
            The axes to finalize.

        Returns
        -------
        None
        """
        self.draw_points(ax)
        self.draw_annotations(ax)