from typing import List, Optional, Union, Dict, Callable, Tuple
from itertools import repeat
import os
import copy
import json
import uuid

import numpy as np

from quickstats import semistaticmethod, timer, cached_import
from quickstats.core import mappings as mp
from quickstats.concepts import Binning
from quickstats.components import ROOTObject
from quickstats.components.modelling import PdfFitTool
from quickstats.interface.root import RooDataSet, RooRealVar
from quickstats.utils.py_utils import get_argnames
from quickstats.utils.common_utils import combine_dict, execute_multi_tasks, in_notebook
from quickstats.utils.roofit_utils import dataset_to_histogram, pdf_to_histogram
from .data_source import DataSource
from .parameter_templates import get_param_templates

class DataModelling(ROOTObject):
    
    _DEFAULT_FIT_OPTION_ = {
        'print_level': -1,
        'min_fit': 2,
        'max_fit': 3,
        'binned': False,
        'minos': False,
        'hesse': True,
        'sumw2': True,
        'asymptotic': False,
        'strategy': 1,
        'range_expand_rate': 1        
    }
    
    _DEFAULT_PLOT_OPTION_ = {
        'bin_range': None,
        'nbins_data': None,
        'nbins_pdf': 1000,
        'show_comparison': True,
        'show_params': True,
        'show_stats': True,
        'show_fit_error': True,
        'show_bin_error': True,
        'value_fmt': "{:.2f}",
        'stats_list': ["chi2/ndf"],
        'init_options': {
            'label_map': {
                'data' : "MC",
                'pdf'  : "Fit"
            }
        },
        'draw_options': {
            'comparison_options':{
                "mode": "difference",
                "ylabel": "MC - Fit",
            }
        },
        'summary_text_option': {
            'x': 0.05,
            'y': 0.9
        },
        'extra_text_option': None,
    }

    # pdf class defined in macros
    _EXTERNAL_PDF_ = ['RooTwoSidedCBShape']

    # name aliases for various pdfs
    _PDF_MAP_ = {
        'RooCrystalBall_DSCB' : 'RooCrystalBall',
        'DSCB'                : 'RooTwoSidedCBShape',
        'ExpGaussExp'         : 'RooExpGaussExpShape',
        'Exp'                 : 'RooExponential',
        'Exponential'         : 'RooExponential',
        'Bukin'               : 'RooBukinPdf',
        'Gaussian'            : 'RooGaussian',
        'Gaus'                : 'RooGaussian'
    }
    
    _DEFAULT_ROOT_CONFIG_ = {
        "SetBatch" : True,
        "TH1Sumw2" : True
    }
    
    _REQUIRE_CONFIG_ = {
        "ROOT"  : True,
        "RooFit": True
    }
    
    @property
    def plot_options(self):
        return self._plot_options
    
    @property
    def fit_options(self):
        return self._fit_options
    
    @property
    def model_class(self):
        return self._model_class
    
    @property
    def param_templates(self):
        return self._param_templates

    def __init__(self, functional_form:Union[str, Callable],
                 fit_range:Union[List[float], Tuple[float]],
                 param_templates:Optional[Callable]=None,
                 nbins:Optional[int]=None,
                 fit_options:Optional[Dict]=None,
                 plot_options:Optional[Dict]=None,
                 observable_name:str="observable",
                 weight_name:Optional[str]=None,
                 verbosity:str="INFO"):
        """
        Modelling of a data distribution by a simple analytic function.
        
        Parameters:
            observable: str
                Name of observable.
        """
        self._fit_options  = mp.concat((self._DEFAULT_FIT_OPTION_, fit_options), copy=True)
        self._fit_options['fit_range'] = fit_range
        self._fit_options['nbins'] = nbins
        self._plot_options = mp.concat((self._DEFAULT_PLOT_OPTION_, plot_options), copy=True)
        self.set_param_templates(param_templates)
        self.set_functional_form(functional_form)
        self.set_names(observable_name, weight_name)
        roofit_config = {
            "MinimizerPrintLevel": self.fit_options.get("print_level", -1)
        }
        super().__init__(roofit_config=roofit_config,
                         verbosity=verbosity)
        self.result = None

    def set_names(self, observable_name: str = 'observable',
                  weight_name: str = 'weight') -> None:
        self.observable_name = observable_name
        self.weight_name = weight_name        
        
    def set_param_templates(self, param_templates:Callable):
        self._param_templates = param_templates
        
    def set_functional_form(self, functional_form:Union[str, Callable]):
        model_class = self.get_model_class(functional_form)
        if self.param_templates is None:
            if isinstance(functional_form, str):
                param_templates = get_param_templates(functional_form)
                self.set_param_templates(param_templates)
            else:
                raise RuntimeError("Missing parameter templates definition.")
        self._model_class = model_class
        if not isinstance(functional_form, str):
            functional_form = type(functional_form).__name__
        self.functional_form = functional_form
        
    @semistaticmethod
    def get_model_class(self, source:Union[str, Callable]):
        """
        Resolves the pdf class that describes the data model.

        Parameters
        ----------
            source : string or callable
                Name of the pdf or a callable representing the pdf class.
        """
        if isinstance(source, Callable):
            return source
        ROOT = cached_import("ROOT")
        pdf_name = self._PDF_MAP_.get(source, source)
        if hasattr(ROOT, pdf_name):
            return getattr(ROOT, pdf_name)

        if pdf_name in self._EXTERNAL_PDF_:
            # load definition of external pdfs
            self.load_extension(pdf_name)
            return self.get_model_class(pdf_name)
        
        raise ValueError(f'Failed to load model pdf: "{source}"')

    def sanity_check(self):
        if self.model_class is None:
            raise RuntimeError("Model pdf not set.")
        if self.param_templates is None:
            raise RuntimeError("Model parameter templates not set.")
    
    @staticmethod
    def get_param_data(parameters:Dict[str, "ROOT.RooRealVar"], value_only:bool=False):
        param_data = {}
        for name, parameter in parameters.items():
            if value_only:
                param_data[name] = parameter.getVal()
            else:
                param_data[name] = {
                    'value'  : parameter.getVal(),
                    'errorhi': parameter.getErrorHi(),
                    'errorlo': parameter.getErrorLo(),
                    'error'  : parameter.getError()
                }
        return param_data

    def get_default_binning(self):
        nbins = self.fit_options['nbins']
        bin_range = self.fit_options['fit_range']
        binning = Binning(bins=nbins, bin_range=bin_range)
        return binning

    def create_data_source(self, data: Union[np.ndarray, "ROOT.RooDataSet", "ROOT.TTree", "DataSource"],
                           weights: Optional[np.ndarray]=None):
        ROOT = cached_import("ROOT")
        binning = self.get_default_binning()
        if isinstance(data, DataSource):
            if data.default_binning is None:
                data.set_binning(binning)
            elif not np.allclose(data.default_binning.bin_edges, binning.bin_edges):
                self.stdout.info('Modified the default binning of data source to reflect the specified fit range.')
                data.set_binning(binning)
            return data
        kwargs = {
            'binning': self.get_default_binning(),
            'verbosity': self.stdout.verbosity
        }
        if isinstance(data, np.ndarray):
            from quickstats.components.modelling import ArrayDataSource
            data_source = ArrayDataSource(data, weights=weights,
                                          observable_name=self.observable_name,
                                          weight_name=self.weight_name,
                                          **kwargs)
        elif isinstance(data, ROOT.RooDataSet):
            from quickstats.components.modelling import RooDataSetDataSource
            data_source = RooDataSetDataSource(data, **kwargs)
        elif isinstance(data, ROOT.TTree):
            from quickstats.components.modelling import TreeDataSource
            data_source = TreeDataSource(data,
                                         observable_name=self.observable_name,
                                         weight_name=self.weight_name,
                                         **kwargs)
        else:
            raise ValueError(f'Unsupported data type: "{type(data).__name__}"')
        return data_source

    def set_param_data(self, *parameters, param_data:Dict) -> None:
        for parameter in parameters:
            param_name = parameter.GetName()
            if param_name in param_data:
                parameter.setVal(param_data[param_name]['value'])
                parameter.setError(param_data[param_name]['error'])
                parameter.setAsymError (param_data[param_name]['errorlo'],
                                        param_data[param_name]['errorhi'])

    def create_model_pdf(self, *parameters, param_data:Optional[Dict]=None):
        model_name = f"model_{self.model_class.Class_Name()}"
        if param_data is not None:
            self.set_param_data(*parameters, param_data=param_data)
        model_pdf = self.model_class(model_name, model_name, *parameters)
        return model_pdf
        
    def fit(self, data: Union[np.ndarray, "ROOT.RooDataSet", "ROOT.TTree", DataSource],
            weights: Optional[np.ndarray]=None):
        with timer() as t:
            data_source = self.create_data_source(data, weights=weights)
            dataset = data_source.as_dataset()
            observable = data_source.get_observable()
            model_parameters = self.param_templates(data_source)
            prefit_param_data = self.get_param_data(model_parameters)
            model_pdf = self.create_model_pdf(observable, *model_parameters.values())
            if dataset.numEntries() == 0:
                raise RuntimeError('No events found in the dataset. Please make sure you have specified the '
                                   'correct fit range and that the input data is not empty.')
            fit_tool   = PdfFitTool(model_pdf, dataset, verbosity=self.stdout.verbosity)
            fit_options = combine_dict(self.fit_options)
            fit_kwargs = {}
            for key in get_argnames(fit_tool.mle_fit):
                if key in fit_options:
                    fit_kwargs[key] = fit_options[key]
            result = fit_tool.mle_fit(**fit_kwargs)
            fit_stats = result['fit_stats']
        fit_time = t.interval
        self.stdout.info(f"Task finished. Total time taken: {fit_time:.3f}s")
        postfit_param_data = self.get_param_data(model_parameters)
        configuration = {
            'functional_form': self.functional_form,
            'observable_name': self.observable_name,
            'weight_name': self.weight_name,
            'fit_options': fit_options
        }
        result = {
            'model_parameters': {
                'prefit': prefit_param_data,
                'postfit': postfit_param_data
            },
            'stats': fit_stats,
            'configuration': configuration,
            'fit_time': fit_time
        }
        self.result = result
        return result

    def get_postfit_parameters(self, detailed:bool=False):
        if not self.result:
            raise RuntimeError('No fit results found. Did you perform a fit?')
        # make a copy
        result = combine_dict(self.result['model_parameters']['postfit'])
        if not detailed:
            for name, data in result.items():
                result[name] = data['value']
            return result
        return result

    def get_summary_text(self, value_fmt:str="{:.2f}",
                         show_params:bool=True,
                         show_stats:bool=True,
                         show_fit_error:bool=True,
                         stats_list:Optional[List[str]]=None):
        if not self.result:
            raise RuntimeError('No fit results found. Did you perform a fit?')        
        summary_text = ""
        if show_params:
            param_data = self.get_postfit_parameters(detailed=True)
            for name, data in param_data.items():
                value = value_fmt.format(data["value"])
                if show_fit_error:
                    error = value_fmt.format(data["error"])
                    summary_text += f"{name} = {value} $\\pm$ {error}\n"
                else:
                    summary_text += f"{name} = {value}\n"
            summary_text += "\n"
        if show_stats:
            stats_result = self.result['stats']
            if stats_list is None:
                stats_list = list(model_summary["stats"])
            for key in stats_list:
                if key not in stats_result:
                    raise RuntimeError(f"Invalid stats item: {key}")
                value = value_fmt.format(stats_result[key])
                summary_text += f"{key} = {value}\n"
            summary_text += "\n"
        return summary_text

    def create_plot(
        self,
        data: Union[np.ndarray, "ROOT.RooDataSet", "ROOT.TTree", DataSource],
        weights: Optional[np.ndarray] = None,
        saveas: Optional[str] = None,
    ):
        if not self.result:
            raise RuntimeError("No results to plot")
        from quickstats.plots import DataModelingPlot
        ROOT = cached_import("ROOT")
        data_source = self.create_data_source(data, weights=weights)
        dataset = data_source.as_dataset()
        observable = data_source.get_observable()
        observables = ROOT.RooArgSet(observable)
        parameters = self.param_templates(data_source)
        param_data = self.get_postfit_parameters(detailed=True)
        pdf = self.create_model_pdf(observable, *parameters.values(),
                                    param_data=param_data)
        plot_options = self.plot_options
        data_hist = dataset_to_histogram(
            dataset,
            nbins=plot_options['nbins_data'],
            bin_range=plot_options['bin_range'],
            evaluate_error=plot_options['show_bin_error'],
        )
        pdf_hist = pdf_to_histogram(
            pdf,
            observables,
            nbins=plot_options['nbins_pdf'],
            bin_range=plot_options['bin_range'],
        )
        pdf_hist_data_binning = pdf_to_histogram(
            pdf,
            observables,
            nbins=plot_options['nbins_data'],
            bin_range=plot_options['bin_range'],
        )
        pdf_hist.reweight(data_hist, inplace=True)
        pdf_hist_data_binning.reweight(data_hist, inplace=True)
        dfs = {
            'data': data_hist,
            'pdf': pdf_hist,
            'pdf_data_binning': pdf_hist_data_binning
            
        }
        plotter = DataModelingPlot(
            data_map=dfs,
            analytic_model=True,
            **plot_options['init_options']
        )

        summary_kwargs = {
            "value_fmt" : plot_options["value_fmt"],
            "show_params" : plot_options['show_params'],
            "show_stats" : plot_options["show_stats"],
            "show_fit_error" : plot_options["show_fit_error"],
            "stats_list" : plot_options["stats_list"]
        }
        summary_text = self.get_summary_text(**summary_kwargs)
        if summary_text:
            options = plot_options.get('summary_text_option', {})
            plotter.add_text(summary_text, **options)
        
        extra_text_option = plot_options.get("extra_text_option", None)
        if extra_text_option is not None:
            if isinstance(extra_text_option, dict):
                plotter.add_text(**extra_text_option)
            elif isinstance(extra_text_option, list):
                for options in extra_text_option:
                    plotter.add_text(**options)
            else:
                raise ValueError('invalid format for the plot option "extra_text_option"')
                
        draw_options = mp.concat((plot_options.get('draw_options'),), copy=True)
        draw_options.setdefault('xlabel', observable.GetName())
        draw_options['primary_target'] = 'data'
        if plot_options['show_comparison']:
            comparison_options = mp.concat((draw_options.get('comparison_options'),), copy=True)
            comparison_options['components'] = [
                {
                    "reference": "pdf_data_binning",
                    "target": "data",
                }
            ]
        else:
            comparison_options = None
        draw_options['comparison_options'] = comparison_options

        axes = plotter.draw(
            data_targets=['data'],
            model_targets=['pdf'],
            **draw_options
        )
        if saveas is not None:
            plotter.figure.savefig(saveas, bbox_inches="tight")
        if in_notebook():
            import matplotlib.pyplot as plt
            plt.show()
        return axes