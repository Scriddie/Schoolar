#! /usr/bin/python3
import logging
import os
import sys
parent_dir = os.path.dirname(os.path.realpath(__file__))
# TODO somehow logging does not work!
logging.basicConfig(filename=parent_dir+'/log.txt',
                    filemode='a',
                    level=logging.INFO)
sys.path.insert(0, parent_dir)
logging.info(sys.path[0])
from main import app as application
application.secret_key = 'anything you wish'
