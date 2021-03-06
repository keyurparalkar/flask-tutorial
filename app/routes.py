from app import app,db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, ProfileEditForm, EmptyForm, BlogPostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
   # posts = [{'author':'KP','body':'HELLOW ORLD'},
    #        {'author':'JohnWick','body':'Willl'}]
    posts = current_user.followed_posts().all()
    return render_template('index.html',title="DEVPOST",posts=posts)


@app.route('/signin',methods=['GET','POST'])
def login():

    if(current_user.is_authenticated):
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if(form.validate_on_submit()):
        user = User.query.filter_by(username=form.username.data).first()
        if(user is None or not user.check_password(form.password.data)):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if(not next_page or url_parse(next_page).netloc!= ''):
            return redirect(url_for('index'))

        return redirect(next_page)
    
    return render_template('forms.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()

    if(form.validate_on_submit()):
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered !')
        return redirect(url_for('login'))

    return render_template('register.html',title='Registration',form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user,'post':'ABC1'},
        {'author':user}
        ]
    
    return render_template('user.html',user=user,posts=posts,form=form)

@app.route('/edit_profile',methods=['GET','POST'])
def edit_profile():
    form = ProfileEditForm()
    if form.validate_on_submit():
        user = current_user
        
        user.username = form.username.data
        user.about_me = form.about_me.data

        db.session.add(user)
        db.session.commit()

        flash('User changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html',title='Edit Profile',form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


        
@app.route('/follow/<username>',methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        
        if(user == current_user):
            flash('You cannot follow yourself !!!')
            return redirect(url_for('user',username=username))
        elif( user is None):
            flash('User does not exists')
            return redirect(url_for('index'))

        current_user.follow(user)
        db.session.commit()
        flash(f'You are now following {username}')
        return redirect(url_for('user',username=username))

    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
    
@app.route('/post_blog',methods=['POST','GET'])
@login_required
def post_blog():
    form = BlogPostForm(request.form)

    if form.validate() and request.method == 'POST':
        user = current_user
        post = Post(body=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Blog Post successfully created !')
        return redirect(url_for('index'))
        
    return render_template('post.html',form=form)
