import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
import pandas as pd
import matplotlib.pyplot as plt

from .core import (
    read_snps,
    build_phasing_table,
    create_dag,
    find_haplotypes,
    plot_graph_interactive
)
from .vcf_to_tsv import convert_vcf_to_tsv

@click.group()
def cli():
    """Hasan: Haplotype Analysis Tool"""
    pass

# Add this line to maintain compatibility with existing entry points
main = cli

@cli.command()
@click.argument('bam_file', type=click.Path(exists=True))
@click.argument('snps_file', type=click.Path(exists=True))
@click.option('--plot/--no-plot', default=False, help='Show interactive plot')
@click.option('--output', '-o', type=click.Path(), help='Output TSV file for haplotypes')
@click.option('--verbose', '-v', is_flag=True, help='Print detailed progress information')
def analyze(bam_file, snps_file, plot, output, verbose):
    """Analyze haplotypes from BAM and SNPs files."""
    console = Console()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeRemainingColumn(),
        console=console,
        disable=not verbose
    ) as progress:
        # Create the main task
        overall_task = progress.add_task("Processing...", total=4)
        
        progress.update(overall_task, description="Reading SNPs file...")
        if verbose:
            console.print("\nReading SNPs file and skipping header...")
            
        snps_df = read_snps(snps_file)
        
        if verbose:
            console.print(f"Found {len(snps_df)} SNPs in input file (excluding header)")
            console.print("\nFirst few SNPs:")
            console.print(snps_df.head())
        
        if verbose:
            console.print(f"Found {len(snps_df)} SNPs in input file")
        if len(snps_df) == 0:
            console.print("[red]Error: No SNPs found in input file[/red]")
            raise click.Abort()
        progress.advance(overall_task)
        
        progress.update(overall_task, description="Building phasing table...")
        if verbose:
            console.print("\nSNPs to analyze:")
            console.print(snps_df)
            console.print("\nAttempting to build phasing table...")
            
        phasing_table = build_phasing_table(bam_file, snps_df)
        
        if verbose:
            console.print(f"\nBuilt phasing table with {len(phasing_table)} entries")
            if not phasing_table:
                console.print("[yellow]Warning: No reads found that cover any SNP positions[/yellow]")
                console.print("This could be because:")
                console.print("- The BAM file doesn't have coverage at these positions")
                console.print("- The chromosome/contig names don't match between BAM and SNPs file")
                console.print("- The SNP positions are outside the mapped region")
        
        if not phasing_table:
            console.print("[red]Error: No valid phasing information found[/red]")
            raise click.Abort()
        progress.advance(overall_task)
        
        progress.update(overall_task, description="Creating DAG...")
        graph = create_dag(phasing_table, snps_df)
        progress.advance(overall_task)
        
        progress.update(overall_task, description="Finding haplotypes...")
        haplotypes = find_haplotypes(graph)
        progress.advance(overall_task)
    
    # Create a nice table output
    table = Table(title="Identified Haplotypes")
    table.add_column("Proportion", justify="right", style="cyan")
    table.add_column("SNPs", style="magenta")
    
    for haplotype in haplotypes:
        snp_list, proportion = haplotype
        # Keep positions and bases, just format them nicely
        snp_string = ' | '.join(snp.replace(':', ' ') for snp in snp_list)
        table.add_row(f"{proportion:.3f}", snp_string)
    
    console.print(table)
    
    if output:
        if verbose:
            console.print(f"Saving results to {output}")
        # Convert haplotypes to DataFrame and save
        haplotypes_df = pd.DataFrame(haplotypes)
        haplotypes_df.to_csv(output, sep='\t', index=True)
    
    if plot:
        if verbose:
            console.print("Generating interactive plot...")
        plot_graph_interactive(graph)
        plt.show()

@cli.command()
@click.argument('input_vcf', type=click.Path(exists=True))
@click.argument('output_tsv', type=click.Path())
@click.option('--verbose', '-v', is_flag=True, help='Print detailed progress information')
def convert(input_vcf, output_tsv, verbose):
    """Convert VCF file to TSV format."""
    console = Console()
    
    try:
        if verbose:
            console.print(f"Converting {input_vcf} to {output_tsv}")
        
        convert_vcf_to_tsv(input_vcf, output_tsv)
        
        if verbose:
            console.print("Conversion completed successfully", style="green")
    except Exception as e:
        console.print(f"Error: {e}", style="red")
        raise click.Abort()

if __name__ == '__main__':
    cli()