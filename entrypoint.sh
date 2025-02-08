#!/bin/sh

# Check if phrases.txt exists
if [ -f "/phrases.txt" ]; then
    echo "Copying phrases.txt to /app/phrases.txt..."
    cp /phrases.txt /app/phrases.txt
else
    echo "phrases.txt not found, creating an empty file at /app/phrases.txt..."
    touch /app/phrases.txt
fi

# Execute the main command
exec "$@"