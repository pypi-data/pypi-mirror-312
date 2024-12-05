import argparse
import pandas as pd
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import localPearson_and_FC, localWeightedPearson_and_FC, localSpearman_and_FC, localWeightedSpearman_and_FC, \
    localMI_and_FC


def main(args=None):
    if args is None:
        parser = argparse.ArgumentParser(description='Calculate correlation and fold change between tracks.')
        parser.add_argument('--track1', type=str, required=True, help='Input file for track1 (e.g., track1.bedgraph)')
        parser.add_argument('--track2', type=str, required=True, help='Input file for track2 (e.g., track2.bedgraph)')

        # Adding choices for --method
        parser.add_argument('--method', type=str, choices=[
            'localPearson_and_FC',
            'localWeightedPearson_and_FC',
            'localSpearman_and_FC',
            'localWeightedSpearman_and_FC',
            'localMI_and_FC'
        ], default='localPearson_and_FC',
                            help='Method to use for processing (e.g., localPearson_and_FC). Default is localPearson_and_FC.')

        parser.add_argument('--method_params', type=str, default='{}',
                            help='Method-specific parameters in JSON format (default: {}).')
        parser.add_argument('--bin_number_of_window', type=int, default=11, help='Bin number of window (default: 11)')
        parser.add_argument('--step', type=int, default=1, help='Step size for sliding window (default: 1)')
        parser.add_argument('--output_dir', type=str, default='output', help='Output directory for result files')
        parser.add_argument('--chroms', nargs='+', help='List of chromosomes to process (default: all)')

        # Displaying usage example
        parser.epilog = '''Usage Example:
        localfinder calculate_correlation_FC --track1 track1.bedgraph --track2 track2.bedgraph \
        --method localPearson_and_FC --method_params '{"param1": "value1"}' \
        --bin_number_of_window 11 --step 1 --output_dir ./results --chroms chr1 chr2'''

        args = parser.parse_args()
    else:
        # Args are provided programmatically
        pass  # args are already set

    # Read the input tracks
    track1 = pd.read_csv(args.track1, header=None, sep='\t')
    track1.columns = ['chr', 'start', 'end', 'readNum_1']

    track2 = pd.read_csv(args.track2, header=None, sep='\t')
    track2.columns = ['chr', 'start', 'end', 'readNum_2']

    # Merge the tracks into a single DataFrame
    df = track1.copy()
    df['readNum_2'] = track2['readNum_2']

    # Filter chromosomes if specified
    if args.chroms:
        df = df[df['chr'].isin(args.chroms)]
        if df.empty:
            print(f"No data found for the specified chromosomes: {args.chroms}")
            sys.exit(1)

    # Parse method-specific parameters
    try:
        method_params = json.loads(args.method_params)
    except json.JSONDecodeError as e:
        print(f"Error parsing method_params: {e}")
        return

    # Add common parameters to method_params
    method_params.update({
        'bin_number_of_window': args.bin_number_of_window,
        'step': args.step,
        'output_dir': args.output_dir
    })

    # Map method names to functions
    method_functions = {
        'localPearson_and_FC': localPearson_and_FC,
        'localWeightedPearson_and_FC': localWeightedPearson_and_FC,
        'localSpearman_and_FC': localSpearman_and_FC,
        'localWeightedSpearman_and_FC': localWeightedSpearman_and_FC,
        'localMI_and_FC': localMI_and_FC
    }

    if args.method not in method_functions:
        print(f"Method '{args.method}' is not recognized. Available methods: {list(method_functions.keys())}")
        return

    # Call the selected method
    method_functions[args.method](
        df=df,
        column1='readNum_1',
        column2='readNum_2',
        chroms=args.chroms,
        **method_params
    )


if __name__ == '__main__':
    main()