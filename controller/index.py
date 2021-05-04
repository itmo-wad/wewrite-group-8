import os

from flask import Blueprint, render_template, abort, jsonify, session, request
from module.article import Article
import math


index = Blueprint("index", __name__)



@index.route('/type/<int:type>-<int:page>')
def classify(type, page):
    start = (page - 1) * 10
    article = Article()
    result = article.find_by_type(type, start, 10)
    total = math.ceil(article.get_count_by_type(type) / 10)
    last = article.find_last_9()
    most = article.find_most_9()

    return render_template('type.html', result=result, page=page, total=total, type=type,last=last,most=most)
#
@index.route('/search/<int:page>-<keyword>')
def search(page, keyword):
    keyword = keyword.strip()
    if keyword is None or keyword == '' or '%' in keyword or len(keyword) > 10:
        abort(404)
    start = (page-1) * 10
    article = Article()
    result = article.find_by_headline(keyword, start, 10)
    total = math.ceil(article.get_count_by_headline(keyword) / 10)
    last = article.find_last_9()
    most = article.find_most_9()

    return render_template('search.html', result=result, page=page, total=total, keyword=keyword,last=last,most=most)








@index.route('/')
def home():

    article=Article()
    result = article.find_with_all(0, 10)
    last=article.find_last_9()
    most=article.find_most_9()
    total = math.ceil(article.get_total_count() / 10)
    content = render_template('index.html', result=result, page=1, total=total,last=last,most=most)
    return content

#
@index.route('/page/<int:page>')
def paginate(page):
    page=int(page)
    article = Article()
    result = article.find_with_all((page-1)*10, 10)
    total = math.ceil(article.get_total_count() / 10)
    last = article.find_last_9()
    most = article.find_most_9()
    content = render_template('index.html', result=result, page=page, total=total,last=last,most=most)
    return content