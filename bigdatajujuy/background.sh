#!/bin/bash
cd /opt/bigdatajujuy
source venv/bin/activate
cd /opt/bigdatajujuy/bigdatajujuy
python manage.py process_tasks
