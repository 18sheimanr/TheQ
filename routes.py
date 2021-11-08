import datetime

from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_required, logout_user, current_user, login_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length

from app import app, db
from models import User
from spotify_client import get_user_playlists

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('.index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    class eventNameForm(FlaskForm):
        name=StringField('Event Name', validators=[Length(min=3)])
        submit = SubmitField('Go')
    form = eventNameForm()
    if form.validate_on_submit():
        return redirect(url_for('.event', event_name=form.name.data))
    else:
        return render_template('index.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('.signUp'))
    else:
        return render_template('profile.html')


@app.route('/signIn', methods=['GET', 'POST'])
def signIn():

    class loginForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password')
        submit = SubmitField('Sign In')

    form = loginForm()
    if form.validate_on_submit():
        name = request.form['username']
        user = User.query.filter_by(username=name).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('.index'))
        else:
            flash('Invalid username or password.')
            return render_template('signIn.html', form=form)
    else:
        return render_template('signIn.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signUp():

    class signUpForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[
            DataRequired(), EqualTo('confirm_password', message='Passwords must match.')])
        confirm_password = PasswordField(
            'Confirm Password', validators=[DataRequired()])
        def validate_username(self, field):
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already in use.')
        submit = SubmitField('Sign Up')

    form = signUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('You can now login.')
            return redirect(url_for('.signIn'))
        except Exception:
            return "Could not register!"
    else:
        return render_template('signup.html', form=form)


@app.route('/event', methods=['GET', 'POST'])
def event():
    event_name = request.args.get("event_name", None)
    return render_template('event.html', event_name=event_name)


@app.route('/start_event', methods=['GET', 'POST'])
@login_required
def start_event():
    class eventForm(FlaskForm):
        name = StringField('name', validators=[DataRequired(), Length(min=3)])
        playlistId = StringField('Playlist ID', validators=[DataRequired(), Length(min=16)])
    if session.get('spotify_token', None) is None \
            or session.get('spotify_token_expires', None) is None \
            or session['spotify_token_expires'] < datetime.datetime.now():
        return redirect('/spotifyAuth')
    else:
        form = eventForm()
        if form.validate_on_submit():
            return redirect(url_for('.event', event_name=form.name, playlistId=form.playlistId))
        playlists = get_user_playlists()
        return render_template('startEvent.html', playlists=playlists, form=form)