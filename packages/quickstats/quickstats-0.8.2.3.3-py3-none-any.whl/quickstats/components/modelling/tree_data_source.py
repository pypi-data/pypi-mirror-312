from typing import Optional, Union, List, Dict

import numpy as np

from quickstats import cached_import
from quickstats.concepts import Binning
from .data_source import DataSource

class TreeDataSource(DataSource):
    """
    TTree representation of a one-dimensional data input
    """

    def __init__(self, tree: Union["ROOT.TTree", "ROOT.TChain"],
                 observable_name: str,
                 weight_name: Optional[str]=None,
                 binning: Optional[Binning]=None,
                 verbosity:Optional[Union[int, str]]="INFO"):
        """
        Parameters
        -----------
        tree : ROOT.TTree or ROOT.TChain
            Input TTree.
        observable_name : str
            Name of the observable for creating datasets. It must be
            a branch found in the tree.
        weight_name : str, optional
            Name of the weight for creating datasets. If specified,
            it must be a branch found in the tree.
        binning : Binning, optional
            Default binning specification for creating histograms.
        verbosity : Union[int, str], optional
            The verbosity level. Default is "INFO".
        """
        self.set_data(tree)
        super().__init__(binning=binning,
                         observable_name=observable_name,
                         weight_name=weight_name,
                         verbosity=verbosity)

    @classmethod
    def from_files(cls, filenames:Union[str, List[str], Dict[str, str]],
                   observable_name: str,
                   default_treename: str=None,
                   weight_name: Optional[str]=None,
                   binning: Optional[Binning]=None,
                   verbosity:Optional[Union[int, str]]="INFO"):
        from quickstats.interface.root import TChain
        specs = TChain._get_specs(filenames, default_treename=default_treename)
        tree = TChain._from_specs(specs)
        return cls(tree, observable_name=observable_name, weight_name=weight_name,
                   binning=binning, verbosity=verbosity)

    def set_data(self, tree:Union["ROOT.TTree", "ROOT.TChain"]) -> None:
        ROOT = cached_import("ROOT")
        from quickstats.interface.root import TChain, TTree
        if isinstance(tree, ROOT.TChain):
            self.data = TChain(tree)
        elif isinstance(tree, ROOT.TTree):
            self.data = TTree(tree)
        else:
            raise TypeError('`tree` must be an instance of ROOT.TTree.')

    def set_binning(self, binning: Optional[Binning]=None) -> None:
        if binning is None:
            bins = 10
            bin_range = (0, 0)
            self.stdout.info(f'Default binning set to uniform from inferred range with {bins} bins.')
            binning = Binning(bins=bins, bin_range=bin_range)
        super().set_binning(binning)

    def set_names(self, observable_name: str,
                  weight_name: Optional[str]=None) -> None:
        columns = self.data.get_column_names()
        if observable_name not in columns:
            raise ValueError(f'Input tree does not contain a branch named "{observable_name}".')
        if (weight_name is not None) and (weight_name not in columns):
            raise ValueError(f'Input tree does not contain a branch named "{weight_name}".')
        super().set_names(observable_name, weight_name)

    def as_dataset(self, name:Optional[str]=None,
                   title:Optional[str]=None) -> "ROOT.RooDataSet":
        name = name or self.get_default_dataset_name()
        title = title or name
        observable = self.get_observable()
        dataset = self.data.get_dataset(observable=observable,
                                        weight_name=self.weight_name,
                                        name=name, title=title)
        return dataset

    def as_histogram(self, name:Optional[str]=None,
                     title:Optional[str]=None,
                     binning: Optional[Binning]=None) -> "ROOT.TH1":
        from quickstats.utils.root_utils import delete_object
        binning = binning or self.default_binning
        name = name or self.get_default_histogram_name()
        title = title or name
        delete_object(name)
        histogram = self.data.get_histo1d(observable=self.observable_name,
                                          weight=self.weight_name,
                                          bins=binning.nbins,
                                          bin_range=binning.bin_range,
                                          name=name,
                                          title=title)
        return histogram

    def as_arrays(self) -> Dict[str, np.ndarray]:
        ROOT = cached_import("ROOT")
        rdf = ROOT.RDataFrame(self.data.obj)
        columns = [self.observable_name]
        if self.weight_name is not None:
            columns.append(self.weight_name)
        arrays = rdf.AsNumpy(columns)
        return arrays