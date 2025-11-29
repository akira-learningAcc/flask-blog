from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
import pytz
from datetime import datetime

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


class Post(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       title = db.Column(db.String(255), nullable=False)
       body = db.Column(db.Text, nullable=False)
       tokyo_timezone = pytz.timezone('Asia/Tokyo')
       created_at = db.Column(db.DateTime,nullable=False,default=datetime.now(tokyo_timezone))

@app.route("/admin")
def admin():
       posts = Post.query.all()
       return render_template("admin.html",posts=posts)

@app.route("/create", methods=["GET","POST"])
def create():
       #リクエストのメソッドの判別
       if request.method == "POST":
              #リクエストできた情報の取得
              title = request.form.get("title")
              body = request.form.get("body")
              #情報の保存
              post = Post(title=title, body=body)
              db.session.add(post)
              db.session.commit()
              return redirect("/admin")
       elif request.method == "GET":
              return render_template("create.html",method="GET")
       
       
       