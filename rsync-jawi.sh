#!/bin/bash

# Ensures only one instance is running at a time
LOCKFILE="/tmp/rsync-jawi.lock"
SRC="/shm/jawi/"
DEST="/me/paper/jawi/"

cp -vfr "$DEST" "$SRC"


# Check if lockfile exists and process is still running
if [ -f "$LOCKFILE" ]; then
    OLDPID=$(cat "$LOCKFILE")
    if ps -p "$OLDPID" > /dev/null 2>&1; then
        echo "Another instance is already running (PID $OLDPID). Exiting."
        exit 1
    else
        echo "Stale lock found. Cleaning up."
        rm -f "$LOCKFILE"
    fi
fi

# Create lockfile with current PID
echo $$ > "$LOCKFILE"

# Define cleanup function on exit
cleanup() {
    rm -f "$LOCKFILE"
    exit
}
trap cleanup INT TERM EXIT

# Main sync loop
while true; do
    rsync -rtvu "$SRC" "$DEST"
    sleep 180
done
