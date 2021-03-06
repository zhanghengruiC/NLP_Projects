# encoding: utf-8

"""
@author: Henry
@site: 
@software: PyCharm
@file: news_auto_extract.py
@time: 2019/10/7 19:19
"""
from flask import request, url_for
from flask import render_template, redirect

from apps.forms.news_extractor import NewsExtractorForm

from apps.views import nlp_bp
from apps.nlp.parse_news import SpeechExtractor, LTPManager
from apps.config import SYNONYMS_PATH, LTP_MODEL_PATH


@nlp_bp.route('/')
def nlp_projects():
    return render_template('index.html')


@nlp_bp.route('/extract/', endpoint='auto_extractor', methods=['GET', 'POST'])
def auto_extractor():
    news_form = NewsExtractorForm(request.form)
    if request.method == 'POST' and news_form.validate():
        LTPM = LTPManager(LTP_MODEL_PATH)
        data = news_form.news.data
        npa = SpeechExtractor(data, SYNONYMS_PATH, LTPM)
        results = npa()  # [[who,say,content],[...],...]
        if results and isinstance(results, list):
            result = [{'person': result[0], 'say': result[1], 'content': result[2], 'news': data} for result in results]
            return render_template('extract.html', forms=result)
        else:
            return render_template('news_extractor.html', forms=news_form)
            # return render_template('extract.html', forms=results)
    return render_template('news_extractor.html', forms=news_form)


# @nlp_bp.route('show_res', endpoint='show_result')
# def show_result(results):
#     return render_template('extract.html', forms=results)


if __name__ == '__main__':
    nlp_bp.run()
