from flask import Flask, render_template
import transformers
import torch


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = transformers.AutoModelForSeq2SeqLM.from_pretrained("./exp_bart/model").to(device)
tokenizer = transformers.AutoTokenizer.from_pretrained("./exp_bart/tokenizer")


def chunk_text(text, tokenizer, max_length=512):
    tokens = tokenizer.encode(text)
    return [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('')
# def api():
#     pass


app.run(host='0.0.0.0', debug=True)
