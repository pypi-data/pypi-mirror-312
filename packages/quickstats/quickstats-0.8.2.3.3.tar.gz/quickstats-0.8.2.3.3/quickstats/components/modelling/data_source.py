from typing import Optional, Union, Dict
from contextlib import contextmanager

import numpy as np

from quickstats import AbstractObject
from quickstats.concepts import Binning

class DataSource(AbstractObject):
    """
    Base class for representation of a one-dimensional data input.
    """
    
    def __init__(self, binning: Optional[Binning]=None,
                 observable_name: str = 'observable',
                 weight_name: str = 'weight',
                 verbosity:Optional[Union[int, str]]="INFO"):
        """
        Parameters
        -----------
        binning : Binning, optional
            Default binning specification for creating histograms.
        observable_name : str
            Name of the observable for creating datasets.
        weight_name : str
            Name of the weight for creating datasets.
        verbosity : Union[int, str], optional
            The verbosity level. Default is "INFO".
        """
        super().__init__(verbosity=verbosity)
        self.set_binning(binning)
        self.set_names(observable_name, weight_name)

    def set_names(self, observable_name: str = 'observable',
                  weight_name: str = 'weight') -> None:
        self.observable_name = observable_name
        self.weight_name = weight_name

    def set_binning(self, binning: Optional[Binning]=None) -> None:
        if (binning is not None):
            if not isinstance(binning, Binning):
                raise TypeError('`binning` must be an instance of quickstats.concepts.Binning.')
            if not binning.is_uniform():
                raise ValueError('Non-uniform binning is not currently supported')
        self.default_binning = binning

    def get_observable(self) -> "ROOT.RooRealVar":
        from quickstats.interface.root import RooRealVar
        bin_range = self.default_binning.bin_range
        nbins = self.default_binning.nbins
        # unspecified binning
        if (bin_range[0] == 0) and (bin_range[1] == 0):
            observable = RooRealVar.create(self.observable_name,
                                           value=0,
                                           nbins=nbins).new()
        else:
            observable = RooRealVar.create(self.observable_name,
                                           range=bin_range,
                                           nbins=nbins).new()
        return observable

    def get_default_histogram_name(self) -> str:
        return f'hist_{self.observable_name}'

    def get_default_dataset_name(self) -> str:
        return f'dataset_{self.observable_name}'

    def as_dataset(self, name:Optional[str]=None,
                   title:Optional[str]=None) -> "ROOT.RooDataSet":
        raise NotImplementedError

    def as_histogram(self, name:Optional[str]=None,
                     title:Optional[str]=None,
                     binning: Optional[Binning]=None) -> "ROOT.TH1":
        raise NotImplementedError

    @contextmanager
    def context_histogram(self, name:Optional[str]=None,
                          title:Optional[str]=None,
                          binning: Optional[Binning]=None) -> "ROOT.TH1":
        histogram = self.as_histogram(name=name, title=title, binning=binning)
        try:
            yield histogram
        finally:
            histogram.Delete()
            
    def as_arrays(self) -> Dict[str, np.ndarray]:
        raise NotImplementedError