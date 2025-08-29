from flask import Flask, request, jsonify, redirect, url_for
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo

# Load environment variables from .env file
load_dotenv()

# MongoDB connection
mongo_uri = os.getenv('MONGO_URI')
client = pymongo.MongoClient(mongo_uri)  # type: ignore
db = client['ToDoApp']  # type: ignore
data_collection = db['ToDo']  # type: ignore

app = Flask(__name__)

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    data = request.form.to_json()
    data['submission_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_collection.insert_one(data)  # type: ignore
    # Assuming frontend will handle redirect or display after this
    return jsonify({'message': 'Submission successful'})

@app.route('/view', methods=['GET'])
def view():
    data = list(data_collection.find({}, {'_id': False}))
    return jsonify({'data': data})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=4000, debug=True)
