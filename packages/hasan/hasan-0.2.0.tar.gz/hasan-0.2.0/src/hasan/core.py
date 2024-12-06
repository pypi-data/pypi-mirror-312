import pysam
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import click
from rich.console import Console
from rich.table import Table

def read_snps(snps_file):
    """Read SNPs from TSV file, properly handling headers."""
    # Read the file
    df = pd.read_csv(snps_file, sep='\t')
    
    # Remove any rows where CHROM column contains 'CHROM' or '#CHROM'
    df = df[~df['CHROM'].astype(str).str.contains('CHROM')]
    
    # Reset the index after filtering
    df = df.reset_index(drop=True)
    
    # Ensure the POS column is numeric
    df['POS'] = pd.to_numeric(df['POS'], errors='coerce')
    
    # Drop any rows with NaN values
    df = df.dropna(subset=['CHROM', 'POS', 'REF', 'ALT'])
    
    return df

def build_phasing_table(bam_file, snps_df, min_quality=20, verbose=False):
    """Build phasing table from BAM file for given SNP positions."""
    if verbose:
        print("\nBuilding phasing table...")
    bam = pysam.AlignmentFile(bam_file, "rb")
    phasing_data = defaultdict(lambda: defaultdict(int))
    
    # Get reference sequence name from BAM file
    ref_name = bam.references[0]
    if verbose:
        print(f"Using reference: {ref_name}")
    
    # Get unique positions
    unique_positions = sorted(snps_df['POS'].unique())
    total_positions = len(unique_positions)
    if verbose:
        print(f"Processing {total_positions} unique SNP positions...")
    
    for i, snp_pos in enumerate(unique_positions, 1):
        if verbose:
            print(f"Processing position {snp_pos} ({i}/{total_positions})...", end='\r')
        try:
            for pileup_column in bam.pileup(ref_name, snp_pos - 1, snp_pos):
                if pileup_column.pos == snp_pos - 1:
                    for pileup_read in pileup_column.pileups:
                        # Skip deletions and reference skips
                        if pileup_read.is_del or pileup_read.is_refskip:
                            continue
                            
                        # Get the alignment
                        alignment = pileup_read.alignment
                        
                        # Skip if no query sequence
                        if not alignment.query_sequence:
                            continue
                            
                        # Check if quality scores exist and meet threshold
                        qualities = alignment.query_qualities
                        if qualities is None:
                            # If no quality scores, assume it passes quality threshold
                            pass
                        elif pileup_read.query_position >= len(qualities):
                            continue
                        elif qualities[pileup_read.query_position] < min_quality:
                            continue
                        
                        # Get the base at this position
                        base = alignment.query_sequence[pileup_read.query_position]
                        phasing_data[snp_pos][base] += 1
                        
        except Exception as e:
            if verbose:
                print(f"\nWarning: Error processing position {snp_pos}: {str(e)}")
            continue
    
    if verbose:
        print("\nFinished processing all positions")
        print("\nPhasing Data Summary:")
        for pos in sorted(phasing_data.keys()):
            print(f"Position {pos}:")
            total_reads = sum(phasing_data[pos].values())
            for base, count in sorted(phasing_data[pos].items()):
                print(f"  {base}: {count} reads ({count/total_reads*100:.1f}%)")
    
    bam.close()
    return phasing_data

def create_dag(phasing_data, snps_df):
    """Create directed acyclic graph from phasing data."""
    G = nx.DiGraph()
    
    # Add start (Y) and end (X) nodes
    G.add_node('Y', pos=(0, 0))
    G.add_node('X', pos=(len(set(snps_df['POS'])) + 1, 0))
    
    # Add nodes for each position and base
    positions = sorted(phasing_data.keys())
    for i, pos in enumerate(positions, 1):
        total_reads = sum(phasing_data[pos].values())
        ref_bases = set(snps_df[snps_df['POS'] == pos]['REF'])
        
        for base, count in phasing_data[pos].items():
            node_id = f"{pos}_{base}"
            is_wt = base in ref_bases
            G.add_node(node_id, pos=(i, 0), base=base, position=pos, 
                      is_wt=is_wt, weight=count/total_reads)
    
    # Connect Y to first position
    first_pos = positions[0]
    total_first = sum(phasing_data[first_pos].values())
    for base, count in phasing_data[first_pos].items():
        G.add_edge('Y', f"{first_pos}_{base}", weight=count/total_first)
    
    # Connect between positions
    for i in range(len(positions)-1):
        curr_pos = positions[i]
        next_pos = positions[i+1]
        
        # Calculate total reads in next position
        total_next = sum(phasing_data[next_pos].values())
        
        # Create edges with weights based on the proportion of reads in the destination
        for curr_base in phasing_data[curr_pos]:
            for next_base, next_count in phasing_data[next_pos].items():
                G.add_edge(
                    f"{curr_pos}_{curr_base}",
                    f"{next_pos}_{next_base}",
                    weight=next_count/total_next  # Simply use the proportion of reads at destination
                )
    
    # Connect last position to X
    last_pos = positions[-1]
    total_last = sum(phasing_data[last_pos].values())
    for base, count in phasing_data[last_pos].items():
        G.add_edge(f"{last_pos}_{base}", 'X', weight=count/total_last)
    
    return G

def find_haplotypes_backup(G, method='min', verbose=False):
    """Original find_haplotypes function kept as backup."""
    # Validate method
    method = method.lower()
    if method not in ['min', 'multiply']:
        raise ValueError(f"Invalid method '{method}'. Must be either 'min' or 'multiply'")
        
    def get_all_paths_with_weights(graph, start='Y', end='X'):
        if verbose:
            print(f"\nSearching for paths from {start} to {end}")
            print(f"Number of nodes in graph: {len(graph.nodes())}")
            print(f"Number of edges in graph: {len(graph.edges())}")
        
        try:
            all_paths = list(nx.all_simple_paths(graph, start, end))
            if verbose:
                print(f"Found {len(all_paths)} possible paths")
        except nx.NetworkXNoPath:
            if verbose:
                print("No path exists between start and end nodes!")
            return []
        
        path_weights = []
        for path in all_paths:
            weights = [graph[path[i]][path[i+1]]['weight'] for i in range(len(path)-1)]
            
            if method == 'multiply':
                path_weight = np.prod(weights)  # Multiply weights together
            else:  # method == 'min'
                path_weight = min(weights)  # Use minimum weight
                
            if path_weight > 0:
                path_weights.append((path, weights, path_weight))
                if verbose:
                    print(f"Path found with weight {path_weight}: {' -> '.join(path)}")
        
        # Sort by path weight (highest to lowest)
        path_weights.sort(key=lambda x: x[2], reverse=True)
        return path_weights

    G_copy = G.copy()
    out_paths = []
    out_min_weights = []
    
    while True:
        # Get all paths and their weights
        path_weights = get_all_paths_with_weights(G_copy)
        
        # Break if no valid paths remain
        if not path_weights:
            if verbose:
                print("\nNo more valid paths found")
            break
            
        # Get path with minimum score
        best_path, path_weights, _ = path_weights[0]
        min_weight = min(path_weights)
        
        # Extract sequence information
        sequence = []
        for node in best_path[1:-1]:  # Skip start and end nodes
            position = G_copy.nodes[node]['position']
            base = G_copy.nodes[node]['base']
            sequence.append(f"{position}:{base}")
        
        if verbose:
            print(f"\nFound haplotype: {' -> '.join(sequence)}")
            print(f"Weight: {min_weight}")
        
        out_paths.append(sequence)
        out_min_weights.append(min_weight)
        
        # Update weights by subtracting minimum weight
        for i in range(len(best_path)-1):
            u, v = best_path[i], best_path[i+1]
            G_copy[u][v]['weight'] -= min_weight
    
    # Normalize frequencies
    total_weight = sum(out_min_weights)
    if total_weight > 0:
        normalized_weights = [round(w/total_weight, 3) for w in out_min_weights]
    else:
        normalized_weights = []
        
    return list(zip(out_paths, normalized_weights))

def find_haplotypes(G, method='min', std_threshold=2.0, verbose=False):
    """Find haplotypes using statistical significance.
    
    Args:
        G: NetworkX DiGraph
        method: str, either 'min' or 'multiply' for weight calculation method
        std_threshold: float, number of standard deviations above mean to consider significant
        verbose: bool, whether to print detailed progress
    """
    # Validate method
    method = method.lower()
    if method not in ['min', 'multiply']:
        raise ValueError(f"Invalid method '{method}'. Must be either 'min' or 'multiply'")
        
    def get_all_paths_with_weights(graph, start='Y', end='X'):
        if verbose:
            print(f"\nSearching for paths from {start} to {end}")
        
        try:
            all_paths = list(nx.all_simple_paths(graph, start, end))
        except nx.NetworkXNoPath:
            if verbose:
                print("No path exists between start and end nodes!")
            return []
        
        # Get all path weights first to calculate statistics
        path_weights = []
        for path in all_paths:
            weights = [graph[path[i]][path[i+1]]['weight'] for i in range(len(path)-1)]
            
            if method == 'multiply':
                path_weight = np.prod(weights)
            else:  # method == 'min'
                path_weight = min(weights)
                
            if path_weight > 0:
                path_weights.append((path, weights, path_weight))
        
        if path_weights:
            # Calculate statistics
            weights_only = [pw[2] for pw in path_weights]
            mean_weight = np.mean(weights_only)
            std_weight = np.std(weights_only)
            
            # Filter paths by statistical significance
            significant_paths = [
                pw for pw in path_weights 
                if pw[2] > mean_weight + (std_threshold * std_weight)
            ]
            
            # Sort by path weight (highest to lowest)
            significant_paths.sort(key=lambda x: x[2], reverse=True)
            return significant_paths
        
        return []

    G_copy = G.copy()
    out_paths = []
    out_min_weights = []
    
    while True:
        # Get statistically significant paths and their weights
        path_weights = get_all_paths_with_weights(G_copy)
        
        # Break if no valid paths remain
        if not path_weights:
            break
            
        # Get path with highest weight
        best_path, path_weights, min_weight = path_weights[0]
        
        # Extract sequence information
        sequence = []
        for node in best_path[1:-1]:  # Skip start and end nodes
            position = G_copy.nodes[node]['position']
            base = G_copy.nodes[node]['base']
            sequence.append(f"{position}:{base}")
        
        if verbose:
            print(f"\nFound significant haplotype: {' -> '.join(sequence)}")
            print(f"Weight: {min_weight}")
        
        out_paths.append(sequence)
        out_min_weights.append(min_weight)
        
        # Update weights by subtracting minimum weight
        for i in range(len(best_path)-1):
            u, v = best_path[i], best_path[i+1]
            G_copy[u][v]['weight'] -= min_weight
    
    # Normalize frequencies
    total_weight = sum(out_min_weights)
    if total_weight > 0:
        normalized_weights = [round(w/total_weight, 3) for w in out_min_weights]
    else:
        normalized_weights = []
        
    return list(zip(out_paths, normalized_weights))

def plot_graph_interactive(G):
    """Plot the DAG with draggable nodes."""
    import matplotlib
    matplotlib.use('TkAgg')  # Use TkAgg backend for interaction
    
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Create initial position dictionary with vertical spacing for bases
    pos = {}
    base_order = {'A': 0, 'G': 1, 'C': 2, 'T': 3}
    vertical_spacing = 0.5
    
    # Add start and end nodes
    pos['Y'] = (-1, 2*vertical_spacing)
    pos['X'] = (max(float(node.split('_')[0]) for node in G.nodes() if node not in ['X', 'Y']) + 1, 2*vertical_spacing)
    
    # Add position nodes with vertical spacing
    for node in G.nodes():
        if node not in ['X', 'Y']:
            position, base = node.split('_')
            x_pos = float(position)
            y_pos = base_order.get(base, len(base_order)) * vertical_spacing
            pos[node] = (x_pos, y_pos)
    
    # Create node colors
    node_colors = []
    for node in G.nodes():
        if node in ['X', 'Y']:
            node_colors.append('lightgray')
        elif G.nodes[node].get('is_wt', False):
            node_colors.append('lightgreen')
        else:
            node_colors.append('lightblue')
    
    # Draw the graph
    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000)
    edges = nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20,
                                 width=[G[u][v]['weight'] * 2 for u, v in G.edges()])
    
    # Add edge labels (weights)
    edge_labels = {(u, v): f'{G[u][v]["weight"]:.2f}' for (u, v) in G.edges()}
    edge_label_objects = nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    # Add node labels
    labels = {}
    for node in G.nodes():
        if node in ['X', 'Y']:
            labels[node] = node
        else:
            position, base = node.split('_')
            labels[node] = f"{position}\n{base}"
    label_objects = nx.draw_networkx_labels(G, pos, labels)

    # Make nodes draggable
    class DraggableNode:
        def __init__(self, nodes, edges, edge_labels, node_labels):
            self.nodes = nodes
            self.edges = edges
            self.edge_labels = edge_labels
            self.node_labels = node_labels
            self.dragged_node = None
            self.offset = None
            
            self.nodes.set_picker(True)
            self.cid_pick = fig.canvas.mpl_connect('pick_event', self.on_pick)
            self.cid_release = fig.canvas.mpl_connect('button_release_event', self.on_release)
            self.cid_motion = fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

        def on_pick(self, event):
            if event.artist == self.nodes:
                self.dragged_node = event.ind[0]
                pos_array = self.nodes.get_offsets()
                self.offset = pos_array[self.dragged_node] - [event.mouseevent.xdata, event.mouseevent.ydata]

        def on_motion(self, event):
            if self.dragged_node is not None and event.inaxes:
                pos_array = self.nodes.get_offsets()
                new_pos = [event.xdata, event.ydata] + self.offset
                pos_array[self.dragged_node] = new_pos
                self.nodes.set_offsets(pos_array)
                
                # Update node positions in pos dictionary
                node_list = list(G.nodes())
                pos[node_list[self.dragged_node]] = tuple(new_pos)
                
                # Redraw edges
                self.edges.remove()
                self.edges = nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20,
                                                  width=[G[u][v]['weight'] * 2 for u, v in G.edges()])
                
                # Update edge labels
                for edge, label_obj in self.edge_labels.items():
                    label_obj.remove()
                self.edge_labels = nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
                
                # Update node labels
                for node, label_obj in self.node_labels.items():
                    label_obj.remove()
                self.node_labels = nx.draw_networkx_labels(G, pos, labels)
                
                fig.canvas.draw_idle()

        def on_release(self, event):
            self.dragged_node = None
            self.offset = None

    # Create draggable node handler
    draggable = DraggableNode(nodes, edges, edge_label_objects, label_objects)
    
    plt.title("Haplotype Graph (Drag nodes to rearrange)")
    plt.axis('off')
    plt.tight_layout()
    
    return plt

@click.command()
@click.argument('bam_file', type=click.Path(exists=True))
@click.argument('snps_file', type=click.Path(exists=True))
@click.option('--method', '-m', 
              type=click.Choice(['min', 'multiply'], case_sensitive=False),
              default='min',
              help='Method for calculating path weights (min or multiply)')
@click.option('--plot/--no-plot', default=False, help='Show interactive plot')
@click.option('--output', '-o', type=click.Path(), help='Output TSV file for haplotypes')
@click.option('--verbose', '-v', is_flag=True, help='Print detailed progress information')
def main(bam_file, snps_file, method, plot, output, verbose):
    """Analyze haplotypes from BAM and SNPs files."""
    console = Console()
    
    with console.status("[bold green]Processing..." if not verbose else "[bold green]Starting haplotype analysis...") as status:
        # Read input files
        if verbose:
            status.update("[bold blue]Reading SNPs file...")
        snps_df = read_snps(snps_file)
        if verbose:
            console.print("[green]✓[/green] Loaded SNPs file with columns:", snps_df.columns.tolist())
        
        # Build phasing table
        phasing_data = build_phasing_table(bam_file, snps_df, verbose=verbose)
        
        # Create and plot graph
        if verbose:
            status.update("[bold blue]Creating graph...")
        G = create_dag(phasing_data, snps_df)
        
        if plot:
            if verbose:
                status.update("[bold blue]Generating interactive plot...")
            plot_graph_interactive(G)
            plt.show()
        
        # Save the graph
        plt.savefig('haplotype_graph.png', bbox_inches='tight', dpi=300)
        
        # Find haplotypes
        if verbose:
            status.update("[bold blue]Finding haplotypes...")
        haplotypes = find_haplotypes(G, method=method.lower(), verbose=verbose)
    
    # Create results table
    results_df = pd.DataFrame(haplotypes, columns=['Haplotype', 'Proportion'])
    results_df['Haplotype'] = results_df['Haplotype'].apply(lambda x: ' -> '.join(x))
    
    # Print pretty table
    table = Table(title="Haplotype Analysis Results")
    table.add_column("Haplotype", style="cyan")
    table.add_column("Proportion", style="magenta")
    
    for _, row in results_df.iterrows():
        table.add_row(row['Haplotype'], f"{float(row['Proportion']):.3f}")
    
    console.print(table)
    
    # Save results if output path provided
    if output:
        results_df.to_csv(output, sep='\t', index=False)
        console.print(f"\n[green]Results saved to:[/green] {output}")
    
    return results_df

if __name__ == "__main__":
    main()
