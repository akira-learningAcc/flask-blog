from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pytz
from datetime import datetime

import os

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

migrate = Migrate(app, db)

class Post(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       title = db.Column(db.String(255), nullable=False)
       body = db.Column(db.Text, nullable=False)
       tokyo_timezone = pytz.timezone('Asia/Tokyo')
       created_at = db.Column(db.DateTime,nullable=False,default=datetime.now(tokyo_timezone))
       img_name = db.Column(db.String(255),nullable=True)
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
                     #1.画像情報の取得
                     file = request.files['img']
                     #2.画像ファイル名の取得
                     filename = file.filename
                     #3.データベースにファイル名を保存
                     post = Post(title=title, body=body,img_name=filename)
                     #4.画像の保存
                     save_path = os.path.join(app.static_folder,'img',filename)
                     file.save(save_path)
                     db.session.add(post)
                     db.session.commit()
                     return redirect("/admin")
              elif request.method == "GET":
                     return render_template("create.html",method="GET")
       
@app.route("/<int:post_id>/update", methods=["GET","POST"])
def update(post_id):
              post = Post.query.get(post_id)
              if request.method == "POST":
                     post.title = request.form.get("title")
                     post. body = request.form.get("body")
                     db.session.commit()
                     return redirect("/admin")
              elif request.method == "GET":
                     return render_template("update.html",post=post)
@app.route("/<int:post_id>/delete")
def delete(post_id):
              post = Post.query.get(post_id)
              db.session.delete(post)
              db.session.commit()
              return redirect("/admin")