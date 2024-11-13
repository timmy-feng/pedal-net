import csv
import os
import shutil
import argparse

parser = argparse.ArgumentParser(
    description="Copy MIDI files to a specified directory."
)
parser.add_argument(
    "--input_dir", type=str, default=".", help="Directory containing the MIDI files"
)
parser.add_argument(
    "--output_dir",
    type=str,
    default="./midi_files/",
    help="Directory to copy MIDI files to",
)
parser.add_argument(
    "--csv_path",
    type=str,
    default="maestro-v3.0.0.csv",
    help="Path to the CSV file containing MIDI file information",
)
args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir
csv_path = args.csv_path

os.makedirs(output_dir, exist_ok=True)
with open(csv_path, mode="r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for index, row in enumerate(reader, start=1):
        midi_filename = row["midi_filename"]
        source_path = os.path.join(input_dir, midi_filename)
        destination_path = os.path.join(output_dir, f"{index}.midi")
        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)
        else:
            print(f"Warning: {midi_filename} not found")
