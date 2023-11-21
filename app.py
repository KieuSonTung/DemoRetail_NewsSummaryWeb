from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def get_answer(question, gsheetid='1n8B1648GenFEgdNiwhXyKG3AxHcT9PCoHp09uY49exc', sheet_name='test'):
    gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, sheet_name)
    qna_df = pd.read_csv(gsheet_url)
    try:
        answer = qna_df.loc[qna_df['question'] == question, 'answer'].to_list()[0]
    except:
        answer = None
    return answer

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        button_value = request.form["button"]
        if button_value:
            answer = get_answer(button_value)
            return render_template("index.html", button_value=button_value, answer=answer)
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)