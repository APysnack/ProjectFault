from application.blueprints.ancillary.utils import send_message
from flask import render_template, Blueprint, request, flash, redirect, url_for
from application.blueprints.ancillary.utils import send_message
import datetime

# ancillary pages primarily expected to remain static
ancillary = Blueprint('ancillary', __name__)


@ancillary.route("/about")
def about():
    current_year = datetime.datetime.now().year
    year_of_meeting_brewk = 2013
    anniversary_years = current_year - year_of_meeting_brewk
    return render_template('ancillary/about.html', title='About', anniversary_years=anniversary_years)


@ancillary.route("/privacy")
def privacy():
    return render_template('ancillary/privacy.html', title='Privacy Policy')


@ancillary.route("/resume")
def resume():
    return render_template('ancillary/resume.html', title='Resume')


@ancillary.route("/terms")
def terms():
    return render_template('ancillary/terms.html', title='Terms of Use')
