#!/bin/bash
set -e
gunicorn iridisite.wsgi --log-file -
