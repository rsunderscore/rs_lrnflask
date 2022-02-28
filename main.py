from flask import Flask, render_template, flash, redirect
#where do these come from Engine

from config import DevConfig
#wtforms
from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
#model
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func, event
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text
import datetime



app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


#force sqlite to enforce FK contraints (perf penalty) 
#other dbs do this by default
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class User(db.Model):
    #__tablename__ = 'user_table_name' #connect to existing table
    
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255))
    
    def __init__(self, username):
        self.username = username
        
    def __repr__(self):
        return "<User '{}'>".format(self.username)
    

#set up many-to-many relationship
#db.Table more granular than db.Model - use when there is no need to access each row
tags = db.Table('post_tags', 
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')), 
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))
    
class Post(db.Model):
    #__tablename__ = 'user_table_name' #connect to existing table
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime(), default=datetime.datetime.now)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    #use many-to-many relationship
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))
    
    def __init__(self, title):
        self.title = title
        
    def __repr__(self):
        return "<Post '{}'>".format(self.title)

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=True, unique=True)
    def __init__(self, title):
        self.title = title
    def __repr__(self):
        return "<Tag '{}'>".format(self.title)

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    
    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])

db.Index('idx_col_example', User.username, User.password) #multi-column index
@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    #return '<h1>Hello World!</h1>'
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    recent, top_tags = sidebar_data()
    return render_template('home.html', posts=posts, recent=recent, top_tags = top_tags)

def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    #research func.count
    top_tags = db.session.query(Tag, 
                                func.count(tags.c.post_id).label('total')).join(tags).group_by(Tag).order_by(text('total DESC')).limit(5).all()
    
    return recent, top_tags

class CommentForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    text = TextAreaField(u'Comment', validators = [DataRequired()])

@app.route('/post/<int:post_id>', methods=('GET', 'POST'))
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        try:
            db.session.add(new_comment)
            db.session.commit()
        except Exception as e:
            flash('Error adding your comment: %s' % str(e), 'error')
            db.session.rollback()
        else:
            flash('Comment added', 'info')
        return redirect(url_for('post', post_id=post_id))
    
    post = Post.query.get+_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()
    
    return render_template('post.html', post=post, tags=tags, comments=comments, recent=recent, top_tags=top_tags, form=form)

if __name__ == '__main__':
    app.run()