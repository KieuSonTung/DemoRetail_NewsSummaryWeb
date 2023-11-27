from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

def get_data(gsheetid='1wq0ouJmxR9sUQMHlsQHKqzeBdVl5dHYEC8gqMCembCg', sheet_name='Sheet1'):
    # check folder data exists
    if not os.path.exists('data'):
        os.mkdir('data/')
    
    qna_path = 'data/qna.csv'
    # if data not available in local => download, else => load data
    if not os.path.exists(qna_path):
        gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, sheet_name)
        df = pd.read_csv(gsheet_url)
        df.to_csv(qna_path, index=False)
    else:
        df = pd.read_csv(qna_path)
    return df

def load_questions_and_answers():
    data = get_data()
    questions = data['question'].tolist()
    answers = data['answer'].tolist()
    return questions, answers

@app.route("/")
def index():
    questions, answers = load_questions_and_answers()
    return render_template('index.html', questions=questions, answers=answers)

if __name__ == "__main__":
    app.run(debug=True)