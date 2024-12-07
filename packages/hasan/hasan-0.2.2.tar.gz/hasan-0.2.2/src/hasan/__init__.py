"""Hasan: Haplotype Analysis from BAM files."""

# Set matplotlib backend before any other imports
import matplotlib
matplotlib.use('TkAgg')

from .core import (
    read_snps,
    build_phasing_table,
    create_dag,
    find_haplotypes,
    plot_graph_interactive
)

__version__ = "0.2.2" 