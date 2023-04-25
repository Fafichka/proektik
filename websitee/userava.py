from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .models import Userava
from . import db


userava = Blueprint('userava', __name__)


@userava.route('/profile', methods=['GET', 'POST'])
@login_required
def ava():
    if request.method == 'POST':
        im = request.form.get('file')
        if len(im) < 1:
            flash('error', category='error')
        else:
            new_ava = Userava(avatar=url_for(im), user_id=current_user.id)
            db.session.add(new_ava)
            db.session.commit()
            flash('!', category='success')
    return render_template("profile.html", user=current_user)

