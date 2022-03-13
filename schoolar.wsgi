#! /usr/bin/python3
import logging
import os
import sys
logging.basicConfig(stream=sys.stderr)
file_path = os.path.realpath(__file__)
sys.path.insert(0, file_path)
logging.info(sys.path[0])
from schoolar import app as application
application.secret_key = 'anything you wish'
