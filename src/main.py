import sys, getopt
import ffmpeg
from decouple import config
from tweet import tweetVideo

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
    #duration = meta['streams'][0]['duration']
    return duration
def process(inputfile, day):
    print("processing...", inputfile, day)
    
    #duration = videoInf(inputfile)
    #pts = str(1/duration) + "*PTS"
    #print(duration, pts)

    #stream = ffmpeg.input(inputfile)
    #stream = ffmpeg.setpts(stream, pts)
    #audio = ffmpeg.input('../audio/track1.mp3')
    #stream = ffmpeg.output(audio,stream,'twitter1.mp4')
    #ffmpeg.run(stream)

#Tweet
def tweet(day):
    upload_result = api.media_upload('./d013twim.mp4')
    #api.update_status(status="{day}", media_ids=[upload_result.media_id_string])


def main(argv):
    inputfile,day = parseArgs(argv)
    process(inputfile,day)
    tweetVideo('./d013twim.mp4')

if __name__ == "__main__":
    main(sys.argv[1:])
