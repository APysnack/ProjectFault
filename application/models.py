from enum import unique
from application import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(100), nullable=False,
                           default='default.jpg')
    rank = db.Column(db.String(20), nullable=False, default='member')

    # NOTE: posts is one single attribute that grabs ALL posts from user with author name (array maybe). I think 'author' is just the name of the relationship
    posts = db.relationship('Post', backref='author', lazy=True)
    artwork = db.relationship('Artwork', backref='author', lazy=True)
    writings = db.relationship('Writings', backref='author', lazy=True)
    audio = db.relationship('Audio', backref='author', lazy=True)
    postComments = db.relationship('PostComment', backref='author', lazy=True)

    liked_audio = db.relationship(
        'AudioLike', foreign_keys='AudioLike.user_id', backref='user', lazy='dynamic')

    liked_post = db.relationship(
        'PostLike', foreign_keys='PostLike.user_id', backref='user', lazy='dynamic')

    liked_project = db.relationship(
        'ProjectLike', foreign_keys='ProjectLike.user_id', backref='user', lazy='dynamic')

    liked_videos = db.relationship(
        'VideoLike', foreign_keys='VideoLike.user_id', backref='user', lazy='dynamic')

    liked_artwork = db.relationship(
        'ArtworkLike', foreign_keys='ArtworkLike.user_id', backref='user', lazy='dynamic')

    liked_writing = db.relationship(
        'WritingsLike', foreign_keys='WritingsLike.user_id', backref='user', lazy='dynamic')

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def like_audio(self, audio):
        if not self.has_liked_audio(audio):
            like = AudioLike(user_id=self.id, audio_id=audio.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def unlike_audio(self, audio):
        if self.has_liked_audio(audio):
            AudioLike.query.filter_by(
                user_id=self.id,
                audio_id=audio.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def has_liked_audio(self, audio):
        return AudioLike.query.filter(
            AudioLike.user_id == self.id,
            AudioLike.audio_id == audio.id).count() > 0

    def like_writing(self, writings):
        if not self.has_liked_writing(writings):
            like = WritingsLike(user_id=self.id, writings_id=writings.id)
            db.session.add(like)

    def unlike_writing(self, writings):
        if self.has_liked_writing(writings):
            WritingsLike.query.filter_by(
                user_id=self.id,
                writings_id=writings.id).delete()

    def has_liked_writing(self, writings):
        return WritingsLike.query.filter(
            WritingsLike.user_id == self.id,
            WritingsLike.writings_id == writings.id).count() > 0

    def like_project(self, project):
        if not self.has_liked_project(project):
            like = ProjectLike(user_id=self.id, project_id=project.id)
            db.session.add(like)

    def unlike_project(self, project):
        if self.has_liked_project(project):
            ProjectLike.query.filter_by(
                user_id=self.id,
                project_id=project.id).delete()

        if self.has_disliked_project(project):
            ProjectDislike.query.filter_by(
                user_id=self.id,
                project_id=project.id).delete()

    def has_liked_project(self, project):
        return ProjectLike.query.filter(
            ProjectLike.user_id == self.id,
            ProjectLike.project_id == project.id).count() > 0

    def dislike_project(self, project):
        if not self.has_disliked_project(project):
            dislike = ProjectDislike(user_id=self.id, project_id=project.id)
            db.session.add(dislike)

    def has_disliked_project(self, project):
        return ProjectDislike.query.filter(
            ProjectDislike.user_id == self.id,
            ProjectDislike.project_id == project.id).count() > 0

    def like_video(self, video):
        if not self.has_liked_video(video):
            like = VideoLike(user_id=self.id, video_id=video.id)
            db.session.add(like)

    def unlike_video(self, video):
        if self.has_liked_video(video):
            VideoLike.query.filter_by(
                user_id=self.id,
                video_id=video.id).delete()

    def has_liked_video(self, video):
        return VideoLike.query.filter(
            VideoLike.user_id == self.id,
            VideoLike.video_id == video.id).count() > 0

    def like_artwork(self, artwork):
        if not self.has_liked_artwork(artwork):
            like = ArtworkLike(user_id=self.id, artwork_id=artwork.id)
            db.session.add(like)

    def unlike_artwork(self, artwork):
        if self.has_liked_artwork(artwork):
            ArtworkLike.query.filter_by(
                user_id=self.id,
                artwork_id=artwork.id).delete()

    def has_liked_artwork(self, artwork):
        return ArtworkLike.query.filter(
            ArtworkLike.user_id == self.id,
            ArtworkLike.artwork_id == artwork.id).count() > 0

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @ staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.rank}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tag = db.Column(db.String(20), nullable=False, default='uncategorized')
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    comments = db.relationship(
        'PostComment', backref='comment', lazy='dynamic')

    def getNumComments(self):
        numComments = PostComment.query.filter_by(post_id=self.id).count()
        return numComments

    def __repr__(self):
        return f"Post('{self.title}', {self.id}, '{self.date_posted}', {self.tag})"


class PostComment(db.Model):
    __tablename__ = 'post_comment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return f"PostComment('{self.id}', '{self.user_id}', '{ self.content }', '{self.post_id}', '{self.date_posted}')"


class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default='New-Audio')
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    artist = db.Column(db.String(100), nullable=False, default='PurelyDef')
    lyrics = db.Column(db.Text, nullable=False, default='No lyrics provided')
    tag = db.Column(db.String(20), nullable=False, default='general')
    url = db.Column(db.String(100), nullable=False, default='default.mp3')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(100), nullable=False,
                           default='default.jpg')
    likes = db.relationship('AudioLike', backref='audio', lazy='dynamic')

    def __repr__(self):
        return f"Audio('{self.id}', '{self.title}', '{self.url}', '{self.tag}')"


class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class AudioLike(db.Model):
    __tablename__ = 'audio_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    audio_id = db.Column(db.Integer, db.ForeignKey('audio.id'))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default='New Project')
    details = db.Column(db.String(1000), nullable=False,
                        default='No Details Provided')
    completion_time = db.Column(db.Integer, nullable=False, default=0)
    votes = db.Column(db.Integer, nullable=False, default=0)
    likes = db.relationship(
        'ProjectLike', backref='project', lazy='dynamic')

    dislikes = db.relationship(
        'ProjectDislike', backref='project', lazy='dynamic')

    def __repr__(self):
        return f"Project('{self.id}', '{self.title}', '{self.details}', '{self.votes}')"


class ProjectLike(db.Model):
    __tablename__ = 'project_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))


class ProjectDislike(db.Model):
    __tablename__ = 'project_dislike'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))


class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    image_file = db.Column(db.String(100), nullable=False,
                           default='default.jpg')
    tag = db.Column(db.String(20), nullable=False, default='general')
    likes = db.relationship('ArtworkLike', backref='artwork', lazy='dynamic')

    def __repr__(self):
        return f"Artwork('{self.id}', '{self.image_file}', {self.tag})"


class ArtworkLike(db.Model):
    __tablename__ = 'artwork_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'))


class WritingsLike(db.Model):
    __tablename__ = 'writing_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    writings_id = db.Column(db.Integer, db.ForeignKey('writings.id'))


class Writings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False, default='New Writing')
    details = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(20), nullable=False, default='general')
    likes = db.relationship('WritingsLike', backref='video', lazy='dynamic')

    def __repr__(self):
        return f"Writings('{self.id}', '{self.title}', '{self.details}', '{self.tag}')"


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False, default='New Video')
    tag = db.Column(db.String(20), nullable=False, default='general')
    url = db.Column(db.String(100), nullable=False)
    likes = db.relationship('VideoLike', backref='video', lazy='dynamic')

    def __repr__(self):
        return f"Video('{self.id}', '{self.title}', '{self.url}', '{self.tag}')"


class VideoLike(db.Model):
    __tablename__ = 'video_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))


class FormModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(100), nullable=False,
                           default='default.jpg')
    tag = db.Column(db.String(100), nullable=False, default='general')

    def __repr__(self):
        return f"FormModel('{self.id}', '{self.image_file}', {self.tag})"


class TIN(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(255), nullable=False, unique=True)
    model_type = db.Column(db.Text, nullable=False)
    children = db.relationship(
        'TINDoc', backref='children', lazy='dynamic')

    def __repr__(self):
        return f"TIN('{self.id}', '{self.number}')"


class TINDoc(db.Model):
    __tablename__ = 'TINDoc'
    id = db.Column(db.Integer, primary_key=True)
    header_cols = db.Column(db.JSON, nullable=False)
    actual_cols = db.Column(db.JSON, nullable=False)
    link = db.Column(db.Text, nullable=False)
    bugs = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    model_type = db.Column(db.Text, nullable=False)
    tin_id = db.Column(db.String(255), db.ForeignKey('TIN.number'))
    comments = db.relationship(
        'DocComment', backref='comments', lazy='dynamic')

    def __repr__(self):
        return f"TINDoc('{self.id}', '{self.name}', '{ self.link }', '{self.bugs}', '{self.tin_id}')"


class DocComment(db.Model):
    __tablename__ = 'DocComment'
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('TINDoc.id'))
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"TINDoc('{self.id}', '{self.doc_id}', '{ self.date_posted }', '{self.content}')"
