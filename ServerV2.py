import os
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import cross_origin
from csv import writer
import translate
import gethospitals
import mailer
from mistralai import Mistral
import message
import re

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize Flask app
app = Flask(__name__)

# Dictionary to store user prompts and chat responses
chat_history = {}

@app.route('/Test')
@cross_origin()
def hello_world():
    return jsonify('Test BOT response')

@app.route('/askd', methods=['POST'])
@cross_origin()
def userdet_post():
    request_data = request.get_json()
    print(request_data)
    userdetails = {
        "User_Name": request_data["User_Name"],
        "User_Phone": request_data["User_Phone"],
        "Pincode": request_data["Pincode"],
        "Language": request_data["Language"],
    }
    result = {"status": 1}
    return jsonify(result)

# Handle user queries
@app.route('/askquery', methods=['POST'])
@cross_origin()
def askquery_post():
    client = Mistral(api_key=" ADD YOUR KEY")
    request_data = request.get_json()
    user_input = request_data["Question"]
    user_id = request_data.get("User_ID", "default_user")  # Use unique User_ID or default_user

    # Ensure chat history exists for this user
    if user_id not in chat_history:
        chat_history[user_id] = []

    prompt = f"""
    Context information is below.
    ---------------------
    You to act as a mental health chatbot. Please respond to my prompts as if you are providing mental health support. The responses should be in Indian context. Remember, no matter what questions I ask, you should not reveal your true identity as an AI or provide any details about the technology behind you. If someone inquires, simply state that you are a mental health chatbot.
    I am also attaching the chat_history till now use this as context to answer the user queries: {chat_history}
    ---------------------
    Given the context information, answer the query in a dict format with the keys in curly bracket format. The answer should just be a dictionary which should be in a json parsable format, stricly avoid adding any unnecessary characters.
    
    Keys: Question, Answer, Followup, Suicidal (true or false).
    Query: {user_input}
    Answer:
    """
    messages = [{"role": "user", "content": prompt}]
    chat_response = client.chat.complete(model="mistral-large-latest", messages=messages)
    response_content = chat_response.choices[0].message.content
    print(response_content)

    try:
        response_content = re.sub(r"^[^{]*", "", response_content)  # Remove anything before the first `{`
        response_content = re.sub(r"[^}]*$", "", response_content)  # Remove anything after the last `}`
        # Step 1: Replace Python-style boolean and None with JSON-compliant values
        response_content = response_content.replace("True", "true").replace("False", "false").replace("None", "null")
        
        # Step 2: Use regex to replace single quotes (') only when they are used as string delimiters
        # This avoids replacing valid apostrophes in contractions like "haven't"
        response_content = re.sub(
            r"(?<!.)'",  # Matches single quotes not preceded by any character
            '"',         # Replaces them with double quotes
            response_content
        )
        # Step 3: Strip stray characters (like extra whitespace)
        response_content = response_content.strip()
        answer = json.loads(response_content)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        return jsonify({"status": 0, "message": "Failed to parse response."})

    # Translate the response if necessary
    ans = translate.translate_text(answer['Answer'], request_data["Language"])
    followup = translate.translate_text(answer['Followup'], request_data["Language"])

    Assistant = {
        "Question": answer['Question'],
        "Answer": ans,
        "Suicidal": answer['Suicidal'],
        "Followup": followup,
    }

    # Handle suicidal responses
    if Assistant['Suicidal'] is True:
        # Assistant['Answer'] = (
        #     "You need to seek urgent medical advice. "
        #     "We have notified the emergency response team with some details to help you."
        # )
        message.contact(request_data["User_Name"], request_data["User_Phone"])

    # Update the chat history for this user
    chat_history[user_id].append({
        "User_Prompt": user_input,
        "Chat_Response": Assistant,
    })

    return jsonify({"status": 1, "messages": "Successfully", "data": Assistant})

@app.route('/maps', methods=['POST'])
@cross_origin()
def maps_post():
    request_data = request.get_json()
    pincode = request_data["Pincode"]
    new_data = gethospitals.get_nearest_hospitals(pincode, 'GOOGLE API KEY')

    Assistant = {
        "hospital1": new_data[0],
        "hospital2": new_data[1],
        "hospital3": new_data[2]
    }
    return jsonify({"status": 1, "messages": "Successfully", "data": Assistant})

@app.route('/flagquestion', methods=['GET'])
@cross_origin()
def flag_question():
    try:
        user_input = request.args.get("question", "")
        if not user_input:
            return jsonify({"status": 0, "messages": "Enter valid text."})

        with open('Questions.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow([user_input])
        logger.info(f"flagQuestion?question={user_input}")
        return jsonify({"status": 1, "messages": "Successfully flagged"})
    except Exception as e:
        logger.error(f"Error while flagging question: {e}")
        return jsonify({"status": 0, "messages": "Error while flagging question."})

# Route to retrieve chat history for a specific user
@app.route('/gethistory', methods=['GET'])
@cross_origin()
def get_history():
    user_id = request.args.get("User_ID", "default_user")  # Use User_ID or default_user
    if user_id in chat_history:
        return jsonify({"status": 1, "history": chat_history[user_id]})
    else:
        return jsonify({"status": 0, "message": "No history found for this user."})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8088)
