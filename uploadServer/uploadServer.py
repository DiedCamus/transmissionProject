#!/usr/bin/env python
#-*-coding:utf-8 -*-
import os
import sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
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

#log in and log out system
app.config['USERNAME']="admin"
app.config['PASSWORD']="admin"
app.config['SECRET_KEY']="xeew\xe4\xc0\xee\xb1]\x9b\xa0\x9e)\x15Qhem\xe5\xf17\xd6\xceB\xb7\xb4"


def allowed_file(filename):
  return '.' in filename and \
      filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    filenames = get_allfilename()
    the_message = u'您可以上传文件'
    return render_template('uploadIndex.html',filenames=filenames, the_message=the_message, USERNAME=app.config['USERNAME'])

@app.route('/uploadFiles', methods=['POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
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
    return render_template('uploadIndex.html', filenames=filenames, the_message=the_message, USERNAME=app.config['USERNAME'])

@app.route('/uploadFiles')
def page_get():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    filenames = get_allfilename()
    the_message = u'上传成功！'
    return render_template('uploadIndex.html', filenames=filenames, the_message=the_message, USERNAME=app.config['USERNAME'])
  
@app.route('/uploadFiles/<filename>')
def uploaded_file(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                filename)

@app.route('/uploadlog.log')
def show_logs():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
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

@app.route('/login', methods=['GET', 'POST'])
def login():
        error = None
        if request.method == 'POST':
                if request.form['username'] != app.config['USERNAME']:
                        error = 'Invalid username'
                elif request.form['password'] != app.config['PASSWORD']:
                        error = 'Invalid password'
                else:
                        session['logged_in'] = True
                        flash('You were logged in')
                        return redirect(url_for('index'))
        return render_template('login.html', error=error)

@app.route('/logout')
def logout():
        session.pop('logged_in', None)
        flash('You were logged out')
        return redirect(url_for('index'))



if __name__ == '__main__':
  app.run(host='0.0.0.0')
