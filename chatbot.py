from SpellingMistakeCorrector.SpellingMistakesCorrector import SpellingMistakeCorrector
from SwearWordDetector.SwearWordDetector import SwearWordDetector
from QuestionAnswerer.ChatBotCore import ChatBot


class Chatbot:
    def __init__(self) -> None:
        self.swear_detector = SwearWordDetector('SwearWordDetector/swear_words.json')
        self.spelling_corrector = SpellingMistakeCorrector('SpellingMistakeCorrector/frequency_updated.csv', threshold=0.2)
        self.chat_bot = ChatBot(dataset_file_path='Datasets/Dataset.csv', confidence_threshold=0.83, greeting_confidence_threshold=0.88)

    def introduction(self) -> str:
        return self.chat_bot.return_response_of_intro_model()

    def chat(self, query:str) -> str:
        spell_corrected_query = self.spelling_corrector.correct_spelling(query)
        censored_query = self.swear_detector.filter_words(spell_corrected_query)
        answer = self.chat_bot.return_answer_only(query=censored_query)
        return answer
    
    def dislike(self) -> str:
        return self.chat_bot.return_response_of_dislike_model()
    
    def greeting(self, query:str) -> str:
        return self.chat_bot.greeting_answer(query)
    
    def analize(self, query:str):
        print(f'پرسش پرسیده شده: {query}')
        spell_corrected_query = self.spelling_corrector.correct_spelling(query)
        print(f'پرسش پس از اصلاح غلط املایی: {spell_corrected_query}')
        censored_query = self.swear_detector.filter_words(spell_corrected_query)
        print(f'پرسش پس از سانسور کلمات رکیک: {censored_query}')
        answer = self.chat_bot.return_question_with_answer(query=censored_query)
        print(answer)


if __name__ == '__main__':
    chatbot = Chatbot()
    response = chatbot.chat('سرویس‌های سیستم')

    with open('Outputs/response.txt', 'w', encoding='utf-8') as file:
        file.write(response)