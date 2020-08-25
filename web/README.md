# Flask-Bootstrap-Demo
This is a simple web app demo using Flask, Flask-login, Flask-SQLAlchemy, and a SQLite3 database. 

### Technology

Flask-Bootstrap-Demo uses a multiple python libraries:
* [Python 2.7](https://www.python.org/) - Python is a programming language that lets you work quickly and integrate systems more effectively.
* [Flask](http://flask.pocoo.org/) - Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - Flask-Login provides user session management for Flask.
* [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/) - Flask-Bcrypt is a Flask extension that provides bcrypt hashing utilities for your application.
* [Bootstrap](http://getbootstrap.com/) - Bootstrap is the most popular HTML, CSS, and JS framework for developing responsive, mobile first projects on the web.
* [SQLite3](https://docs.python.org/2/library/sqlite3.html) - SQLite is a C library that provides a lightweight disk-based database

### Installation
Install the dependencies.
```sh
$ python -m pip install -r requirements.txt
```

### Run
```
python app.py
```


### file change 

#### html部分
content_table.html : 主要改動介面
site-template-ch.html : 可以當成基底，方便login, profile 使用jinja語法(extends 'site-template-ch.html' )，使用一樣的版型

#### js部分
content_table.js : 主要js改動，一些凍結、readmore等
write_log.js : 寫log檔，收集userid和postid
suggestion.js : 搜尋補字，用list存現有的公司名稱
popper.js :  外部套件
jquery.min.js : 外部套件
content-table-mit.js : 外部套件
bootstap-table.js : 外部套件

#### cs部分
hight_light.css : 關鍵字亮點
content_table.css : 主要css改動, 一些顏色改變

#### 環境部分
requirements_change.txt : 環境設定，有更新一些套件

#### 套件部分有的字型和顏色有改動，或是更新版本
bootstrap.min.css, custom.css, sb-admin.css, font-awesome 裡面的 font-awesome.min.css



