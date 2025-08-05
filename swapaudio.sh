#!/bin/bash

# PulseAudio swap toggle script
# Requires: pactl (or pacmd), PulseAudio

# Name of the remapped sink
SWAP_SINK_NAME="swapped"

# Get the current default sink name
DEFAULT_SINK=$(pactl info | awk -F': ' '/Default Sink/ {print $2}')

# Check if the swapped sink is currently default
if [[ "$DEFAULT_SINK" == "$SWAP_SINK_NAME" ]]; then
    echo "Reverting to original sink..."

    # Get the original sink (first one that is NOT the swapped sink)
    ORIGINAL_SINK=$(pactl list short sinks | awk -v swap="$SWAP_SINK_NAME" '$2 != swap {print $2; exit}')

    # Set it as default
    pactl set-default-sink "$ORIGINAL_SINK"

    # Move all playing streams to the original sink
    for input in $(pactl list short sink-inputs | awk '{print $1}'); do
        pactl move-sink-input "$input" "$ORIGINAL_SINK"
    done

    # Unload swapped sink module
    pactl unload-module module-remap-sink

    echo "Audio channels set to normal (Left–Right)"
else
    echo "Swapping audio channels..."

    # Load remapped swapped sink
    pactl unload-module module-remap-sink 2>/dev/null
    pactl load-module module-remap-sink sink_name=$SWAP_SINK_NAME master="$DEFAULT_SINK" channels=2 master_channel_map=right,left channel_map=left,right

    # Set as default sink
    pactl set-default-sink "$SWAP_SINK_NAME"

    # Move all playing streams to the swapped sink
    for input in $(pactl list short sink-inputs | awk '{print $1}'); do
        pactl move-sink-input "$input" "$SWAP_SINK_NAME"
    done

    echo "Audio channels swapped (Left ⇄ Right)"
fi
