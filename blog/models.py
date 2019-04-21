from blog import db
from werkzeug.security import generate_password_hash, check_password_hash
from blog import login_manager
from flask_login import UserMixin  

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

user_favorite_post = db.Table('user-favorite-post', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True), 
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)

class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    favorite = db.relationship('Post'
                                ,secondary=user_favorite_post
                                ,lazy='subquery'
                                ,backref=db.backref('list_favorite_user', lazy=True))

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __init__(self, email):
        self.email = email

    def is_already_favorite(self, post_id):
        return post_id in self.favorite

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

post_category = db.Table('post-category',
                         db.Column('post_id', db.Integer, db.ForeignKey(
                             'posts.id'), primary_key=True),
                         db.Column('category_id', db.Integer, db.ForeignKey(
                             'category.id'), primary_key=True)
                         )
# Category & Post many-to-many relationship


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    comments = db.relationship('Comment', backref='belong_to_post', lazy=True)
    add_category = db.relationship('Category', secondary=post_category, lazy='subquery',
                                   backref=db.backref('list_post', lazy=True))

    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id

    def __repr__(self):
        return(f'This post has title {self.title}')


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        print(f'Category: {self.name}')


class Comment(db.Model):

    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, content, user_id, post_id):
        self.content = content
        self.user_id = user_id
        self.post_id = post_id

    def __repr__(self):
        print(f'Comment content: {self.content}, belongs to author {self.user_id}, belongs to post {self.post_id} ')

