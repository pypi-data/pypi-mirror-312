#!/bin/bash
set +ex

VERSION="5.9.3"
URL="https://github.com/dropzone/dropzone/releases/download/v$VERSION/dist.zip"
OUTPUT_ZIP="dist.zip"
curl -L -o $OUTPUT_ZIP $URL
unzip $OUTPUT_ZIP
rm $OUTPUT_ZIP

rm -dr js_lib_dropzone/static/js_lib_dropzone
mv dist js_lib_dropzone/static/js_lib_dropzone

