#! /usr/bin/python3
import logging
import os
import sys
parent_dir = os.path.realpath(__file__)+'/..'
logging.basicConfig(filename=parent_dir+'log.txt',
                    filemode='a',
                    level=logging.INFO)
sys.path.insert(0, parent_dir)
logging.info(sys.path[0])
from schoolar import app as application
application.secret_key = 'anything you wish'
