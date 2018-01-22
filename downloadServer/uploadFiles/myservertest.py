#!/usr/bin/env python
import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import re
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        f = self.listmyfile
        if f:
            self.copyfile(f,self.wfile)
            f.close()
    
    def listmyfile(self,path):
       try:
           filellist = ox.listdir(path)
       except os.error:
           self.send_error(404,"Permission denied to list the files")
       filelist.sort(key=lambda a: a.lower())
       f = StringIO()
       html_head = """
           <!DOCTYPE html>  
            <html lang="en">  
            <head>  
                <meta charset="UTF-8">  
                <title>drag upload</title>  
            </head>  
            <style>  
                #uuz{  
                    width: 1280px;  
                    height: 768px;  
                    border: 1px dashed orange;  
                    text-align: center;
                }

            </style>

            <body>  
                <div id="uuz"> 

        """
        f.write(html_head)
        html_input = """
            <h2>Directory listing for /</h2>
            <hr>
            <form action="/uploadFiles" ENCTYPE="multipart/form-data" method="post"><input name="file" type="file"/><input type="submit" value="upload"/></form>
            <hr>
        """
        f.write(html_input)
        f.write("<hr>\n<ul>\n")
        for name in filelist:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write('<li><a href="%s">%s</a>\n'
                    % (urllib.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n</body>\n")
        html_script = """
        <script>  
        window.onload = function(){  
            var uuz = document.getElementById('uuz');  
      
            uuz.ondragenter = function(e){  
                e.preventDefault();  
            }  
      
            uuz.ondragover = function(e){  
                e.preventDefault();  
                this.innerHTML = 'release your mouse';  
            }  
      
            uuz.ondragleave = function(e){  
                e.preventDefault();  
                this.innerHTML = 'drag your file';  
            }  
      
            uuz.ondrop = function(e){  
                e.preventDefault();  
      
                var upfile = e.dataTransfer.files[0]; //获取要上传的文件对象(可以上传多个)  
                var formdata = new FormData();  
                var xhr = new XMLHttpRequest();  
      
                formdata.append('file', upfile); //设置服务器端接收的name为upfile  
                xhr.open('post','/uploadFiles'); //以post方式发送到1.php  
      
                xhr.onreadystatechange = function(){  
                    if(this.status==200){ //上传成功  
                        alert('upload success');  
                    }else{  
                        alert('upload failed');  
                    }  
                }  
      
                xhr.send(formdata);  
            }  
        }  
        </script>
        """
        f.write(html_script)
        f.write("</html>")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f
        


    def list_files(self,path):
        try:
            filelist = os.listdir(path)
        except os.error:
            self.send_error(404, "Permission denied to list the files")
        filelist.sort(key=lambda a: a.lower()) #all files are sorted according to name
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write("<hr>\n")
        f.write("<form action=\"/uploadFiles\" ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write("<input name=\"file\" type=\"file\"/>")
        f.write("<input type=\"submit\" value=\"upload\"/></form>\n")
        f.write("<hr>\n<ul>\n")
        for name in filelist:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write('<li><a href="%s">%s</a>\n'
                    % (urllib.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f



    
    def translate_path(self, path):
        print "translate_path", path
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path    

    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)


def test(HandlerClass = SimpleHTTPRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)
 
if __name__ == '__main__':
    test()
