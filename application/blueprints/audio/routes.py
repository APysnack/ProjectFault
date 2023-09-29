from flask import render_template, Blueprint, send_from_directory, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from application.models import Audio
from application.blueprints.users.forms import AudioForm
from application.blueprints.users.utils import save_picture
from flask_login import login_required, current_user
import markdown
import os
from application import db
from markdownify import markdownify

audio = Blueprint('audio', __name__)


@audio.route("/audio/instrumental")
def instrumental():
    genre = 'instrumental'
    audios = Audio.query.filter_by(tag='instrumental').order_by(
        Audio.date_posted.desc()).all()
    return render_template('audio/audioGenre.html', audios=audios, genre=genre)


@audio.route("/audio/alternative")
def alternative():
    genre = 'alternative'
    audios = Audio.query.filter_by(tag='alternative').order_by(
        Audio.date_posted.desc()).all()
    return render_template('audio/audioGenre.html', audios=audios, genre=genre)


@audio.route("/audio/indie-rap")
def indie_rap():
    genre = 'indie_rap'
    audios = Audio.query.filter_by(tag='indie-rap').order_by(
        Audio.date_posted.desc()).all()
    return render_template('audio/audioGenre.html', audios=audios, genre=genre)


@audio.route("/audio/hip-hop")
def hip_hop():
    genre = 'hip_hop'
    audios = Audio.query.filter_by(tag='hip-hop').order_by(
        Audio.date_posted.desc()).all()
    return render_template('audio/audioGenre.html', audios=audios, genre=genre)


@audio.route("/audio/<string:tag>/<int:id>")
def song_page(tag, id):
    song = Audio.query.get_or_404(id)
    audios = Audio.query.filter_by(tag=tag).order_by(
        Audio.date_posted.desc()).all()

    position = 0

    for i, audio in enumerate(audios):
        if int(audio.id) is id:
            position = i

    return render_template('audio/song-page.html', song=song, audios=audios, position=position)


@audio.route('/audio/<path:filename>')
def download_file(filename):
    return send_from_directory('static/audio/audio-files/', filename)


@login_required
@audio.route('/updateSong/<int:song_id>', methods=["GET", "POST"])
def updateSong(song_id):
    if current_user.rank != 'admin':
        return redirect(url_for('main.index'))

    audio_form = AudioForm()
    song = Audio.query.filter_by(id=song_id).first()

    if request.method == "POST":
        if audio_form.validate_on_submit():
            if audio_form.audio.data:
                audio_file = audio_form.audio.data
                audio_filename = secure_filename(audio_file.filename)
                file_path = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], audio_filename)
                audio_file.save(file_path)
                song.url = audio_filename

            if audio_form.image.data:
                image_file = save_picture(audio_form.image.data, {
                                          'width': 150, 'height': 150})
                song.image_file = image_file

            if audio_form.lyrics.data:
                audio_lyrics = markdown.markdown(
                    audio_form.lyrics.data, extensions=['nl2br'])
                song.lyrics = audio_lyrics

            if audio_form.title.data:
                song.title = audio_form.title.data

            if audio_form.tag.data:
                song.tag = audio_form.tag.data

            db.session.commit()
            flash('Audio has been updated!', 'success')
            return redirect(url_for('audio.updateSong', song_id=song_id))

    else:
        audio_form.title.data = song.title
        audio_form.tag.data = song.tag
        audio_form.lyrics.data = markdownify(song.lyrics)
        return render_template('audio/updateSong.html', song=song, audio_form=audio_form)
