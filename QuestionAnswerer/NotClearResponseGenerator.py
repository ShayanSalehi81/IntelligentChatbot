import random


class NotClearGenerator:
    def __init__(self):
        self.not_clear_responses = self.load_dataset('Datasets/not_clear_phrases.txt')
    
    def load_dataset(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content.split('\n')
    
    def return_not_clear_response(self):
        return random.choice(self.not_clear_responses)