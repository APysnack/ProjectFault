from application.blueprints.ancillary.utils import send_message
from flask import render_template, Blueprint, request, flash, redirect, url_for
from application.blueprints.ancillary.forms import ContactForm
from application.blueprints.ancillary.utils import send_message

# ancillary pages primarily expected to remain static
ancillary = Blueprint('ancillary', __name__)


@ancillary.route("/about")
def about():
    return render_template('ancillary/about.html', title='About')


@ancillary.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = request.form.get("name", "none")
        email = request.form.get("email", "none")
        message = request.form.get("message", "none")
        send_message(name, email, message)
        flash(f'Your Message has been Sent!', 'success')

        return redirect(url_for('ancillary.contact'))
    return render_template('ancillary/contact.html', title='Contact', form=form)


@ancillary.route("/donate")
def donate():
    return render_template('ancillary/donate.html', title='Donate')


@ancillary.route("/privacy")
def privacy():
    return render_template('ancillary/privacy.html', title='Privacy Policy')


@ancillary.route("/resume")
def resume():
    return render_template('ancillary/resume.html', title='Resume')


@ancillary.route("/terms")
def terms():
    return render_template('ancillary/terms.html', title='Terms of Use')

