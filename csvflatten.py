#!/usr/bin/python3
# csvflattener.py
# Version: 0.5
# Author: lukahn
# Description: Simple script to flatten multi-line cell CSV files by replacing unquoted newline strings with a substitute
# Limitations: Non-unicode characters aren't displayed in Pycharm terminals or Excel correctly, but are saved correctly to a file
#              Requires Python 3
# Improvements: Complete
# Changelog: 0.1: Initial release. Replaces full quoted CSV files with a single skip
#            0.2: Added argument parsing and proper CSV support, including support for more than one multi-line in a cell, and multiple cells
#            0.3: Added debugging
#            0.4: Fixed opening a file from stdin
#            0.5: Added support for Windows and Linux line feeds
import sys
import csv
import os
import logging
import traceback
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-d", "--debug",                    dest="debug",       help="Enables debugging output.",                                                                        default=False,                          action="store_true")
parser.add_argument("-f", "--file", "--filename",       dest="filename",    help="Reads input from FILE, instead of stdin.",                                                                          metavar="file")
parser.add_argument("-o", "--out", "--output",          dest="output",      help="Saves output to a FILE, instead of stdout.",                                                                        metavar="file")
parser.add_argument("-a", "--append",                   dest="append",      help="When combined with the -o flag, appends output to the FILE, instead creating a new file.",         default=False,                          action="store_true")
parser.add_argument("-r", "--replace", "--replacement", dest="replacement", help="Specifies the replacement characters to replace newlines when flattening (default: %(default)s).", default="\" \\\\n \"", metavar="replacement") #Actually use \\n
parser.add_argument("-D", "--delim", "--delimiter",     dest="delimiter",   help="Specifies the CSV delimiter character (default: %(default)s).",                                    default=",",     metavar="delimiter")
parser.add_argument("-q", "--quote",                    dest="quotechar",   help="Specifies the CSV quote character (default: %(default)s).",                                        default="\"",    metavar="quotechar")
parser.add_argument("-Q", "--quoting",                  dest="quoting",     help="Specifies the CSV quoting type. Choices are (%(choices)s) (default: %(default)s).",                default="ALL",                                              choices=["NONE", "NONNUMERIC", "MINIMAL", "ALL"])
parser.add_argument("-v", "--verbose",                  dest="verbose",     help="Prints the result to stdout, even if a filename is specified.",                                    default=False,                          action="store_true")

args = parser.parse_args()


#Set variables
##Sets the logger for debug if set

if args.debug:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.debug("Setting the variables")

##Get the filename (we'll set it to be a file later on if needed)
input_filename = sys.stdin

##Get the replacement string. Converting the replacement from the help default to properly format the backslshes.
replacement = " \\n "
if not args.replacement == "\" \\\\n \"":
    replacement = args.replacement
logging.debug("Replacement set to: " + replacement)

##Initialise the output list
output_list = []
logging.debug("Initialised the output list: " + str(output_list))

##Dict to convert the quoting type to the format expected
quoting_dict={"NONE":csv.QUOTE_NONE,
             "NONNUMERIC":csv.QUOTE_NONNUMERIC,
             "MINIMAL":csv.QUOTE_MINIMAL,
             "ALL":csv.QUOTE_ALL}
logging.debug("Initialised the quoting dict: " + str(quoting_dict))

##Sets whether to write or append to a file
if args.output is not None:
    write_type="w+"
    if args.append:
        write_type="a+"
    logging.debug("Set the write type to: " + str(write_type))



#Open the file, and make the substitution
logging.debug("Starting the file open procedure")
# with open(input_filename, newline='') as input_file:
try:
    if args.filename is not None:
        logging.debug("Opening the file: " + args.filename)
        input_filename = open(args.filename, newline='')
    else:
        logging.debug("Waiting for input from stdin")
    input_list = csv.reader(input_filename, delimiter=args.delimiter, quotechar=args.quotechar, quoting=quoting_dict[args.quoting])
    for row in input_list:
        logging.debug("Row contents: " + str(row))
        new_row = []
        for column in row:
            logging.debug("Column contents: " + str(column))
            if "\r\n" in column:
                column = column.replace("\r\n", replacement)
                logging.debug("Column (CRLF) replaced. New contents: " + str(column))
            elif "\n" in column:
                column = column.replace("\n", replacement)
                logging.debug("Column (LF) replaced. New contents: " + str(column))
            new_row.append(column)
            logging.debug("Added column to the new row. Size: " + str(len(new_row)))
        output_list.append(new_row)
    logging.debug("Finished the file open procedure")
    if args.filename is not None:
        input_filename.close()
except Exception:
    traceback.print_exc()
    input_filename.close()
    os._exit(1)

#Write the output
logging.debug("Starting the file writing procedure")
if args.output is not None:
    logging.debug("Writing to file: " + str(args.output))
    with open(args.output, write_type, newline='') as output_file:
        output_writer = csv.writer(output_file, delimiter=args.delimiter, quotechar=args.quotechar, quoting=quoting_dict[args.quoting], lineterminator=os.linesep)
        for row in output_list:
            logging.debug("Final row contents: " + str(row))
            if args.verbose:
                logging.debug("Writing to terminal")
                terminal_writer = csv.writer(sys.stdout, delimiter=args.delimiter, quotechar=args.quotechar, quoting=quoting_dict[args.quoting], lineterminator=os.linesep)
                terminal_writer.writerow(row)
            logging.debug("Writing to file")
            output_writer.writerow(row)
else:
    logging.debug("Writing to terminal only")
    terminal_writer = csv.writer(sys.stdout, delimiter=args.delimiter, quotechar=args.quotechar, quoting=quoting_dict[args.quoting], lineterminator=os.linesep)
    for row in output_list:
        terminal_writer.writerow(row)
logging.debug("Finished the file writing procedure")
logging.debug("Quit")
