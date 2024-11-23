from mido import MidiFile, MidiTrack, Message
import os
import argparse

MAX_PEDAL = 127
CC_PEDAL = 64

pedal_bucket_notes = [69, 71, 72, 74, 76, 77, 79, 81]
pedal_instrument = 56  # trumpet
pedal_channel = 1 # channel 0 is used for piano

parser = argparse.ArgumentParser(
    description="Flatten MIDI files by adding pedal notes."
)
parser.add_argument(
    "--input_dir",
    type=str,
    default="./midi_files",
    help="Path to the input MIDI files directory.",
)
parser.add_argument(
    "--output_dir",
    type=str,
    default="./midi_files_flattened",
    help="Path to the output flattened MIDI files directory.",
)
parser.add_argument(
    "--pedal_buckets",
    type=int,
    nargs="+",
    default=[0, 8, 120],
    help="Pedal buckets for the pedal notes, lowest pedal for each interval. Default: [0, 8, 120]",
)
args = parser.parse_args()

pedal_buckets = [
    (args.pedal_buckets[i], args.pedal_buckets[i + 1] if i + 1 < len(args.pedal_buckets) else MAX_PEDAL)
    for i, _ in enumerate(args.pedal_buckets)
]

assert(len(pedal_buckets) <= len(pedal_bucket_notes))

input_midi_path = args.input_dir
output_midi_path = args.output_dir

def flatten_midi(input_path, output_path):
    midi = MidiFile(input_path)

    pedal_track = MidiTrack()
    pedal_track.append(
        Message(
            "program_change",
            program=pedal_instrument,
            channel=pedal_channel,
            time=0,
        )
    )
    prev_pedal_bucket = None
    prev_pedal_time = 0
    track_time = 0
    for msg in midi.tracks[1]:
        track_time += msg.time
        if msg.type == "control_change" and msg.control == CC_PEDAL:
            pedal_value = msg.value
            for i, (min_val, max_val) in enumerate(pedal_buckets):
                if min_val <= pedal_value <= max_val:
                    pedal_bucket = i
                    break

            if pedal_bucket == prev_pedal_bucket:
                continue

            if prev_pedal_bucket is not None:
                pedal_track.append(
                    Message(
                        "note_off",
                        channel=pedal_channel,
                        note=pedal_bucket_notes[prev_pedal_bucket],
                        velocity=64,
                        time=track_time - prev_pedal_time,
                    )
                )
                pedal_track.append(
                    Message(
                        "note_on",
                        channel=pedal_channel,
                        note=pedal_bucket_notes[pedal_bucket],
                        velocity=64,
                        time=0,
                    )
                )
            else:
                pedal_track.append(
                    Message(
                        "note_on",
                        channel=pedal_channel,
                        note=pedal_bucket_notes[pedal_bucket],
                        velocity=64,
                        time=track_time,
                    )
                )
            prev_pedal_time = track_time
            prev_pedal_bucket = pedal_bucket
    midi.tracks.append(pedal_track)
    midi.save(output_path)


os.makedirs(output_midi_path, exist_ok=True)

for midi_file in os.listdir(input_midi_path):
    if midi_file.endswith(".midi"):
        input_file_path = os.path.join(input_midi_path, midi_file)
        output_file_path = os.path.join(output_midi_path, midi_file)
        flatten_midi(input_file_path, output_file_path)
