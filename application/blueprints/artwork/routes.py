from flask import render_template, Blueprint
from application.models import Artwork

artwork = Blueprint('artwork', __name__)


@artwork.route("/digital-art")
def digital_art():
    artwork = Artwork.query.filter_by(tag='digital').order_by(
        Artwork.date_posted.desc()).all()
    arr1, arr2, arr3, arr4, arrayLengths = [], [], [], [], []

    for i, art in enumerate(artwork):
        if i % 4 == 0:
            arr1.append(art)
        elif i % 4 == 1:
            arr2.append(art)
        elif i % 4 == 2:
            arr3.append(art)
        else:
            arr4.append(art)

    arrayLengths.extend((len(arr1), len(arr2), len(arr3), len(arr4)))
    image_array = arr1 + arr2 + arr3 + arr4

    return render_template('art/digital_art.html', title='Digital Art', image_array=image_array, arrayLengths=arrayLengths, art_id=0)


@artwork.route("/photography")
def photography():
    artwork = Artwork.query.filter_by(tag='photo').order_by(
        Artwork.date_posted.desc()).all()
    arr1, arr2, arr3, arr4, arrayLengths = [], [], [], [], []

    for i, art in enumerate(artwork):
        if i % 4 == 0:
            arr1.append(art)
        elif i % 4 == 1:
            arr2.append(art)
        elif i % 4 == 2:
            arr3.append(art)
        else:
            arr4.append(art)

    arrayLengths.extend((len(arr1), len(arr2), len(arr3), len(arr4)))
    image_array = arr1 + arr2 + arr3 + arr4

    return render_template('art/photography.html', title='Photography', image_array=image_array, arrayLengths=arrayLengths)
