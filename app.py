from flask import Flask, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return "Hello, Azure! Your Flask app is running."

# Define a route for an API endpoint that returns JSON
@app.route('/api/data')
def get_data():
    data = {
        "message": "Welcome to the Flask API!",
        "status": "success"
    }
    return jsonify(data)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
