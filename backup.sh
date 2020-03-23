#!/bin/bash
filename=clintwin
zip -r $filename .
aws s3 cp $WORKSPACE/$filename.zip s3://clintwin-artifacts/