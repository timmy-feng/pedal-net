ground_truth_path = '/Users/lucykim/Downloads/midi_files_ground_truth'
prediction_path = '/Users/lucykim/Downloads/midi_files_w_pedal'

import os
import csv
from get_f1 import get_f1, get_f1_naive

prediction_file_set = set()
for root, dirs, files in os.walk(prediction_path):
    for file in files:
        prediction_file_set.add(file[:-5])

# Assuming a CSV file named 'f1_scores.csv' exists in the current directory
with open('f1_scores.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    # Write the header if the file is empty
    if file.tell() == 0:
        writer.writerow(['File Name', 'Naive F1 Score 69', 'Naive F1 Score 71', 'Naive F1 Score 72', 'Ground F1 Score 69', 'Ground F1 Score 71', 'Ground F1 Score 72'])

    for root, dirs, files in os.walk(ground_truth_path):
        count = 0
        for file in files:
            if file[:-5] in prediction_file_set:
                ground = ground_truth_path+'/'+file
                predicted = prediction_path+'/'+file

                naive_f1 = get_f1_naive(predicted)
                print('naive:',naive_f1)

                ground_f1 = get_f1(ground, predicted)
                print('ground:',ground_f1)
                count += 1
            
                # Write the scores for the current file
                writer.writerow([file, naive_f1[0], naive_f1[1], naive_f1[2], ground_f1[0], ground_f1[1], ground_f1[2]])