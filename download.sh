#!/bin/bash

# Define the URL of the zip file
URL="https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/quora.zip"

# Define the output file name
OUTPUT_FILE="quora.zip"

# Download the zip file
echo "Downloading $OUTPUT_FILE..."
curl -O $URL

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "Download completed. Unzipping $OUTPUT_FILE..."
    # Unzip the downloaded file
    unzip $OUTPUT_FILE
    
    # Check if unzip was successful
    if [ $? -eq 0 ]; then
        echo "Unzip completed successfully."
    else
        echo "Failed to unzip $OUTPUT_FILE."
    fi
else
    echo "Failed to download $OUTPUT_FILE."
fi
