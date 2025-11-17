#!/bin/bash

LOCAL_FILE=$1       
BUCKET=$2           
EXPIRES=$3   

aws s3 cp "$LOCAL_FILE" "s3://$BUCKET/"

aws s3 presign "s3://$BUCKET/$(basename "$LOCAL_FILE")" --expires-in "$EXPIRES"
