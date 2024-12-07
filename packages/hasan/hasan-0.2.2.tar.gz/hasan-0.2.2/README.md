# Hasan: Haplotype Analysis from BAM files

![Hasan Workflow](https://github.com/SemiQuant/Hasan/blob/master/Plan.png?raw=true)

Hasan (Haplotype Algorithm for SNP Amplicon Networks) is a Python package for analyzing haplotypes from BAM files using SNP information. It constructs directed acyclic graphs (DAGs) to identify and visualize potential haplotypes based on sequencing data.

## Features

- Read and process SNP information from TSV files
- Convert VCF files to compatible TSV format
- Build phasing tables from BAM files
- Create directed acyclic graphs (DAGs) for haplotype visualization
- Find and analyze potential haplotypes
- Interactive graph visualization with draggable nodes
- Command-line interface with rich output formatting

## Installation

```bash
pip install hasan
```

## Requirements

- Python ≥ 3.6
- pysam
- pandas
- networkx
- matplotlib
- click
- rich

## Usage

### Command Line Interface

The package provides two main commands:

1. Analyze haplotypes:
```bash
hasan analyze <bam_file> <snps_file> [options]
```

Options:
- `--method/-m`: Method for calculating path weights ('min' or 'multiply')
- `--plot/--no-plot`: Enable/disable interactive plot visualization
- `--output/-o`: Specify output TSV file for haplotype results
- `--verbose/-v`: Print detailed progress information

Example:
```bash
hasan analyze sample.bam variants.tsv --method min --plot --output results.tsv --verbose
```

2. Convert VCF to TSV:
```bash
hasan convert <input_vcf> <output_tsv> [options]
```

Options:
- `--verbose/-v`: Print detailed progress information

Example:
```bash
hasan convert variants.vcf variants.tsv --verbose
```

### Input File Formats

#### SNPs File (TSV format)
```
CHROM   POS     REF     ALT     QUAL    DP
chr1    1000    A       G       40      20
chr1    1500    C       T       35      15
```

Note: When converting from VCF, variants are filtered to:
- Exclude indels (only SNPs are kept)
- Require minimum quality score (QUAL ≥ 30)
- Require minimum depth (DP ≥ 10)

### Python API

```python
from hasan import read_snps, build_phasing_table, create_dag, find_haplotypes

# Read SNP information
snps_df = read_snps("variants.tsv")

# Build phasing table
phasing_data = build_phasing_table("sample.bam", snps_df)

# Create graph
G = create_dag(phasing_data, snps_df)

# Find haplotypes
haplotypes = find_haplotypes(G, method='min')
```

## Output

The package provides multiple output formats:

1. Interactive visualization (when using `--plot`)
2. Static graph image (`haplotype_graph.png`)
3. TSV file with haplotype frequencies (when using `--output`)
4. Rich console output showing:
   - Haplotype sequences
   - Proportions for each haplotype
   - Progress information (in verbose mode)

## How It Works

1. **SNP Reading**: Loads SNP positions and variants from a TSV file.
2. **Phasing Table**: Processes BAM file to count base occurrences at SNP positions.
3. **Graph Construction**: Creates a DAG where:
   - Nodes represent bases at each position
   - Edges represent connections between consecutive positions
   - Edge weights represent proportion of reads supporting the connection
4. **Haplotype Finding**: Identifies possible haplotypes by finding paths through the graph.

## Visualization

The interactive visualization allows you to:
- Drag nodes to rearrange the graph
- View edge weights representing read proportions
- Distinguish between reference (green) and alternate (blue) bases

