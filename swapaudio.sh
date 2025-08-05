#!/bin/bash

# PulseAudio swap toggle script with GUI notifications
# Dependencies: pactl, notify-send (usually provided by libnotify)

SWAP_SINK_NAME="swapped"
DEFAULT_SINK=$(pactl info | awk -F': ' '/Default Sink/ {print $2}')

if [[ "$DEFAULT_SINK" == "$SWAP_SINK_NAME" ]]; then
    # Revert to original sink
    ORIGINAL_SINK=$(pactl list short sinks | awk -v swap="$SWAP_SINK_NAME" '$2 != swap {print $2; exit}')
    pactl set-default-sink "$ORIGINAL_SINK"

    for input in $(pactl list short sink-inputs | awk '{print $1}'); do
        pactl move-sink-input "$input" "$ORIGINAL_SINK"
    done

    pactl unload-module module-remap-sink

    notify-send "🔊 Audio Channels" "Restored to normal (Left–Right)"
else
    # Swap left/right channels
    pactl unload-module module-remap-sink 2>/dev/null
    pactl load-module module-remap-sink sink_name=$SWAP_SINK_NAME master="$DEFAULT_SINK" channels=2 master_channel_map=right,left channel_map=left,right

    pactl set-default-sink "$SWAP_SINK_NAME"

    for input in $(pactl list short sink-inputs | awk '{print $1}'); do
        pactl move-sink-input "$input" "$SWAP_SINK_NAME"
    done

    notify-send "🔄 Audio Channels" "Swapped (Left ⇄ Right)"
fi
