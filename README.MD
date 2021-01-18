# 🐦 twim
i created this tool to automate the process of video editing for my twitter working timelapse.

## What it does?
1- create a 1min video timelapse from a long video 

2- add a music track to the video

3- calculate total pomodoro sessions

4- tweet to my account  using twitter API

## Usage

1. Create a file hidden file named .env in the `/src` directory and add your twitter api credentials
    <pre>
    consumer_key='YOUR_KEY_HERE'`
    consumer_secret='YOUR_KEY_HERE'
    access_token='YOUR_KEY_HERE'
    access_token_secret='YOUR_KEY_HERE'</pre>

2. Run the script
    <pre>Usage: python3 main.py -i < inputfile > -d < day ></pre>

    **inputfile**: is the long video in MP4 format

    **day**: the current working day number

-> if you want to merge two video streams 
    <pre>Usage: python3 merge.py -i < file1 > -c < file2 ></pre>

    **file1,file2**: is the long video in MP4 format


## Requirements
- Python3
- Pip3

## Useful tip
<pre>create an alias to run the script</pre>
