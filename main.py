from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__, static_folder='.')

# Віддаємо наш index.html на головній сторінці
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Віддаємо будь-які додаткові статичні файли (CSS, JS, картинки), якщо вони є
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# Ендпоінти API для даних
@app.route('/api/grades', methods=['GET'])
def get_grades():
    return jsonify({
        "status": "success",
        "grades": {
            "Математика": [11, 10, 12],
            "Фізика": [10, 9],
            "Англійська мова": [11, 12],
            "Українська мова": [10, 11]
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
