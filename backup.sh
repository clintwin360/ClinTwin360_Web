#!/bin/bash
filename=clintwin_$(date +"%Y%m%d_%H%M%S")
zip -r $filename .
aws s3 cp $filename s3://clintwin-artifacts/