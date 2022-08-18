from flask import render_template, request, Blueprint, flash, jsonify
from application import db
from flask_login import current_user
from application.models import Project

code = Blueprint('code', __name__)


@code.route("/code/randomOrderGenerator")
def randomOrderGenerator():
    return render_template('code/projects/randomOrderGenerator.html')


@code.route("/upcoming", methods=["GET", "POST"])
def upcoming():
    if request.method == 'POST':
        vote_count = request.get_json()
        for vote in vote_count:
            value = list(vote.values())
            project = Project.query.filter_by(id=value[0]).first()

            if not (current_user.has_liked_project(project) or current_user.has_disliked_project(project)):
                if value[1] == 1:
                    current_user.like_project(project)
                    project.votes = project.votes + 1
                elif value[1] == 0:
                    pass
                else:
                    current_user.dislike_project(project)
                    project.votes = project.votes - 1

            elif current_user.has_liked_project(project):
                if value[1] == 1:
                    pass
                elif value[1] == 0:
                    current_user.unlike_project(project)
                    project.votes = project.votes - 1
                else:
                    current_user.unlike_project(project)
                    current_user.dislike_project(project)
                    project.votes = project.votes - 2
            else:
                if value[1] == 1:
                    current_user.unlike_project(project)
                    current_user.like_project(project)
                    project.votes = project.votes + 2
                elif value[1] == 0:
                    current_user.unlike_project(project)
                    project.votes = project.votes + 1
                else:
                    pass

        db.session.commit()

        flash('Your changes have been submitted!', 'success')
        return jsonify(dict(redirect='upcoming'))

    projects = Project.query.order_by(Project.votes.desc()).all()
    return render_template('code/upcoming.html', title='Upcoming Projects', projects=projects)
