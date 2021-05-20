from flask import Blueprint, render_template, request, url_for
from datetime import datetime
from werkzeug.utils import redirect
from pybo.models import Question
from ..forms import QuestionForm, AnswerForm
from .. import db

bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/bot/')
def Bot():
    return render_template('chat/chatbot.html')
