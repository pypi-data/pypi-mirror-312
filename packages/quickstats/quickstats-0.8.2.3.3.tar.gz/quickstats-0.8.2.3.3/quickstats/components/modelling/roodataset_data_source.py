from typing import Optional, Union, List, Dict

import numpy as np

from quickstats import cached_import
from quickstats.concepts import Binning
from .data_source import DataSource

class RooDataSetDataSource(DataSource):
    """
    RooDataSet representation of a one-dimensional data input
    """

    def __init__(self, dataset: "ROOT.RooDataSet",
                 binning: Optional[Binning]=None,
                 verbosity: Optional[Union[int, str]]="INFO"):
        """
        Parameters
        -----------
        dataset : ROOT.RooDataSet
            Input dataset.
        binning : Binning, optional
            Default binning specification for creating histograms.
        verbosity : Union[int, str], optional
            The verbosity level. Default is "INFO".
        """
        super().__init__(binning=binning, verbosity=verbosity)
        self.set_data(dataset)

    def get_observable(self) -> "ROOT.RooRealVar":
        return self.data.get().first()

    def set_data(self, dataset: "ROOT.RooDatSet") -> None:
        ROOT = cached_import("ROOT")
        if not isinstance(dataset, ROOT.RooDataSet):
            raise TypeErrror(f'`dataset` must be an instance of ROOT.RooDataSet.')
        observable = dataset.get().first()
        if self.default_binning is None:
            from quickstats.concepts import Binning
            nbins = observable.numBins()
            bin_range = (observable.getMin(), observable.getMax())
            binning = Binning(bins=nbins, bin_range=bin_range)
            self.set_binning(binning)
        observable_name = observable.GetName()
        if dataset.weightVar():
            weight_name = dataset.weightVar().GetName()
        else:
            weight_name = None
        self.set_names(observable_name, weight_name)
        if self.default_binning is not None:
            bin_low, bin_high = self.default_binning.bin_range
            nbins = self.default_binning.nbins
            observable.setBins(nbins)
        self.data = dataset

    def as_dataset(self, name:Optional[str]=None,
                   title:Optional[str]=None) -> "ROOT.RooDataSet":
        return self.data

    def as_histogram(self, name:Optional[str]=None,
                     title:Optional[str]=None,
                     binning: Optional[Binning]=None) -> "ROOT.TH1":
        ROOT = cached_import("ROOT")
        binning = binning or self.default_binning
        name = name or self.get_default_histogram_name()
        title = title or name
        nbins = binning.nbins
        bin_low, bin_high = binning.bin_range
        rbinning = ROOT.RooFit.Binning(binning.nbins,
                                       bin_low,
                                       bin_high)
        histogram = self.data.createHistogram(self.observable_name,
                                              rbinning)
        return histogram

    def as_arrays(self) -> np.ndarray:
        return self.data.to_numpy()