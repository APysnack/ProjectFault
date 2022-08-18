from flask import render_template, Blueprint
from application.models import Writings

text = Blueprint('text', __name__)


@text.route("/writings")
def writings():
    return render_template('text/textWritings.html', title='Writing')


@text.route("/poetry")
def poetry():
    genre = 'poetry'
    writings = Writings.query.filter_by(tag='poem').order_by(
        Writings.date_posted.desc()).all()
    return render_template('text/textForum.html', title='Poetry', writings=writings, genre=genre)


@text.route("/topicals")
def topicals():
    genre = 'topicals'
    writings = Writings.query.filter_by(tag='topical').order_by(
        Writings.date_posted.desc()).all()
    return render_template('text/textForum.html', title='Topicals', writings=writings, genre=genre)


@text.route("/text_battles")
def text_battles():
    genre = 'text_battles'
    writings = Writings.query.filter_by(tag='text-battle').order_by(
        Writings.date_posted.desc()).all()
    return render_template('text/textForum.html', title='Battles', writings=writings, genre=genre)


@text.route("/<string:tag>/<int:writing_id>")
def text_thread(tag, writing_id):
    text_content = Writings.query.get_or_404(writing_id)
    return render_template('text/text_thread.html', title=text_content.title, text=text_content)
