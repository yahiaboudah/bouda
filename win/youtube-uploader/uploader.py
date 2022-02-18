#!/usr/bin/python


# ---------------------- ------- IMPORTS ---------------------------------
# ------------------------------------------------------------------------
import http.client as httplib
import httplib2
import os
import random
import sys
import time
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


#---------------------- CONSTANTS ---------------------------------------
#-------------------------------------------------------------------------

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see this:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"


# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")



# -------------------------------- FUNCTIONS -------------------------------
# -----------------------------------------------------------------------------

class YoutubeOptions():
    def __init__(self, config):

        self.auth_host_name = "localhost"
        self.auth_host_port = [8080, 8090]
        self.noauth_local_webserver = False
        self.logging_level = "ERROR"

        self.file = config["file"]
        self.title = config["title"]
        self.description = config["description"]
        self.category = config["category"]
        self.privacyStatus = config["privacyStatus"]
        self.keywords = config["keywords"]


class Uploader():

    def __init__(self, options, user_channel, client_app):
        self.youtube = None
        self.options = options
        self.user_channel = user_channel
        self.client_app = client_app
    
    # ESTABLISH HANDSHAKE AND GET OUR YOUTUBECHANNEL VARIABLE
    # THROUGH OUR CLIENT SECRET AND THE USER CREDENTIAL
    def get_authenticated_service(self):


        # DEFINE FLOW
        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
            scope=YOUTUBE_UPLOAD_SCOPE,
            message=MISSING_CLIENT_SECRETS_MESSAGE)

        # DEFINE STORAGE:
        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()

        # OPEN THE BROWSER AND GET USER CREDENTIALS IF NO FILE EXISTS
        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage, self.options)

        
        # RETURN OUR BUILD WITH CREDS, YOUTUBE API, EVERYTHING ELSE
        self.youtube =  build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            http=credentials.authorize(httplib2.Http()))

    # DO SOMETHING WITH OUR BUILD (YOUTUBECHANNEL), UPLOAD..etc
    def initialize_upload(self):
    
        # DEFINE OUR UPLOAD OPTIONS:
        tags = None
        options = self.options
        if options.keywords:
            tags = options.keywords.split(",")

        body=dict(
            snippet=dict(
            title=options.title,
            description=options.description,
            tags=tags,
            categoryId=options.category
            ),
            status=dict(
            privacyStatus=options.privacyStatus
            )
        )

        # PASS OUR OPTIONS TO THE INSERT, AND GET OUR POST REQUEST
        insert_request = self.youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(options.file, chunksize=-1 , resumable=True)
        )

        #PASS THE REQUEST TO THE UPLOAD FUNCTION TO ACTUALLY UPLOAD
        self.resumable_upload(insert_request)

    def resumable_upload(self, insert_request):
        
        response = None
        error = None
        retry = 0
        
        while response is None:
            
            try:
                print( "Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print ("Video id '%s' was successfully uploaded." % response['id'])
                    else:
                        exit("The upload failed with an unexpected response: %s" % response)
            except HttpError as e:
                if (e.resp.status in RETRIABLE_STATUS_CODES):
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS as e:
                error = "A retriable error occurred: %s" % e

            if error is not None:
                print(error)
                retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            # WAIT BEFORE TRYING AGAIN
            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)
    
    def upload(self):
        
        print(self.options.file)
        if not os.path.exists(self.options.file):
            print("Please specify a valid file.")
            return

        # THIS SETS OUR YOUTUBE CONTROLLER VARIABLE
        self.get_authenticated_service()

        try:
            start_time = time.time()
            self.initialize_upload()
            print("upload time: ", round(time.time()-start_time), "seconds")

        except HttpError as e:
            print( "An HTTP error %d occurred:\n%s" % (e.resp.status, "e.content"))
