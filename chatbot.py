from SpellingMistakeCorrector.SpellingMistakesCorrector import SpellingMistakeCorrector
from SwearWordDetector.SwearWordDetector import SwearWordDetector
from QuestionAnswerer.ChatBotCore import ChatBot


class Chatbot:
    def __init__(self) -> None:
        self.swear_detector = SwearWordDetector('SwearWordDetector/swear_words.json')
        self.spelling_corrector = SpellingMistakeCorrector('SpellingMistakeCorrector/frequency_combined.csv', threshold=0.2)
        self.chat_bot = ChatBot(dataset_file_path='Datasets/Dataset.csv',)

    def chat(self, query) -> str:
        spell_corrected_query = self.spelling_corrector.correct_spelling(query)
        censored_query = self.swear_detector.filter_words(spell_corrected_query)
        answer = self.chat_bot.return_answer(query=censored_query)
        return answer


if __name__ == '__main__':
    chatbot = Chatbot()
    response = chatbot.chat('سرویس‌های سیستم')

    with open('Outputs/response.txt', 'w', encoding='utf-8') as file:
        file.write(response)