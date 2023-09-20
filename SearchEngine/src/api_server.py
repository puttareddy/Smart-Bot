from flask import Flask, request, jsonify, Response
from activity_agent import SharedActivityAgent
from http import HTTPStatus
from FileParser import get_texts_from_files, get_pdf_texts, get_doc_texts

import sys
from streamlit.web import cli as stcli

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'docx', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/question', methods=['POST'])
def ask_question():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json_dict = request.json
        question = json_dict["question"]
        agentResponse = SharedActivityAgent.ask_question(question)
        json_object = jsonify(agentResponse)
        return json_object
    else:
        return 'Content-Type not supported!', 404
    
@app.route('/role', methods=['POST'])
def save_role():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json_dict = request.json
        role = json_dict["role"]
        SharedActivityAgent.save_role(role)
        return Response(status=200)
    else:
        return 'Content-Type not supported!', 404

@app.route('/file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            obj = { "error": "File not found"}
            return Response(status=HTTPStatus.NOT_ACCEPTABLE, response=obj)
        file = request.files['file']
        
        if file.filename == '':
            obj = { "error": "No file name"}
            return Response(status=HTTPStatus.NOT_ACCEPTABLE, response=obj)
        if file and allowed_file(file.filename):
            files = []
            files.append(file)
            fileText = ""
            if ".pdf" in file.filename:
                fileText = get_pdf_texts(files)
            elif ".docx" in file.filename:
                fileText = get_doc_texts(files)
            SharedActivityAgent.initialize_vector_store(text=fileText)
            return Response(status=200)

if __name__ == '__main__':
    print("Starting API server")
    app.run(debug=True, host='0.0.0.0', port=5003)