from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.json
    # Faça alguma lógica com os dados recebidos do frontend
    result = {'message': 'Dados recebidos com sucesso!', 'data': data}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
