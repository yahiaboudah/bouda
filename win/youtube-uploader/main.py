from uploader import *

data = {
    "file": "small_sample.mp4",
    "title": "SOVA AND KILLJOY VIBING SMALL VERSION",
    "description": "sova and killjoy lil dance THE SAMALL SAMPLE",
    "category": 22,
    "privacyStatus": VALID_PRIVACY_STATUSES[0],
    "keywords": "Video keywords, comma separated"
}

uploader = Uploader(YoutubeOptions(data), "user_channel", "client_app")
uploader.upload()