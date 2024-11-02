import random


class DislikeResponseGenerator:
    def __init__(self):
        self.dislike_responses = self.load_dataset('Datasets/dislike_responses.txt')
    
    def load_dataset(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content.split('\n')
    
    def return_dislike_response(self):
        return random.choice(self.dislike_responses)