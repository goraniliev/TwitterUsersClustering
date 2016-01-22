from flask import Flask, request
from api.API import get_api_instance
from clustering.kmedoids import get_clusters
from db.Insert_users import insert_users_from_time_to_db, set_auto_increment_keys_for_already_inserted_users

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
    api = get_api_instance()
    first = int(request.form.get('first_page'))
    last = int(request.form.get('last_page'))
    insert_users_from_time_to_db(api, first, last)
    return app.send_static_file('main.html')


@app.route('/modify_users', methods=['POST'])
def set_keys():
    api = get_api_instance()
    set_auto_increment_keys_for_already_inserted_users(api)
    return app.send_static_file('home.html')


@app.route('/show_clusters', methods=['GET', 'POST'])
def show_clusters():
    clusters = get_clusters()
    for c in clusters:
        print len(clusters[c])
    return app.send_static_file('main.html')


if __name__ == '__main__':
    app.run(debug=True)
