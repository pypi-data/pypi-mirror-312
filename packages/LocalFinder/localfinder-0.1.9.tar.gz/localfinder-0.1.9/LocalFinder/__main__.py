import argparse
import sys
import importlib.metadata

from LocalFinder.commands.bin_tracks import main as bin_tracks_main
from LocalFinder.commands.calculate_correlation_FC import main as calc_corr_main
from LocalFinder.commands.find_significantly_different_regions import main as find_regions_main
from LocalFinder.commands.visualize_tracks import main as visualize_main
from LocalFinder.pipeline import run_pipeline  # Import from pipeline.py

def main():
    # Retrieve package version
    try:
        version = importlib.metadata.version("LocalFinder")
    except importlib.metadata.PackageNotFoundError:
        version = "0.0.0"  # Fallback version

    # Create the top-level parser
    parser = argparse.ArgumentParser(
        prog='localfinder',
        description='LocalFinder: A tool for finding significantly different genomic regions of two tracks using local features.'
    )
    parser.add_argument('--version', '-V', action='version',
                        version=f'LocalFinder {version}',
                        help='Show program\'s version number and exit.')

    # Create subparsers for subcommands
    subparsers = parser.add_subparsers(dest='command', title='Subcommands',
                                       description='Valid subcommands',
                                       help='Additional help')

    # Subcommand: bin_tracks
    parser_bin = subparsers.add_parser(
        'bin_tracks',
        help='Convert input files into bins with BedGraph format.',
        description='Bin genomic tracks into fixed-size bins and output in BedGraph format.'
    )
    parser_bin.add_argument('--input_files', nargs='+', required=True,
                            help='Input BigWig files to be binned.')
    parser_bin.add_argument('--output_files', nargs='+', required=True,
                            help='Output BedGraph files for binned data.')
    parser_bin.add_argument('--bin_size', type=int, default=200,
                            help='Size of each bin (default: 200).')
    parser_bin.add_argument('--chrom_sizes', type=str, required=True,
                            help='Path to the chromosome sizes file.')
    parser_bin.add_argument('--chroms', nargs='+', required=True,
                            help='Chromosomes to process (e.g., chr20).')
    parser_bin.set_defaults(func=bin_tracks_main)

    # Subcommand: calculate_correlation_FC
    parser_calc = subparsers.add_parser(
        'calculate_correlation_FC',
        help='Calculate correlation and fold change between tracks.',
        description='Calculate the local Pearson correlation and fold change between two BedGraph tracks.'
    )
    parser_calc.add_argument('--track1', required=True,
                             help='First input BedGraph file.')
    parser_calc.add_argument('--track2', required=True,
                             help='Second input BedGraph file.')
    parser_calc.add_argument('--method', choices=['localPearson_and_FC'], default='localPearson_and_FC',
                             help='Method to calculate correlation and fold change (default: localPearson_and_FC).')
    parser_calc.add_argument('--method_params', type=str, default='{}',
                             help='Parameters for the method in JSON format (default: {}).')
    parser_calc.add_argument('--bin_number_of_window', type=int, default=11,
                             help='Number of bins in the sliding window (default: 11).')
    parser_calc.add_argument('--step', type=int, default=1,
                             help='Step size for the sliding window (default: 1).')
    parser_calc.add_argument('--output_dir', required=True,
                             help='Output directory for results.')
    parser_calc.add_argument('--chroms', nargs='+', required=True,
                             help='Chromosomes to process (e.g., chr20).')
    parser_calc.set_defaults(func=calc_corr_main)

    # Subcommand: find_significantly_different_regions
    parser_find = subparsers.add_parser(
        'find_significantly_different_regions',
        help='Find significantly different regions between tracks.',
        description='Identify genomic regions that show significant differences in correlation and fold change.'
    )
    parser_find.add_argument('--track_FC', required=True,
                             help='Fold change BedGraph file.')
    parser_find.add_argument('--track_correlation', required=True,
                             help='Correlation BedGraph file.')
    parser_find.add_argument('--output_dir', required=True,
                             help='Output directory for significant regions.')
    parser_find.add_argument('--min_region_size', type=int, default=5,
                             help='Minimum number of consecutive bins to define a region (default: 5).')
    parser_find.add_argument('--fc_high_percentile', type=float, default=75,
                             help='High percentile for fold change (default: 75).')
    parser_find.add_argument('--fc_low_percentile', type=float, default=25,
                             help='Low percentile for fold change (default: 25).')
    parser_find.add_argument('--corr_high_percentile', type=float, default=75,
                             help='High percentile for correlation (default: 75).')
    parser_find.add_argument('--corr_low_percentile', type=float, default=25,
                             help='Low percentile for correlation (default: 25).')
    parser_find.add_argument('--chroms', nargs='+', required=True,
                             help='Chromosomes to process (e.g., chr20).')
    parser_find.set_defaults(func=find_regions_main)

    # Subcommand: visualize_tracks
    parser_visualize = subparsers.add_parser(
        'visualize_tracks',
        help='Visualize genomic tracks.',
        description='Create visualizations of genomic tracks using specified methods.'
    )
    parser_visualize.add_argument('--input_files', nargs='+', required=True,
                                  help='Input BedGraph files to visualize.')
    parser_visualize.add_argument('--output_file', required=True,
                                  help='Output visualization file (e.g., PNG, HTML).')
    parser_visualize.add_argument('--method', choices=['pyGenomeTracks', 'plotly'], required=True,
                                  help='Visualization method to use.')
    parser_visualize.add_argument('--chroms', nargs='+', required=True,
                                  help='Chromosomes to visualize (e.g., chr20).')
    parser_visualize.add_argument('--region_info', nargs=3, required=True, metavar=('CHROM', 'START', 'END'),
                                  help='Region to visualize in the format: CHROM START END (e.g., chr20 1000000 2000000).')
    parser_visualize.add_argument('--colors', nargs='+',
                                  help='Colors for the tracks (optional).')
    parser_visualize.set_defaults(func=visualize_main)

    # Subcommand: pipeline
    parser_pipeline = subparsers.add_parser(
        'pipeline',
        help='Run the full pipeline.',
        description='Run all steps of the LocalFinder pipeline sequentially.'
    )
    # Define necessary arguments for pipeline
    parser_pipeline.add_argument('--input_files', nargs='+', required=True,
                                 help='Input BigWig files to process.')
    parser_pipeline.add_argument('--output_dir', type=str, required=True,
                                 help='Output directory for all results.')
    parser_pipeline.add_argument('--chrom_sizes', type=str, required=True,
                                 help='Path to the chromosome sizes file.')
    parser_pipeline.add_argument('--bin_size', type=int, default=200,
                                 help='Size of each bin for binning tracks (default: 200bp)')
    parser_pipeline.add_argument('--method', type=str, default='localPearson_and_FC',
                                 help='Method for calculate_correlation_FC (default: localPearson_and_FC)')
    parser_pipeline.add_argument('--method_params', type=str, default='{}',
                                 help='Method-specific parameters in JSON format')
    parser_pipeline.add_argument('--bin_number_of_window', type=int, default=11,
                                 help='Bin number of window (default: 11)')
    parser_pipeline.add_argument('--step', type=int, default=1,
                                 help='Step size for sliding window (default: 1)')
    parser_pipeline.add_argument('--fc_high_percentile', type=float, default=75,
                                 help='Percentile threshold for high FC (default: 75)')
    parser_pipeline.add_argument('--fc_low_percentile', type=float, default=25,
                                 help='Percentile threshold for low FC (default: 25)')
    parser_pipeline.add_argument('--corr_high_percentile', type=float, default=75,
                                 help='Percentile threshold for high correlation (default: 75)')
    parser_pipeline.add_argument('--corr_low_percentile', type=float, default=25,
                                 help='Percentile threshold for low correlation (default: 25)')
    parser_pipeline.add_argument('--chroms', nargs='+', default=None,
                                 help='List of chromosomes to process (default: all)')
    parser_pipeline.set_defaults(func=run_pipeline)

    # Parse the arguments
    args = parser.parse_args()

    # Execute the appropriate function based on the subcommand
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()