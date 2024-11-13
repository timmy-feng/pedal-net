from mido import MidiFile, MidiTrack, Message
import os

CC_PEDAL = 64

pedal_buckets = [(0, 15), (16, 31), (32, 47), (48, 63), (64, 79), (80, 95), (96, 111), (112, 127)]
pedal_bucket_notes = [69, 71, 72, 74, 76, 77, 79, 81]
pedal_instrument = 56  # trumpet

input_midi_path = "./midi_files/"
output_midi_path = "./midi_files_flattened/"


def flatten_midi(input_path, output_path):
    midi = MidiFile(input_path)

    pedal_track = MidiTrack()
    pedal_track.append(
        Message(
            "program_change",
            program=pedal_instrument,
            channel=0,
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
                        channel=0,
                        note=pedal_bucket_notes[prev_pedal_bucket],
                        velocity=64,
                        time=track_time - prev_pedal_time,
                    )
                )
                pedal_track.append(
                    Message(
                        "note_on",
                        channel=0,
                        note=pedal_bucket_notes[pedal_bucket],
                        velocity=64,
                        time=0,
                    )
                )
            else:
                pedal_track.append(
                    Message(
                        "note_on",
                        channel=0,
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
