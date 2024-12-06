import os
import argparse
from xps_export import xpsexport

def main():
    """
    Command-line interface for the file parser using argparse.
    """
    parser = argparse.ArgumentParser(
        description="Utility for parsing files to XML.")
    parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("output_file", help="Path to the output file.")
    parser.add_argument("--create-plots", action="store_true",
                        help="Generate plots.")
    parser.add_argument("--create-csv", action="store_true",
                        help="Generate CSV files.")

    args = parser.parse_args()

    # Validate input file
    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        return

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    xpsexport.parse_file_to_xml(args.input_file, args.output_file,
                      args.create_plots, args.create_csv)



if __name__ == "__main__":
    main()
    