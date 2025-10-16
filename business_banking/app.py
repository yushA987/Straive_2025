from flask import Flask, request, jsonify, make_response
import models_mongose
import services
import jwt
from datetime import datetime, timedelta
from functools import wraps
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import current_app
from flask_cors import CORS



SECRET_KEY = 'your-secret-key'  # Replace with strong secret in production
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=10)  # Token expires in 10 mins
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         auth_header = request.headers.get('Authorization')
#         if auth_header and auth_header.startswith('Bearer '):
#             token = auth_header.split(' ')[1]
#         if not token:
#             current_app.logger.warning(f"Unauthorized access attempt without token. Endpoint: {request.path}, IP: {request.remote_addr}")
#             return jsonify({'error': 'Token is missing! To get the token login'}), 401
#         try:
#             data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#             current_user = models_mongose.get_user_by_id(data['user_id'])
#             if not current_user:
#                 current_app.logger.warning(f"Token valid but user not found. UserID: {data['user_id']}, Endpoint: {request.path}")
#                 return jsonify({'error': 'User not found!'}), 401
#         except jwt.ExpiredSignatureError:
#             current_app.logger.warning(f"Expired token used. Endpoint: {request.path}, IP: {request.remote_addr}")
#             return jsonify({'error': 'Token has expired! Please login again'}), 401
#         except jwt.InvalidTokenError:
#             current_app.logger.warning(f"Invalid token used. Endpoint: {request.path}, IP: {request.remote_addr}")
#             return jsonify({'error': 'Invalid token!'}), 401
#         return f(current_user, *args, **kwargs)
#     return decorated
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')  # ✅ read from cookie

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = models_mongose.get_user_by_id(data['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except Exception as e:
            print(e)
            return jsonify({'error': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)
    return decorated



CORS(
    app,
    supports_credentials=True,
    origins=["http://localhost:3000"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)
if not os.path.exists('logs'):
    os.mkdir('logs')

log_handler = RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=3)
log_formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
log_handler.setFormatter(log_formatter)

app.logger.setLevel(logging.INFO)
app.logger.addHandler(log_handler)
@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()
        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']
        h = resp.headers

        h['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        h['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        h['Access-Control-Allow-Headers'] = headers or 'Content-Type, Authorization'
        h['Access-Control-Allow-Credentials'] = 'true'
        return resp

@app.route('/loan/<user_id>', methods=['GET'])
@token_required
def loan(current_user, user_id):
    if current_user['UserID'] != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    loan_type = request.args.get('type', 'home_loan').lower()

    if loan_type not in services.LOAN_RULES:
        return jsonify({"error": f"Invalid loan type '{loan_type}'. Choose from {list(services.LOAN_RULES.keys())}"}), 400

    result = services.check_loan_eligibility(current_user, loan_type)
    status_code = 200 if result["status"] == "success" else 400
    app.logger.info(f"User '{user_id}' checked eligibility for '{loan_type}' loan.")
    return jsonify(result), status_code


from flask import request, jsonify
import re
from werkzeug.security import generate_password_hash


@app.route('/update/<user_id>', methods=['PUT'])
@token_required
def update_user_details(current_user, user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Extract fields
    pan = data.get("PAN")
    tan = data.get("TAN")
    username = data.get("UserName")
    password = data.get("Password")
    salary = data.get("Salary")

    update_fields = {}

    # ✅ PAN/TAN (already implemented)
    if pan is not None:
        update_fields["PAN"] = pan
    if tan is not None:
        update_fields["TAN"] = tan

    # ✅ Username
    if username:
        update_fields["UserName"] = username

    # ✅ Password (with validation)
    if password:
        if len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400
        if not re.search(r"\d", password):
            return jsonify({"error": "Password must contain at least one digit"}), 400
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return jsonify({"error": "Password must contain at least one special character"}), 400

        hashed = generate_password_hash(password)
        update_fields["Password"] = hashed

    # ✅ Salary
    if salary is not None:
        try:
            salary = float(salary)
            update_fields["Salary"] = salary
        except ValueError:
            return jsonify({"error": "Invalid salary value"}), 400

    if not update_fields:
        return jsonify({"error": "No valid fields provided for update"}), 400

    # Call your model's update method (extend it to handle all fields, not just PAN/TAN)
    success = models_mongose.update_user(user_id, update_fields)

    if success:
        return jsonify({"message": "User details updated successfully"}), 200
    else:
        return jsonify({"error": "User not found or update failed"}), 404


@app.route('/users', methods=['GET'])
def get_all_users():
    users = models_mongose.get_all_users()
    user_list = [dict(user) for user in users]
    return jsonify(user_list), 200

@app.route('/user/<user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    if current_user['UserID'] != user_id:
        app.logger.warning(f"Unauthorized access attempt by {current_user['UserID']} for {user_id}")
        return jsonify({'error': 'Unauthorized access'}), 403

    user_dict = dict(current_user)
    user_dict.pop('Password', None)
    app.logger.info(f"User '{user_id}' accessed their details.")
    return jsonify(user_dict), 200

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    required_fields = {"UserID", "UserName", "Balance", "AccountType", "Salary", "Password"}

    if not data:
        return jsonify({"error": "No data provided"}), 400

    missing_fields = required_fields - data.keys()
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    try:
        user = {
            "UserID": data["UserID"],
            "UserName": data["UserName"],
            "Balance": float(data["Balance"]),
            "PAN": data.get("PAN"),
            "TAN": data.get("TAN"),
            "AccountType": data["AccountType"],
            "Salary": float(data["Salary"]),
            "Password": data["Password"]
        }

        models_mongose.insert_user(user)
        app.logger.info(f"New user created: {user['UserID']}")
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    deleted = models_mongose.delete_user_by_id(user_id)
    if deleted:
        app.logger.info(f"User '{user_id}' deleted from system.")
        return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     if not data or not data.get('UserID') or not data.get('Password'):
#         return jsonify({'error': 'UserID and Password required'}), 400
#     print(data["UserID"], data["Password"])
#     user = models_mongose.get_user_by_credentials(data['UserID'], data['Password'])
#     if user:
#         app.logger.info(f"User '{user['UserID']}' logged in successfully.")
#     else:
#         app.logger.warning(f"Failed login attempt for UserID '{user['UserID']}'")
#
#     if not user:
#         return jsonify({'error': 'Invalid UserID or Password'}), 401
#
#     token = generate_token(user['UserID'])
#     return jsonify({'token': token}), 200

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     if not data or not data.get('UserID') or not data.get('Password'):
#         return jsonify({'error': 'UserID and Password required'}), 400
#
#     user = models_mongose.get_user_by_credentials(data['UserID'], data['Password'])
#     if user:
#         app.logger.info(f"User '{user['UserID']}' logged in successfully.")
#     else:
#         app.logger.warning(f"Failed login attempt for UserID '{data.get('UserID')}'")
#         return jsonify({'status': 'fail', 'message': 'Invalid UserID or Password'}), 401
#
#     token = generate_token(user['UserID'])
#
#     # Remove password before sending back user data
#     if 'Password' in user:
#         user.pop('Password')
#
#     return jsonify({'status': 'success', 'token': token, 'user': user}), 200
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print("LOGIN DATA:", data)

    userid = data.get('username')
    password = data.get('password')

    # ✅ Authenticate using the helper
    user = models_mongose.get_user_by_credentials(userid, password)

    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    # ✅ Generate JWT token
    token = jwt.encode(
        {
            'user_id': user['UserID'],
            'exp': datetime.utcnow() + timedelta(minutes=15)
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    # ✅ Set token as HttpOnly cookie
    response = make_response(jsonify({
        'message': 'Login successful',
        'user': {
            'UserID': user['UserID'],
            'UserName': user['UserName'],
            'AccountType': user['AccountType'],
            'Balance': user['Balance']
        }
    }))
    response.set_cookie(
        'access_token',
        token,
        httponly=True,
        secure=False,      # True in production
        samesite='Lax',
        max_age=15 * 60    # 15 minutes
    )

    print("✅ Login successful for:", user['UserID'])
    return response


@app.route('/withdraw', methods=['POST'])
@token_required
def withdraw(current_user):
    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({"error": "Amount is required"}), 400

    amount = float(data['amount'])
    if amount <= 0:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    # Check if user has enough balance
    if current_user['Balance'] < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    try:
        # Deduct amount
        models_mongose.update_balance(current_user['UserID'], -amount)

        # Fetch updated user to return
        updated_user = models_mongose.get_user_by_id(current_user['UserID'])
        app.logger.info(f"User '{current_user['UserID']}' withdrew ₹{amount}")

        return jsonify({
            "status": "success",
            "message": f"Withdrew ₹{amount} successfully",
            "user": updated_user
        }), 200
    except Exception as e:
        app.logger.error(f"Withdraw failed: {str(e)}")
        return jsonify({"error": "Withdraw failed"}), 500


@app.route('/')
def home():
    return jsonify({"message": "Banking API running"}), 200

@app.route('/transfer', methods=['POST'])
@token_required
def transfer_funds(current_user):
    data = request.get_json()
    print(data)
    required_fields = {"ReceiverUserID", "Amount"}
    if not data or not required_fields <= data.keys():
        return jsonify({"error": "ReceiverUserID and Amount are required"}), 400

    receiver_id = data["ReceiverUserID"]
    amount = float(data["Amount"])

    if amount <= 0:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    sender = current_user
    if sender['UserID'] == receiver_id:
        return jsonify({"error": "Cannot transfer funds to the same account"}), 400

    receiver = models_mongose.get_user_by_id(receiver_id)
    if not receiver:
        return jsonify({"error": "Receiver account not found"}), 404

    if sender["Balance"] < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    try:
        models_mongose.update_balance(sender["UserID"], -amount)

        models_mongose.update_balance(receiver["UserID"], amount)

        updated_sender = models_mongose.get_user_by_id(sender["UserID"])
        updated_receiver = models_mongose.get_user_by_id(receiver["UserID"])

        app.logger.info(f"Transferred ₹{amount} from {sender['UserID']} to {receiver['UserID']}")

        return jsonify({
            "message": f"Transferred ₹{amount} to {receiver['UserID']} successfully",
            "sender": {
                "UserID": updated_sender["UserID"],
                "UserName": updated_sender.get("UserName"),
                "Balance": updated_sender["Balance"]
            },
            "receiver": {
                "UserID": updated_receiver["UserID"],
                "UserName": updated_receiver.get("UserName"),
                "Balance": updated_receiver["Balance"]
            }
        }), 200

    except Exception as e:
        app.logger.error(f"Transfer failed: {str(e)}")
        return jsonify({"error": "Transfer failed"}), 500

@app.route('/deposit', methods=['POST'])
@token_required
def deposit(current_user):
    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({"error": "Amount is required"}), 400

    amount = float(data['amount'])
    if amount <= 0:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    try:
        # Add amount to balance
        models_mongose.update_balance(current_user['UserID'], amount)
        updated_user = models_mongose.get_user_by_id(current_user['UserID'])

        app.logger.info(f"User '{current_user['UserID']}' deposited ₹{amount}")

        return jsonify({
            "status": "success",
            "message": f"Deposited ₹{amount} successfully",
            "user": updated_user
        }), 200
    except Exception as e:
        app.logger.error(f"Deposit failed: {str(e)}")
        return jsonify({"error": "Deposit failed"}), 500


@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Logged out successfully"})
    response.set_cookie('access_token', '', expires=0, httponly=True, samesite='Lax')
    return response

@app.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """
    Returns the currently authenticated user's details.
    """
    # You can choose what to return — here's a simple example:
    user_data = {
        "UserID": current_user.get("UserID"),
        "UserName": current_user.get("UserName"),
        "AccountType": current_user.get("AccountType"),
        "Salary": current_user.get("Salary"),
        "Balance": current_user.get("Balance"),
        "PAN": current_user.get("PAN"),
        "TAN": current_user.get("TAN"),
    }
    return jsonify(user_data), 200



if __name__ == "__main__":
    # models_mongose.init_db()
    app.run(debug=True)
