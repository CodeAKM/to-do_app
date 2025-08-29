from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo

# Load environment variables from .env file
load_dotenv()

# MongoDB connection
mongo_uri = os.getenv('MONGO_URI')

client = pymongo.MongoClient(mongo_uri) # type: ignore
db = client['ToDoApp'] # type: ignore
data_collection = db['ToDo'] # type: ignore

app = Flask(__name__)


@app.route('/', methods=['GET'])
def form():
    current_day = datetime.now().strftime("%A")
    current_time = datetime.now().strftime("%H:%M:%S")
    return render_template('form.html', current_day=current_day, current_time=current_time)

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    data = request.form.to_dict()
    data['submission_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_collection.insert_one(data) # type: ignore
    return redirect(url_for('submit_form'))

@app.route('/submit')
def submit_form():
    return render_template('submit.html')

@app.route('/view', methods=['GET'])
def view():
    data = list(data_collection.find({}, {'_id': False}))
    return {'data': data}

if __name__ == "__main__":
    app.run(debug=True)