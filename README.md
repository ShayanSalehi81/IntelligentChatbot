# Persian Chatbot

This repository contains a Persian-language chatbot framework designed to handle greetings, respond to specific queries, detect and correct spelling mistakes, and manage inappropriate language. The bot leverages pretrained BERT models for sentence embedding and employs various modules for generating responses, correcting spelling errors, and filtering profanities. 

## Project Structure

- **Datasets**: Contains the datasets used for training and generating responses.
  - `Dataset.csv`: The main dataset with target questions and answers.
  - `greeting_dataset_filtered.csv`: Filtered dataset specifically for greeting-related responses.
  - `greeting_response.json`: JSON file with predefined greeting responses.
  - `questions_with_answers.xlsx`: Questions with potential answers in an Excel format.
  - `dislike_responses.txt`, `introduction.txt`, `not_clear_phrases`: Text files used for generating responses for specific scenarios.
  - `target_and_similar_questions.csv`: Stores various phrasing for questions to enhance response accuracy.

- **Embeddings**: Stores precomputed embeddings for efficient similarity calculations.
  - `greeting_embeddings.npy`: Embeddings specifically for greeting-related questions.
  - `qa_embeddings.npy`: General embeddings for question-answer pairs.

- **QuestionAnswerer**: Core classes for generating different types of responses.
  - `DislikeResponseGenerator.py`, `IntroductionResponseGenerator.py`, `NotClearResponseGenerator.py`, `GreetingModel.py`: Modules dedicated to generating responses for specific categories.

- **Scripts**: Utility scripts for data preprocessing and preparation.
  - `CreateGreetingDataset.py`: Script to prepare the greeting dataset.
  - `FrequencyDatasetUpdater.py`: Updates the frequency dataset based on token usage.
  - `SpellingMistakesCorrector.py`: Uses Levenshtein distance to correct spelling mistakes in Persian text.

- **SwearWordDetector**: Module for detecting and filtering inappropriate language.
  - `swear_words.json`: JSON file containing a list of inappropriate words in Persian.
  - `SwearWordDetector.py`: Main class for detecting and filtering out swear words.

- **Root Files**:
  - `app.py`: Main application script for running the chatbot.
  - `chatbot.py`: Defines the `ChatBot` class, the central component for query handling and response generation.
  - `Dockerfile`: Docker configuration for containerizing the application.
  - `requirements.txt`: Lists Python dependencies for the project.

## Requirements

To install the required packages, run:

```bash
pip install -r requirements.txt
```

## Components Overview

### ChatBot Core

The `ChatBot` class in `chatbot.py` is the main entry point for handling user queries and generating responses. It uses a pretrained BERT model to generate embeddings for questions and calculates cosine similarity to find the best response. The chatbot also includes various models for handling greetings, dislikes, and introductions.

- **Parameters**:
  - `confidence_threshold`: Minimum confidence required to return an answer.
  - `greeting_confidence_threshold`: Minimum confidence for detecting a greeting.
  
- **Key Methods**:
  - `return_answer_only`: Generates a response based on the similarity of the input query to stored questions.
  - `return_response_of_dislike_model`: Returns a response when a user expresses dislike.
  - `return_response_of_intro_model`: Provides an introduction response.
  - `greeting_answer`: Responds specifically to greeting-related queries.

### Spelling Mistake Correction

The `SpellingMistakeCorrector` class in `SpellingMistakeCorrector.py` corrects misspellings in user queries. It uses a BK-Tree and Levenshtein distance for identifying potential corrections based on a frequency dataset (`frequency.csv`).

- **Features**:
  - `correct_spelling`: Tokenizes the query and replaces misspelled tokens with their closest matches from the frequency dictionary.

### Swear Word Detection

The `SwearWordDetector` class in `SwearWordDetector.py` identifies and filters inappropriate language. It uses a list of swear words stored in `swear_words.json`.

- **Features**:
  - `filter_words`: Replaces detected swear words in the text with a specified symbol.
  - `has_swear`: Checks if a given text contains any swear words.
  - `add_word` and `remove_word`: Allows for dynamically updating the list of swear words.

### Response Generators

Each response generator is designed for a specific type of response.

- **GreetingModel** (`GreetingModel.py`): Returns responses for greetings.
- **DislikeResponseGenerator** (`DislikeResponseGenerator.py`): Generates responses when the bot receives negative feedback.
- **IntroductionResponseGenerator** (`IntroductionResponseGenerator.py`): Provides introductory responses.
- **NotClearResponseGenerator** (`NotClearResponseGenerator.py`): Responds when the query is unclear.

## Running the Application

To start the application, run:

```bash
python app.py
```

This will launch the chatbot and allow you to interact with it through a command-line interface (or integrate with a web interface).

## Docker

The Dockerfile allows for easy containerization of the application. To build and run the Docker container:

```bash
docker build -t persian-chatbot .
docker run -p 8000:8000 persian-chatbot
```

## Configuration and Customization

- **Thresholds**: You can adjust the confidence thresholds for both general responses and greetings within the `ChatBot` class initializer.
- **Swear Words**: Update `swear_words.json` to modify the list of words flagged as inappropriate.
- **Frequency Dictionary**: Customize `frequency.csv` to influence the spell correction module.

## Future Improvements

- **Web Interface**: Add a web interface for a more user-friendly experience.
- **Enhanced NLP**: Incorporate more advanced Persian NLP techniques for better accuracy and context handling.
- **Custom Embeddings**: Experiment with different embedding models to improve similarity matching.

## Contributing

Contributions are welcome! Please open an issue to discuss potential improvements or submit a pull request.

## License

This project is licensed under the MIT License.