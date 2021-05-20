from flask import Blueprint, render_template, url_for, request, jsonify
from pybo.models import Question, Answer, User
from datetime import datetime
from pybo import db
from werkzeug.utils import redirect
from pybo.movieapi import Mrank
from pybo.naverapi import navermovie




bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    # q = Question(subject='pybo가 무엇인가요?', content='pybo에 대해서 알고 싶습니다.', create_date=datetime.now())
    # from pybo import db
    # db.session.add(q)
    # db.session.commit()
    #
    # u1 = User(pw=123456, name='1', age=18, address='서울', birth='2004-01-01', sex=1, create_date=datetime.now())
    # u2 = User(pw=123456, name='2', age=19, address='서울', birth='2003-01-01', sex=1, create_date=datetime.now())
    # u3 = User(pw=123456, name='3', age=17, address='서울', birth='2005-01-01', sex=2, create_date=datetime.now())
    # u4 = User(pw=123456, name='4', age=20, address='서울', birth='2002-01-01', sex=1, create_date=datetime.now())
    # u5 = User(pw=123446, name='5', age=13, address='서울', birth='2009-01-01', sex=2, create_date=datetime.now())
    # u6 = User(pw=123456, name='6', age=26, address='서울', birth='1996-01-01', sex=1, create_date=datetime.now())
    # u7 = User(pw=123456, name='7', age=22, address='부산', birth='2000-01-01', sex=2, create_date=datetime.now())
    # u8 = User(pw=123456, name='8', age=15, address='광주', birth='2007-01-01', sex=2, create_date=datetime.now())
    # u9 = User(pw=123456, name='9', age=18, address='서울', birth='2004-01-01', sex=1, create_date=datetime.now())
    # u10 = User(pw=123456, name='10', age=21, address='서울', birth='2001-01-01', sex=2, create_date=datetime.now())
    #
    # db.session.add(u1)
    # db.session.add(u2)
    # db.session.add(u3)
    # db.session.add(u4)
    # db.session.add(u5)
    # db.session.add(u6)
    # db.session.add(u7)
    # db.session.add(u8)
    # db.session.add(u9)
    # db.session.add(u10)
    # db.session.commit()
    #
    return 'Hello, Pybo!'

@bp.route('/')
def index():

    return redirect(url_for('question._list'))

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/detail.html', question=question)

@bp.route('/test')
def test():
    for i in range(100):
        q = Question(subject='테스트 데이터 [{}]'.format(i), content='내용없음', create_date=datetime.now())
        db.session.add(q)
    db.session.commit()
    return redirect(url_for('question._list'))

@bp.route('/webhook', methods=['GET','POST'])
def webhook():
    print('webhook')
    req = request.get_json()
    print(req['queryResult']['intent']['displayName'])
    rankdata = Mrank()
    # print(rankdata)
    result = ''
    if req['queryResult']['intent']['displayName'] == 'movie ranking':
        count = 1
        for tmp in rankdata:
            result = result + str(count) + '위 : ' + tmp['title'] + '\n'
            if count == 3:
                break
            count += 1
    elif req['queryResult']['intent']['displayName'] == 'movie info - title':
        movieresult = navermovie(req['queryResult']['queryText'])
        print(movieresult)
        mdata = movieresult['items'][0]
        # print(req['queryResult']['queryText'])
        # for tmp in rankdata:
        #     # print('aa')
        #     if req['queryResult']['queryText'] in tmp['title']:
        #         result += '제목 : ' + tmp['title']
        #         result += ' 평점 : ' + tmp['star']
        #         result += ' 장르 : ' + tmp['genre']
        #         print(navermovie(req['queryResult']['queryText']))
        #     # print('result: '+ result)
        print(mdata['director'])
        return movie_info(mdata['image'], mdata['title'], '감독: ' + mdata['director'], ' 출연진: ' + mdata['actor'])
    return ''
def movie_info(img, title, director, actor):
    response_json = jsonify(
        fulfillment_text='영화정보',
        fulfillment_messages=[
            {
                "payload": {
                    "richContent": [[
                        {
                            "type": "image",
                            "rawUrl": img
                        },
                        {
                            "type": "info",
                            "title": title,
                            "subtitle": director + actor
                        }
                    ]]
                }
            }
        ]
    )
    return response_json
