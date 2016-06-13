#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line sample for the Google Prediction API

Command-line application that trains on your input data. This sample does
the same thing as the Hello Prediction! example. You might want to run
the setup.sh script to load the sample data to Google Storage.

Usage:
  $ python prediction_service.py "bucket/object" "model_id" "project_id" "my-xxxxx.json"

You can also get help on all the command-line flags the program understands
by running:

  $ python prediction_service.py --help

To get detailed log output run:

  $ python prediction_service.py --logging_level=DEBUG
"""
from __future__ import print_function

__author__ = ('jcgregorio@google.com (Joe Gregorio), '
              'marccohen@google.com (Marc Cohen)')

import argparse
import os
from pprint import pprint as pp
import sys
import time

sys.path.append( os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib') )

import httplib2
from apiclient import discovery
from apiclient import sample_tools
from oauth2client import client
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from oauth2client import tools

# Time to wait (in seconds) between successive checks of training status.
SLEEP_TIME = 10
scopes=['https://www.googleapis.com/auth/prediction','https://www.googleapis.com/auth/devstorage.read_only']

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('object_name',
    help='Full Google Storage path of csv data (ex bucket/object)')
argparser.add_argument('model_id',
    help='Model Id of your choosing to name trained model')
argparser.add_argument('project_id',
    help='Model Id of your choosing to name trained model')
argparser.add_argument('credential',
    help='Specify json file name of Service Account Credential')

def print_header(line):
  '''Format and print header block sized to length of line'''
  header_str = '='
  header_line = header_str * len(line)
  print('\n' + header_line)
  print(line)
  print(header_line)

def main(argv):
  # create flags
  parents=[argparser]
  parent_parsers = [tools.argparser]
  parent_parsers.extend(parents)
  parser = argparse.ArgumentParser(
      description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=parent_parsers)
  flags = parser.parse_args(argv[1:])

  credential_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), flags.credential)

  credentials = ServiceAccountCredentials.from_json_keyfile_name(
    credential_file, scopes=scopes)

  http = credentials.authorize(http = httplib2.Http())
  service = discovery.build('prediction', 'v1.6', http=http)

  try:
    # Get access to the Prediction API.
    papi = service.trainedmodels()

    # List models.
    print_header('Fetching list of first ten models')
    result = papi.list(maxResults=10, project=flags.project_id).execute()
    print('List results:')
    pp(result)

    # Start training request on a data set.
    print_header('Submitting model training request')
    body = {'id': flags.model_id, 'storageDataLocation': flags.object_name}
    start = papi.insert(body=body, project=flags.project_id).execute()
    print('Training results:')
    pp(start)

    # Wait for the training to complete.
    print_header('Waiting for training to complete')
    while True:
      status = papi.get(id=flags.model_id, project=flags.project_id).execute()
      state = status['trainingStatus']
      print('Training state: ' + state)
      if state == 'DONE':
        break
      elif state == 'RUNNING':
        time.sleep(SLEEP_TIME)
        continue
      else:
        raise Exception('Training Error: ' + state)

      # Job has completed.
      print('Training completed:')
      pp(status)
      break

    # Describe model.
    print_header('Fetching model description')
    result = papi.analyze(id=flags.model_id, project=flags.project_id).execute()
    print('Analyze results:')
    pp(result)

    # Make some predictions using the newly trained model.
    print_header('Making some predictions')
    for sample_text in ['mucho bueno', 'bonjour, mon cher ami']:
      body = {'input': {'csvInstance': [sample_text]}}
      result = papi.predict(
        body=body, id=flags.model_id, project=flags.project_id).execute()
      print('Prediction results for "%s"...' % sample_text)
      pp(result)

    # Delete model.
    print_header('Deleting model')
    result = papi.delete(id=flags.model_id, project=flags.project_id).execute()
    print('Model deleted.')

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize.')


if __name__ == '__main__':
    main(sys.argv)
