import os
import json
import torch
import random
import numpy as np
import pandas as pd

from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity


class Greeting:
    def __init__(self, dataset_file_path, response_file_path):
        self.greeting_dataframe = self.load_data(dataset_file_path)
        self.greeting_response = self.load_response(response_file_path)
        self.examples = self.greeting_dataframe['example'].to_list()
        self.intents = self.greeting_dataframe['intent'].to_list()
        self.tokenizer = AutoTokenizer.from_pretrained("sharif-dal/dal-bert")
        self.embedding_model = AutoModel.from_pretrained("sharif-dal/dal-bert")
        self.dataset_embeddings = self.get_or_generate_embeddings(file_path='Embeddings/greeting_embeddings.npy')

    def load_data(self, file_path):
        return pd.read_csv(file_path)  
    
    def load_response(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def get_one_sentence_embedding(self, sentence):
        inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            output = self.embedding_model(**inputs)
        return output.last_hidden_state.mean(dim=1).numpy()
    
    def get_embeddings(self, sentences):
        embeddings = []
        for sentence in tqdm(sentences, desc="Generating embeddings"):
            inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = self.embedding_model(**inputs)
            embeddings.append(outputs.last_hidden_state.mean(dim=1).numpy())
        return np.vstack(embeddings)
    
    def save_embeddings(self, embeddings, file_path):
        np.save(file_path, embeddings)

    def load_embeddings(self, file_path):
        return np.load(file_path)
    
    def get_or_generate_embeddings(self, file_path):
        if os.path.exists(file_path):
            print(f"Loading embeddings from {file_path}")
            return self.load_embeddings(file_path)
        else:
            print(f"Generating embeddings for {file_path}")
            embeddings = self.get_embeddings(self.examples)
            self.save_embeddings(embeddings, file_path)
            return embeddings
        
    def calculate_cosine_similarity(self, embeddings1, embeddings2):
        return cosine_similarity(embeddings1, embeddings2)
    
    def find_most_similar_question(self, query):
        query_embedding = self.get_one_sentence_embedding(query)
        similarity_matrix = self.calculate_cosine_similarity(query_embedding, self.dataset_embeddings)
        
        max_similarity = similarity_matrix.max(axis=1)[0]
        predicted_index = similarity_matrix.argmax(axis=1)[0]
        
        confidence = (max_similarity + 1) / 2  # Normalize to range [0, 1]
        return predicted_index, confidence
    
    def return_complex_answer(self, query):
        index, confidence = self.find_most_similar_question(query)
        response = f'سوال تشخیص داده شده: {self.intents[index]} \n میزان اعتماد آن: {confidence} \n\n\n'
        return response
    
    def return_simple_answer(self, query):
        index, confidence = self.find_most_similar_question(query)
        answers = next((item['answers'] for item in self.greeting_response if item['intent'] == self.intents[index]))
        return random.choice(answers), confidence