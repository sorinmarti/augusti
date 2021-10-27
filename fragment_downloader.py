import argparse
import csv
import shutil
from pathlib import Path
import requests
import os.path

# Create the parser
my_parser = argparse.ArgumentParser(prog='FragLoader',
                                    description='Download IIIF fragments from a CSV file')

# Add the arguments
my_parser.add_argument('csv_file',
                       metavar='CSV-File',
                       type=str,
                       help='the file to extract the download urls from')

my_parser.add_argument('url_column',
                       metavar='URL-Column',
                       type=int,
                       help='The column of the csv containing the urls')

my_parser.add_argument('--delimiter',
                       default='\t',
                       type=str,
                       )

my_parser.add_argument('--condition-column',
                       default=-1,
                       type=int,
                       )

my_parser.add_argument('--condition-value',
                       default='',
                       type=str,
                       )

my_parser.add_argument('--output-folder',
                       default='output',
                       type=str,
                       )

my_parser.add_argument('--file-name-column',
                       default=None,
                       type=str,
                       )

my_parser.add_argument('-i0', '--ignore-first-line',
                       action='store_true')

# Execute the parse_args() method
args = my_parser.parse_args()

# Check if given csv-file exists
p = Path(args.csv_file)
if p.exists() and p.is_file():
    # File exists.
    # Read the file as csv
    with open(p, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=args.delimiter)
        # Show the user a sample of their urls
        print("These are examples of download urls:")
        csv_list = list(csv_reader)
        example_end = 5
        total_length = len(csv_list)
        if total_length < 5:
            example_end = total_length - 1
        for row in csv_list[1:example_end]:
            print('Ex.:', row[args.url_column])

        # Show the user a sample of his conditions
        if args.condition_column >= 0:
            print("These are examples of your conditions:")
            for row in csv_list[1:example_end]:
                print('Ex.:', row[args.condition_column])

        u_input = input("Is this correct? [Y/n]")
        if u_input == '' or u_input.lower()=='y':
            # Check if output folder exists
            if not os.path.exists(f"./{args.output_folder}"):
                os.makedirs(f"./{args.output_folder}")

            processed_line = 0
            for row in csv_list:
                if (args.ignore_first_line and processed_line > 0) or (not args.ignore_first_line):
                    # Download urls (ignore lines with less than 5 chars. Can't be an url...)
                    if len(row[args.url_column]) > 5:
                        # Line is valid to download. If a condition column is set: check now
                        download_image = True
                        if args.condition_column >= 0:
                            if args.condition_value not in row[args.condition_column]:
                                download_image = False
                                print(f'Skipped b/c of condition: {row[args.url_column]}')

                        if download_image:
                            r = requests.get(row[args.url_column], stream=True)
                            if r.status_code == 200:
                                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                                r.raw.decode_content = True
                                # Open a local file with wb ( write binary ) permission.
                                prefix = ""
                                if args.file_name_column is not None:
                                    prefix = args.file_name_column + "_"
                                with open(f"./{args.output_folder}/{prefix}{processed_line}.jpg", 'wb') as f:
                                    shutil.copyfileobj(r.raw, f)
                                    print(f'Sucessfully downloaded: {row[args.url_column]}')
                            else:
                                my_parser.error(f'Image Couldn\'t be retreived: {row[args.url_column]}')
                processed_line += 1
        else:
            my_parser.error('Script aborted.')
else:
    my_parser.error(f'CSV file does not exist: {p}')
