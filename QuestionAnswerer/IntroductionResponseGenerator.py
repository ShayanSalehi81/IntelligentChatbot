import random


class IntroductionGenerator:
    def __init__(self):
        self.intro_responses = self.load_dataset('Datasets/introduction.txt')
    
    def load_dataset(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content.split('\n')
    
    def return_intro_response(self):
        return random.choice(self.intro_responses)