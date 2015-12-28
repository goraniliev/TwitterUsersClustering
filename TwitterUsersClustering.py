from flask import Flask, request
from api.API import get_api_instance
from db.Insert_users import insert_users_to_db

app = Flask(__name__)


@app.route('/')
def home_page():
    return app.send_static_file('home.html')


@app.route('/main', methods=['POST'])
def main_page():
    api = get_api_instance(request.form.get('consumer_key'), request.form.get('consumer_secret'),
                           request.form.get('access_token'), request.form.get('access_token_secret'))
    return app.send_static_file('main.html')


@app.route('/insert_users', methods=['POST'])
def insert_users():
    insert_users_to_db()
    return app.send_static_file('main.html')

if __name__ == '__main__':
    app.run(debug=True)
