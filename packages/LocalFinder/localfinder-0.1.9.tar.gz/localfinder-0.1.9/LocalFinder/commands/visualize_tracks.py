import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import visualize_tracks, get_plotly_default_colors

def main(args=None):
    parser = argparse.ArgumentParser(description='Visualize genomic tracks.')
    parser.add_argument('--input_files', nargs='+', required=True, help='List of input BedGraph files to visualize.')
    parser.add_argument('--output_file', required=True, help='Output image file (e.g., PNG, SVG, HTML).')
    parser.add_argument('--method', choices=['pyGenomeTracks', 'plotly'], default='pyGenomeTracks',
                        help='Visualization method to use (default: pyGenomeTracks).')
    parser.add_argument('--region_info', nargs=3, metavar=('CHROM', 'START', 'END'),
                        help='Genomic region to plot (e.g., chr1 1000000 2000000).')
    parser.add_argument('--colors', nargs='+', help='List of colors for the tracks.')
    parser.add_argument('--chroms', nargs='+', help='List of chromosomes to process (default: all)')
    args = parser.parse_args(args)

    # Convert region_info to a tuple if provided
    region = None
    if args.region_info:
        chrom = args.region_info[0]
        start = int(args.region_info[1])
        end = int(args.region_info[2])
        region = (chrom, start, end)

    # Adjust output format for plotly
    if args.method == 'plotly':
        if not args.output_file.endswith('.html'):
            args.output_file += '.html'

    # Handle color assignment if no colors are provided
    if not args.colors:
        # Use Plotly's default color sequence for both methods
        args.colors = get_plotly_default_colors(len(args.input_files))

    # Call the visualize_tracks function
    visualize_tracks(
        input_files=args.input_files,
        output_file=args.output_file,
        method=args.method,
        region=region,
        colors=args.colors,
        chroms=args.chroms
    )

    print(f"Track visualization saved to {args.output_file}")

if __name__ == '__main__':
    main()
