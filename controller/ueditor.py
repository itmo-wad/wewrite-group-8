import time

from flask import Blueprint, render_template, session, request, jsonify
import os

from common.utility import compress_image

ueditor = Blueprint("ueditor", __name__)

@ueditor.route('/uedit', methods=['GET', 'POST'])
def uedit():

    param = request.args.get('action')
    if request.method == 'GET' and param == 'config':
            return render_template('config.json')

    elif request.method == 'POST' and request.args.get('action') == 'uploadimage':
        f = request.files['upfile']
        filename = f.filename

        suffix = filename.split('.')[-1]
        newname = time.strftime('%Y%m%d_%H%M%S.' + suffix)
        f.save('./resource/upload/' + newname)

        source = dest = './resource/upload/' + newname
        compress_image(source, dest, 1200)

        result = {}
        result['state'] = 'SUCCESS'
        result["url"] = f"/upload/{newname}"
        result['title'] = filename
        result['original'] = filename

        return jsonify(result)

    elif request.method == 'GET' and param == 'listimage':
        list = []
        filelist = os.listdir('./resource/upload')
        for filename in filelist:
            if filename.lower().endswith('.png') or filename.lower().endswith('.jpg'):
                list.append({'url': '/upload/%s' % filename})

        result = {}
        result['state'] = 'SUCCESS'
        result['list'] = list
        result['start'] = 0
        result['total'] = 50
        return jsonify(result)
