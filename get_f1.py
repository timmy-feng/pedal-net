from mido import MidiFile
from sklearn.metrics import f1_score
import numpy as np


def get_f1(ground_truth_path, prediction_path):
    """
    input relative file paths get an f1 score for each pedal bucket
    expects ground truth to have bagpipe pedaling processing done already
    """
    ground_truth_69 = create_note_sequence(ground_truth_path, 69)
    prediction_69 = create_note_sequence(prediction_path, 69)

    if len(ground_truth_69) != len(prediction_69):
        if len(prediction_69) < len(ground_truth_69):
            ground_truth_69 = ground_truth_69[: len(prediction_69)]
        elif len(prediction_69) > len(ground_truth_69):
            ground_truth_69 += [0] * (len(prediction_69) - len(ground_truth_69))
            print("ERROR:  predicted more amount of ticks for bucket 69 than ground truth")
            print("actual len:",len(ground_truth_69))
            print("predicted len:",len(prediction_69))

    ground_truth_71 = create_note_sequence(ground_truth_path, 71)
    prediction_71 = create_note_sequence(prediction_path, 71)

    if len(ground_truth_71) != len(prediction_71):
        if len(prediction_71) < len(ground_truth_71):
            ground_truth_71 = ground_truth_71[: len(prediction_71)]
        elif len(prediction_71) > len(ground_truth_71):
            ground_truth_71 += [0] * (len(prediction_71) - len(ground_truth_71))
            print("ERROR:  predicted more amount of ticks for bucket 71 than ground truth")
            print("actual len:",len(ground_truth_71))
            print("predicted len:",len(prediction_71))

    ground_truth_72 = create_note_sequence(ground_truth_path, 72)
    prediction_72 = create_note_sequence(prediction_path, 72)

    if len(ground_truth_72) != len(prediction_72):
        if len(prediction_72) < len(ground_truth_72):
            ground_truth_72 = ground_truth_72[: len(prediction_72)]
        elif len(prediction_72) > len(ground_truth_72):
            ground_truth_72 += [0] * (len(prediction_72) - len(ground_truth_72))
            print("ERROR:  predicted more amount of ticks for bucket 72 than ground truth")
            print("actual len:",len(ground_truth_72))
            print("predicted len:",len(prediction_72))

    scores = (
        f1_score(ground_truth_69, prediction_69),
        f1_score(ground_truth_71, prediction_71),
        f1_score(ground_truth_72, prediction_72),
    )

    return scores


def get_f1_naive(ground_truth_path, prediction_path):
    midi = MidiFile(prediction_path)

    ground_truth_69 = create_note_sequence(ground_truth_path, 69)
    prediction_69 = create_note_sequence(prediction_path, 69)

    if len(ground_truth_69) != len(prediction_69):
        if len(prediction_69) < len(ground_truth_69):
            ground_truth_69 = ground_truth_69[: len(prediction_69)]
        elif len(prediction_69) > len(ground_truth_69):
            ground_truth_69 += [0] * (len(prediction_69) - len(ground_truth_69))
            print("ERROR:  predicted more amount of ticks for bucket 69 than ground truth")
            print("actual len:",len(ground_truth_69))
            print("predicted len:",len(prediction_69))

    ground_truth_71 = create_note_sequence(ground_truth_path, 71)
    prediction_71 = create_note_sequence(prediction_path, 71)

    if len(ground_truth_71) != len(prediction_71):
        if len(prediction_71) < len(ground_truth_71):
            ground_truth_71 = ground_truth_71[: len(prediction_71)]
        elif len(prediction_71) > len(ground_truth_71):
            ground_truth_71 += [0] * (len(prediction_71) - len(ground_truth_71))
            print("ERROR:  predicted more amount of ticks for bucket 71 than ground truth")
            print("actual len:",len(ground_truth_71))
            print("predicted len:",len(prediction_71))

    ground_truth_72 = create_note_sequence(ground_truth_path, 72)
    prediction_72 = create_note_sequence(prediction_path, 72)

    if len(ground_truth_72) != len(prediction_72):
        if len(prediction_72) < len(ground_truth_72):
            ground_truth_72 = ground_truth_72[: len(prediction_72)]
        elif len(prediction_72) > len(ground_truth_72):
            ground_truth_72 += [0] * (len(prediction_72) - len(ground_truth_72))
            print("ERROR:  predicted more amount of ticks for bucket 72 than ground truth")
            print("actual len:",len(ground_truth_72))
            print("predicted len:",len(prediction_72))

    naive_69 = np.ones_like(prediction_69)
    naive_71 = np.ones_like(prediction_71)
    naive_72 = np.ones_like(prediction_72)

    scores = (
        f1_score(ground_truth_69, naive_69),
        f1_score(ground_truth_71, naive_71),
        f1_score(ground_truth_72, naive_72),
    )

    return scores


def create_note_sequence(midi_file_path, target_note):
    """
    Creates a binary time sequence array (0 and 1) for a specific note in a MIDI file's bagpipe track.

    Parameters:
        midi_file_path (str): Path to the MIDI file.
        target_note (int): MIDI note number to track.

    Returns:
        list[int]: Binary time sequence array.
    """
    midi = MidiFile(midi_file_path)

    # Determine the length of the song in ticks
    total_ticks = sum(
        msg.time for track in midi.tracks for msg in track if not msg.is_meta
    )

    # Create a time sequence array initialized to 0
    note_sequence = [0] * int(total_ticks)

    track = midi.tracks[-1]
    current_tick = 0
    note_active = False  # Tracks whether the target note is currently held

    for msg in track:
        if not msg.is_meta:
            # Update the current tick
            for _ in range(msg.time):
                if current_tick < total_ticks and note_active:
                    note_sequence[current_tick] = 1
                current_tick += 1

            # Process note events
            if msg.type == "note_on" and msg.note == target_note and msg.velocity > 0:
                note_active = True
            elif msg.type == "note_off" or (
                msg.type == "note_on" and msg.velocity == 0
            ):
                if msg.note == target_note:
                    note_active = False
        # elif msg.type == "end_of_track":
        #     current_tick += msg.time
        #     return note_sequence[:current_tick]
    
    return note_sequence

def are_midi_files_same_len_in_ticks(path1, path2):
    """
    Compare the length of two MIDI files in ticks.

    Parameters:
        path1 (str): Path to the first MIDI file.
        path2 (str): Path to the second MIDI file.

    Returns:
        bool: True if the files have the same length in ticks, False otherwise.
    """
    midi1 = MidiFile(path1)
    midi2 = MidiFile(path2)

    # Calculate the total ticks for each MIDI file
    total_ticks1 = sum(
        msg.time for track in midi1.tracks for msg in track if not msg.is_meta
    )
    total_ticks2 = sum(
        msg.time for track in midi2.tracks for msg in track if not msg.is_meta
    )

    # Compare the total ticks
    is_same_len = total_ticks1 == total_ticks2
    if not is_same_len:
        print("len of 1:", total_ticks1)
        print("len of 2:", total_ticks2)
    else:
        print('len of both:', total_ticks1)
    return is_same_len

# Example unit test
# midi_file_path = "midi_files_flattened/star_wars_by_han_ar_single_z0_full.midi"  # Replace with your MIDI file path
# # target_note = 71  # Replace with the MIDI note number for the specific note

# # sequence = (create_note_sequence(midi_file_path, target_note))[400:1000]
# # print(sequence)

# # Integration Test
# naive_f1s = get_f1_naive(midi_file_path)
# print(naive_f1s)
