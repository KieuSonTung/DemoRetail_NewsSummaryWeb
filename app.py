from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

def get_data(gsheetid='1n8B1648GenFEgdNiwhXyKG3AxHcT9PCoHp09uY49exc', sheet_name='test'):
    # check folder data exists
    if not os.path.exists('data'):
        os.mkdir('data/')
    
    qna_path = 'data/qna.csv'
    # if data not available in local => download, else => load data
    if not os.path.exists(qna_path):
        gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, sheet_name)
        df = pd.read_csv(gsheet_url)
        df.to_csv('qna.csv', index=False)
    else:
        df = pd.read_csv(qna_path)
    
    return df

# find the answer
def get_answer(df, question):
    try:
        answer = df.loc[df['question'] == question, 'answer'].to_list()[0]
    except:
        answer = None
    return answer

@app.route("/", methods=["GET", "POST"])
def index():
    df = get_data()
    if request.method == "POST":
        button_value = request.form["button"]
        if button_value:
            answer = get_answer(df, button_value)
            return render_template("index.html", button_value=button_value, answer=answer)
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)