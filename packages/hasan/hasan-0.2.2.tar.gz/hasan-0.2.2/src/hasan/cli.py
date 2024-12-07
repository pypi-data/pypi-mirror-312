import click
from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt
import pandas as pd
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
    """Haplotype Analysis Tool"""
    pass

@cli.command()
@click.argument('bam_file', type=click.Path(exists=True))
@click.argument('snps_file', type=click.Path(exists=True))
@click.option('--method', '-m', 
              type=click.Choice(['min', 'multiply'], case_sensitive=False),
              default='min',
              help='Method for calculating path weights')
@click.option('--plot/--no-plot', default=False, help='Show interactive plot')
@click.option('--output', '-o', type=click.Path(), help='Output TSV file')
@click.option('--verbose', '-v', is_flag=True, help='Print detailed progress')
def analyze(bam_file, snps_file, method, plot, output, verbose):
    """Analyze haplotypes from BAM and SNPs files."""
    console = Console()
    
    with console.status("[bold green]Processing..." if not verbose else "[bold green]Starting analysis...") as status:
        # Read input files
        if verbose:
            status.update("[bold blue]Reading SNPs file...")
        snps_df = read_snps(snps_file)
        
        if snps_df.empty:
            console.print("[red]Error: No SNPs found in input file[/red]")
            raise click.Abort()
            
        if verbose:
            console.print(f"Found {len(snps_df)} SNPs in input file")
            console.print("SNPs DataFrame head:")
            console.print(snps_df.head())
        
        # Build phasing table
        if verbose:
            status.update("[bold blue]Building phasing table...")
        phasing_data = build_phasing_table(bam_file, snps_df, verbose=verbose)
        
        if not phasing_data:
            console.print("[red]Error: No phasing data generated[/red]")
            raise click.Abort()
            
        if verbose:
            console.print("\nPhasing data summary:")
            for ref in phasing_data:
                console.print(f"Reference {ref}: {len(phasing_data[ref])} positions")
        
        # Create graphs for each reference
        if verbose:
            status.update("[bold blue]Creating graphs...")
        graphs = create_dag(phasing_data, snps_df)
        
        if not graphs:
            console.print("[red]Error: No graphs created[/red]")
            raise click.Abort()
            
        if verbose:
            console.print(f"\nCreated graphs for {len(graphs)} references")
            for ref in graphs:
                G = graphs[ref]
                console.print(f"Reference {ref}: {len(G.nodes())} nodes, {len(G.edges())} edges")
        
        # Process each reference sequence
        all_results = []
        for ref_name, graph in graphs.items():
            if verbose:
                status.update(f"[bold blue]Processing reference: {ref_name}")
                console.print(f"\nAnalyzing reference: {ref_name}")
            
            if plot:
                if verbose:
                    status.update(f"[bold blue]Generating plot for {ref_name}...")
                plt.figure(figsize=(15, 8))
                plot_graph_interactive(graph)
                plt.title(f"Haplotype Graph - {ref_name}")
                plt.savefig(f'haplotype_graph_{ref_name}.png', bbox_inches='tight', dpi=300)
                plt.show()
            
            # Find haplotypes
            if verbose:
                status.update(f"[bold blue]Finding haplotypes for {ref_name}...")
            haplotypes = find_haplotypes(graph, method=method.lower(), verbose=verbose)
            
            if not haplotypes:
                console.print(f"[yellow]Warning: No haplotypes found for reference {ref_name}[/yellow]")
                continue
                
            if verbose:
                console.print(f"Found {len(haplotypes)} haplotypes for {ref_name}")
            
            # Add reference name to results
            results_df = pd.DataFrame(haplotypes, columns=['Haplotype', 'Proportion'])
            results_df['Reference'] = ref_name
            results_df['Haplotype'] = results_df['Haplotype'].apply(lambda x: ' -> '.join(x))
            all_results.append(results_df)
    
    if not all_results:
        console.print("[red]Error: No haplotypes found in any reference[/red]")
        raise click.Abort()
    
    # Combine all results
    final_results = pd.concat(all_results, ignore_index=True)
    
    # Print pretty table
    for ref_name in final_results['Reference'].unique():
        ref_results = final_results[final_results['Reference'] == ref_name]
        
        table = Table(title=f"Haplotype Analysis Results - {ref_name}")
        table.add_column("Haplotype", style="cyan")
        table.add_column("Proportion", style="magenta")
        
        for _, row in ref_results.iterrows():
            table.add_row(row['Haplotype'], f"{float(row['Proportion']):.3f}")
        
        console.print(table)
        console.print("")  # Add blank line between tables
    
    # Save results if output path provided
    if output:
        final_results.to_csv(output, sep='\t', index=False)
        console.print(f"\n[green]Results saved to:[/green] {output}")
    
    return final_results

@cli.command()
@click.argument('vcf_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--verbose', '-v', is_flag=True, help='Print detailed progress')
def convert(vcf_file, output_file, verbose):
    """Convert a VCF file to TSV format for haplotype analysis."""
    console = Console()
    
    with console.status("[bold green]Converting VCF to TSV..." if not verbose else "[bold green]Starting conversion...") as status:
        try:
            if verbose:
                console.print(f"Converting {vcf_file} to {output_file}")
            
            convert_vcf_to_tsv(vcf_file, output_file)
            
            console.print(f"[green]Successfully converted VCF to TSV:[/green] {output_file}")
        
        except Exception as e:
            console.print(f"[red]Error during conversion: {str(e)}[/red]")
            raise click.Abort()

def main():
    return cli()

if __name__ == '__main__':
    main()