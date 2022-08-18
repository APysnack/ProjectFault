import markdown
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from application import db
from application.models import Post, PostLike, PostComment
from application.blueprints.posts.forms import PostForm, CommentForm
from markdownify import markdownify

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        md_content = markdown.markdown(form.content.data, extensions=['nl2br'])
        post = Post(title=form.title.data,
                    content=md_content, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('users.account'))
    return render_template('posts/create_post.html', title='New Post', form=form, legend='Create A New Post')


@posts.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
    reply_form = CommentForm()
    post = Post.query.get_or_404(post_id)

    if reply_form.validate_on_submit():
        this_user_id = current_user.id
        this_content = markdown.markdown(
            reply_form.content.data, extensions=['nl2br'])
        this_post_id = request.view_args['post_id']
        postComment = PostComment(user_id=this_user_id,
                                  content=this_content, post_id=this_post_id)
        db.session.add(postComment)
        db.session.commit()
        flash('Your comment has been submitted!', 'success')
        return redirect(url_for('posts.post', post_id=this_post_id))

    return render_template('posts/post.html', title=post.title, post=post, reply_form=reply_form)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def updatepost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = markdown.markdown(
            form.content.data, extensions=['nl2br'])
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = markdownify(post.content)
    return render_template('posts/create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.query(PostLike).filter_by(post_id=post.id).delete()
    db.session.query(PostComment).filter_by(post_id=post.id).delete()
    Post.query.filter_by(id=post.id).delete()

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('users.account'))
