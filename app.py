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

sessions = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    session_id = req.get('session', '')

    # Extract user query from Dialogflow's request
    user_query = req.get('queryResult', {}).get('queryText', '')
    
    print(f"Web hook is getting triggered: {req}")
    logging.info(f"Handling a request to endpoint: {req}")
    logging.info("===================================================================================")

     # Initialize conversation for the session if it doesn't exist
    if session_id not in sessions:
        sessions[session_id] = [
            {
                "role": "system",
                "content": "You are a helpful assistant for answering all questions, mainly questions about cars. Also don't give the answer in bold text. Give normal only. Everytime give me answers in single paragraph."
            }
        ]
    
    # Add user query to the session's message history
    sessions[session_id].append({"role": "user", "content": user_query})

    # # Send user query to GPT API
    # completion = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant for answering all questions, mainly questions about cars. Also don't give the answer in bold text. Give normal only. Everytime give me answers in single paragraph."},
    #         {
    #             "role": "user",
    #             "content": user_query
    #         }
    #     ]
    # )
    
    # Send conversation history to GPT API
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=sessions[session_id]
    )
    
    gpt_response = completion.choices[0].message.content.strip()
    sessions[session_id].append({"role": "assistant", "content": gpt_response})
    
    logging.info(f"Output response: {completion}")
    logging.info("===================================================================================")
    logging.info(f"Final response: {gpt_response}")
    
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
