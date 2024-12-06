from typing import Optional, Union, Dict

import numpy as np

from quickstats.concepts import Binning
from .data_source import DataSource

class ArrayDataSource(DataSource):
    """
    Array representation of a one-dimensional data input
    """
    
    def __init__(self, data: np.ndarray,
                 weights: Optional[np.ndarray]=None,
                 binning: Optional[Binning]=None,
                 observable_name: str = 'observable',
                 weight_name: str = 'weight',
                 verbosity:Optional[Union[int, str]]="INFO"):
        """
        Parameters
        -----------
        data : np.ndarray
            Input data.
        weights : np.ndarray, optional
            Weights for the input data. Must have the same shape as `data`.
        binning : Binning, optional
            Default binning specification for creating histograms.
        observable_name : str, default = 'observable'
            Name of the observable for creating datasets.
        weight_name : str, default = 'weight'
            Name of the weight for creating datasets.
        verbosity : Union[int, str], optional
            The verbosity level. Default is "INFO".
        """
        self.set_data(data=data, weights=weights)
        super().__init__(binning=binning,
                         observable_name=observable_name,
                         weight_name=weight_name,
                         verbosity=verbosity)

    def set_data(self, data: np.ndarray, weights: Optional[np.ndarray]=None) -> None:
        if not isinstance(data, np.ndarray):
            raise TypeError('`data` must be an instance of np.ndarray.')
        data = np.array(data)
        if weights is None:
            weights = np.ones(data.shape)
        else:
            weights = np.array(weights)
        if data.shape != weights.shape:
            raise ValueError('`weights` must have the same shape as `data`.')
        self.data, self.weights = data, weights

    def set_binning(self, binning: Optional[Binning]=None) -> None:
        if binning is None:
            bins = 10
            bin_range = (np.min(self.data), np.max(self.data))
            self.stdout.info(f'Default binning set to uniform from {bin_range[0]} to {bin_range[1]} with {bins} bins.')
            binning = Binning(bins=bins, bin_range=bin_range)
        super().set_binning(binning)

    def as_dataset(self, name:Optional[str]=None,
                   title:Optional[str]=None) -> "ROOT.RooDataSet":
        import ROOT
        from quickstats.interface.root import RooRealVar, RooDataSet
        arrays = self.as_arrays()
        variables = ROOT.RooArgSet()
        observable = self.get_observable()
        variables.add(observable)
        if self.weight_name:
            weight_var = RooRealVar.create(self.weight_name, value=1).new()
            variables.add(weight_var)
        name = name or self.get_default_dataset_name()
        title = title or name        
        dataset = RooDataSet.from_numpy(arrays, variables,
                                        weight_name=self.weight_name,
                                        name=name, title=title)
        return dataset
        
    def as_histogram(self, name:Optional[str]=None,
                     title:Optional[str]=None,
                     binning: Optional[Binning]=None) -> "ROOT.TH1":
        from quickstats.interface.root import TH1
        from quickstats.utils.root_utils import delete_object
        binning = binning or self.default_binning
        py_hist = TH1.from_numpy_data(self.data,
                                      weights=self.weights,
                                      bins=binning.nbins,
                                      bin_range=binning.bin_range)
        name = name or self.get_default_histogram_name()
        title = title or name
        delete_object(name)
        histogram = py_hist.to_ROOT(name=name, title=title)
        return histogram

    def as_arrays(self) -> Dict[str, np.ndarray]:
        arrays = {
            self.observable_name: self.data,
            self.weight_name: self.weights
        }
        return arrays