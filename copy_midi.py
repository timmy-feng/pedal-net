import csv
import os
import shutil

output_dir = "./midi_files/"
csv_path = "maestro-v3.0.0.csv"

os.makedirs(output_dir, exist_ok=True)
with open(csv_path, mode="r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for index, row in enumerate(reader, start=1):
        midi_filename = row["midi_filename"]
        source_path = os.path.join(".", midi_filename)
        destination_path = os.path.join(output_dir, f"{index}.midi")
        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)
        else:
            print(f"Warning: {midi_filename} not found")
