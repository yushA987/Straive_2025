from flask import Flask

app = Flask(__name__)

@app.route("/<name>")
def print_hello(name):
    return f'Hello, {name}'

@app.route("/Add/<num1>/<num2>")
def calculate_add(num1, num2):
    n1 = int(num1)
    n2 = int(num2)
    res = n1 + n2
    return str(res)

@app.route("/Subtract/<num1>/<num2>")
def calculate_subtract(num1, num2):
    n1 = int(num1)
    n2 = int(num2)
    res = n1 - n2
    return str(res)

@app.route("/Multiply/<num1>/<num2>")
def calculate_multiply(num1, num2):
    n1 = int(num1)
    n2 = int(num2)
    res = n1 * n2
    return str(res)

if __name__ == '__main__':
    app.run(debug = True)