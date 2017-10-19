import argparse
import datetime
import re


def adjust_time(tc, delay):
    tc = datetime.datetime.strptime(tc, '%H:%M:%S,%f')
    td = datetime.timedelta(milliseconds=delay)
    return (tc + td).strftime('%H:%M:%S.%f')[:-3]

def read_file(infile, delay=0):
    outfile_name = infile.name.rsplit('.')[0] + '_out.' + infile.name.rsplit('.')[1]
    outfile = open(outfile_name, "w")
    for line in infile:
        newline = re.sub(r'[0-9]+:[0-9]{0,2}:[0-9]{0,2},[0-9]{0,3}', lambda match: adjust_time(match.group(), delay), line)
        outfile.write(newline)

def main():
    parser = argparse.ArgumentParser(description='Subtitle time adjustment helper')
    parser.add_argument('FILES', type=argparse.FileType('r'), nargs='+', help='One or more .srt files to be adjusted')
    parser.add_argument('-d','--delay', type=int, default=0, help='The number of milliseconds to be added')
    args = parser.parse_args()

    for f in args.FILES:
        read_file(f, args.delay)

if __name__ == "__main__":
    main()
