from flask import Flask, request, render_template
from chatbot import Bot, pairs

app = Flask(__name__)


chatbot = Bot(pairs)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    user_input = request.args.get('message', '').strip()
    mode = request.args.get('mode', 'chat')

    if not user_input:
        return {'response': 'Please type something.', 'sentiment': None}

    if mode == 'sentiment':
        sentiment_result = chatbot.sentimentfunction(user_input)
        return {
            'response': f"Analysis: {sentiment_result}",
            'sentiment': sentiment_result
        }
    else:
        bot_response = chatbot.chatfunction(user_input)
        return {
            'response': bot_response,
            'sentiment': None
        }

if __name__ == '__main__':
    app.run(debug=True, port=4500)