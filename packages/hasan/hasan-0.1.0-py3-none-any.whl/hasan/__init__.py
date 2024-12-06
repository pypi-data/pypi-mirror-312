"""Hasan: Haplotype Analysis from BAM files."""

from .core import (
    read_snps,
    build_phasing_table,
    create_dag,
    find_haplotypes,
    plot_graph_interactive
)

__version__ = "0.1.0" 