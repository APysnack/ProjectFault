from flask import render_template, Blueprint

games = Blueprint('games', __name__)


@games.route("/games/world-tournament")
def world_tournament():
    return render_template('games/worldTournament.html')
