from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, current_app
from flask_login import login_user, current_user, logout_user, login_required
from application import db, bcrypt
from application.models import Artwork, PostComment, User, Post, Writings, Video, Project, Audio, AudioLike, VideoLike, WritingsLike, ProjectDislike, ProjectLike, ArtworkLike
from application.blueprints.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm,
                                                ResetPassword, AdminForm, UpdateUserForm, VideoForm, WritingForm, ProjectForm, AudioForm, ArtworkForm)
from application.blueprints.users.utils import save_picture, save_audio_file, send_email_confirmation, send_reset_email
import markdown
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
            image_file = save_picture(form.image.data)
            current_user.image_file = image_file
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email

    image_file = current_user.image_file

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

    forms = {
        "update_self_form": AdminForm(),
        "update_user_form": UpdateUserForm(),
        "artwork_form": ArtworkForm(),
        "audio_form": AudioForm(),
        "project_form": ProjectForm(),
        "video_form": VideoForm(),
        "writing_form": WritingForm(),
    }

    image_to_display = current_user.image_file

    # populates form placeholder with current user info
    if request.method == 'GET':
        selected_form = forms.get("update_self_form")
        selected_form.username.data = current_user.username
        selected_form.email.data = current_user.email

    elif request.method == 'POST':
        form_type = request.form.get("form_type")
        selected_form = forms.get(form_type)

        if selected_form and selected_form.validate():
            if form_type == "update_self_form":
                if selected_form.image.data:
                    image_file = save_picture(selected_form.image.data)
                    current_user.image_file = image_file

                current_user.username = selected_form.username.data
                current_user.email = selected_form.email.data

            elif form_type == "artwork_form":
                if selected_form.artwork.data:
                    art_link = save_picture(selected_form.artwork.data)
                    artwork = Artwork(
                        user_id=current_user.id, image_file=art_link, tag=selected_form.tag.data)
                    db.session.add(artwork)

            elif form_type == "audio_form":
                audio_url = save_audio_file(selected_form.audio.data)
                image_file = save_picture(selected_form.image.data)
                audio_lyrics = markdown.markdown(
                    selected_form.lyrics.data, extensions=['nl2br'])
                audio = Audio(user_id=current_user.id, title=selected_form.title.data,
                              lyrics=audio_lyrics, image_file=image_file, tag=selected_form.tag.data, url=audio_url)
                db.session.add(audio)

            elif form_type == "video_form":
                video = Video(user_id=current_user.id, title=selected_form.title.data,
                              url=selected_form.url.data, tag=selected_form.tag.data)
                db.session.add(video)

            elif form_type == "writing_form":
                md_content = markdown.markdown(
                    selected_form.content.data, extensions=['nl2br'])
                writing = Writings(user_id=current_user.id, title=selected_form.title.data,
                                   details=selected_form.details.data, content=md_content, tag=selected_form.tag.data)
                db.session.add(writing)

            elif form_type == "project_form":
                project = Project(title=selected_form.title.data, details=selected_form.details.data,
                                  completion_time=selected_form.completion_time.data)
                db.session.add(project)

            elif form_type == "update_user_form":
                user_to_modify = selected_form.username.data
                rank = selected_form.memberType.data
                user = User.query.filter_by(username=user_to_modify).first()

                if (rank == 'remove'):
                    PostComment.query.filter_by(user_id=user.id).delete()
                    Post.query.filter_by(user_id=user.id).delete()
                    User.query.filter_by(id=user.id).delete()
                else:
                    user.rank = rank

            db.session.commit()
            flash('Changes successful!', 'success')
            return redirect(url_for('users.admin'))

    return render_template('users/admin.html', title='Admin', image_to_display=image_to_display, **forms)


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
    registration_closed = True

    if request.method == 'GET':
        if current_user.is_authenticated or registration_closed:
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
