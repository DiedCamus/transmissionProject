
=============================================================
#how to configure a linux server the with education network
=================================================================
>sudo vim /etc/network/interfaces
add follows:
>auto enp5s0
>iface enp5s0 inet dhcp

>sudo vim /etc/apt/sources.list
add follows:

deb http://cn.archive.ubuntu.com/ubuntu/ xenial main restricted
deb http://cn.archive.ubuntu.com/ubuntu/ xenial-updates main restricted
deb http://cn.archive.ubuntu.com/ubuntu/ xenial universe
deb http://cn.archive.ubuntu.com/ubuntu/ xenial-updates universe
deb http://cn.archive.ubuntu.com/ubuntu/ xenial multiverse
deb http://cn.archive.ubuntu.com/ubuntu/ xenial-updates multiverse
deb http://cn.archive.ubuntu.com/ubuntu/ xenial-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu xenial-security main restricted
deb http://security.ubuntu.com/ubuntu xenial-security universe
deb http://security.ubuntu.com/ubuntu xenial-security multiverse

======================================================================
===============================================================================
===============================================================================












============================================
#git文件夹下主要文件目录
=========================
downloadServer/   #在单向系统的receiver端给内网提供下载服务
uploadServer/     #在单向系统的sender端给外网提供上传服务

===================================================================
#sender端的服务器，即上传服务器的搭建方法
=============================================================
1.安装python2.7版本（大多数ubuntu系统预装了python2.7，一部分预装的是python3.5，python3目前兼容性不如python2）
sudo apt-get install python2.7

2.安装pip
sudo apt-get install pip

3.安装flask
sudo pip install flask

至此，服务器运行所需要的基本环境已经完成
在git中保存的版本里，有一个uploadServer的文件夹，该文件夹在单向系统的sender端给外网提供上传服务
uploadServer文件夹下主要文件目录
static/             #网页呈现所需的一些静态文件
templates/          #动态网页模板
uploadFiles/        #上传文件目录
uploadServer.py     #python服务器程序
uploadlog.log       #上传日志
processfile.sh      #监控uploadFiles文件夹下文件，发现新文件就通过flute发送给receiver


运行服务器
python uploadServer.py
运行shell脚本
./processfile.sh


通过配置外网机器和sender端的静态ip即可访问上传服务器



4.安装dhcp（optional，如果嫌麻烦可以直接配静态ip）
sudo apt-get install isc-dhcp-server
我之前安装的时候ubuntu服务器抽风了，从默认的中国节点获取不到资源
可以从提示的错误信息中把网址单独复制出来把cn改成com然后直接下载deb安装包安装
安装完成后修改conf文件
sudo vim /etc/dhcp/dhcpd.conf

在最后添加以下内容：
subnet 162.105.155.0 netmask 255.255.255.0 {
	range 162.105.155.150 162.105.155.253;
	option routers 162.105.155.1;
	option subnet-mask 255.255.255.0;
	option broadcast-address 162.105.155.255;
	option domain-name-servers 162.105.155.1;
	option ntp-servers 162.105.155.1;
	option netbios-name-servers 162.105.155.1;
	option netbios-node-type 8;
} 
上传服务器主机地址为162.105.155.1
外网访问http:162.105.155.1:5000即可







==========================================================
#receiver端的服务器，即下载服务器的搭建方法
========================================================
环境搭建和上传服务器一模一样
1.安装python2.7版本
2.安装pip
3.安装flask
4.安装dhcp

启动服务器
python downloadServer.py











