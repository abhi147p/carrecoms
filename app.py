from flask import Flask, request, jsonify
from settings import *
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = OPEN_AI_KEY

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Extract user query from Dialogflow's request
    user_query = req['queryResult']['queryText']

    # Send user query to GPT API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Choose your GPT model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_query}
        ]
    )

    # Extract GPT response
    gpt_response = response['choices'][0]['message']['content'].strip()

    # Return GPT response to Dialogflow
    return jsonify({
        "fulfillmentMessages": [
            {"text": {"text": [gpt_response]}}
        ]
    })

if __name__ == '__main__':
    app.run(port=5000)
