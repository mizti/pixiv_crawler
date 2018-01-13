# coding: utf-8

from pixivpy3 import *
import json
from time import sleep
import traceback
import os
import re
import random

def debug_print(s):
    if not __debug__:
        print(s)

api = PixivAPI() # public API
aapi = AppPixivAPI() # API require logins

f = open('client.json', 'r')
client_info = json.load(f)
f.close()
api.login(client_info['pixiv_id'], client_info['password'])

# ID Range
#STARTID = 1500000
#ENDID = 2000000
STARTID = 10
ENDID = 2900000
# MAX = 29520000 # This is the last number of Pixiv

print("Start crawling")
# Save directory
if not os.path.exists("./pixiv_images"):
    os.mkdir("./pixiv_images")
saving_direcory_path = './pixiv_images/'

# Excluded tags. Add tags you don't want to download.
exclude_tags = ["講座", "線画"]

lst = list(range(STARTID, ENDID + 1))
random.shuffle(lst)
for ID in lst:
    try:
        sleep(1)
        artist_pixiv_id = ID

        user_result = aapi.user_detail(artist_pixiv_id)
        if 'error' in user_result:
            debug_print("skip: user not exist")
            continue

        # too few follower
        if user_result.profile.total_follower < 3:
            debug_print("skip: too few follower")
            continue

        # No works uploaded
        if user_result.profile.total_illusts < 1:
            debug_print("skip: no works uploaded")
            continue

        separator = '------------------------------------------------------------'
        # Target Artist details
        print('Artist: %s' % user_result.user.name)
        print('Follower Num: %s' % user_result.profile.total_follower)
        print('Works Num: %d' % user_result.profile.total_illusts)
        print(separator)

        json_result = api.users_works(artist_pixiv_id, per_page=300)
        json_result.response.sort(key=lambda x: x.stats.score, reverse=True)
        total_works = json_result.pagination.total

        #if not os.path.exists(saving_direcory_path):
        #    os.mkdir(saving_direcory_path)

        for work_no in range(0, total_works):
            illust = json_result.response[work_no]

            skip_this_work = False

            # Check the score
            score = illust.stats.score
            if score < 500:
                debug_print("skip: low score")
                skip_this_work = True

            # R18
            if illust.age_limit != "all-age":
                debug_print("skip: HENTAI")
                skip_this_work = True

            # Non-illustration work
            if illust.type != "illustration":
                debug_print("skip: not illust")
                skip_this_work = True

            # Having excluded tags
            for tag in exclude_tags:
                r = re.compile(".*" + tag + ".*")
                if any(r.match(i) for i in illust.tags):
                    debug_print("tag " + tag + " detected!!")
                    skip_this_work = True

            # Shape too long
            if (illust.height / illust.width) > 2.5 or (illust.width / illust.height) > 2.5:
                debug_print("skip: too thin size")
                skip_this_work = True

            if not(skip_this_work):        
                print('Procedure: %d/%d of Artist %d' % (work_no + 1, total_works, ID))
                print('Title: %s Score: %s' % (illust.title, illust.stats.score))
                print('Tags: %s' % illust.tags)
                print(separator)
                # Select image size to download
                #aapi.download(illust.image_urls.px_128x128, saving_direcory_path) #small
                aapi.download(illust.image_urls.px_480mw, saving_direcory_path) #medium
                #aapi.download(illust.image_urls.large, saving_direcory_path) #large
                sleep(5)

        print('\nThat\'s all.')
    except:
        debug_print("exception")
        traceback.print_exc()
        sleep(1)
        continue
