# from flask import Flask
# from itsdangerous.url_safe import URLSafeTimedSerializer

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'R5k123x?fW76wwER,mP'  # Replace with your actual secret key

# # Initialize the URLSafeTimedSerializer
# serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'], expires_in=3600)  # Expires in 1 hour

# @app.route("/generate_token/<int:user_id>")
# def generate_token(user_id):
#     # Generate a token for the given user ID
#     token = serializer.dumps({'user_id': user_id})
#     return f"Your token: {token}"

# @app.route("/verify_token/<token>")
# def verify_token(token):
#     try:
#         data = serializer.loads(token, max_age=3600)  # Verify token (1-hour validity)
#         user_id = data.get('user_id')
#         return f"User ID: {user_id}"
#     except Exception as e:
#         return f"Invalid or expired token: {str(e)}"

# if __name__ == "__main__":
#     app.run(debug=True)
