from typing import Dict, Optional, Union, List, Sequence

from functools import partial
from itertools import repeat

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from quickstats.plots import AbstractPlot
from quickstats.plots.template import create_transform, format_axis_ticks, isolate_contour_styles
from quickstats.utils.common_utils import combine_dict
from quickstats.utils.string_utils import remove_neg_zero
from quickstats.maths.interpolation import get_regular_meshgrid
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon, Rectangle


class Likelihood2DPlot(AbstractPlot):

    STYLES = {
        'pcolormesh': {
            'cmap': 'GnBu',
            'shading': 'auto',
            'rasterized': True
        },
        'colorbar': {
            'pad': 0.02,            
        },
        'contour': {
            'linestyles': 'solid',
            'linewidths': 3
        },
        'contourf': {
            'alpha': 0.5,
            'zorder': 0 
        },
        'polygon': {
            'fill': True,
            'hatch': '/',
            'alpha': 0.5,
            'color': 'gray'            
        },
        'alphashape': {
            'alpha': 2
        },
        'bestfit': {
            'marker': 'P',
            'linewidth': 0,
            'markersize': 15
        },
        'highlight': {
            'linewidth': 0,
            'marker': '*',
            'markersize': 20,
            'color': '#E9F1DF',
            'markeredgecolor': 'black'            
        }
    }

    LABEL_MAP = {
        'contour': '{sigma_label}',
        'bestfit': 'Best fit ({x:.2f}, {y:.2f})',
        'polygon': 'Nan NLL region'
    }

    CONFIG = {
        # intervals to include in the plot
        'interval_formats': {
            "68_95"               : ('0.68', '0.95'),
            "one_two_sigma"       : ('1sigma', '2sigma'),
            "68_95_99"            : ('0.68', '0.95', '0.99'),
            "one_two_three_sigma" : ('1sigma', '2sigma', '3sigma')
        },
        'interpolation': 'cubic',
        'num_grid_points': 500,
        'sm_values': None,
        'sm_line_styles': {}
    }
    
    # qmu from https://pdg.lbl.gov/2018/reviews/rpp2018-rev-statistics.pdf#page=31
    COVERAGE_PROBA_DATA = {
        '0.68': {
            'qmu': 2.30,
            'label': '68% CL',
            'color': "hh:darkblue"
        },
        '1sigma': {  
            'qmu': 2.30, # 68.2%
            'label': '1 $\sigma$',
            'color': "hh:darkblue"
        },
        '0.90': {
            'qmu': 4.61,
            'label': '90% CL',
            'color': "#36b1bf"
        },
        '0.95': {
            'qmu': 5.99,
            'label': '95% CL',
            'color': "#F2385A"
        },
        '2sigma': {
            'qmu': 6.18, # 95.45%
            'label': '2 $\sigma$',
            'color': "#F2385A"
        },
        '0.99': {
            'qmu': 9.21,
            'label': '99% CL',
            'color': "#FDC536"
        },
        '3sigma': {
            'qmu': 11.83, # 99.73%
            'label': '3 $\sigma$',
            'color': "#FDC536"
        }
    }

    def __init__(self, data_map: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
                 label_map: Optional[Dict] = None,
                 color_cycle: Optional[Union[List, str, "ListedColorMap"]]=None,
                 styles: Optional[Union[Dict, str]] = None,
                 styles_map: Optional[Dict] = None,
                 analysis_label_options: Optional[Dict] = None,
                 config: Optional[Dict] = None):

        self.data_map = data_map
        self.styles_map = combine_dict(styles_map)
        self.coverage_proba_data = combine_dict(self.COVERAGE_PROBA_DATA)
        self.highlight_data = []
        super().__init__(label_map=label_map,
                         styles=styles,
                         color_cycle=color_cycle,
                         analysis_label_options=analysis_label_options,
                         config=config)
        
    def get_sigma_levels(self, interval_format:str="one_two_three_sigma"):
        if interval_format not in self.config['interval_formats']:
            choices = ','.join([f'"{choice}"' for choice in self.config['interval_formats']])
            raise ValueError(f'undefined sigma interval format: {interval_format} (choose from {choices})')
        sigma_levels = self.config['interval_formats'][interval_format]
        return sigma_levels

    def get_nan_shapes(self, data: pd.DataFrame,
                       xattrib: str, yattrib: str,
                       zattrib: str = 'qmu'):
        df_nan = data[np.isnan(data[zattrib])]
        xy = df_nan[[xattrib, yattrib]].values
        import alphashape
        shape = alphashape.alphashape(xy, alpha=self.config['alphashape_alpha'])
        if hasattr(shape, 'geoms'):
            shapes = [s for s in shape.geoms]
        else:
            shapes = [shape]
        return shapes
    
    def draw_shades(self, ax, shapes):
        if len(shapes) == 0:
            return None
        for shape in shapes:
            x, y = shape.exterior.coords.xy
            xy = np.column_stack((np.array(x).ravel(), np.array(y).ravel()))
            polygon = Polygon(xy, **self.config['polygon_styles'],
                              label=self.config['polygon_label'])
            ax.add_patch(polygon)
            if 'shade' not in self.legend_data:
                self.update_legend_handles({'shade': polygon})
                self.legend_order.append('shade')

    def draw_single_data(self, ax, data: pd.DataFrame,
                         xattrib: str, yattrib: str,
                         zattrib: str = 'qmu',
                         config: Optional[Dict] = None,
                         styles: Optional[Dict] = None,
                         draw_contour: bool = True,
                         draw_contourf: bool =False,
                         draw_colormesh: bool = False,
                         draw_clabel: bool = False,
                         draw_colorbar: bool =True,
                         clabel_size=None,
                         interval_format:str="one_two_three_sigma",
                         remove_nan_points_within_distance:Optional[float]=None,
                         shade_nan_points:bool=False,
                         domain: Optional[str] = None):

        handles = {}
        sigma_handles = {}
        if config is None:
            config = self.config
        if styles is None:
            styles = self.styles
            
        sigma_levels = self.get_sigma_levels(interval_format=interval_format)
        sigma_values = [self.coverage_proba_data[level]['qmu'] for level in sigma_levels]
        sigma_labels = [self.coverage_proba_data[level]['label'] for level in sigma_levels]
        sigma_colors = [self.coverage_proba_data[level]['color'] for level in sigma_levels]

        contour_labels = []
        for sigma_label in sigma_labels:
            contour_label_fmt = self.get_label('contour', domain=domain)
            if not contour_label_fmt:
                contour_label_fmt = self.get_label('contour')
            contour_label = contour_label_fmt.format(sigma_label=sigma_label)
            contour_labels.append(contour_label)

        interpolate_method = self.config.get('interpolation', None)
        if interpolate_method:
            from scipy import interpolate
            x, y, z = data[xattrib], data[yattrib], data[zattrib]
            # remove nan data
            mask = ~np.isnan(z)
            x, y, z = x[mask], y[mask], z[mask]
            
            n = self.config.get('num_grid_points', 500)
            X, Y = get_regular_meshgrid(x, y, n=n)
            Z = interpolate.griddata(np.stack((x, y), axis=1), z, (X, Y), interpolate_method)
        else:
            X_unique = np.sort(data[xattrib].unique())
            Y_unique = np.sort(data[yattrib].unique())
            X, Y = np.meshgrid(X_unique, Y_unique)
            Z = (data.pivot_table(index=xattrib, columns=yattrib, values=zattrib).T.values
                 - data[zattrib].min())

        # deal with regions with undefined likelihood
        if (remove_nan_points_within_distance is not None) or (shade_nan_points):
            nan_shapes = self.get_nan_shapes(data, xattrib, yattrib, zattrib)
        else:
            nan_shapes = None
        if (remove_nan_points_within_distance is not None) and (len(nan_shapes) > 0):
            if len(nan_shapes) > 0:
                from shapely import Point
                XY = np.column_stack((X.ravel(), Y.ravel()))
                d = remove_nan_points_within_distance
                for shape in nan_shapes:
                    x_ext, y_ext = shape.exterior.coords.xy
                    min_x_cutoff, max_x_cutoff = np.min(x_ext) - d, np.max(x_ext) + d
                    min_y_cutoff, max_y_cutoff = np.min(y_ext) - d, np.max(y_ext) + d
                    # only focus on points within the largest box formed by the convex hull + distance
                    box_mask = (((XY[:, 0] > min_x_cutoff) & (XY[:, 0] < max_x_cutoff)) & 
                                ((XY[:, 1] > min_y_cutoff) & (XY[:, 1] < max_y_cutoff)))
                    mask = np.full(box_mask.shape, False)
                    XY_box = XY[box_mask]
                    # remove points inside the polygon
                    mask_int = np.array([shape.contains(Point(xy)) for xy in XY_box])
                    XY_box_ext = XY_box[~mask_int]
                    # remove points within distance d of the polygon
                    mask_int_d = np.array([shape.exterior.distance(Point(xy)) < d for xy in XY_box_ext])
                    slice_int = np.arange(mask.shape[0])[box_mask][mask_int]
                    slice_int_d = np.arange(mask.shape[0])[box_mask][~mask_int][mask_int_d]
                    mask[slice_int] = True
                    mask[slice_int_d] = True
                    Z[mask.reshape(Z.shape)] = np.nan
        
        if draw_colormesh:
            pcm = ax.pcolormesh(X, Y, Z, **styles['pcolormesh'])
            handles['pcm'] = pcm

        if sigma_values:
            
            if draw_contour:
                contour_styles = combine_dict(styles['contour'])
                if 'colors' not in contour_styles:
                    contour_styles['colors'] = sigma_colors
                contour = ax.contour(X, Y, Z, levels=sigma_values, **contour_styles)
                handles['contour'] = contour

                if draw_clabel:
                    clabel = ax.clabel(contour, **styles['clabel'])
                    handles['clabel'] = clabel

                # handle for individual contour level
                sigma_contour_styles = isolate_contour_styles(contour_styles)
                for i, (styles_, label_, color_) in enumerate(zip(sigma_contour_styles, contour_labels, sigma_colors)):
                    kwargs = combine_dict(styles_)
                    kwargs['label'] = label_
                    if 'color' not in kwargs:
                        kwargs['color'] = color_
                    handle = Line2D([0], [0], **kwargs)
                    key = f'contour_level_{i}'
                    sigma_handles[key] = handle
                    if key not in self.legend_order:
                        self.legend_order.append(key)
                
            if draw_contourf:
                contourf_styles = combine_dict(styles['contourf'])
                if 'colors' not in contourf_styles:
                    contourf_styles['colors'] = sigma_colors
                sigma_values_ = [-np.inf] + sigma_values
                contourf = ax.contourf(X, Y, Z, levels=sigma_values_, **contourf_styles)
                handles['contourf'] = contourf

                # handle for individual contourf level
                sigma_contourf_styles = isolate_contour_styles(contourf_styles)
                for styles_, label_, color_ in zip(sigma_contourf_styles, contour_labels, sigma_colors):
                    kwargs = combine_dict(styles_)
                    kwargs['label'] = label_
                    if 'color' not in kwargs:
                        kwargs['color'] = color_
                    kwargs['facecolor'] = kwargs.pop('color')
                    handle = Rectangle((0, 0), 1, 1, **kwargs)
                    key = f'contourf_{label_}'
                    sigma_handles[key] = handle
                    if key not in self.legend_order:
                        self.legend_order.append(key)

        if draw_colorbar:
            if 'pcm' in handles:
                mappable = pcm
            elif 'contourf' in handles:
                mappable = contourf
            elif 'contour' in handles:
                mappable = contour
            else:
                mappable = None
            if mappable is not None:
                cbar = plt.colorbar(mappable, ax=ax, **styles['colorbar'])
                cbar.set_label(zlabel, **styles['colorbar_label'])
                format_axis_ticks(cbar.ax, **styles['colorbar_axis'])
                handles['cbar'] = cbar
        
        if shade_nan_points and (len(nan_shapes) > 0):
            self.draw_shades(ax, nan_shapes)
            
        self.update_legend_handles(handles, raw=True, domain=domain)
        self.update_legend_handles(sigma_handles, domain=domain)
    
    def is_single_data(self):
        return not isinstance(self.data_map, dict)

    def add_highlight(self, x: float, y: float, label: str = "SM prediction",
                      styles: Optional[Dict] = None):
        highlight_data = {
            'x': x,
            'y': y,
            'label': label,
            'styles': styles
        }
        self.highlight_data.append(highlight_data)

    def resolve_targets(self, targets: Optional[List[str]] = None) -> List[Optional[str]]:
        if targets is None:
            targets = [None] if self.is_single_data() else list(self.data_map)
        return targets

    def resolve_target_styles(self, targets: List[Optional[str]]):
        target_styles = {}
        for target in targets:
            styles = self.styles_map.get(target, {})
            target_styles[target] = combine_dict(self.styles, styles)
        return target_styles

    def draw_highlight(self, ax, x, y, label:str,
                       styles:Optional[Dict]=None,
                       domain:Optional[str]=None):
        if styles is None:
            styles = self.styles['highlight']
        handle = ax.plot(x, y, label=label, **styles)
        key = f'highlight_{label}'
        self.update_legend_handles({key: handle[0]}, domain=domain)
        if key not in self.legend_order:
            self.legend_order.append(key)

    def draw(self, xattrib:str, yattrib:str, zattrib:str='qmu',
             targets:Optional[List[str]]=None,
             xlabel: Optional[str] = "", ylabel: Optional[str] = "",
             zlabel: Optional[str] = "$-2\Delta ln(L)$",
             title: Optional[str] = None,
             ymax:Optional[float]=None, ymin:Optional[float]=None,
             xmin:Optional[float]=None, xmax:Optional[float]=None,
             draw_contour: bool = True,
             draw_contourf: bool = False,
             draw_colormesh: bool = False, 
             draw_clabel: bool = False,
             draw_colorbar: bool = False,
             draw_bestfit:Union[List[str], bool]=True,
             draw_sm_line: bool = False,
             draw_legend: bool = True,
             legend_order: Optional[List[str]] = None,
             interval_format:str="one_two_sigma",
             remove_nan_points_within_distance:Optional[float]=None,
             shade_nan_points:bool=False):
        
        targets = self.resolve_targets(targets)
        target_styles = self.resolve_target_styles(targets=targets)
        
        self.reset_legend_data()
        if legend_order is not None:
            self.legend_order = legend_order
        ax = self.draw_frame()
        
        for target, styles in target_styles.items():
            if (target is None):
                data = self.data_map
            elif target in self.data_map:
                data = self.data_map[target]
            else:
                raise RuntimeError(f'No input data found for the target "{target}".')
                
            self.draw_single_data(ax, data, xattrib=xattrib, yattrib=yattrib,
                                  zattrib=zattrib, styles=styles,
                                  draw_colormesh=draw_colormesh,
                                  draw_contour=draw_contour,
                                  draw_contourf=draw_contourf,
                                  draw_clabel=draw_clabel,
                                  draw_colorbar=draw_colorbar,
                                  interval_format=interval_format,
                                  remove_nan_points_within_distance=remove_nan_points_within_distance,
                                  shade_nan_points=shade_nan_points,
                                  domain=target)
            
            if ((draw_bestfit is True) or
                (isinstance(draw_bestfit, (list, tuple)) and target in draw_bestfit)):
                valid_data = data.query(f'{zattrib} >= 0')
                bestfit_idx = np.argmin(valid_data[zattrib].values)
                bestfit_x   = valid_data.iloc[bestfit_idx][xattrib]
                bestfit_y   = valid_data.iloc[bestfit_idx][yattrib]
                bestfit_label_fmt = self.get_label('bestfit', domain=target)
                if not bestfit_label_fmt:
                    bestfit_label_fmt = self.get_label('bestfit')
                bestfit_label = bestfit_label_fmt.format(x=bestfit_x, y=bestfit_y)
                bestfit_label = remove_neg_zero(bestfit_label)
                self.draw_highlight(ax, bestfit_x, bestfit_y,
                                    label=bestfit_label,
                                    styles=styles['bestfit'],
                                    domain=target)
        
        if self.highlight_data:
            for options in self.highlight_data:
                self.draw_highlight(ax, **options)

        if draw_sm_line and self.config['sm_values'] is not None:
            sm_x, sm_y = self.config['sm_values']
            transform = create_transform(transform_x="data", transform_y="axis")
            ax.vlines(sm_x, ymin=0, ymax=1, zorder=0, transform=transform,
                      **self.config['sm_line_styles'])
            transform = create_transform(transform_x="axis", transform_y="data")
            ax.hlines(sm_y, xmin=0, xmax=1, zorder=0, transform=transform,
                      **self.config['sm_line_styles'])

        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel, title=title)
        self.set_axis_range(ax, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

        if draw_legend:
            legend_domains = self.get_legend_domains()
            self.draw_legend(ax, domains=legend_domains)

        return ax
