#!/bin/sh
pid=`ps aux | grep python | grep crawl | awk '{ print $2 }'`
kill -KILL $pid
