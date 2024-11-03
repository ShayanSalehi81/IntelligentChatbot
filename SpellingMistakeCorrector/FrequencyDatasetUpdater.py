import re
import csv
from collections import defaultdict


def update_frequency_csv(input_dataset, frequency_csv, output_file):
    token_frequency = defaultdict(int)

    with open(frequency_csv, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header
        for row in reader:
            token, frequency = row
            token_frequency[token] += int(frequency)

    with open(input_dataset, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header
        for row in reader:
            for sentence in row:
                tokens = re.findall(r'\b\w+\b', sentence)  
                for token in tokens:
                    token_frequency[token] += 10  # Adding with a 10-time multiplier

    sorted_tokens = sorted(token_frequency.items(), key=lambda item: item[1], reverse=True)

    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Token', 'Frequency'])
        for token, frequency in sorted_tokens:
            writer.writerow([token, frequency])


if __name__ == "__main__":
    input_dataset = 'Datasets/Dataset.csv'
    frequency_csv = 'SpellingMistakeCorrector/frequency.csv'
    output_file = 'SpellingMistakeCorrector/frequency_updated.csv'
    update_frequency_csv(input_dataset, frequency_csv, output_file)
