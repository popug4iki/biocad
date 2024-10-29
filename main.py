from flask import Flask, render_template, send_from_directory, request, make_response, jsonify
import transformers
import torch
import fitz
import re


def format_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    text = text.replace("\n", " ")
    text = re.sub(r'(?<=[.!?])\s', '\n', text)
    return text.strip()


def capitalize_sentences(text):
    return re.sub(r'(?<=[.!?])\s*(\w)', lambda x: ' ' + x.group(1).upper(), text.capitalize())


def remove_duplicates(text):
    seen = set()
    unique_lines = []

    for line in text.splitlines():
        if line not in seen:
            seen.add(line)
            unique_lines.append(line)

    return "\n".join(unique_lines)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = transformers.AutoModelForSeq2SeqLM.from_pretrained(
    "./exp_bart/model").to(device)
tokenizer = transformers.AutoTokenizer.from_pretrained("./exp_bart/tokenizer")


def chunk_text(text, tokenizer, max_length=512):
    tokens = tokenizer.encode(text)
    return [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:path>')
def static_1(path):
    return send_from_directory('static', path)


@app.route('/scripts/<path:path>')
def scripts(path):
    return send_from_directory('scripts', path)


@app.route('/api', methods=['POST'])
def api():
    file = request.files.get('file')
    percentage = int(request.form.get('percentage')) / 100

    if not file:
        return make_response(jsonify({"error": "Файл не загружен"}), 400)

    try:
        pdf_data = file.read()

        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        raw = "".join(page.get_text() for page in pdf_document)
        raw = remove_duplicates(raw)

        if not raw:
            return make_response(jsonify({"error": "Текст не был извлечен из PDF"}), 400)

        all_chunks = []
        chunks = chunk_text(raw, tokenizer)

        for chunk in chunks:
            inputs = {'input_ids': torch.tensor([chunk]).to(device)}
            outputs = model.generate(
                **inputs, max_length=int(percentage * len(chunk)))
            generated_text = tokenizer.decode(
                outputs[0], skip_special_tokens=True)
            all_chunks.append(generated_text)

        formatted_text = format_text(" ".join(all_chunks))

        return make_response(jsonify({"result": capitalize_sentences(formatted_text)}), 200)

    except Exception as e:
        print("Ошибка:", e)
        return make_response(jsonify({"error": "Ошибка при обработке файла"}), 500)


app.run(host='127.0.0.1', debug=True)
