# flickrinfo.py

# About
Anyone who's seen my presentations knows that I have a very stylized look and
feel to my slides.  Part of the way that I do this is through aggressive use of
creative commons licensed photo graphs.  Flickr and
https://search.creativecommons.org make this very easy to find said content.

Just having the content though does not mean that you are abiding by the
license of using the content.  Most creative commons licenses require
attribution.  This tool makes it easy to do that.

# Prerequisites
In order to make this as friendly for other people to use I (ironically) added
more module dependencies.  This was to better handle use of environment
variables and configuration files (and to be cross platform).  In my own
environment I use a secure password store.  Your milage may vary.

The following python modules must be installed:
  - [click](https://pypi.python.org/pypi/click)
  - [envparse](https://pypi.python.org/pypi/envparse)
  - [flickrapi](https://pypi.python.org/pypi/flickrapi)

# Usage
When retreiving an image from Flickr, save it using the original filename.
Then, later, if you need to go back and find out who that content belonged to
run the following:

```
$ flickrinfo.py 9460232742_6841037a3a_o.jpg

Username: NASA on The Commons
Realname: 
Title:    Apollo 17 Night Launch
URL:      https://www.flickr.com/photos/nasacommons/9460232742/


Apollo 17 Night Launch by  (No known copyright restrictions)

```

It should be noted that the file is merely being used to supply metadata to the
API.  As such you don't even need the file locally (though that would be
silly).  On the other hand, if you just want to test this out, here are some
good files to look at:

  - `9983396456_35f654cc6e_o.jpg`
  - `4896792758_e6d4e91300_o.jpg`
  - `3378098505_59328624e7_o.jpg`

# Bugs
  - If "RealName" is not populated, in the friendly string fill use username
    instead.

# License
This tool is licensed under the Affero GPL v3.  See [LICENSE] for details.
Using this tool will also require other python modules not distributed with the
tool as noted in 'Prerequisites'.
