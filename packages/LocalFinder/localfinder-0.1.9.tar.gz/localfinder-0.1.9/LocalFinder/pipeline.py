import os
import sys
import argparse

from LocalFinder.commands.bin_tracks import main as bin_tracks_main
from LocalFinder.commands.calculate_correlation_FC import main as calc_corr_main
from LocalFinder.commands.find_significantly_different_regions import main as find_regions_main

def run_pipeline(args):
    """
    Run the full LocalFinder pipeline:
    1. Bin tracks
    2. Calculate correlation and fold change
    3. Find significantly different regions
    """
    # Check for required external tools
    from LocalFinder.utils import check_external_tools
    check_external_tools()

    # Create output directories
    os.makedirs(args.output_dir, exist_ok=True)
    bin_output_dir = os.path.join(args.output_dir, 'binned_tracks')
    calc_output_dir = os.path.join(args.output_dir, 'calculated_tracks')
    regions_output_dir = os.path.join(args.output_dir, 'significant_regions')

    os.makedirs(bin_output_dir, exist_ok=True)
    os.makedirs(calc_output_dir, exist_ok=True)
    os.makedirs(regions_output_dir, exist_ok=True)

    # Step 1: Run bin_tracks
    print("Running bin_tracks...")
    bin_output_files = [os.path.join(bin_output_dir, os.path.basename(f) + '.bedgraph') for f in args.input_files]
    bin_args = argparse.Namespace(
        input_files=args.input_files,
        output_files=bin_output_files,
        bin_size=args.bin_size,
        chrom_sizes=args.chrom_sizes,
        chroms=args.chroms
    )
    bin_tracks_main(bin_args)

    # Step 2: Run calculate_correlation_FC
    print("Running calculate_correlation_FC...")
    # Assuming two input files for simplicity
    if len(bin_output_files) < 2:
        print("Need at least two input files for calculate_correlation_FC.")
        sys.exit(1)
    calc_args = argparse.Namespace(
        track1=bin_output_files[0],
        track2=bin_output_files[1],
        method=args.method,
        method_params=args.method_params,
        bin_number_of_window=args.bin_number_of_window,
        step=args.step,
        output_dir=calc_output_dir,
        chroms=args.chroms
    )
    calc_corr_main(calc_args)

    # Step 3: Run find_significantly_different_regions
    print("Running find_significantly_different_regions...")
    # Use the output files from calculate_correlation_FC
    track_FC_file = os.path.join(calc_output_dir, 'tracks_log_Wald_pValue.bedgraph')
    track_correlation_file = os.path.join(calc_output_dir, 'tracks_pearson.bedgraph')
    regions_args = argparse.Namespace(
        track_FC=track_FC_file,
        track_correlation=track_correlation_file,
        output_dir=regions_output_dir,
        min_region_size=args.min_region_size,
        fc_high_percentile=args.fc_high_percentile,
        fc_low_percentile=args.fc_low_percentile,
        corr_high_percentile=args.corr_high_percentile,
        corr_low_percentile=args.corr_low_percentile,
        chroms=args.chroms
    )
    find_regions_main(regions_args)

    print("Pipeline completed successfully.")