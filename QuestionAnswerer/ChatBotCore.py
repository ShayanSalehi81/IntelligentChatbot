import os
import torch
import random
import numpy as np
import pandas as pd

from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from QuestionAnswerer.DislikeResponseGenerator import DislikeResponseGenerator
from QuestionAnswerer.NotClearResponseGenerator import NotClearGenerator
from QuestionAnswerer.IntroductionResponseGenerator import IntroductionGenerator
from QuestionAnswerer.GreetingModel import Greeting


class ChatBot:
    def __init__(self, dataset_file_path, confidence_threshold, greeting_confidence_threshold):
        self.confidence_threshold = confidence_threshold
        self.greeting_confidence_threshold = greeting_confidence_threshold
        self.qa_dataframe = self.load_data(dataset_file_path)
        self.target_questions = self.qa_dataframe['target_question'].to_list()
        self.target_answers = self.qa_dataframe['target_answer'].to_list()
        self.extended_answers = self.load_extended_answers()
        self.prefixes = self.load_fixes_dataset('Datasets/prefixes.txt')
        self.postfixes = self.load_fixes_dataset('Datasets/postfixes.txt')
        self.model_path = self.get_or_download_model(model_name='sharif-dal/dal-bert')
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.embedding_model = AutoModel.from_pretrained(self.model_path)
        self.dataset_embeddings = self.get_or_generate_embeddings(file_path='Embeddings/qa_embeddings.npy')
        self.greeting_model = Greeting(dataset_file_path='Datasets/greeting_dataset_filtered.csv', response_file_path='Datasets/greeting_response.json')
        self.dislike_model = DislikeResponseGenerator()
        self.intro_model = IntroductionGenerator()
        self.not_clear_model = NotClearGenerator()
    
    def load_fixes_dataset(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content.split('\n')

    def load_data(self, file_path):
        return pd.read_csv(file_path)
    
    def load_extended_answers(self):
        extended_answers = {}
        for _, row in self.qa_dataframe.iterrows():
            if pd.notna(row['extended_answers']):
                extended_answers[row['target_answer']] = list(row['extended_answers'].split(','))    
            else:
                extended_answers[row['target_answer']] = list() 
        return extended_answers   
    
    def get_or_download_model(self, model_name, local_model_dir='Models/dal-bert'):
        if not os.path.exists(local_model_dir):
            print(f"Model not found locally. Downloading {model_name} and saving to {local_model_dir}.")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name)
            os.makedirs(local_model_dir, exist_ok=True)
            tokenizer.save_pretrained(local_model_dir)
            model.save_pretrained(local_model_dir)
            print(f"Model saved to {local_model_dir}.")
        else:
            print(f"Model found locally at {local_model_dir}.")
        return local_model_dir
    
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
            embeddings = self.get_embeddings(self.qa_dataframe['target_question'].tolist())
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
    
    def return_question_with_answer(self, query):
        index, confidence = self.find_most_similar_question(query)
        prefix, postfix = random.choice(self.prefixes), random.choice(self.postfixes)
        answer = prefix + ' ' + random.choice(self.extended_answers[self.target_answers[index]]).strip() + ' ' + postfix
        response = f'سوال تشخیص داده شده: {self.target_questions[index]} \n میزان اعتماد آن: {confidence} \n پاسخ گسترش یافته آن: {answer} \n\n\n'
        return response
    
    def return_answer_only(self, query):
        greeting_response, greeting_confidence = self.greeting_model.return_simple_answer(query)
        if greeting_confidence > self.greeting_confidence_threshold:
            return greeting_response
        index, confidence = self.find_most_similar_question(query)
        if confidence < self.confidence_threshold:
            return self.not_clear_model.return_not_clear_response()
        prefix, postfix = random.choice(self.prefixes), random.choice(self.postfixes)
        answer = prefix + ' ' + random.choice(self.extended_answers[self.target_answers[index]]).strip() + ' ' + postfix
        return answer

    def return_response_of_dislike_model(self):
        return self.dislike_model.return_dislike_response()
    
    def return_response_of_intro_model(self):
        return self.intro_model.return_intro_response()
    
    def greeting_answer(self, query):
        return self.greeting_model.return_complex_answer(query=query)