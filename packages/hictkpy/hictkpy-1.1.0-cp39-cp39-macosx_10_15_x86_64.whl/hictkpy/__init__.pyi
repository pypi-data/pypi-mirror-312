from collections.abc import Sequence
import os
import pathlib
from typing import Annotated, Optional, overload

import numpy
from numpy.typing import ArrayLike
import pandas
import pyarrow
import scipy.sparse

from . import cooler as cooler, hic as hic
import hictkpy


class Bin:
    """Genomic Bin."""

    @property
    def id(self) -> int: ...

    @property
    def rel_id(self) -> int: ...

    @property
    def chrom(self) -> str: ...

    @property
    def start(self) -> int: ...

    @property
    def end(self) -> int: ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

class BinTable:
    """Class representing a table of genomic bins."""

    @overload
    def __init__(self, chroms: dict[str, int], resolution: int) -> None:
        """
        Construct a table of bins given a dictionary mapping chromosomes to their sizes and a resolution.
        """

    @overload
    def __init__(self, bins: pandas.DataFrame) -> None:
        """
        Construct a table of bins from a pandas.DataFrame with columns ["chrom", "start", "end"].
        """

    def __repr__(self) -> str: ...

    def chromosomes(self, include_ALL: bool = False) -> dict[str, int]:
        """Get chromosomes sizes as a dictionary mapping names to sizes."""

    def resolution(self) -> int:
        """
        Get the bin size for the bin table. Return 0 in case the bin table has a variable bin size.
        """

    def type(self) -> str:
        """
        Get the type of table underlying the BinTable object (i.e. fixed or variable).
        """

    def __len__(self) -> int:
        """Get the number of bins in the bin table."""

    def __iter__(self) -> hictkpy.BinTableIterator:
        """Return an iterator over the bins in the table."""

    @overload
    def get(self, bin_id: int) -> hictkpy.Bin:
        """Get the genomic coordinate given a bin ID."""

    @overload
    def get(self, bin_ids: Sequence[int]) -> pandas.DataFrame:
        """
        Get the genomic coordinates given a sequence of bin IDs. Genomic coordinates are returned as a pandas.DataFrame with columns ["chrom", "start", "end"].
        """

    @overload
    def get(self, chrom: str, pos: int) -> hictkpy.Bin:
        """Get the bin overlapping the given genomic coordinate."""

    @overload
    def get(self, chroms: Sequence[str], pos: Sequence[int]) -> pandas.DataFrame:
        """
        Get the bins overlapping the given genomic coordinates. Bins are returned as a pandas.DataFrame with columns ["chrom", "start", "end"].
        """

    def get_id(self, chrom: str, pos: int) -> int:
        """Get the ID of the bin overlapping the given genomic coordinate."""

    def get_ids(self, chroms: Sequence[str], pos: Sequence[int]) -> Annotated[ArrayLike, dict(dtype='int64')]:
        """Get the IDs of the bins overlapping the given genomic coordinates."""

    def merge(self, df: pandas.DataFrame) -> pandas.DataFrame:
        """
        Merge genomic coordinates corresponding to the given bin identifiers. Bin identifiers should be provided as a pandas.DataFrame with columns "bin1_id" and "bin2_id". Genomic coordinates are returned as a pandas.DataFrame containing the same data as the DataFrame given as input, plus columns ["chrom1", "start1", "end1", "chrom2", "start2", "end2"].
        """

    def to_df(self, range: str | None = None, query_type: str = 'UCSC') -> pandas.DataFrame:
        """
        Return the bins in the BinTable as a pandas.DataFrame. The optional "range" parameter can be used to only fetch a subset of the bins in the BinTable.
        """

class File:
    """Class representing a file handle to a .cool or .hic file."""

    def __init__(self, path: str | os.PathLike, resolution: Optional[int] = None, matrix_type: str = 'observed', matrix_unit: str = 'BP') -> None:
        """
        Construct a file object to a .hic, .cool or .mcool file given the file path and resolution.
        Resolution is ignored when opening single-resolution Cooler files.
        """

    def __repr__(self) -> str: ...

    def uri(self) -> str:
        """Return the file URI."""

    def path(self) -> pathlib.Path:
        """Return the file path."""

    def is_hic(self) -> bool:
        """Test whether file is in .hic format."""

    def is_cooler(self) -> bool:
        """Test whether file is in .cool format."""

    def chromosomes(self, include_ALL: bool = False) -> dict[str, int]:
        """Get chromosomes sizes as a dictionary mapping names to sizes."""

    def bins(self) -> hictkpy.BinTable:
        """Get table of bins."""

    def resolution(self) -> int:
        """Get the bin size in bp."""

    def nbins(self) -> int:
        """Get the total number of bins."""

    def nchroms(self, include_ALL: bool = False) -> int:
        """Get the total number of chromosomes."""

    def attributes(self) -> dict:
        """Get file attributes as a dictionary."""

    def fetch(self, range1: Optional[str] = None, range2: Optional[str] = None, normalization: Optional[str] = None, count_type: str = 'int', join: bool = False, query_type: str = 'UCSC') -> PixelSelector:
        """Fetch interactions overlapping a region of interest."""

    def avail_normalizations(self) -> list[str]:
        """Get the list of available normalizations."""

    def has_normalization(self, normalization: str) -> bool:
        """Check whether a given normalization is available."""

    @overload
    def weights(self, name: str, divisive: bool = True) -> Annotated[ArrayLike, dict(float)]:
        """Fetch the balancing weights for the given normalization method."""

    @overload
    def weights(self, names: Sequence[str], divisive: bool = True) -> pandas.DataFrame:
        """
        Fetch the balancing weights for the given normalization methods.Weights are returned as a pandas.DataFrame.
        """

class MultiResFile:
    """Class representing a file handle to a .hic or .mcool file"""

    def __init__(self, path: str | os.PathLike) -> None:
        """Open a multi-resolution Cooler file (.mcool) or .hic file."""

    def __repr__(self) -> str: ...

    def path(self) -> pathlib.Path:
        """Get the file path."""

    def is_mcool(self) -> bool:
        """Test whether the file is in .mcool format."""

    def is_hic(self) -> bool:
        """Test whether the file is in .hic format."""

    def chromosomes(self, include_ALL: bool = False) -> dict[str, int]:
        """Get chromosomes sizes as a dictionary mapping names to sizes."""

    def resolutions(self) -> Annotated[ArrayLike, dict(dtype='uint32', shape=(None), order='C')]:
        """Get the list of available resolutions."""

    def attributes(self) -> dict:
        """Get file attributes as a dictionary."""

    def __getitem__(self, arg: int, /) -> File:
        """
        Open the Cooler or .hic file corresponding to the resolution given as input.
        """

class PixelFP:
    """Pixel in BG2 format."""

    @property
    def bin1_id(self) -> int: ...

    @property
    def bin2_id(self) -> int: ...

    @property
    def rel_bin1_id(self) -> int: ...

    @property
    def rel_bin2_id(self) -> int: ...

    @property
    def chrom1(self) -> str: ...

    @property
    def start1(self) -> int: ...

    @property
    def end1(self) -> int: ...

    @property
    def chrom2(self) -> str: ...

    @property
    def start2(self) -> int: ...

    @property
    def end2(self) -> int: ...

    @property
    def count(self) -> float: ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

class PixelInt:
    """Pixel in BG2 format."""

    @property
    def bin1_id(self) -> int: ...

    @property
    def bin2_id(self) -> int: ...

    @property
    def rel_bin1_id(self) -> int: ...

    @property
    def rel_bin2_id(self) -> int: ...

    @property
    def chrom1(self) -> str: ...

    @property
    def start1(self) -> int: ...

    @property
    def end1(self) -> int: ...

    @property
    def chrom2(self) -> str: ...

    @property
    def start2(self) -> int: ...

    @property
    def end2(self) -> int: ...

    @property
    def count(self) -> int: ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

class PixelSelector:
    """
    Class representing pixels overlapping with the given genomic intervals.
    """

    @overload
    def __init__(self, selector: "std::__1::shared_ptr<hictk::cooler::PixelSelector const>", type: str, join: bool) -> None: ...

    @overload
    def __init__(self, selector: "std::__1::shared_ptr<hictk::hic::PixelSelector const>", type: str, join: bool) -> None: ...

    @overload
    def __init__(self, selector: "std::__1::shared_ptr<hictk::hic::PixelSelectorAll const>", type: str, join: bool) -> None: ...

    def __repr__(self) -> str: ...

    def coord1(self) -> tuple[str, int, int]:
        """Get query coordinates for the first dimension."""

    def coord2(self) -> tuple[str, int, int]:
        """Get query coordinates for the second dimension."""

    def __iter__(self) -> hictkpy.PixelIterator:
        """Return an iterator over the selected pixels."""

    def to_arrow(self, query_span: str = "upper_triangle") -> pyarrow.Table:
        """Retrieve interactions as a pyarrow.Table."""

    def to_pandas(self, query_span: str = "upper_triangle") -> pandas.DataFrame:
        """Retrieve interactions as a pandas DataFrame."""

    def to_df(self, query_span: str = "upper_triangle") -> pandas.DataFrame:
        """Alias to to_pandas()."""

    def to_numpy(self, query_span: str = "full") -> numpy.ndarray:
        """Retrieve interactions as a numpy 2D matrix."""

    def to_coo(self, query_span: str = "upper_triangle") -> scipy.sparse.coo_matrix:
        """Retrieve interactions as a SciPy COO matrix."""

    def to_csr(self, query_span: str = "upper_triangle") -> scipy.sparse.csr_matrix:
        """Retrieve interactions as a SciPy CSR matrix."""

    def describe(self, metrics: Sequence[str] = ..., keep_nans: bool = False, keep_infs: bool = False, exact: bool = False) -> dict:
        """
        Compute one or more descriptive metrics in the most efficient way possible. Known metrics: nnz, sum, min, max, mean, variance, skewness, kurtosis.
        """

    def nnz(self, keep_nans: bool = False, keep_infs: bool = False) -> int:
        """Get the number of non-zero entries for the current pixel selection."""

    def sum(self, keep_nans: bool = False, keep_infs: bool = False) -> int | float:
        """Get the total number of interactions for the current pixel selection."""

    def min(self, keep_nans: bool = False, keep_infs: bool = False) -> int | float | None:
        """
        Get the minimum number of interactions for the current pixel selection (excluding pixels with no interactions). Return None in case the pixel selector overlaps with an empty region.
        """

    def max(self, keep_nans: bool = False, keep_infs: bool = False) -> int | float | None:
        """
        Get the maximum number of interactions for the current pixel selection. Return None in case the pixel selector overlaps with an empty region.
        """

    def mean(self, keep_nans: bool = False, keep_infs: bool = False) -> float | None:
        """
        Get the average number of interactions for the current pixel selection (excluding pixels with no interactions. Return None in case the pixel selector overlaps with an empty region.
        """

    def variance(self, keep_nans: bool = False, keep_infs: bool = False, exact: bool = False) -> float | None:
        """
        Get the variance of the number of interactions for the current pixel selection (excluding pixels with no interactions). Return None in case the pixel selector overlaps with an empty region.
        """

    def skewness(self, keep_nans: bool = False, keep_infs: bool = False, exact: bool = False) -> float | None:
        """
        Get the skewness of the number of interactions for the current pixel selection (excluding pixels with no interactions). Return None in case the pixel selector overlaps with an empty region.
        """

    def kurtosis(self, keep_nans: bool = False, keep_infs: bool = False, exact: bool = False) -> float | None:
        """
        Get the kurtosis of the number of interactions for the current pixel selection (excluding pixels with no interactions). Return None in case the pixel selector overlaps with an empty region.
        """

class ThinPixelFP:
    """Pixel in COO format."""

    @property
    def bin1_id(self) -> int: ...

    @property
    def bin2_id(self) -> int: ...

    @property
    def count(self) -> float: ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

class ThinPixelInt:
    """Pixel in COO format."""

    @property
    def bin1_id(self) -> int: ...

    @property
    def bin2_id(self) -> int: ...

    @property
    def count(self) -> int: ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

__hictk_version__: str = '2.0.1'

def is_cooler(path: str | os.PathLike) -> bool:
    """Test whether path points to a cooler file."""

def is_hic(path: str | os.PathLike) -> bool:
    """Test whether path points to a .hic file."""

def is_mcool_file(path: str | os.PathLike) -> bool:
    """Test whether path points to a .mcool file."""

def is_scool_file(path: str | os.PathLike) -> bool:
    """Test whether path points to a .scool file."""

