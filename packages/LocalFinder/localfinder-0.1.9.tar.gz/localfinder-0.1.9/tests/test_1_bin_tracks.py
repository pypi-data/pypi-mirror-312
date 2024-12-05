import unittest
import os
import argparse
from LocalFinder.commands.bin_tracks import main as bin_tracks_main


class TestBinTracks(unittest.TestCase):
    def test_bin_tracks(self):
        # Input files (list of two files)
        input_files = [
            'tests/data/E071-H3K4me1.pval.signal.bigwig',
            'tests/data/E100-H3K4me1.pval.signal.bigwig'
        ]

        # Create output directory using os
        output_dir = 'tests/data_bin_tracks'
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

        # Corresponding output files in tests/data/bin_tracks
        output_files = [
            os.path.join(output_dir, 'E071-H3K4me1.pval.signal.chr20.binSize1000000.bedgraph'),
            os.path.join(output_dir, 'E100-H3K4me1.pval.signal.chr20.binSize1000000.bedgraph')
        ]
        chrom_sizes = 'tests/annotations/hg19.chrom.sizes'  # Path to the chromosome sizes file

        args = argparse.Namespace(
            input_files=input_files,
            output_files=output_files,
            bin_size=1000000,
            chrom_sizes=chrom_sizes,
            chroms=['chr20']  # Specify the chromosome(s) to process
        )

        # Run the command
        bin_tracks_main(args)

        # Check that output files exist
        for output_file in output_files:
            self.assertTrue(os.path.exists(output_file))
            # Additional checks on each output file can be added here

            # For example, verify that the output only contains data for 'chr20'
            with open(output_file, 'r') as f:
                for line in f:
                    chrom = line.strip().split('\t')[0]
                    self.assertEqual(chrom, 'chr20', f"Chromosome {chrom} found in output, expected 'chr20'.")

    # @classmethod
    # def tearDownClass(cls):
    #     # Remove the generated output files after tests
    #     output_files = [
    #         'tests/data/bin_tracks/E071-H3K4me1.pval.signal.chr20.binSize1000000.bedgraph',
    #         'tests/data/bin_tracks/E100-H3K4me1.pval.signal.chr20.binSize1000000.bedgraph'
    #     ]
    #     for output_file in output_files:
    #         if os.path.exists(output_file):
    #             os.remove(output_file)


if __name__ == '__main__':
    unittest.main()
