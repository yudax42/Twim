import sys, getopt
import ffmpeg

#inputs

#Parsing the arguments
def parseArgs(argv):
    try:
        opts, args = getopt.getopt(argv,"i:d:")
    except getopt.GetoptError:
        print('Usage: main.py -i <inputfile> -d <day>')
        sys.exit(2)
    if len(opts) != 2:
        print('Usage: main.py -i <inputfile> -d <day>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-i':
            inputfile = arg
        elif opt == '-d':
            day = arg
    return inputfile, day

#Video processing
def videoInf(inputfile):
    meta = ffmpeg.probe(inputfile)
    duration = round(float(meta['streams'][0]['duration']) / 60)
    print(duration)

def process(inputfile, day):
    print("processing...", inputfile, day)
    videoInf(inputfile)
    #stream = ffmpeg.input(inputfile)
    #audio = stream.audio.filter('-an')
    #stream = ffmpeg.output(audio,stream,'twitter1.mp4')
    #ffmpeg.run(stream)


def main(argv):
    inputfile,day = parseArgs(argv)
    process(inputfile,day)


if __name__ == "__main__":
    main(sys.argv[1:])
