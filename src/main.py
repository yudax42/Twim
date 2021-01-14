import sys, getopt
import ffmpeg

#inputs
inputfile = ''
day = ''


#Parsing the arguments
def parseArgs(argv):
    try:
        opts, args = getopt.getopt(argv,"i:d:")
    except getopt.GetoptError:
        print 'main.py -i <inputfile> -d <day>'
        sys.exit(2)
    if len(opts) != 2:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-i':
            inputfile = arg
        elif opt == '-d':
            day = arg


def main(argv):
    parseArgs(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
