from application.blueprints.ancillary.utils import send_message
from flask import render_template, Blueprint, request, flash, redirect, url_for
from application.blueprints.ancillary.forms import ContactForm
from application.blueprints.ancillary.utils import send_message
from application.models import FormModel, TIN, TINDoc, DocComment
from application import db
from application.config import authorizedUser
from flask_login import current_user

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


@ancillary.route("/genzeon")
def genzeon():
    if current_user.is_authenticated:
        if current_user.username != authorizedUser:
            return redirect(url_for('main.index'))
        return render_template('ancillary/genzeon/genzeon.html', title='Genzeon')
    else:
        return redirect(url_for('main.index'))


@ancillary.route("/tin_db")
def tin_db():
    if current_user.is_authenticated:
        if current_user.username != authorizedUser:
            return redirect(url_for('main.index'))
        tin_list = TIN.query.order_by(TIN.number.asc()).all()
        form_models = FormModel.query.all()
        return render_template('ancillary/genzeon/tin_db.html', title='Genzeon', tin_list=tin_list, form_models=form_models)
    else:
        return redirect(url_for('main.index'))


@ancillary.route("/form_models")
def form_models():
    if current_user.is_authenticated:
        if current_user.username != authorizedUser:
            return redirect(url_for('main.index'))
        form_models = FormModel.query.all()
        tin_list = TIN.query.order_by(TIN.number.asc()).all()
        return render_template('ancillary/genzeon/form_models.html', title='Genzeon', form_models=form_models, tin_list=tin_list)
    else:
        return redirect(url_for('main.index'))


@ancillary.route("/<string:docID>")
def doc_page(docID):
    if current_user.is_authenticated:
        if current_user.username != authorizedUser:
            return redirect(url_for('main.index'))
        doc = TINDoc.query.get(docID)
        model = FormModel.query.filter_by(tag=doc.model_type).first()
        return render_template('ancillary/genzeon/doc_page.html', title='Genzeon', doc=doc, model=model)
    else:
        return redirect(url_for('main.index'))
