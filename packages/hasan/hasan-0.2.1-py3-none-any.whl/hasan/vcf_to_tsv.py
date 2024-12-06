#!/usr/bin/env python3

import sys
import re

def parse_vcf(vcf_file):
    """Parse VCF file and return a list of variant dictionaries."""
    variants = []
    
    with open(vcf_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Skip header lines
            if line.startswith('#'):
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
                
            # Filter based on quality and support
            # Adjust these thresholds as needed
            try:
                quality = float(qual)
                depth = int(info_dict.get('DP', 0))
                
                if quality < 30 or depth < 10:  # Example thresholds
                    continue
                    
                variant = {
                    'CHROM': chrom,
                    'POS': pos,
                    'REF': ref,
                    'ALT': alt,
                    'QUAL': qual,
                    'DP': depth
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
    fields = ['CHROM', 'POS', 'REF', 'ALT', 'QUAL', 'DP']
    
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