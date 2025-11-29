from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_INFO = {
       'user': 'postgres',
       'password': 'password',
       'host': 'localhost',
       'port': '5432',
       'database': 'postgres'
}

db = SQLAlchemy()
SQLALCHEMY_DATABASE_URI = (
    "postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
).format(**DB_INFO)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

@app.route("/<int:number>")
def hello_world(number):
       posts = [
              {
                     'title': '記事のタイトル1',
                     'body': '記事の内容がここに入ります。',
                     'created_at': '2024-06-01 12:00'
              },{
                     'title': '記事のタイトル2',
                     'body': '記事の内容がここに入ります。',
                     'created_at': '2024-06-01 12:00'
              },{
                     'title': '記事のタイトル3',
                     'body': '記事の内容がここに入ります。',
                     'created_at': '2024-06-01 12:00'
              },{
                     'title': '記事のタイトル4',
                     'body': '記事の内容がここに入ります。',
                     'created_at': '2024-06-01 12:00'
              }
       ]
       post = posts[number]
       return render_template("admin.html",post=post)