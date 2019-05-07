#!/bin/bash
cd /opt/bigdatajujuy
source venv/bin/activate
cd /opt/bigdatajujuy/bigdatajujuy
gunicorn bigdatajujuy.wsgi -t 600 -b 127.0.0.1:8015 -w 6 --user=servidor --group=servidor --log-file=/opt/bigdatajujuy/gunicorn.log 2>>/opt/bigdatajujuy/gunicorn.log
