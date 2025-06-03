#not using modularity, just paths
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from flask import Flask, request, jsonify
from flask_cors import CORS
from llama_engine import Llama_MainClass as LMC

Advisor = LMC.MainClass

app = Flask(__name__)
CORS(app)

@app.route('/api/run', methods=['POST'])
def run():
    data = request.get_json()
    prompt = data.get('prompt')

    prompting = Advisor(prompt)
    result = prompting.run()
    return jsonify(result) 

if __name__ == '__main__':
    app.run(port=5000)
