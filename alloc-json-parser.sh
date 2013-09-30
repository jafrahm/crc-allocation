#!/bin/bash

tempfile="output.json"
wget -q -O $tempfile https://crcum.rc.colorado.edu/allocation/projects/ucb/json/ --no-check-certificate
python /home/frahm/scripts/json_parser.py -f $tempfile
rm $tempfile
