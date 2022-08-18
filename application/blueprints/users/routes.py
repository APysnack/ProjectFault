from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, current_app
from flask_login import login_user, current_user, logout_user, login_required
from application import db, bcrypt
from application.models import Artwork, PostComment, User, Post, Writings, Video, Project, Audio, AudioLike, VideoLike, WritingsLike, ProjectDislike, ProjectLike, ArtworkLike
from application.blueprints.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, MassEmailForm,
                                                RequestResetForm, ResetPassword, AdminForm, UpdateUserForm, VideoForm, WritingForm, ProjectForm, AudioForm, ArtworkForm)
from application.blueprints.users.utils import save_picture, send_email_confirmation, send_reset_email, send_mass_email
from werkzeug.utils import secure_filename
import markdown
import os
import math

users = Blueprint('users', __name__)


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if current_user.rank == 'admin':
        return redirect(url_for('users.admin'))
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_picture(form.image.data, 'avatar')
            current_user.image_file = image_file
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email

    image_file = url_for('static', filename='images/' +
                         current_user.image_file)

    liked_videos = []
    my_videos = current_user.liked_videos
    for video in my_videos:
        liked_videos.append(Video.query.filter_by(id=video.video_id).first())

    liked_posts = []
    my_posts = current_user.liked_post
    for post in my_posts:
        liked_posts.append(Post.query.filter_by(id=post.post_id).first())

    # may go back and sort these by date, but this functionality is adequate for the beta version of the site
    liked_artwork = []
    my_artwork = current_user.liked_artwork
    for artwork in my_artwork:
        liked_artwork.append(Artwork.query.filter_by(
            id=artwork.artwork_id).first())

    # allocates the number of images that should appear in each column e.g. if 12 liked images, array results in [3, 3, 2, 2]
    baseNum = math.floor(len(liked_artwork) / 4)
    arrayLengths = [baseNum, baseNum, baseNum, baseNum]
    remainders = len(liked_artwork) % 4
    for i in range(remainders):
        arrayLengths[i] = arrayLengths[i] + 1

    liked_writings = []
    my_writings = current_user.liked_writing
    for writing in my_writings:
        liked_writings.append(Writings.query.filter_by(
            id=writing.writings_id).first())

    liked_audios = []
    my_audios = current_user.liked_audio
    for audio in my_audios:
        liked_audios.append(Audio.query.filter_by(
            id=audio.audio_id).first())

    user_posts = current_user.posts

    page = request.args.get('page', 1, type=int)
    forum_posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)

    return render_template('users/account.html', title='Account', forum_posts=forum_posts, user_posts=user_posts, image_file=image_file, form=form, liked_videos=liked_videos, liked_posts=liked_posts, liked_artwork=liked_artwork, liked_writings=liked_writings, liked_audios=liked_audios, arrayLengths=arrayLengths)


@ users.route("/admin", methods=["GET", "POST"])
@ login_required
def admin():
    if current_user.rank != 'admin':
        return redirect(url_for('main.index'))
    form = AdminForm()
    artwork_form = ArtworkForm()
    audio_form = AudioForm()
    project_form = ProjectForm()
    videoForm = VideoForm()
    writingForm = WritingForm()
    mass_email_form = MassEmailForm()
    update_form = UpdateUserForm()

    if writingForm.validate_on_submit():
        md_content = markdown.markdown(
            writingForm.content.data, extensions=['nl2br'])

        writing = Writings(user_id=current_user.id, title=writingForm.title.data,
                           details=writingForm.details.data, content=md_content, tag=writingForm.tag.data)
        db.session.add(writing)
        db.session.commit()
        flash('Writing has been added!', 'success')
        return redirect(url_for('users.admin'))

    if videoForm.validate_on_submit():
        video = Video(user_id=current_user.id, title=videoForm.title.data,
                      url=videoForm.url.data, tag=videoForm.tag.data)
        db.session.add(video)
        db.session.commit()
        flash('Video has been added!', 'success')
        return redirect(url_for('users.admin'))

    if project_form.validate_on_submit():
        project = Project(title=project_form.title.data, details=project_form.details.data,
                          completion_time=project_form.completion_time.data)
        db.session.add(project)
        db.session.commit()
        flash('Project has been added!', 'success')
        return redirect(url_for('users.admin'))

    if audio_form.validate_on_submit():
        audio_file = audio_form.audio.data
        audio_filename = secure_filename(audio_file.filename)
        file_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'], audio_filename)
        audio_file.save(file_path)
        image_file = save_picture(audio_form.image.data, 'audio_img')
        audio_lyrics = markdown.markdown(
            audio_form.lyrics.data, extensions=['nl2br'])
        audio = Audio(user_id=current_user.id, title=audio_form.title.data, lyrics=audio_lyrics,
                      image_file=image_file, tag=audio_form.tag.data, url=audio_filename)
        db.session.add(audio)
        db.session.commit()
        flash('Audio has been added!', 'success')
        return redirect(url_for('users.admin'))

    if artwork_form.validate_on_submit():
        if artwork_form.artwork.data:
            art_link = save_picture(artwork_form.artwork.data, 'artwork')
            artwork = Artwork(user_id=current_user.id,
                              image_file=art_link, tag=artwork_form.tag.data)
            db.session.add(artwork)
            db.session.commit()
            flash('Artwork has been added!', 'success')
            return redirect(url_for('users.admin'))

    if form.validate_on_submit():
        if form.image.data:
            image_file = save_picture(form.image.data, 'avatar')
            current_user.image_file = image_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.admin'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' +
                         current_user.image_file)

    if mass_email_form.validate_on_submit():
        title = mass_email_form.title.data
        content = mass_email_form.content.data
        members = User.query.filter_by(rank='member').all()
        send_mass_email(title, content, members)
        flash('Email successfully sent to all registered users!', 'success')
        return redirect(url_for('users.admin'))

    if update_form.validate_on_submit():
        if current_user.rank == 'admin':
            user_to_modify = update_form.username.data
            print(user_to_modify)
            rank = update_form.memberType.data
            user = User.query.filter_by(username=user_to_modify).first()
            print(user)
            if(rank == 'remove'):
                print(user.id)
                PostComment.query.filter_by(user_id=user.id).delete()
                Post.query.filter_by(user_id=user.id).delete()
                User.query.filter_by(id=user.id).delete()
                db.session.commit()
                flash('User successfully deleted', 'success')
            else:
                user.rank = rank
                db.session.commit()
                flash('User successfully updated', 'success')
        return redirect(url_for('users.admin'))

    return render_template('users/admin.html', title='Admin', update_form=update_form, mass_email_form=mass_email_form, image_file=image_file, form=form, artwork_form=artwork_form, writing_form=writingForm, video_form=videoForm, project_form=project_form, audio_form=audio_form)


@users.route("/confirm_registration/<token>", methods=['GET', 'POST'])
def confirm_registration(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('You have entered an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    elif user.rank == 'member':
        return redirect(url_for('main.index'))
    else:
        user.rank = 'member'
        db.session.commit()
        flash(f'Thank you! You have successfully completed your registration!', 'success')
        return redirect(url_for('main.media'))


@users.route('/like-content', methods=["POST", "GET"])
def like_content():
    if request.method == 'POST':
        content = request.get_json()
        if content["content_type"] == 'video':
            video = Video.query.filter_by(id=content["id"]).first()

            if content["liked_by_user"]:
                if current_user.has_liked_video(video):
                    pass
                else:
                    current_user.like_video(video)
            else:
                if current_user.has_liked_video(video):
                    current_user.unlike_video(video)
                else:
                    pass

        if content["content_type"] == 'post':
            post = Post.query.filter_by(id=content["id"]).first_or_404()

            if content["liked_by_user"]:
                if current_user.has_liked_post(post):
                    pass
                else:
                    current_user.like_post(post)
            else:
                if current_user.has_liked_post(post):
                    current_user.unlike_post(post)
                else:
                    pass

        if content["content_type"] == 'text':
            writing = Writings.query.filter_by(id=content["id"]).first_or_404()

            if content["liked_by_user"]:
                if current_user.has_liked_writing(writing):
                    pass
                else:
                    current_user.like_writing(writing)
            else:
                if current_user.has_liked_writing(writing):
                    current_user.unlike_writing(writing)
                else:
                    pass

        if content["content_type"] == 'audio':
            audio = Audio.query.filter_by(id=content["id"]).first_or_404()

            if content["liked_by_user"]:
                if current_user.has_liked_audio(audio):
                    pass
                else:
                    current_user.like_audio(audio)
            else:
                if current_user.has_liked_audio(audio):
                    current_user.unlike_audio(audio)
                else:
                    pass
        db.session.commit()

        str = "success"
        return jsonify(str)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Successfully logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.media'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('users/login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password, rank='unconfirmed')
        db.session.add(user)
        db.session.commit()
        send_email_confirmation(user)
        flash(
            f'Account created for {form.username.data}! An email has been sent to {form.email.data}, please confirm your address to complete registration.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title='Reset Password', form=form)


@ users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('You have entered an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html', title='Reset Password', form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('users/user_posts.html', posts=posts, user=user)
