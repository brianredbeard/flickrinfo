#!/usr/bin/env python

# flickrinfo.py - A utility to retrieve information from the flickr api
# Copyright (C) 2017 Brian 'redbeard' Harrington
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

import click

from envparse import Env

import flickrapi
from flickrapi.exceptions import FlickrError

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

env = Env(
    FLICKR_API_KEY=str,
    FLICKR_API_SECRET=str,
)

# We will search for flickr api keys in the file ~/.flickr_api
env.read_envfile(os.path.join(os.path.expanduser('~'), '.flickr_api'))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--api-key',
              help='Flickr API key',
              default=env.str('FLICKR_API_KEY'))
@click.option('--api-secret',
              help='Flickr API secret',
              default=env.str('FLICKR_API_SECRET'))
@click.argument('files',
                metavar='filename',
                nargs=-1)
def main(api_key, api_secret, files):
    """A tool to retrieve flickr photo metadata"""

    # The click module allows zero arguments as being valid, this isn't the
    # behavior that I want for this.
    if len(files) == 0:
        print("No filename(s) supplied.  Exiting.")
        sys.exit(1)

    # Create a handle to the flickr api
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

    # Get a list of all current licenses known/handled by flickr
    licenses = flickr.photos.licenses.getInfo()['licenses']['license']

    # Iterate over all files provided as arguments. It would be nicer to
    # flickr if these were bundled into one call, but for readability sake
    # we're doing it this way.
    for filename in files:
        # Strip the filename from any other path components
        filename = os.path.basename(filename)

        # There is magic in flickr's filenames, retrieve just the filename and
        # the process these values into meaning.
        photofile, jpg = os.path.splitext(filename)

        # Create an array based on the flickr filename (note: these filenames
        # are the defaults rendered by their download mechanism).  The
        # components of the array are as follows:
        # photoarr[0] = photo id
        # photoarr[1] = photo hash
        # photoarr[2] = photo size
        photoarr = photofile.split("_")

        # Retrieve the photo metadata from the API
        try:
            photo = flickr.photos.getinfo(photo_id=photoarr[0])
        except FlickrError, e:
            print('Photo ID {} could not be retrieved:\n{}\n'
                  .format(photoarr[0], e))
            continue

        # The structure returned back is as follows (as of 2017-01-12):
        # {
        # "photo": {
        #   "id": "9460232742",
        #   "secret": "0c2a8d69e0",
        #   "server": "7325",
        #   "farm": 8,
        #   "dateuploaded": "1481101200",
        #   "isfavorite": 0,
        #   "license": 7,
        #   "safety_level": 0,
        #   "rotation": 0,
        #   "originalsecret": "6841037a3a",
        #   "originalformat": "jpg",
        #   "owner": {
        #     "nsid": "44494372@N05",
        #     "username": "NASA on The Commons",
        #     "realname": "",
        #     "location": "",
        #     "iconserver": "1584",
        #     "iconfarm": 2,
        #     "path_alias": "nasacommons"
        #   },
        #   "title": {
        #     "_content": "Apollo 17 Night Launch"
        #   },
        #   "description": {
        #     "_content": "Liftoff of the Apollo 17 Saturn V Moon Rocket..."
        #   },
        #   "visibility": {
        #     "ispublic": 1,
        #     "isfriend": 0,
        #     "isfamily": 0
        #   },
        #   "dates": {
        #     "posted": "1481101200",
        #     "taken": "1972-12-07 00:00:00",
        #     "takengranularity": 0,
        #     "takenunknown": 0,
        #     "lastupdate": "1481117156"
        #   },
        #   "views": "51653",
        #   "editability": {
        #     "cancomment": 0,
        #     "canaddmeta": 0
        #   },
        #   "publiceditability": {
        #     "cancomment": 0,
        #     "canaddmeta": 0
        #   },
        #   "usage": {
        #     "candownload": 1,
        #     "canblog": 0,
        #     "canprint": 0,
        #     "canshare": 1
        #   },
        #   "comments": {
        #     "_content": 0
        #   },
        #   "notes": {
        #     "note": []
        #   },
        #   "people": {
        #     "haspeople": 0
        #   },
        #   "tags": {
        #     "tag": [
        #       {
        #         "id": "44489032-9460232742-1381796",
        #         "author": "44494372@N05",
        #         "authorname": "NASA on The Commons",
        #         "raw": "Apollo 17",
        #         "_content": "apollo17",
        #         "machine_tag": 0
        #       },
        #       {
        #         "id": "44489032-9460232742-1290920",
        #         "author": "44494372@N05",
        #         "authorname": "NASA on The Commons",
        #         "raw": "Night Launch",
        #         "_content": "nightlaunch",
        #         "machine_tag": 0
        #       },
        #       {
        #         "id": "44489032-9460232742-3044859",
        #         "author": "44494372@N05",
        #         "authorname": "NASA on The Commons",
        #         "raw": "Saturn V Rocket",
        #         "_content": "saturnvrocket",
        #         "machine_tag": 0
        #       }
        #     ]
        #   },
        #   "urls": {
        #     "url": [
        #       {
        #        "type": "photopage",
        #        "_content": "https://www.flickr.com/photos/nasacommons/946..."
        #       }
        #     ]
        #   },
        #   "media": "photo"
        # },
        # "stat": "ok"
        # }

        # Extract useful info from the response
        username = photo['photo']['owner']['username']
        realname = photo['photo']['owner']['realname']
        title = photo['photo']['title']['_content']
        url = photo['photo']['urls']['url'][0]['_content']
        for l in licenses:
            if l['id'] == str(photo['photo']['license']):
                license = l
                break
            else:
                license = None
        print(
            '\nUsername: {}\nRealname: {}\nTitle:    {}\nURL:      {}\n'
            .format(username, realname, title, url))

        print(
            '\n{} by {} ({})\n'
            .format(title, realname, license['name']))

if __name__ == '__main__':
    main()
