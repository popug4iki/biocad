from flask import Flask, render_template, send_from_directory, request, make_response, jsonify
import transformers
import torch
import PyPDF2
import re
import io


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
    source_id = request.form.get(
        'source-id') or (request.json.get('source-id') if request.is_json else None)
    percentage = request.form.get('percentage') or (
        request.json.get('percentage') if request.is_json else None)

    if source_id not in ['0', '1']:
        return make_response(jsonify({"error": "Неверный source-id"}), 400)

    try:
        percentage = int(percentage) / 100 if percentage is not None else 1.0
    except ValueError:
        return make_response(jsonify({"error": "Неверное значение percentage"}), 400)

    all_chunks = []

    try:
        if source_id == '1':
            file = request.files.get('file')
            if not file:
                return make_response(jsonify({"error": "Файл не загружен"}), 400)

            pdf_data = file.read()
            pdf_file = io.BytesIO(pdf_data)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            raw = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                raw += page.extract_text() or ""

            raw = remove_duplicates(raw)

            if not raw:
                return make_response(jsonify({"error": "Текст не был извлечен из PDF"}), 400)

            chunks = chunk_text(raw, tokenizer)
            for chunk in chunks:
                inputs = {'input_ids': torch.tensor([chunk]).to(device)}
                outputs = model.generate(
                    **inputs, max_length=int(percentage * len(chunk))
                )
                generated_text = tokenizer.decode(
                    outputs[0], skip_special_tokens=True)
                all_chunks.append(generated_text)

        elif source_id == '0':
            if request.is_json:
                data = request.get_json()
                text = data.get('text', "")
            else:
                text = request.form.get('text', "")

            if not text:
                return make_response(jsonify({"error": "Текст не был предоставлен"}), 400)

            text = remove_duplicates(text)
            chunks = chunk_text(text, tokenizer)
            for chunk in chunks:
                inputs = {'input_ids': torch.tensor([chunk]).to(device)}
                outputs = model.generate(
                    **inputs, max_length=int(percentage * len(chunk))
                )
                generated_text = tokenizer.decode(
                    outputs[0], skip_special_tokens=True)
                all_chunks.append(generated_text)

        formatted_text = format_text(" ".join(all_chunks))
        return make_response(jsonify({"result": capitalize_sentences(formatted_text)}), 200)

    except Exception as e:
        print("Ошибка:", e)
        return make_response(jsonify({"error": "Ошибка при обработке запроса"}), 500)


app.run(host='127.0.0.1', debug=False)
