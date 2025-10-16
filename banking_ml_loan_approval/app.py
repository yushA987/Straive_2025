from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from sklearn.linear_model import LogisticRegression
import numpy as np

app = Flask(__name__)
# Use SQLite instead of MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
swagger = Swagger(app)

# -----------------
# Database model
# -----------------
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    balance = db.Column(db.Float)

with app.app_context():
    db.create_all()

# -----------------
# CRUD APIs
# -----------------
@app.route('/customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], age=data['age'], balance=data['balance'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'}), 200

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    result = [{'id': c.id, 'name': c.name, 'age': c.age, 'balance': c.balance} for c in customers]
    return jsonify(result)

@app.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    customer.name = data.get('name', customer.name)
    customer.age = data.get('age', customer.age)
    customer.balance = data.get('balance', customer.balance)
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})

@app.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})

# -----------------
# ML Model Training & Prediction
# -----------------
@app.route('/train', methods=['POST'])
def train_model():
    X = np.array([[25, 2000], [40, 6000], [50, 8000], [30, 3000]])
    y = np.array([0, 1, 1, 0])  # 0=low, 1=high income

    global model
    model = LogisticRegression()
    model.fit(X, y)
    return jsonify({'message': 'Model trained successfully'})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array([[data['age'], data['balance']]])
    prediction = model.predict(features)[0]
    return jsonify({'prediction': int(prediction)})


loan_model = None


@app.route('/train_loan', methods=['POST'])
def train_loan_model():
    # Sample data: [age, balance], 1 = eligible, 0 = not eligible
    X_loan = np.array([
        [25, 5000],
        [40, 10000],
        [50, 15000],
        [22, 2000],
        [35, 7000],
        [28, 3000]
    ])
    y_loan = np.array([1, 1, 1, 0, 1, 0])  # Eligibility labels

    global loan_model
    loan_model = LogisticRegression()
    loan_model.fit(X_loan, y_loan)
    return jsonify({'message': 'Loan approval model trained successfully'})


@app.route('/predict_loan', methods=['POST'])
def predict_loan():
    data = request.get_json()
    if loan_model is None:
        return jsonify({'error': 'Loan model is not trained yet'}), 400

    features = np.array([[data['age'], data['balance']]])
    prediction = loan_model.predict(features)[0]
    eligibility = 'Eligible' if prediction == 1 else 'Not Eligible'
    return jsonify({'loan_approval': eligibility})


if __name__ == '__main__':
    app.run(debug=True)
