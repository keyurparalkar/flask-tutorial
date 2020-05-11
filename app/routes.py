from app import app
from flask import render_template
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {"username":"Keyur Paralkar"}
    posts = [{"author":"John","body":"This is TEMP Page"}
             ,{"author":"Wick","body":"Focus, Commitment, and Sheer will !!"}]
    
    return render_template('index.html',title="KAP",user=user,posts=posts)


@app.route('/signin')
def login():
    form = LoginForm() 
    return render_template('forms.html',form=form)
