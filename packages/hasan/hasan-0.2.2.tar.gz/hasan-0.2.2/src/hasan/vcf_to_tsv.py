#!/usr/bin/env python3

import sys
import re

def parse_vcf(vcf_file):
    """Parse VCF file and return a list of variant dictionaries."""
    variants = []
    format_idx = None
    sample_idx = None
    
    with open(vcf_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Get header format
            if line.startswith('#CHROM'):
                headers = line[1:].split('\t')
                format_idx = headers.index('FORMAT') if 'FORMAT' in headers else None
                # Get the sample index (first sample column after FORMAT)
                sample_idx = format_idx + 1 if format_idx is not None else None
                continue
            # Skip other header lines
            elif line.startswith('#'):
                continue
                
            # Parse variant data
            fields = line.split('\t')
            if len(fields) < 8:  # VCF should have at least 8 mandatory fields
                continue
                
            # Extract relevant fields
            chrom, pos, id_, ref, alt, qual, filter_, info = fields[:8]
            
            # Skip indels
            if len(ref) > 1 or len(alt) > 1:
                continue
                
            # Parse INFO field
            info_dict = dict(item.split('=') if '=' in item else (item, True) 
                           for item in info.split(';'))
            
            # Get allele support information
            ref_support = 0
            alt_support = 0
            total_depth = 0
            alt_freq = 0.0

            # Try to get allele support from FORMAT field first
            if format_idx is not None and sample_idx is not None and len(fields) > sample_idx:
                format_fields = fields[format_idx].split(':')
                sample_values = fields[sample_idx].split(':')
                
                # Create a dictionary of format fields and their values
                format_dict = dict(zip(format_fields, sample_values))
                
                # Try to get AD (Allele Depth)
                if 'AD' in format_dict:
                    try:
                        ad_values = [int(x) for x in format_dict['AD'].split(',')]
                        ref_support = ad_values[0]
                        alt_support = ad_values[1] if len(ad_values) > 1 else 0
                        total_depth = ref_support + alt_support
                    except (ValueError, IndexError):
                        pass
                
                # Alternative: try AO/RO fields
                elif 'AO' in format_dict and 'RO' in format_dict:
                    try:
                        ref_support = int(format_dict['RO'])
                        alt_support = int(format_dict['AO'])
                        total_depth = ref_support + alt_support
                    except ValueError:
                        pass

            # If no FORMAT field or parsing failed, try INFO field
            if total_depth == 0:
                try:
                    total_depth = int(info_dict.get('DP', 0))
                    # Some VCF files store allele counts in INFO
                    ao = info_dict.get('AO', '0')
                    ro = info_dict.get('RO', '0')
                    alt_support = int(ao)
                    ref_support = int(ro)
                except ValueError:
                    pass

            # Calculate allele frequency
            if total_depth > 0:
                alt_freq = round(alt_support / total_depth * 100, 2)
            
            # Determine zygosity based on allele frequency
            zygosity = 'UNKNOWN'
            if alt_freq > 95:
                zygosity = 'HOM'
            elif alt_freq > 5:
                zygosity = 'HET'
            
            # Filter based on quality and support
            try:
                quality = float(qual)
                if quality < 30 or total_depth < 10:  # Example thresholds
                    continue
                    
                variant = {
                    'CHROM': chrom,
                    'POS': pos,
                    'REF': ref,
                    'ALT': alt,
                    'QUAL': qual,
                    'DP': total_depth,
                    'REF_SUPPORT': ref_support,
                    'ALT_SUPPORT': alt_support,
                    'ALT_FREQ': f"{alt_freq}%",
                    'ZYGOSITY': zygosity
                }
                variants.append(variant)
            except (ValueError, KeyError):
                continue
    
    return variants

def convert_vcf_to_tsv(input_file, output_file):
    """Convert VCF file to TSV format."""
    # Parse VCF file
    variants = parse_vcf(input_file)
    
    # Define fields to extract
    fields = ['CHROM', 'POS', 'REF', 'ALT', 'QUAL', 'DP', 'REF_SUPPORT', 
             'ALT_SUPPORT', 'ALT_FREQ', 'ZYGOSITY']
    
    # Write TSV file
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write('\t'.join(fields) + '\n')
        
        # Write variant data
        for variant in variants:
            row = []
            for field in fields:
                value = str(variant.get(field, ''))
                # Clean up value (remove newlines, tabs)
                value = re.sub(r'[\n\t]', ' ', value)
                row.append(value)
            f.write('\t'.join(row) + '\n')

def main():
    if len(sys.argv) != 3:
        print("Usage: python vcf_to_tsv.py input.vcf output.tsv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        convert_vcf_to_tsv(input_file, output_file)
        print(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()