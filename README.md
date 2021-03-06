# Augusti Toolset
This is a temporary repository to keep the scripts for the augusti seminar.

## Data file
You'll need a current data file with the annotation metadata. You can download it with
your augusti.freizo.org login. In the following examples it is assumed that the file is 
named 'annos.tsv' and resides in the same folder as the following scripts.

## fragment_downloader.py
This script allows a user to download images (or any files for that matter) which are listed in a
comma separated file. The script allows to define a condition column and value which determines if a
line in the csv file gets downloaded. The user can choose to ignore the first line and set an output
directory for the downloaded images which will be created if it does not exist. File names are numbered
by default but a user can set the filename-column to derive the filename from.
**Note**: Column index starts at 0.

**Example**: `python fragment_downloader.py -i0 data.csv 3`

--> Downloads the urls saved in column 3 of the file 'data.csv' starting from the second line.

**Example**: `python fragment_downloader.py --delimiter ; --condition-column 4 --condition-value foo data.csv 3`

--> Downloads the urls saved in column 3 of the file 'data.csv' if the column 4 contains the value 'foo'.
    The file is delimited by semicolons.

**Example**: `python fragment_downloader.py -h`

--> Prints a detailed help text.

## stacked_bars_textannos.py
This script creates a stacked bargraph (see file 'stacked.html') with the Bokeh library.

**Usage**: `python stacked_bars_textannos.py`

## Use the downloaded images with Orange
- Download Orange at https://orangedatamining.com/
- Download the data.tsv file from https://augusti.freizo.org/curator/annosearch.cgi?tsv=1 (Login first)
- Download the needed images with the `fragment_downloader.py` script
- Open the OWS file from this repository with Orange
- Change 'Import Images' to point to your image directory.
- Look at the Hierarchical Clustering

## Intro into Orange Image Analytics
- Clustering: https://www.youtube.com/watch?v=Iu8g2Twjn9U (4:40)
- Classification: https://www.youtube.com/watch?v=lvgx62a8XQk (4:05)
