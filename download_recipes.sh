#!/bin/bash

cd all

echo "Starting recipe download..."

# Loop from 1 to 400
for i in {1..400}
do
    echo "Fetching recipe #$i..."
    
    # wget command:
    # -q suppresses the progress bar output to keep the terminal clean
    # -O names the saved file dynamically based on the ID
    wget -q "https://heda-server.fly.dev/r/$i" -O "$i.html"
    
    # Wait for 5 seconds before the next request, unless it's the last one
    if [ $i -lt 400 ]; then
        sleep 5
    fi
done

echo "Download complete! All recipes saved in the 'recipes' directory."
