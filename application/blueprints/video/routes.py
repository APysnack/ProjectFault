from flask import render_template, Blueprint
from application.models import Video
from sqlalchemy import or_

video = Blueprint('video', __name__)


@video.route("/video/lrc-videos")
def lrc():
    genre = 'lrc-videos'
    videos = Video.query.filter_by(tag='lrc-videos').order_by(
        Video.date_posted.desc()).all()
    details = '''<p>LRC, or \"Live Rap Circle\" was a series of Hip Hop battling events that I coordinated in 2015. These events were filmed in College Park Maryland and
        Washington, D.C.. I founded, funded, and oversaw booking, hiring, video-editing, graphic design, and promotion for these events.</p>
        <p><b>Note</b>: It was the additional help from many competitors that we were able to successfully execute LRC II. I am grateful to Coma, Richard Cranium, 
        Psych, and Reginald Loud for their many contributions</p>
        <p>Since GrindTime was popularized in 2009, Live Rap Battling has taken a form similar to spoken word poetry, using emotional performances and acapella style vocals.
        The primary purpose of Rap Battles is to insult your opponent in a clever way, often using Comedy, Play on Words, and Multisyllabic rhyming.</p>
        <p>These performances are for entertainment, and often the primary purpose is to manipulate the ambiguity of language. I fully condemn any form of violence or hate speech.
        Some content may be viewed as offensive, is not suitable for those under 18, and <b>viewer discretion is advised.</b></p>'''

    return render_template('video/videoGenre.html', title='LRC', videos=videos, genre=genre, details=details)


@video.route("/video/video-battles")
def video_battles():
    genre = 'battle-videos'
    details = '''<p>These videos reflect a series of hip hop battling events that I participated in.
    These were filmed in various locations, including Baltimore, Rhode Island, San Antonio, and more.</p>
    <p>Since GrindTime was popularized in 2009, Live Rap Battling has taken a form similar to spoken word poetry, using emotional performances and acapella style vocals.
    The primary purpose of Rap Battles is to insult your opponent in a clever way, often using Comedy, Play on Words, and Multisyllabic rhyming.</p>
    <p>These performances are for entertainment, and often the primary purpose is to manipulate the ambiguity of language. I fully condemn any form of violence or hate speech.
    Some content may be viewed as offensive, is not suitable for those under 18, and <b>viewer discretion is advised.</b></p>'''

    videos = Video.query.filter_by(tag='battle-videos').order_by(
        Video.date_posted.desc()).all()

    return render_template('video/videoGenre.html', title='PurelyDef Battles', videos=videos, genre=genre, details=details)


@video.route("/video/music-videos")
def music_videos():
    genre = 'music-videos'
    details = '''This collection includes music videos that I have either appeared in, or have done filming and video editing for.'''
    videos = Video.query.filter_by(tag='music-videos').order_by(
        Video.date_posted.desc()).all()

    return render_template('video/videoGenre.html', title='Music Videos', videos=videos, genre=genre, details=details)


@video.route("/video/the-musicians-101")
def musician_101():
    return render_template('video/musician_101.html', title='The Musician\'s 101')


@video.route("/video/comedy-videos")
def comedy_videos():
    genre = 'comedy-videos'
    details = '''This collection includes my 2 stand up comedy albums, along with some live performances and other comedic videos meant 
    for entertainment. All of this content was created for the sole purpose of entertainment and making others laugh, and was not intended
    to be offensive to anyone. That being said, this content does contain vulgarity and topics that may be viewed as offensive to some.
    Viewer discretion is advised.'''
    videos = Video.query.filter_by(tag='comedy-videos').order_by(
        Video.date_posted.desc()).all()
    return render_template('video/videoGenre.html', title='Comedy Videos', videos=videos, genre=genre, details=details)
