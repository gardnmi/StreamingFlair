import praw
import datetime
import time
import os
import HTMLParser
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RedditCFB.settings')
from commentfilter.models import Comment, Post, Flair, Parent, Subreddit
# This is the imports specifically for the long_running.py
import logging
import socket
import sys
from generate_db import my_long_running_process
 
lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
try:
    lock_id = "gardnmi.generate_db"   # this should be unique. using your username as a prefix is a convention
    lock_socket.bind('\0' + lock_id)
    logging.debug("Acquired lock %r" % (lock_id,))
except socket.error:
    # socket already locked, task must already be running
    logging.info("Failed to acquire lock %r" % (lock_id,))
    sys.exit()
 
my_long_running_process()