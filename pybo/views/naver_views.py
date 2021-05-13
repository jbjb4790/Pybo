from flask import Blueprint, render_template, url_for, request
from werkzeug.utils import redirect
from pybo.naverapi import naverbook, navermovie
from ..forms import NaverBookForm, NaverMovieForm

bp = Blueprint('naver', __name__, url_prefix='/naver')


@bp.route('/book', methods=('GET','POST'))
def Naverbook():
    form = NaverBookForm()

    if request.method == 'POST' and form.validate_on_submit():
        result = naverbook(form.search.data)
        return render_template('naver/naverbook.html', bookinfo_list=result['items'], form=form)
    return render_template('naver/naverbook.html', form=form)

@bp.route('/movie', methods=('GET','POST'))
def Navermovie():
    form = NaverMovieForm()

    if request.method == 'POST' and form.validate_on_submit():
        result = navermovie(form.search.data)
        return render_template('naver/navermovie.html', movieinfo_list=result['items'], form=form)
    return render_template('naver/navermovie.html', form=form)


# SQL , NO-SQL

#SQL - MYSQL, 오라클 , 마리아DB, MS-SQL, SQLite
#NO-SQL - MONGODB, Redis, ......

