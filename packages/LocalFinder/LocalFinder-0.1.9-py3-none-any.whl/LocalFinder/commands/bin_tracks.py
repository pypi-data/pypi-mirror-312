import argparse
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import process_and_bin_file

def main(args=None):
    if args is None:
        parser = argparse.ArgumentParser(description='Prepare data by converting input tracks to bedgraph format with specified bin size.')
        parser.add_argument('--input_files', type=str, nargs='+', required=True, help='Input files in bigwig/bedgraph/bam/sam format.')
        parser.add_argument('--output_files', type=str, nargs='+', required=True, help='Output bedgraph files.')
        parser.add_argument('--bin_size', type=int, default=200, help='Bin size for binning (default: 200bp).')
        parser.add_argument('--chrom_sizes', type=str, required=True, help='Path to the chromosome sizes file.')
        parser.add_argument('--chroms', nargs='+', help='List of chromosomes to process (default: all)')
        args = parser.parse_args()
    else:
        # Args are provided programmatically
        pass  # args are already set

    input_files = args.input_files
    output_files = args.output_files
    bin_size = args.bin_size
    chrom_sizes = args.chrom_sizes
    chroms = args.chroms

    if len(input_files) != len(output_files):
        print("The number of input files must match the number of output files.")
        sys.exit(1)

    # Loop over input and output files
    for input_file, output_file in zip(input_files, output_files):
        # Process and bin each file
        process_and_bin_file(input_file, output_file, bin_size, chrom_sizes, chroms)

if __name__ == "__main__":
    main()