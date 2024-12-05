import argparse
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import find_significant_regions

def main(args=None):
    if args is None:
        parser = argparse.ArgumentParser(
            description='Identify significantly different genomic regions using rank-based classification.'
        )
        parser.add_argument(
            '--track_FC',
            type=str,
            required=True,
            help='Input file for FC feature (e.g., tracks_log_Wald_pValue.bedgraph)'
        )
        parser.add_argument(
            '--track_correlation',
            type=str,
            required=True,
            help='Input file for correlation feature (e.g., tracks_pearson.bedgraph)'
        )
        parser.add_argument(
            '--output_dir',
            type=str,
            default='output_SDRs',
            help='Output directory for result files'
        )
        parser.add_argument(
            '--min_region_size',
            type=int,
            default=5,
            help='Minimum number of consecutive bins to define a region (default: 5)'
        )
        parser.add_argument(
            '--fc_high_percentile',
            type=float,
            default=95,
            help='Percentile threshold for high FC (default: 75)'
        )
        parser.add_argument(
            '--fc_low_percentile',
            type=float,
            default=10,
            help='Percentile threshold for low FC (default: 25)'
        )
        parser.add_argument(
            '--corr_high_percentile',
            type=float,
            default=95,
            help='Percentile threshold for high correlation (default: 75)'
        )
        parser.add_argument(
            '--corr_low_percentile',
            type=float,
            default=10,
            help='Percentile threshold for low correlation (default: 25)'
        )
        parser.add_argument(
            '--chroms',
            nargs='+',
            help='List of chromosomes to process (default: all)'
        )
        args = parser.parse_args()
    else:
        # Args are provided programmatically
        pass  # args are already set

    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Call the function to find significant regions
    find_significant_regions(
        track_FC_file=args.track_FC,
        track_correlation_file=args.track_correlation,
        output_dir=args.output_dir,
        min_region_size=args.min_region_size,
        fc_high_percentile=args.fc_high_percentile,
        fc_low_percentile=args.fc_low_percentile,
        corr_high_percentile=args.corr_high_percentile,
        corr_low_percentile=args.corr_low_percentile,
        chroms=args.chroms
    )

if __name__ == '__main__':
    main()
