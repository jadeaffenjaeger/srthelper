import argparse
import datetime
import re


# change value of single timecode
def adjust_time(tc, delay):
    # convert timestamp to timedelta
    tc = datetime.datetime.strptime(tc, '%H:%M:%S,%f') - datetime.datetime(1900, 1, 1)
    td = datetime.timedelta(milliseconds=delay)

    if (tc + td).days < 0:
        return '-' + str(-(tc + td))[:-3].replace('.', ',')
    return (str(tc + td)[:-3].replace('.', ','))

# parse individual file for timecodes
def read_file(infile, delay=0):
    outfile_name = '.'.join(infile.name.rsplit('.')[:-1]) + '_resync.' + infile.name.rsplit('.')[-1]
    outfile = open(outfile_name, "w")
    for line in infile:
        newline = re.sub(r'[0-9]+:[0-9]{0,2}:[0-9]{0,2},[0-9]{0,3}', lambda match: adjust_time(match.group(), delay), line)
        outfile.write(newline)

def main():
    # Set up command line args
    parser = argparse.ArgumentParser(description='Subtitle time adjustment helper')
    parser.add_argument('FILES', type=argparse.FileType('r'), nargs='+', help='One or more .srt files to be adjusted')
    parser.add_argument('-d','--delay', type=int, default=0, help='The number of milliseconds to be added')
    args = parser.parse_args()

    # Go through supplied files
    for f in args.FILES:
        read_file(f, args.delay)

if __name__ == "__main__":
    main()
