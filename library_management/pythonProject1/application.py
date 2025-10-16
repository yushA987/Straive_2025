# from flask import Flask, jsonify, redirect
# from flask_restful import Api, MethodNotAllowed, NotFound
# from flask_cors import CORS
# from util.common import domain, port, prefix, build_swagger_config_json
# from resource.swaggerConfig import SwaggerConfig
# from resource.bookResource import BooksGETResource, BookGETResource, BookPOSTResource, BookPUTResource, BookDELETEResource
# from flask_swagger_ui import get_swaggerui_blueprint
#
# # ============================================
# # Main
# # ============================================
# application = Flask(__name__)
# app = application
# app.config['PROPAGATE_EXCEPTIONS'] = True
# CORS(app)
# api = Api(app, prefix=prefix, catch_all_404s=True)
#
# # ============================================
# # Swagger
# # ============================================
# build_swagger_config_json()
# swaggerui_blueprint = get_swaggerui_blueprint(
#     prefix,
#     f'http://{domain}:{port}{prefix}/swagger-config',
#     config={
#         'app_name': "Flask API",
#         "layout": "BaseLayout",
#         "docExpansion": "none"
#     },
# )
# app.register_blueprint(swaggerui_blueprint)
#
# # ============================================
# # Error Handler
# # ============================================
#
#
# @app.errorhandler(NotFound)
# def handle_method_not_found(e):
#     response = jsonify({"message": str(e)})
#     response.status_code = 404
#     return response
#
#
# @app.errorhandler(MethodNotAllowed)
# def handle_method_not_allowed_error(e):
#     response = jsonify({"message": str(e)})
#     response.status_code = 405
#     return response
#
#
# @app.route('/')
# def redirect_to_prefix():
#     if prefix != '':
#         return redirect(prefix)
#
#
# # ============================================
# # Add Resource
# # ============================================
# # GET swagger config
# api.add_resource(SwaggerConfig, '/swagger-config')
# # GET books
# api.add_resource(BooksGETResource, '/books')
# api.add_resource(BookGETResource, '/books/<int:id>')
# # POST book
# api.add_resource(BookPOSTResource, '/books')
# # PUT book
# api.add_resource(BookPUTResource, '/books/<int:id>')
# # DELETE book
# api.add_resource(BookDELETEResource, '/books/<int:id>')
#
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, jsonify, redirect
from flask_restful import Api, MethodNotAllowed, NotFound
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy

# Import the db object and Resources from bookResource
from resource.bookResource import (
    db, Book,
    BooksGETResource,
    BookGETResource,
    BookPOSTResource,
    BookPUTResource,
    BookDELETEResource
)

# Swagger config import
from resource.swaggerConfig import SwaggerConfig

# ============================================
# Environment Configuration
# ============================================
from util.common import domain, port, prefix, build_swagger_config_json

# ============================================
# Flask App Initialization
# ============================================
application = Flask(__name__)
app = application

# Enable CORS (Cross-Origin Resource Sharing)
CORS(app)

# SQLAlchemy Configuration (change credentials as per your setup)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB with the app
db.init_app(app)

# Flask-RESTful API Initialization
api = Api(app, prefix=prefix, catch_all_404s=True)

# Create tables (if not exists)
with app.app_context():
    db.create_all()

# ============================================
# Swagger UI Setup
# ============================================
build_swagger_config_json()

swaggerui_blueprint = get_swaggerui_blueprint(
    prefix,
    f'http://{domain}:{port}{prefix}/swagger-config',
    config={
        'app_name': "Flask API",
        "layout": "BaseLayout",
        "docExpansion": "none"
    },
)

app.register_blueprint(swaggerui_blueprint)

# ============================================
# Error Handlers
# ============================================
@app.errorhandler(NotFound)
def handle_method_not_found(e):
    return jsonify({"message": str(e)}), 404

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    return jsonify({"message": str(e)}), 405

@app.route('/')
def redirect_to_prefix():
    if prefix != '':
        return redirect(prefix)
    return "Flask API is running"

# ============================================
# Register API Resources
# ============================================
api.add_resource(SwaggerConfig, '/swagger-config')
api.add_resource(BooksGETResource, '/books')
api.add_resource(BookGETResource, '/books/<int:id>')
api.add_resource(BookPOSTResource, '/books')
api.add_resource(BookPUTResource, '/books/<int:id>')
api.add_resource(BookDELETEResource, '/books/<int:id>')

# ============================================
# Run the Application
# ============================================
if __name__ == '__main__':
    app.run(debug=True)
