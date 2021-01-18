import sys, getopt
import ffmpeg
import os
os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches >/dev/null 2>&1')


#Parsing the arguments
'''
    parseArgs: returns input files
'''
def parseArgs(argv):
    try:
        opts, args = getopt.getopt(argv,"i:c:")
    except getopt.GetoptError:
        print('Usage: main.py -i <file1> -c <file2>')
        sys.exit(2)
    if len(opts) != 2:
        print('Usage: main.py -i <file1> -c <file2>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-i':
            file1 = arg
        elif opt == '-c':
            file2 = arg
    return file1, file2


#Video processing
'''
    process: merging two streams
'''
def process(file1, file2):
    file_1 = ffmpeg.input(file1)
    file_2 = ffmpeg.input(file2)
    merged = ffmpeg.concat(file_1, file_2)
    merged.output('merged.mp4').run()

def main(argv):
    file1,file2 = parseArgs(argv)
    process(file1,file2)

if __name__ == "__main__":
    main(sys.argv[1:])
