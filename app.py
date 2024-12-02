from flask import Flask, request, jsonify
from settings import *
import openai

app = Flask(__name__)


from openai import OpenAI
client = OpenAI(
  api_key = OPEN_AI_KEY
)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Extract user query from Dialogflow's request
    user_query = req.get('queryInput', {}).get('text', {}).get('text', '')

    # Send user query to GPT API
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for answering all questions, mainly questions about cars."},
            {
                "role": "user",
                "content": user_query
            }
        ]
    )
    
    gpt_response = completion.choices[0].message.content.strip()
    
    # Return GPT response to Dialogflow
    return jsonify({
        "fulfillmentMessages": [
            {"text": {"text": [gpt_response]}}
        ]
    })

if __name__ == '__main__':
    app.run(port=5000)
