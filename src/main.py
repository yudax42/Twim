import sys, getopt
import ffmpeg
from tweet import tweetVideo
import os
os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches >/dev/null 2>&1')

#Parsing the arguments
'''
    parseArgs: returns input file and day from arguments
'''
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
'''
    videoInf: returns video duration in minutes
'''
def videoInf(inputfile):
    meta = ffmpeg.probe(inputfile)
    duration = round(float(meta['streams'][0]['duration']) / 60)
    return duration
'''
    process: converts long video to timelapse
'''
def process(inputfile, day):
    duration = videoInf(inputfile)
    #find and sets presentation timestamps for 1min video
    pts = str(1/duration) + "*PTS"
    stream = ffmpeg.input(inputfile)
    stream = ffmpeg.setpts(stream, pts)
    #merge the stream with music track
    audio = ffmpeg.input('../audio/track1.mp3')
    stream = ffmpeg.output(audio,stream,day+'twim.mp4')
    ffmpeg.run(stream)

def main(argv):
    inputfile,day = parseArgs(argv)
    totalpomo = round(videoInf(inputfile) / 50)
    print("⚙️ processing the video ...")
    process(inputfile,day)
    print("🐦 tweeting...")
    tweetVideo('./'+day+'twim.mp4','📅 '+ day+" - " + str(totalpomo) + " pomodoro sessions\n 50 min each")
    print("✅ Done!")

if __name__ == "__main__":
    main(sys.argv[1:])
