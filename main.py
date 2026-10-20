from flask import Flask, jsonify, request

app = Flask(__name__)

# Приклад даних оцінок, які можна оновлювати або віддавати у твій Mini App
grades_db = {
    "Математика": [11, 10, 12],
    "Фізика": [10, 9],
    "Англійська мова": [11, 12],
    "Українська мова": [10, 11]
}

@app.route('/')
def home():
    return "Human.ua Backend is running successfully!"

@app.route('/api/grades', methods=['GET'])
def get_grades():
    return jsonify({"grades": grades_db})

@app.route('/api/grades', methods=['POST'])
def update_grades():
    global grades_db
    data = request.json
    if data and "grades" in data:
        grades_db = data["grades"]
        return jsonify({"status": "success", "grades": grades_db})
    return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
