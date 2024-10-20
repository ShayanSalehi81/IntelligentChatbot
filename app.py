from flask import Flask, request, jsonify
from chatbot import Chatbot

app = Flask(__name__)

chatbot = Chatbot()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    response = chatbot.chat(query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
