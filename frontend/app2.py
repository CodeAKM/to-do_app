from flask import Flask, render_template
from flask import Flask, request, render_template, redirect, url_for, flash
from datetime import datetime
import requests

BACKEND_URL = 'http://127.0.0.0:4000'

app = Flask(__name__)

def submit():
    form_data = dict(request.form)
    try:
        response = requests.post(BACKEND_URL + '/submit', json=form_data)
        if response.ok:
            return redirect(url_for('success'))
        else:
            error_message = response.json().get('message', 'Submission failed.')
            flash(error_message)
            return redirect(url_for('home'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('home'))


@app.route('/', methods=['GET'])
def form():
    current_day = datetime.now().strftime("%A")
    current_time = datetime.now().strftime("%H:%M:%S")
    return render_template('form.html', current_day=current_day, current_time=current_time)

@app.route('/submit')
def submit_form():
    return render_template('submit.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)
