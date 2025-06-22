#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

chmod +x ./bin/ffmpeg