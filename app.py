from flask import Flask, request, jsonify
from settings import *
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

OPEN_AI_KEY = os.getenv("OPEN_AI")

from openai import OpenAI
client = OpenAI(
  api_key = OPEN_AI_KEY
)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Extract user query from Dialogflow's request
    user_query = req.get('queryResult', {}).get('queryText', '')
    
    print(f"Web hook is getting triggered: {req}")
    logging.info(f"Handling a request to endpoint: {req}")

    # Send user query to GPT API
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for answering all questions, mainly questions about cars. Also don't give the answer in bold text. Give normal only."},
            {
                "role": "user",
                "content": user_query
            }
        ]
    )
    
    gpt_response = completion.choices[0].message.content.strip()
    
    # Return GPT response to Dialogflow
    return jsonify({
        "fulfillmentText": gpt_response,
        "fulfillmentMessages": [
            {"text": {"text": [gpt_response]}}
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))  # Default to 8000 if PORT is not set
    app.run(host='0.0.0.0', port=port)
