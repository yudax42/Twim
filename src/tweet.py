import os
import sys
import time

import json
import requests
from decouple import config
from requests_oauthlib import OAuth1


MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'

#twitter api credentials
CONSUMER_KEY = config('consumer_key')
CONSUMER_SECRET = config('consumer_secret')
ACCESS_TOKEN = config('access_token')
ACCESS_TOKEN_SECRET = config('access_token_secret')


oauth = OAuth1(CONSUMER_KEY,
  client_secret=CONSUMER_SECRET,
  resource_owner_key=ACCESS_TOKEN,
  resource_owner_secret=ACCESS_TOKEN_SECRET)


class VideoTweet(object):

  def __init__(self, file_name, msg):
    '''
    Defines video tweet properties
    '''
    self.video_filename = file_name
    self.msg = msg
    self.total_bytes = os.path.getsize(self.video_filename)
    self.media_id = None
    self.processing_info = None


  def upload_init(self):
    '''
    Initializes Upload
    '''
    request_data = {
      'command': 'INIT',
      'media_type': 'video/mp4',
      'total_bytes': self.total_bytes,
      'media_category': 'tweet_video'
    }

    req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)
    media_id = req.json()['media_id']
    self.media_id = media_id


  def upload_append(self):
    '''
    Uploads media in chunks and appends to chunks uploaded
    '''
    segment_id = 0
    bytes_sent = 0
    file = open(self.video_filename, 'rb')

    while bytes_sent < self.total_bytes:
      chunk = file.read(4*1024*1024)
      
      request_data = {
        'command': 'APPEND',
        'media_id': self.media_id,
        'segment_index': segment_id
      }

      files = {
        'media':chunk
      }

      req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, files=files, auth=oauth)

      if req.status_code < 200 or req.status_code > 299:
        sys.exit(0)

      segment_id = segment_id + 1
      bytes_sent = file.tell()

  def upload_finalize(self):
    '''
    Finalizes uploads and starts video processing
    '''

    request_data = {
      'command': 'FINALIZE',
      'media_id': self.media_id
    }

    req = requests.post(url=MEDIA_ENDPOINT_URL, data=request_data, auth=oauth)

    self.processing_info = req.json().get('processing_info', None)
    self.check_status()


  def check_status(self):
    '''
    Checks video processing status
    '''
    if self.processing_info is None:
      return

    state = self.processing_info['state']

    if state == u'succeeded':
      return

    if state == u'failed':
      sys.exit(0)

    check_after_secs = self.processing_info['check_after_secs']
    time.sleep(check_after_secs)


    request_params = {
      'command': 'STATUS',
      'media_id': self.media_id
    }

    req = requests.get(url=MEDIA_ENDPOINT_URL, params=request_params, auth=oauth)
    
    self.processing_info = req.json().get('processing_info', None)
    self.check_status()


  def tweet(self):
    '''
    Publishes Tweet with attached video
    '''
    request_data = {
      'status': self.msg,
      'media_ids': self.media_id
    }

    req = requests.post(url=POST_TWEET_URL, data=request_data, auth=oauth)

def tweetVideo(filename,msg):
    videoTweet = VideoTweet(filename,msg)
    videoTweet.upload_init()
    videoTweet.upload_append()
    videoTweet.upload_finalize()
    videoTweet.tweet()
