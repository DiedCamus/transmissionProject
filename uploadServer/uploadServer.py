#!/usr/bin/env python
#-*-coding:utf-8 -*-
import os
import sys
import time
import sqlite3
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
from werkzeug import secure_filename
UPLOAD_FOLDER = "uploadFiles"
ISOTIMEFORMAT="%Y-%m-%d %X" #set the time format
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploadFiles/'

app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

#log in and log out system
app.config['ADMINUSER']="admin"
app.config['ADMINPASSWORD']="ofcl2504"
app.config['DATABASE']="user.db"
app.config['SECRET_KEY']="xeew\xe4\xc0\xee\xb1]\x9b\xa0\x9e)\x15Qhem\xe5\xf17\xd6\xceB\xb7\xb4"
current_username="None"




#database settings
def connect_db():
        return sqlite3.connect(app.config['DATABASE'])

def init_db():
        coon = connect_db()
        c = coon.cursor()
        c.execute('''CREATE TABLE USERS
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                USERNAME TEXT NOT NULL,
                PASSWORD TEXT NOT NULL);''')
        coon.commit()
        coon.close()

def insert_db(username, password):
        coon = connect_db()
        c = coon.cursor()
	sql = "INSERT INTO USERS (USERNAME, PASSWORD) VALUES ('%s', '%s');"%(username, password)
        c.execute(sql)
        coon.commit()
        coon.close()

def delete_db(username):
	coon = connect_db()
	c = coon.cursor()
	print "delete %s"%(username)
	sql = "DELETE FROM USERS WHERE USERNAME=\"%s\";"%(username)
	print sql
	c.execute(sql)
	out=c.fetchall()
	print out
	coon.commit()
	coon.close()



#init the basic files
currentpath=os.getcwd()
uploadpath=os.path.join(currentpath,UPLOAD_FOLDER)
if os.path.isdir(uploadpath):
	print "upload dir exisits"
else:
	print "upload dir not exisits, make it"
	os.makedirs(uploadpath)

db_path=os.path.join(currentpath,app.config['DATABASE'])
if os.path.isfile(db_path):
	print "database exisits"
else:
	print "database not exisits, make it"
	init_db()






def allowed_file(filename):
  return '.' in filename and \
      filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    filenames = get_allfilename()
    the_message = u'您可以上传文件'
    return render_template('uploadIndex.html',filenames=filenames, the_message=the_message, USERNAME=current_username)

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
    return render_template('uploadIndex.html', filenames=filenames, the_message=the_message, USERNAME=current_username)

@app.route('/uploadFiles')
def page_get():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    filenames = get_allfilename()
    the_message = u'上传成功！'
    return render_template('uploadIndex.html', filenames=filenames, the_message=the_message, USERNAME=current_username)
  
@app.route('/uploadFiles/<filename>')
def uploaded_file(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                filename)



@app.route('/uploadlog')
def show_logs():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	fp = open("uploadlog.log", "r")
	lines = fp.readlines()
	return render_template('uploadlog.html',logs=lines)



@app.route('/uploadlog.log')
def download_logs():
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
		username = request.form['username']
		password = request.form['password']
		if username == app.config['ADMINUSER']:
			session['logged_in'] = True
			global current_username
			current_username = username
			return redirect(url_for('index'))
		coon = connect_db()
		c = coon.cursor()
		sql = "SELECT * FROM USERS WHERE USERNAME='%s'"%(username)
		c.execute(sql)
		out = c.fetchall()
		coon.close()
		num = len(out)
		if num == 0:
                        error = '无效的用户名'
			return render_template('error.html', error=error, nextpage="login")
                else:
                        print "username=",out[0][1],"password=",out[0][2]
			if password == out[0][2]:
				session['logged_in'] = True
				global current_username
				current_username = username
				return redirect(url_for('index'))
			else:
				error = '密码错误'
				return render_template('error.html',error=error, nextpage="login")
        return render_template('login_new.html')

@app.route('/logout')
def logout():
        session.pop('logged_in', None)
        #flash('You were logged out')
        return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		adminpassword = request.form['adminpassword']
		#print adminpassword
		if username == app.config['ADMINUSER']:
			error = "不可使用管理员用户名"
			return render_template('error.html',error=error)
		coon = connect_db()
		c = coon.cursor()
		sql = "SELECT * FROM USERS WHERE USERNAME='%s'"%(username)
		c.execute(sql)
		out = c.fetchall()
		coon.close()
		if len(out) > 0:
			error = "用户名已存在!"
			return render_template('error.html',error=error)
		if adminpassword == app.config['ADMINPASSWORD']:
			insert_db(username, password)
			error = "注册成功"
			return render_template('error.html', error=error, nextpage="login")
			#return "<head><meta http-equiv=\"refresh\" content=\"1;url='%s'\"></head><h1>register success!</h1>"%(url_for('login'))
		else:
			error = "管理员密码错误"
			return render_template('error.html', error=error)
	else:
		return render_template('register_new.html', error=error)

@app.route('/edit_users', methods=['GET', 'POST'])
def edit_users():
	error = None
	#username = request.form['username']
	coon = connect_db()
	c = coon.cursor()
	#c.execute("select * from users;")
	#print c.fetchall()
	if request.method == 'POST':
		username = request.form['username']
		sql = "DELETE FROM USERS WHERE USERNAME='%s';"%(username)
		c.execute(sql)
		out = c.fetchall()
		print out
		coon.commit()
		coon.close()
		#delete_db(username)
		return redirect(url_for('edit_users'))
	else:
		print "edit_users"
		sql = "SELECT * FROM USERS"
		c.execute(sql)
		out = c.fetchall()
		coon.close()
		return render_template('edit_users.html',allusers=out)
		
@app.route('/resend',methods=['POST', 'GET'])
def file_resend():
	if request.method == 'POST':
		filepath = os.path.join(os.getcwd(), 'uploadFiles')
		print filepath
		filename = request.form['filename']
		oldfile=os.path.join(filepath, filename)
		print filename
		portion=os.path.splitext(oldfile)
		print portion
		if portion[1]==".sent":
			print "\nyes\n"
			newfile=os.path.join(filepath, portion[0])
			print "oldfile:",oldfile,"  newfile:",newfile
			os.rename(oldfile, newfile)
		return redirect(url_for('file_resend'))
	else:
		filenames = get_allfilename()
		return render_template('resend.html', filenames=filenames)			



if __name__ == '__main__':
  app.run(host='0.0.0.0')
