#!/usr/bin/env python
#-*-coding:utf-8 -*-
import os
import sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
UPLOAD_FOLDER = "uploadFiles"
ISOTIMEFORMAT="%Y-%m-%d %X" #set the time format

currentpath=os.getcwd()
uploadpath=os.path.join(currentpath,UPLOAD_FOLDER)
if os.path.isdir(uploadpath):
	print "upload dir exisits"
else:
	print "upload dir not exisits, make it"
	os.makedirs(uploadpath)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploadFiles/'

app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
  return '.' in filename and \
      filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    filenames = get_allfilename()
    the_message = u'您可以上传文件'
    return render_template('uploadIndex.html',filenames=filenames, the_message=the_message, my_message1="1234")

@app.route('/uploadFiles', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file[]")
    ip = request.remote_addr
    fp = open("uploadlog.log","a")
    for file in uploaded_files:
        if file:
            #filename = secure_filename(file.filename)
            filename = file.filename
            print filename
            savepath=(os.path.join(app.config['UPLOAD_FOLDER'],filename.encode("utf-8")))
            print savepath
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename.encode("utf-8")))
            logtext = time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ))  +  "  uploaded from  " + ip + "  \"" + filename +"\"\n";
            fp.write(logtext)
    #filenames = get_allfilename()
    fp.close()
    the_message = u'上传成功！'
    print "do this"
    filenames = get_allfilename()
    return render_template('uploadIndex.html', filenames=filenames, the_message=the_message, my_message1="1234")

@app.route('/uploadFiles')
def page_get():
    filenames = get_allfilename()
    the_message = u'上传成功！'
    return render_template('uploadIndex.html', filenames=filenames, the_message=the_message, my_message1="1234")
  
@app.route('/uploadFiles/<filename>')
def uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'],
                filename)

@app.route('/uploadlog.log')
def show_logs():
    #return render_template('log.html')
    directory = os.getcwd()
    return send_from_directory(directory, "uploadlog.log", as_attachment=True)
    #return "show log"
    #return send_from_directory(app.config['LOGS_FOLDER'],filename)


def get_allfilename():
    filenames = []
    filepath = os.path.join(os.getcwd(), 'uploadFiles')
    try:
        list = os.listdir(filepath)
    except os.error:
        print "os.listdir error"
    list.sort(key=lambda a: a.lower())
    for file in list:
        if file:
            filenames.append(file)
    print filenames
    return filenames


if __name__ == '__main__':
  app.run(host='0.0.0.0')
