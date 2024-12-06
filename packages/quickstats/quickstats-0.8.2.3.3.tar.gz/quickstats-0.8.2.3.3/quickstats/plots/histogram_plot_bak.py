from typing import Optional, Union, Dict, Tuple, List, Callable

import numpy as np
from matplotlib.artist import Artist
from matplotlib.axes import Axes

from quickstats.core import mappings as mp
from quickstats.maths.numerics import get_subsequences
from quickstats.concepts import Histogram1D, StackedHistogram
from .abstract_plot import AbstractPlot
from .core import PlotFormat, ErrorDisplayFormat
from .template import get_artist_colors, is_transparent_color, remake_handles


def check_consistency(y1: np.ndarray, y2: np.ndarray) -> None:
    """
    Check if two arrays are consistent by verifying if their values match.

    Parameters
    ----------
    y1 : np.ndarray
        First array to compare.
    y2 : np.ndarray
        Second array to compare.

    Raises
    ------
    RuntimeError
        If the arrays do not match.
    """
    if not np.allclose(y1, y2):
        raise RuntimeError(
            "histogram bin values do not match the supplied weights; please check your inputs."
        )


def get_masked_error(
    error: Optional[Union[Tuple[np.ndarray, np.ndarray], np.ndarray]],
    mask: np.ndarray,
) -> Optional[Union[Tuple[np.ndarray, np.ndarray], np.ndarray]]:
    """
    Apply a mask to the error array or tuple of error arrays.

    Parameters
    ----------
    error : Optional[Union[Tuple[np.ndarray, np.ndarray], np.ndarray]]
        Error data, either as a tuple of arrays or a single array.
    mask : np.ndarray
        Boolean mask to apply to the error data.

    Returns
    -------
    Optional[Union[Tuple[np.ndarray, np.ndarray], np.ndarray]]
        Masked error data or None if no error data is provided.
    """
    if error is None:
        return None
    if isinstance(error, tuple):
        return error[0][mask], error[1][mask]
    return error[mask]


def has_color_option(styles: Dict) -> bool:
    """
    Check if the styles dictionary contains any color-related options.

    Parameters
    ----------
    styles : Dict
        Dictionary of style options.

    Returns
    -------
    bool
        True if any color option is present, False otherwise.
    """
    color_options = {'color', 'facecolor', 'edgecolor', 'colors'}
    return any(option in styles for option in color_options)


class HistogramPlot(AbstractPlot):
    """
    Class for plotting histograms with various styles and error displays.
    """

    COLOR_CYCLE = "atlas_hdbs"

    STYLES = {
        "hist": {
            "histtype": "step",
            "linestyle": "-",
            "linewidth": 2,
        },
        "errorbar": {
            "marker": "o",
            "markersize": 10,
            "linestyle": "none",
            "linewidth": 0,
            "elinewidth": 2,
            "capsize": 0,
            "capthick": 0,
        },
        "fill_between": {
            "alpha": 0.5,
            "color": "gray",
        },
        "bar": {
            "linewidth": 0,
            "alpha": 0.5,
            "color": "gray",
        },
    }

    CONFIG = {
        "show_xerr": False,
        "error_on_top": True,
        "inherit_color": True,
        "combine_stacked_error": False,
        "box_legend_handle": False,
        "isolate_error_legend": False,
    }

    def draw_hist(
        self,
        ax: Axes,
        histogram: Union[Histogram1D, StackedHistogram],
        styles: Optional[Dict] = None,
    ) -> List[Artist]:
        """
        Draw a histogram on the given axis.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axis to draw the histogram on.
        histogram : Union[Histogram1D, StackedHistogram]
            Histogram data to be plotted.
        styles : Optional[Dict], optional
            Additional styling options for the histogram, by default None.

        Returns
        -------
        List[Artist]
            Handles for the drawn histogram bars.

        Raises
        ------
        TypeError
            If the histogram type is unsupported.
        """
        styles = mp.concat((self.styles["hist"], styles), copy=True)

        if isinstance(histogram, Histogram1D):
            n, _, patches = ax.hist(
                histogram.bin_centers,
                weights=histogram.bin_content,
                bins=histogram.bin_edges,
                **styles,
            )
            handles = [patches]
            check_consistency(n, histogram.bin_content)
        elif isinstance(histogram, StackedHistogram):
            x = [h.bin_centers for h in histogram.histograms.values()]
            y = [h.bin_content for h in histogram.histograms.values()]
            n, _, patches = ax.hist(
                x,
                weights=y,
                bins=histogram.bin_edges,
                stacked=True,
                **styles,
            )
            handles = list(patches)
            y_base = 0.
            for n_i, y_i in zip(n, y):
                check_consistency(n_i - y_base, y_i)
                y_base += y_i
        else:
            raise TypeError(f"unsupported histogram type: {type(histogram)}")

        return handles

    def draw_errorbar(
        self,
        ax: Axes,
        histogram: Union[Histogram1D, StackedHistogram],
        styles: Optional[Dict] = None,
        with_error: bool = True,
    ) -> Artist:
        """
        Draw an error bar plot for the histogram data.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axis to draw the error bars on.
        histogram : Union[Histogram1D, StackedHistogram]
            Histogram data to be plotted.
        styles : Optional[Dict], optional
            Additional styling options for the error bars, by default None.
        with_error : bool, optional
            Whether to display error bars, by default True.

        Returns
        -------
        Artist
            Handle for the error bar plot.
        """
        styles = mp.concat((self.styles["errorbar"], styles))
        x = histogram.bin_centers
        y = histogram.bin_content

        if with_error:
            xerr = histogram.bin_widths / 2 if self.config['show_xerr'] else None
            yerr = histogram.bin_errors
        else:
            xerr = None
            yerr = None

        if histogram.is_masked():
            mask = ~histogram.bin_mask
            x = x[mask]
            y = y[mask]
            xerr = get_masked_error(xerr, mask)
            yerr = get_masked_error(yerr, mask)

        handle = ax.errorbar(x, y, xerr=xerr, yerr=yerr, **styles)
        return handle

    def draw_filled_error(
        self,
        ax: Axes,
        histogram: Union[Histogram1D, StackedHistogram],
        styles: Optional[Dict] = None,
    ) -> Artist:
        """
        Draw filled error regions on the plot.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axis to draw the filled error regions on.
        histogram : Union[Histogram1D, StackedHistogram]
            Histogram data to be plotted.
        styles : Optional[Dict], optional
            Additional styling options for the filled areas, by default None.

        Returns
        -------
        Artist
            Handle for the filled error region.

        Raises
        ------
        RuntimeError
            If the histogram is fully masked and nothing can be drawn.
        """
        styles = mp.concat((self.styles['fill_between'], styles), copy=True)
        x = histogram.bin_centers
        rel_yerr = histogram.rel_bin_errors
        if rel_yerr is None:
            rel_yerr = (histogram.bin_content, histogram.bin_content)
            # make artist transparent
            styles['color'] = 'none'
            styles.pop('facecolor', None)
            styles.pop('edgecolor', None)

        handle = None
        if histogram.is_masked():
            # handle cases where data is not continuous
            indices = np.arange(np.shape(x)[0])
            mask = ~histogram.bin_mask
            section_indices = get_subsequences(indices, mask, min_length=2)
            if not len(section_indices):
                raise RuntimeError('histogram is fully masked, nothing to draw')
            for indices in section_indices:
                mask = np.full(x.shape, False)
                mask[indices] = True
                x_i = x[mask]
                rel_yerr_i = get_masked_error(rel_yerr, mask)
                # extend to edge
                x_i[0] = histogram.bin_edges[indices[0]]
                x_i[-1] = histogram.bin_edges[indices[-1] + 1]
                if (handle is not None) and (not has_color_option(styles)):
                    styles['color'] = handle.get_facecolors()[0]
                handle_i = ax.fill_between(x_i, rel_yerr_i[0], rel_yerr_i[1], **styles)
                if handle is None:
                    handle = handle_i
        else:
            handle = ax.fill_between(x, rel_yerr[0], rel_yerr[1], **styles)
        return handle

    def draw_shaded_error(
        self,
        ax: Axes,
        histogram: Union[Histogram1D, StackedHistogram],
        styles: Optional[Dict] = None,
    ) -> Artist:
        """
        Draw shaded error bars as a bar plot.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axis to draw the shaded error bars on.
        histogram : Union[Histogram1D, StackedHistogram]
            Histogram data to be plotted.
        styles : Optional[Dict], optional
            Additional styling options for the bars, by default None.

        Returns
        -------
        Artist
            Handle for the drawn bars.
        """
        styles = mp.concat((self.styles["bar"], styles), copy=True)
        x = histogram.bin_centers
        y = histogram.bin_content
        yerr = histogram.bin_errors

        if yerr is None:
            yerr = (np.zeros_like(y), np.zeros_like(y))
            styles["color"] = "none"
            styles.pop("facecolor", None)
            styles.pop("edgecolor", None)

        height = yerr[0] + yerr[1]
        bottom = y - yerr[0]
        widths = histogram.bin_widths

        handle = ax.bar(x, height=height, bottom=bottom, width=widths, **styles)
        return handle

    def draw_histogram_data(
        self,
        ax: "matplotlib.axes.Axes",
        histogram: Union[Histogram1D, StackedHistogram],
        plot_format: Union[PlotFormat, str] = 'errorbar',
        error_format: Union[ErrorDisplayFormat, str] = 'errorbar',
        styles: Optional[Dict] = None,
        error_styles: Optional[Dict] = None,
        domain: str = 'main'
    ):
        """
        Draws the histogram data with the specified plot and error formats.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axis to draw the data on.
        histogram : Union[Histogram1D, StackedHistogram]
            Histogram data to be plotted.
        plot_format : Union[PlotFormat, str], optional
            Format for plotting the histogram, by default 'errorbar'.
        error_format : Union[ErrorDisplayFormat, str], optional
            Format for plotting the error, by default 'errorbar'.
        styles : Optional[Dict], optional
            Styling options for the plot, by default None.
        error_styles : Optional[Dict], optional
            Styling options for the error representation, by default None.

        Returns
        -------
        Tuple[List, List]
            Handles for the plot and error elements.
        """
        styles = styles or {}
        error_styles = error_styles or {}
        plot_format = PlotFormat.parse(plot_format)
        error_format = ErrorDisplayFormat.parse(error_format)

        plot_handles, error_handles = [], []

        if plot_format == PlotFormat.HIST:
            handles = self.draw_hist(ax, histogram, styles=styles)
            plot_handles.extend(handles)

        def custom_draw(histogram_c, styles_c, error_styles_c):
            if plot_format == PlotFormat.ERRORBAR:
                with_error = error_format == ErrorDisplayFormat.ERRORBAR
                handle = self.draw_errorbar(ax, histogram_c, styles=styles_c, with_error=with_error)
                plot_handles.append(handle)
            # inherit colors from plot handle
            # priority: edgecolor > facecolor
            if not has_color_option(error_styles_c):
                plot_handle = plot_handles[len(error_handles)]
                if plot_format == PlotFormat.HIST:
                    # case histtype = 'step' or 'stepfilled'
                    if isinstance(plot_handle, list):
                        plot_handle = plot_handle[0]
                    colors = get_artist_colors(plot_handle)
                    color = colors['edgecolor']
                    if is_transparent_color(color):
                        color = colors['facecolor']
                elif plot_format == PlotFormat.ERRORBAR:
                    # marker handle
                    plot_handle = plot_handle[0]
                    colors = get_artist_colors(plot_handle)
                    color = colors['markeredgecolor']
                    if is_transparent_color(color):
                        color = colors['markerfacecolor']
                else:
                    raise ValueError(f'unsupported plot format: {plot_format}')
                zorder = plot_handle.get_zorder()
                if self.config['error_on_top']:
                    error_styles_c['zorder'] = zorder + 0.1
                if self.config['inherit_color']:
                    error_styles_c['color'] = color
            if error_styles_c.get('color', None) is None:
                error_styles_c.pop('color')
            # draw errors
            if error_format == ErrorDisplayFormat.FILL:
                handle = self.draw_filled_error(ax, histogram_c, styles=error_styles_c)
                error_handles.append(handle)
            elif error_format == ErrorDisplayFormat.SHADE:
                handle = self.draw_shaded_error(ax, histogram_c, styles=error_styles_c)
                error_handles.append(handle)
            elif (error_format == ErrorDisplayFormat.ERRORBAR) and (plot_format != PlotFormat.ERRORBAR):
                error_styles_c = mp.concat((error_styles_c, {'marker': 'none'}), copy=True)
                handle = self.draw_errorbar(ax, histogram_c, styles=error_styles_c, with_error=True)
                error_handles.append(handle)

        combine_stacked_error = self.config['combine_stacked_error']
        # must draw error for individual histogram when plot with errorbar
        if plot_format == PlotFormat.ERRORBAR:
            combine_stacked_error = False
        if isinstance(histogram, Histogram1D) or \
           (isinstance(histogram, StackedHistogram) and combine_stacked_error):
            error_color = error_styles.get('color')
            # use artist default color when drawn
            if isinstance(error_color, list):
                error_color = None
            error_label = error_styles.get('label')
            if isinstance(error_label, list):
                error_label = self.label_map.get(f'{domain}.error', domain)
            error_styles = mp.concat((error_styles, {'color': error_color, 'label': error_label}), copy=True)
            custom_draw(histogram, styles, error_styles)
        elif isinstance(histogram, StackedHistogram):
            def make_list(option):
                if option is None:
                    return [None] * histogram.count
                if not isinstance(option, list):
                    return [option] * histogram.count
                assert len(option) == histogram.count
                return option
            colors = make_list(styles.get('color', None))
            labels = make_list(styles.get('label', None))
            error_colors = make_list(error_styles.get('color', None))
            error_labels = make_list(error_styles.get('label', None))
            for i, (_, histogram_i) in enumerate(histogram.offset_histograms):
                styles_i = mp.concat((styles, {'color': colors[i], 'label': labels[i]}), copy=True)
                error_styles_i = mp.concat((error_styles, {'color': error_colors[i], 'label': error_labels[i]}), copy=True)
                custom_draw(histogram_i, styles_i, error_styles_i)

        handles = {}
        # there should be one-to-one correspondence between plot handle and error handle
        # except when plotting stacked histograms but showing merged errors
        if isinstance(histogram, StackedHistogram) and (combine_stacked_error):
            assert (len(plot_handles) == histogram.count) and (len(error_handles) == 1)
            for name, handle in zip(histogram.histograms.keys(), plot_handles):
                handles[f'{domain}.{name}'] = handle
            if histogram.has_errors():
                handles[f'{domain}.error'] = error_handles[0]
        else:
            if (plot_format == PlotFormat.ERRORBAR) and (error_format == ErrorDisplayFormat.ERRORBAR):
                assert len(error_handles) == 0
                error_handles = [None] * len(plot_handles)
            else:
                assert len(plot_handles) == len(error_handles)
            if isinstance(histogram, StackedHistogram):
                keys = [f'{domain}.{name}' for name in histogram.histograms.keys()]
            else:
                keys = [domain]
            isolate_error_legend = self.config['isolate_error_legend']
            for key, plot_handle, error_handle in zip(keys, plot_handles, error_handles):
                # case histogram plot with histtype = 'step' or 'stepfilled'
                if isinstance(plot_handle, list):
                    plot_handle = plot_handle[0]
                if error_handle is None:
                    handles[key] = plot_handle
                else:
                    if isolate_error_legend:
                        handles[key] = plot_handle
                        handles[f'{key}.error'] = error_handle
                    else:
                        if self.config['error_on_top']:
                            handles[key] = (plot_handle, error_handle)
                        else:
                            handles[key] = (error_handle, plot_handle)
                
        if not self.config['box_legend_handle']:
            for key, handle in handles.items():
                handles[key] = remake_handles([handle], polygon_to_line=True, fill_border=False)[0]
        return handles