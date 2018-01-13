# Pixiv Crawler

**VERY IMPORTANT: USE THIS TOOL ON YOUR OWN RESPONSIVIRITY**

## What is this?

* This is a pixiv illustration crawler. (This tool uses non official APIs. This may cause regulation violation. Use on your own risk)

* This tool skips following images by default:
    * Low score illustrations
    * Explicit(R18) illustrations
    * Non-illustration items
    * Too long or bold images(like 4-frame manga)
    * When the artist has too few followers
* This tool will choose artist randomly, then check images is appropriate for downloading or not.

## How to use?

1. Install dependencies

~~~~shell
pip install -r requirements.txt
~~~~

1. Set a user credential
Write your username / password in "client.json". 


1. Run.

~~~python
python crawl.py
~~~
