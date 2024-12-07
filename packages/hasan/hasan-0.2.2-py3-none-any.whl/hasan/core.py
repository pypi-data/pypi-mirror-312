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
    phasing_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    # Get all reference sequences from BAM file
    ref_names = bam.references
    if verbose:
        print(f"Found {len(ref_names)} reference sequences: {', '.join(ref_names)}")
    
    # Process each chromosome/reference sequence
    for ref_name in ref_names:
        # Get positions for this reference
        ref_snps = snps_df[snps_df['CHROM'] == ref_name]
        if ref_snps.empty:
            if verbose:
                print(f"No SNPs found for reference {ref_name}, skipping...")
            continue
            
        unique_positions = sorted(ref_snps['POS'].unique())
        total_positions = len(unique_positions)
        if verbose:
            print(f"\nProcessing {total_positions} SNP positions for {ref_name}...")
        
        for i, snp_pos in enumerate(unique_positions, 1):
            if verbose:
                print(f"Processing position {snp_pos} ({i}/{total_positions})...", end='\r')
            
            # Get reference base and zygosity for this position
            snp_info = ref_snps[ref_snps['POS'] == snp_pos].iloc[0]
            ref_base = snp_info['REF']
            zygosity = snp_info.get('ZYGOSITY', 'UNK')
            
            try:
                # Convert 1-based SNP position to 0-based for pileup
                zero_based_pos = snp_pos - 1
                for pileup_column in bam.pileup(ref_name, zero_based_pos, zero_based_pos + 1):
                    if pileup_column.pos == zero_based_pos:  # Compare with 0-based position
                        for pileup_read in pileup_column.pileups:
                            # Skip deletions and reference skips
                            if pileup_read.is_del or pileup_read.is_refskip:
                                continue
                                
                            # Get the alignment
                            alignment = pileup_read.alignment
                            
                            # Skip if no query sequence
                            if not alignment.query_sequence:
                                continue
                                
                            # Check quality
                            qualities = alignment.query_qualities
                            if qualities is None:
                                pass
                            elif pileup_read.query_position >= len(qualities):
                                continue
                            elif qualities[pileup_read.query_position] < min_quality:
                                continue
                            
                            # Get the base at this position
                            base = alignment.query_sequence[pileup_read.query_position]
                            
                            # Count strategy based on zygosity
                            if base == ref_base:
                                if zygosity == 'HET':
                                    # For heterozygous positions, count both as WT and specific base
                                    phasing_data[ref_name][snp_pos]['WT'] += 1
                                    phasing_data[ref_name][snp_pos][base] += 1
                                else:
                                    # For homozygous or unknown, just count as WT
                                    phasing_data[ref_name][snp_pos]['WT'] += 1
                            else:
                                # For non-reference bases, always count as specific base
                                phasing_data[ref_name][snp_pos][base] += 1
                            
            except Exception as e:
                if verbose:
                    print(f"\nWarning: Error processing {ref_name}:{snp_pos}: {str(e)}")
                continue
    
    if verbose:
        print("\nFinished processing all positions")
        print("\nPhasing Data Summary:")
        for ref_name in sorted(phasing_data.keys()):
            print(f"\nReference: {ref_name}")
            for pos in sorted(phasing_data[ref_name].keys()):
                print(f"Position {pos}:")
                total_reads = sum(phasing_data[ref_name][pos].values())
                for base, count in sorted(phasing_data[ref_name][pos].items()):
                    print(f"  {base}: {count} reads ({count/total_reads*100:.1f}%)")
    
    bam.close()
    return phasing_data

def create_dag(phasing_data, snps_df):
    """Create a single directed acyclic graph combining all reference sequences."""
    G = nx.DiGraph()
    
    # Add start (Y) and end (X) nodes
    G.add_node('Y', pos=(0, 0))
    
    # Track total positions to set X node position
    total_positions = 0
    position_offset = 0
    
    # Process each reference sequence
    for ref_name in phasing_data:
        ref_snps = snps_df[snps_df['CHROM'] == ref_name]
        positions = sorted(phasing_data[ref_name].keys())
        
        # Add nodes for each position and base
        for i, pos in enumerate(positions, 1):
            total_reads = sum(phasing_data[ref_name][pos].values())
            ref_bases = set(ref_snps[ref_snps['POS'] == pos]['REF'])
            
            for base, count in phasing_data[ref_name][pos].items():
                # Include reference name in node_id to make it unique
                node_id = f"{ref_name}_{pos}_{base}"
                is_wt = base in ref_bases
                G.add_node(node_id, pos=(i + position_offset, 0), base=base, 
                          position=pos, ref_name=ref_name,
                          is_wt=is_wt, weight=count/total_reads)
        
        # Connect nodes within this reference
        ref_positions = sorted(phasing_data[ref_name].keys())
        
        # Connect Y to first position of first reference
        if position_offset == 0:
            first_pos = ref_positions[0]
            total_first = sum(phasing_data[ref_name][first_pos].values())
            for base, count in phasing_data[ref_name][first_pos].items():
                G.add_edge('Y', f"{ref_name}_{first_pos}_{base}", weight=count/total_first)
        
        # Connect between positions
        for i in range(len(ref_positions)-1):
            curr_pos = ref_positions[i]
            next_pos = ref_positions[i+1]
            
            total_next = sum(phasing_data[ref_name][next_pos].values())
            
            for curr_base in phasing_data[ref_name][curr_pos]:
                for next_base, next_count in phasing_data[ref_name][next_pos].items():
                    G.add_edge(
                        f"{ref_name}_{curr_pos}_{curr_base}",
                        f"{ref_name}_{next_pos}_{next_base}",
                        weight=next_count/total_next
                    )
        
        # Connect last position to first position of next reference (if not last reference)
        if ref_name != list(phasing_data.keys())[-1]:
            next_ref = list(phasing_data.keys())[list(phasing_data.keys()).index(ref_name) + 1]
            last_pos = ref_positions[-1]
            next_first_pos = sorted(phasing_data[next_ref].keys())[0]
            
            total_last = sum(phasing_data[ref_name][last_pos].values())
            total_next_first = sum(phasing_data[next_ref][next_first_pos].values())
            
            for curr_base, curr_count in phasing_data[ref_name][last_pos].items():
                for next_base, next_count in phasing_data[next_ref][next_first_pos].items():
                    # Use average of current and next weights
                    weight = ((curr_count/total_last) + (next_count/total_next_first)) / 2
                    G.add_edge(
                        f"{ref_name}_{last_pos}_{curr_base}",
                        f"{next_ref}_{next_first_pos}_{next_base}",
                        weight=weight
                    )
        
        # Update position offset for next reference
        position_offset += len(positions)
        total_positions += len(positions)
    
    # Add X node and connect last reference's positions to it
    G.add_node('X', pos=(total_positions + 1, 0))
    last_ref = list(phasing_data.keys())[-1]
    last_pos = sorted(phasing_data[last_ref].keys())[-1]
    total_last = sum(phasing_data[last_ref][last_pos].values())
    
    for base, count in phasing_data[last_ref][last_pos].items():
        G.add_edge(f"{last_ref}_{last_pos}_{base}", 'X', weight=count/total_last)
    
    return {'combined': G}  # Return dict to maintain compatibility with existing code

def find_haplotypes(G, method='min', std_threshold=2.0, verbose=False):
    """Find haplotypes using statistical significance."""
    method = method.lower()
    if method not in ['min', 'multiply']:
        raise ValueError(f"Invalid method '{method}'. Must be either 'min' or 'multiply'")
    
    def get_all_paths_with_weights(graph, start='Y', end='X'):
        if verbose:
            print(f"\nSearching for paths from {start} to {end}")
        
        try:
            if method == 'multiply':
                # Pre-process graph to remove very low-weight edges
                threshold = 0.001  # Reduced threshold to 0.1%
                G_filtered = graph.copy()
                edges_to_remove = [(u, v) for u, v, d in G_filtered.edges(data=True) 
                                 if d['weight'] < threshold]
                if verbose:
                    print(f"Removing {len(edges_to_remove)} edges with weight < {threshold}")
                G_filtered.remove_edges_from(edges_to_remove)
                
                # Find paths using Dijkstra's algorithm
                paths = []
                try:
                    path = nx.shortest_path(G_filtered, start, end, 
                                          weight=lambda u, v, d: -np.log(d['weight']))
                    paths.append(path)
                    if verbose:
                        print(f"Found initial path with {len(path)} nodes")
                except nx.NetworkXNoPath:
                    if verbose:
                        print("No path found between start and end nodes")
                    return []
                
                # Try to find alternative paths
                for i in range(4):  # Look for 4 more paths
                    if paths:
                        temp_G = G_filtered.copy()
                        # Remove edges from all found paths
                        for found_path in paths:
                            path_edges = list(zip(found_path[:-1], found_path[1:]))
                            temp_G.remove_edges_from(path_edges)
                        
                        try:
                            path = nx.shortest_path(temp_G, start, end,
                                                  weight=lambda u, v, d: -np.log(d['weight']))
                            if path not in paths:  # Only add if path is unique
                                paths.append(path)
                                if verbose:
                                    print(f"Found alternative path {i+1} with {len(path)} nodes")
                        except nx.NetworkXNoPath:
                            if verbose:
                                print(f"No more alternative paths found after {len(paths)} paths")
                            break
                
                all_paths = paths
            else:
                # For 'min' method, use simple paths but with a limit
                all_paths = []
                for path in nx.all_simple_paths(graph, start, end):
                    all_paths.append(path)
                    if len(all_paths) >= 10:  # Limit to 10 paths for 'min' method too
                        break
            
            if verbose:
                print(f"Found {len(all_paths)} possible paths")
            
            path_weights = get_path_weights(graph, all_paths)
            if verbose and path_weights:
                print("Path weights found:")
                for path, weights, weight in path_weights[:3]:  # Show top 3 paths
                    print(f"Path weight: {weight:.4f}")
                    print(f"Edge weights: {[f'{w:.4f}' for w in weights]}")
            
            return path_weights
                
        except Exception as e:
            if verbose:
                print(f"Error finding paths: {str(e)}")
            return []
    
    def get_path_weights(graph, paths):
        """Helper function to calculate path weights."""
        path_weights = []
        for path in paths:
            try:
                weights = [graph[path[i]][path[i+1]]['weight'] for i in range(len(path)-1)]
                
                if method == 'multiply':
                    # Use log sum for multiplication to avoid numerical underflow
                    path_weight = np.exp(sum(np.log(weights)))
                else:  # method == 'min'
                    path_weight = min(weights)
                    
                if path_weight > 0:
                    path_weights.append((path, weights, path_weight))
            except Exception as e:
                if verbose:
                    print(f"Error calculating weights for path: {str(e)}")
                continue
        
        # Sort by path weight (highest to lowest)
        path_weights.sort(key=lambda x: x[2], reverse=True)
        return path_weights

    if verbose:
        print("\nStarting haplotype analysis...")
        print("Graph properties:")
        print(f"Nodes: {len(G.nodes())}")
        print(f"Edges: {len(G.edges())}")
    
    # Create a working copy of the graph
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
            
        # Get path with highest weight
        best_path, path_weights, min_weight = path_weights[0]
        
        # Only keep paths with weight above threshold (0.1% for multiply method)
        if method == 'multiply' and min_weight < 0.001:  # Changed from 0.005
            if verbose:
                print(f"Skipping path with weight {min_weight} (below threshold 0.001)")
            break
            
        # Extract sequence information
        sequence = []
        for node in best_path[1:-1]:  # Skip start and end nodes
            ref_name = G_copy.nodes[node]['ref_name']
            position = G_copy.nodes[node]['position']
            base = G_copy.nodes[node]['base']
            sequence.append(f"{ref_name}:{position}:{base}")
        
        if verbose:
            print(f"\nFound haplotype: {' -> '.join(sequence)}")
            print(f"Weight: {min_weight}")
        
        out_paths.append(sequence)
        out_min_weights.append(min_weight)
        
        # Update weights by subtracting minimum weight
        for i in range(len(best_path)-1):
            u, v = best_path[i], best_path[i+1]
            G_copy[u][v]['weight'] -= min_weight
            # Remove edge if weight becomes very small
            if G_copy[u][v]['weight'] <= 0.0001:  # Changed from 0.001
                G_copy.remove_edge(u, v)
    
    # Normalize frequencies
    total_weight = sum(out_min_weights)
    if total_weight > 0:
        normalized_weights = [round(w/total_weight, 3) for w in out_min_weights]
    else:
        normalized_weights = []
    
    if verbose:
        print("\nFinal Results:")
        for path, weight in zip(out_paths, normalized_weights):
            print(f"Haplotype: {' -> '.join(path)}, Frequency: {weight}")
    
    # Consolidate identical paths and paths with very similar weights
    consolidated = {}  # Use dictionary to track unique paths
    
    for path, weight in zip(out_paths, normalized_weights):
        # Convert path to tuple for hashing
        path_tuple = tuple(path)
        if path_tuple in consolidated:
            consolidated[path_tuple] += weight
        else:
            consolidated[path_tuple] = weight
    
    # Convert back to lists and sort by weight
    consolidated_items = sorted(consolidated.items(), key=lambda x: x[1], reverse=True)
    consolidated_paths = [list(path) for path, _ in consolidated_items]
    consolidated_weights = [weight for _, weight in consolidated_items]
    
    # Re-normalize the consolidated weights
    total_weight = sum(consolidated_weights)
    if total_weight > 0:
        consolidated_weights = [round(w/total_weight, 3) for w in consolidated_weights]
    
    if verbose:
        print("\nConsolidated Results:")
        for path, weight in zip(consolidated_paths, consolidated_weights):
            print(f"Haplotype: {' -> '.join(path)}, Frequency: {weight}")
    
    # Only return paths with weight >= 1%
    significant_paths = [(path, weight) for path, weight in zip(consolidated_paths, consolidated_weights) 
                        if weight >= 0.01]
    
    if not significant_paths:
        if verbose:
            print("No significant haplotypes found (all < 1%)")
        return []
        
    return significant_paths

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
        
        # Build phasing table
        phasing_data = build_phasing_table(bam_file, snps_df, verbose=verbose)
        
        # Create graphs for each reference
        if verbose:
            status.update("[bold blue]Creating graphs...")
        graphs = create_dag(phasing_data, snps_df)
        
        # Process each reference sequence
        all_results = []
        for ref_name, G in graphs.items():
            if verbose:
                status.update(f"[bold blue]Processing reference: {ref_name}")
            
            if plot:
                if verbose:
                    status.update(f"[bold blue]Generating plot for {ref_name}...")
                plt.figure(figsize=(15, 8))
                plot_graph_interactive(G)
                plt.title(f"Haplotype Graph - {ref_name}")
                plt.savefig(f'haplotype_graph_{ref_name}.png', bbox_inches='tight', dpi=300)
                plt.show()
            
            # Find haplotypes
            if verbose:
                status.update(f"[bold blue]Finding haplotypes for {ref_name}...")
            haplotypes = find_haplotypes(G, method=method.lower(), verbose=verbose)
            
            # Add reference name to results
            results_df = pd.DataFrame(haplotypes, columns=['Haplotype', 'Proportion'])
            results_df['Reference'] = ref_name
            results_df['Haplotype'] = results_df['Haplotype'].apply(lambda x: ' -> '.join(x))
            all_results.append(results_df)
    
    # Combine all results
    final_results = pd.concat(all_results, ignore_index=True)
    
    # Print single combined table
    table = Table(title="Global Haplotype Analysis Results")
    table.add_column("Haplotype", style="cyan")
    table.add_column("Proportion", style="magenta")
    
    for _, row in final_results.iterrows():
        table.add_row(row['Haplotype'], f"{float(row['Proportion']):.3f}")
    
    console.print(table)
    console.print("")
    
    # Save results if output path provided
    if output:
        final_results.to_csv(output, sep='\t', index=False)
        console.print(f"\n[green]Results saved to:[/green] {output}")
    
    return final_results

if __name__ == "__main__":
    main()
