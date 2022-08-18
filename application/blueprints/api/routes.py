from flask import Blueprint, jsonify, request, current_app
from application.models import Artwork
from flask_login import current_user
from application import db
from application.models import Artwork, Post, Writings, Video, Project, Audio, AudioLike, VideoLike, WritingsLike, ProjectDislike, ProjectLike, ArtworkLike, \
    FormModel, TIN, TINDoc, DocComment
import base64
import PIL.Image as Image
import io
import secrets
import os

api = Blueprint('api', __name__)


@api.route("/api/create-game/wt", methods=["POST"])
def create_game_wt():
    if request.method == 'POST':
        newGame = request.get_json()
        print(newGame)

    my_str = "success"
    return jsonify(my_str)


@api.route("/api/add_tin_model", methods=["POST"])
def add_tin_model():
    if request.method == 'POST':
        newModel = request.get_json()
        imgdata = base64.b64decode(newModel["img"])
        random_hex = secrets.token_hex(8)
        file_ext = newModel["ext"]
        new_filename = random_hex + file_ext
        picture_path = os.path.join(
            current_app.root_path, 'static/images', new_filename)
        i = Image.open(io.BytesIO(imgdata))
        i.save(picture_path)

    formModel = FormModel(image_file=new_filename, tag=newModel["name"])
    db.session.add(formModel)
    db.session.commit()

    my_str = "success"
    return jsonify(my_str)


@api.route("/api/add_tin_to_model", methods=["POST"])
def add_tin_to_model():
    if request.method == 'POST':
        obj = request.get_json()
        model = FormModel.query.filter_by(id=obj["modelNum"]).first()
        tin = TIN.query.filter_by(number=obj["tinNum"]).first()
        tin.model_type = model.tag
        for child in tin.children:
            child.model_type = model.tag
        db.session.commit()

    my_str = "success"
    return jsonify(my_str)


@api.route("/api/add_doc_comment", methods=["POST"])
def add_doc_comment():
    if request.method == 'POST':
        obj = request.get_json()
        docComment = DocComment(
            doc_id=obj["docParent"], content=obj["comment"])
        db.session.add(docComment)
        db.session.commit()

    my_str = "success"
    return jsonify(my_str)


@api.route("/api/del_tin_model", methods=["POST"])
def del_tin_model():
    if request.method == 'POST':
        newModel = request.get_json()
        formModelName = newModel["modelName"]
        FormModel.query.filter_by(tag=formModelName).delete()
        db.session.commit()

    my_str = "success"
    return jsonify(my_str)


@api.route("/api/get-model-tins/<string:model_id>")
def get_model_tins(model_id):
    if request.method == 'GET':
        model = FormModel.query.filter_by(id=model_id).first()
        tinList = TIN.query.filter_by(model_type=model.tag).order_by(
            TIN.number.asc()).all()
        myList = []
        for tin in tinList:
            myList.append(tin.number)

        return jsonify(myList)


@api.route("/api/get-doc-db")
def get_doc_db():
    if request.method == 'GET':
        docList = TINDoc.query.order_by(TINDoc.name.desc()).all()
        myList = []
        for doc in docList:
            temp_dict = {}
            temp_dict['id'] = doc.id
            temp_dict['tin_id'] = doc.tin_id
            temp_dict['name'] = doc.name
            temp_dict['header_cols'] = doc.header_cols
            temp_dict['data_cols'] = doc.actual_cols
            temp_dict['storage_url'] = doc.link
            temp_dict['bugs_url'] = doc.bugs
            temp_dict['model_type'] = doc.model_type
            commentList = []
            commentDict = {}
            for comment in doc.comments:
                commentDict = {}
                commentDict['date'] = comment.date_posted
                commentDict['content'] = comment.content
                commentList.append(commentDict)
            temp_dict['comments'] = commentList
            myList.append(temp_dict)

        return jsonify(myList)


@api.route("/api/add_tin", methods=["POST"])
def add_tin():
    if request.method == 'POST':
        newTIN = request.get_json()
        tin = TIN(number=newTIN["num"], model_type=newTIN["model"])
        db.session.add(tin)
        db.session.commit()

    my_str = "success"
    return jsonify(my_str)


@api.route("/api/add_doc", methods=["POST"])
def add_doc():
    if request.method == 'POST':
        newDoc = request.get_json()
        if '.pdf' in newDoc["title"].lower():
            title = newDoc["title"].lower().replace('.pdf', '')
        else:
            title = newDoc["title"].lower()

        tin = db.session.query(TIN).filter_by(number=newDoc["tin"]).first()
        model = tin.model_type
        tinDoc = TINDoc(header_cols=newDoc["headers"], actual_cols=newDoc["data"], link=newDoc["sharepoint"], bugs=newDoc["devops"],
                        name=title, tin_id=newDoc["tin"], model_type=model)
        db.session.add(tinDoc)
        db.session.commit()
    my_str = "success"
    return jsonify(my_str)


@api.route("/api/digital-art/<string:art_type>", methods=["POST", "GET"])
def api_digital(art_type):
    if request.method == 'POST':
        like_status = request.get_json()
        artwork = Artwork.query.filter_by(id=like_status["id"]).first()
        if like_status["isLiked"]:
            current_user.like_artwork(artwork)
        else:
            current_user.unlike_artwork(artwork)

        db.session.commit()

        my_str = "success"
        return(my_str)

    if request.method == 'GET':
        if art_type == 'digital':
            artworkList = Artwork.query.filter_by(tag='digital').order_by(
                Artwork.date_posted.desc()).all()

        if art_type == 'photo':
            artworkList = Artwork.query.filter_by(tag='photo').order_by(
                Artwork.date_posted.desc()).all()

        myList = []

        for i, artwork in enumerate(artworkList):
            temp_dict = {}
            temp_dict["position"] = i
            temp_dict["id"] = artwork.id
            temp_dict["src"] = artwork.image_file
            temp_dict["isLiked"] = current_user.has_liked_artwork(artwork)
            myList.append(temp_dict)

        return jsonify(myList)


@api.route('/api/delete', methods=["POST"])
def remove_from_db():
    if request.method == 'POST':
        if current_user.rank == 'admin':
            object = request.get_json()
            objType = object["type"]
            objID = object["id"]
            if objType == 'Artwork':
                db.session.query(ArtworkLike).filter_by(
                    artwork_id=objID).delete()
                Artwork.query.filter_by(id=objID).delete()
                db.session.commit()
            if objType == 'Audio':
                db.session.query(AudioLike).filter_by(audio_id=objID).delete()
                Audio.query.filter_by(id=objID).delete()
                db.session.commit()
            elif objType == 'Video':
                Video.query.filter_by(id=objID).delete()
                db.session.query(VideoLike).filter_by(video_id=objID).delete()
                db.session.commit()
            elif objType == 'Writings':
                Writings.query.filter_by(id=objID).delete()
                db.session.query(WritingsLike).filter_by(
                    writings_id=objID).delete()
                db.session.commit()
            elif objType == 'Project':
                Project.query.filter_by(id=objID).delete()
                db.session.query(ProjectLike).filter_by(
                    project_id=objID).delete()
                db.session.query(ProjectDislike).filter_by(
                    project_id=objID).delete()
                db.session.commit()
            else:
                my_str = "there was an error with your request"

        my_str = "success"
        return(my_str)


@api.route("/api/likes/<string:like_type>/<string:like_tag>", methods=["POST", "GET"])
def user_likes(like_type, like_tag):
    if request.method == 'POST':
        like_status = request.get_json()

        if like_type == 'audio':
            audio = Audio.query.filter_by(id=like_status["id"]).first()
            if like_status["isLiked"]:
                current_user.like_audio(audio)
            else:
                current_user.unlike_audio(audio)

        if like_type == 'video':
            video = Video.query.filter_by(id=like_status["id"]).first()
            if like_status["isLiked"]:
                current_user.like_video(video)
            else:
                current_user.unlike_video(video)

        if like_type == 'post':
            post = Post.query.filter_by(id=like_status["id"]).first()
            if like_status["isLiked"]:
                current_user.like_post(post)
            else:
                current_user.unlike_post(post)

        if like_type == 'writing':
            writing = Writings.query.filter_by(id=like_status["id"]).first()
            if like_status["isLiked"]:
                current_user.like_writing(writing)
            else:
                current_user.unlike_writing(writing)

        db.session.commit()

        my_str = "success"
        return(my_str)

    if request.method == 'GET':
        myList = []

        if like_type == 'audio':
            # my likes is the api called made from the account page, where user is retrieving their list of "liked" audio
            if like_tag == 'my_likes':
                if current_user.is_authenticated:
                    audioList = []
                    my_audios = current_user.liked_audio
                    for audio in my_audios:
                        audioList.append(Audio.query.filter_by(
                            id=audio.audio_id).first())

            else:
                audioList = Audio.query.filter_by(tag=like_tag).order_by(
                    Audio.date_posted.desc()).all()

            if not audioList:
                mystr = 'empty'
                return jsonify(mystr)

            for i, audio in enumerate(audioList):
                temp_dict = {}
                temp_dict["position"] = i
                temp_dict["id"] = audio.id
                temp_dict["title"] = audio.title
                temp_dict["image_file"] = audio.image_file
                temp_dict["url"] = audio.url
                if current_user.is_authenticated:
                    temp_dict["isLiked"] = current_user.has_liked_audio(audio)
                else:
                    temp_dict["isLiked"] = 'logged_out'
                temp_dict["tag"] = audio.tag
                myList.append(temp_dict)

        if like_type == 'video':
            videoList = Video.query.filter_by(tag=like_tag).order_by(
                Video.date_posted.desc()).all()

            for i, video in enumerate(videoList):
                temp_dict = {}
                temp_dict["position"] = i
                temp_dict["id"] = video.id
                temp_dict["title"] = video.title
                temp_dict["url"] = video.url
                temp_dict["isLiked"] = current_user.has_liked_video(video)
                temp_dict["tag"] = video.tag
                myList.append(temp_dict)

        if like_type == 'post':
            post = Post.query.filter_by(id=like_tag).first()
            temp_dict = {}
            temp_dict["position"] = 0
            temp_dict["id"] = post.id
            temp_dict["title"] = post.title
            if current_user.is_authenticated:
                temp_dict["isLiked"] = current_user.has_liked_post(post)
            else:
                temp_dict["isLiked"] = False
            temp_dict["content"] = post.content
            temp_dict["author_id"] = post.user_id
            myList.append(temp_dict)

        if like_type == 'writing':
            text = Writings.query.filter_by(id=like_tag).first()
            temp_dict = {}
            temp_dict["position"] = 0
            temp_dict["id"] = text.id
            temp_dict["title"] = text.title
            temp_dict["details"] = text.details
            temp_dict["isLiked"] = current_user.has_liked_writing(text)
            temp_dict["content"] = text.content
            temp_dict["author_id"] = text.user_id
            myList.append(temp_dict)

        return jsonify(myList)
