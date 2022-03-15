from moviesite import db, login_manager
from flask_login import UserMixin

# you cant get user id by this functions
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username
class Movie(db.Model):
    m_id = db.Column(db.Integer, primary_key=True)  
    movie_title = db.Column(db.String(80), nullable=False)
    movie_desc = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20))
    movie_link = db.Column(db.String(80))
    action = db.Column(db.Boolean, default=False)
    suspense = db.Column(db.Boolean, default=False)
    adventure = db.Column(db.Boolean, default=False)
    horror = db.Column(db.Boolean, default=False)
    comedy = db.Column(db.Boolean, default=False)
    scifci = db.Column(db.Boolean, default=False)
    release_date = db.Column(db.Integer)

    def __repr__(self):
        return f' {self.movie_title,self.movie_desc}'

category_movie_list =["action", "suspense", "adventure", "horror","comedy","scifci"] 
  