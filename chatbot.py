from SpellingMistakeCorrector.SpellingMistakesCorrector import SpellingMistakeCorrector
from SwearWordDetector.SwearWordDetector import SwearWordDetector
from QuestionAnswerer.ChatBotCore import ChatBot


class Chatbot:
    def __init__(self) -> None:
        self.swear_detector = SwearWordDetector('SwearWordDetector/swear_words.json')
        self.spelling_corrector = SpellingMistakeCorrector('SpellingMistakeCorrector/frequency_combined.csv', threshold=0.2)
        self.chat_bot = ChatBot(questions_data_file_path='Datasets\Result_QA.csv')

    def chat(self, query) -> str:
        spell_corrected_query = self.spelling_corrector.correct_spelling(query)
        censored_query = self.swear_detector.filter_words(spell_corrected_query)
        most_similar_question = self.chat_bot.find_most_similar_question(query=censored_query)
        return most_similar_question


if __name__ == '__main__':
    chatbot = Chatbot()
    print(chatbot.chat('صلام'))