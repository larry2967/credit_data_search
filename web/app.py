# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, json
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, Form, TextField, TextAreaField, validators, SubmitField
from wtforms.validators import DataRequired
from models.Users import User
from models.Users import db
import re
from datetime import datetime
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(HOST="http://localhost", PORT=9200)
# setup the app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "SuperSecretKey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

# 加密
bcrypt = Bcrypt(app)

# setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# create the db structure
with app.app_context():
    db.create_all()

#固定的樣式回傳表格
report_posts = [
    {
        "date" : "2020/07/31",
        "num" : "1",
        "category" : "食品業",
        "name" : "<em>統一</em>",
        "center" : "數金處",
        "abstract" : "1990年，玉山商業銀行由黃永仁發起成立，成立時標榜無大企業參與，完全由專業金融人員、學者及中小企業參與[7]。經財政部核准後，於1992年2月21日開始營業[8]，林鐘雄擔任首任董事長。2000年，洛杉磯分行開業[9]。<span id='more' style='display:none'>2002年1月28日，玉山銀行與旗下轉投資的玉山票券金融公司、玉山綜合證券共同以股份轉換方式成立玉山金融控股公司[10]，成為玉山金控的子公司。2002年，香港分行開業[11]。2004年，玉山銀行以新臺幣133.68億元標購遭中央存款保險公司接管的高雄區中小企業銀行，分行數由54家一口氣增加至114家[12]。2006年12月25日，同屬玉山金控的玉山票券金融公司併入玉山銀行。2011年7月9日，玉山銀行以新臺幣18.6億元合併竹南信用合作社[13]。2012年11月3日，再以新臺幣1.1億元併入嘉義市第四信用合作社，使得國內分行數增加為136家，成為國內分行數第三多的民營銀行[14]。2013年，成立第三方支付平台。2013年，完成投資柬埔寨子行聯合商業銀行Union Commercial Bank Plc70%股權[15]。2014年，獲通過ISO 50001能源管理系統認證[16]。2018年，獲國際信評Moody's調升信用評等至A2（長期）/P-1（短期）。2019年，獲國際信評S&P調升信用評等至A-（長期）/A-2（短期），同時中華信評也給予調升信評至twAA+（長期）/twA-1+（短期）。12月17日，於臺大校園內成立雙語示範銀行，為民營銀行第一間</span><button onclick='readmore()' id='myBtn'>Read more...</button><button onclick='readless()' id='myBtn2'>Read less...</button>",
        "file" : "https://123.com.tw",
    },{
         "date" : "2020/08/03",
        "num" : "2",
        "category" : "生技醫療",
        "name" : "合一",
        "center" : "財富處",
        "abstract" : "今天天氣好冷，好想穿外套 ",
        "file" : "https://456.com.tw",

    }
]

diary_posts = [
    {
         "date" : "2020/07/31",
        "category" : "食品業",
        "center" : "數金處",
        "future" : "股票大跌",
        "content" : "空空在原地蹦躂了好幾下，發現就是不能感應到承魁的氣息，也沒有辦法離開這片鬼地方。不僅是承魁，就連其他博浪錘之類的靈器，好像都被屏蔽了。不在身邊的靈器213423524634哈哈哈哈哈哈哈哈哈哈哈哈啊"
    },{
        "date" : "2020/08/03",
        "category" : "生技醫療",
        "center" : "財富處",
        "future" : "股票大漲",
        "content" : "因應疫情影響，疫苗研發成功",
    }
]

class SearchForm(Form):
    """
    這個方法是將搜尋表單存在routes中，因此它將會出現應用的所有頁面中
    不需要在所有render_template()呼叫中將表單作為顯示模板參數新增進去。
    """
    keyword = TextField('請輸入關鍵字:', validators=[validators.required()])
    
    @app.route('/searchbykeyword', methods=['GET','POST'])
    @login_required
    def searchbykeyword():
        index_name_report = "index_name_keyword"
        index_name_weeknote = "index_name_weeknote"
        form = SearchForm(request.form)
        report_results_list = []
        weeknote_results_list = []

        if (request.method=='POST'):
            keyword =request.form['keyword']
            
            body = {
                "query": {
                   "bool": {
                            "should": [
                                { "match": { "com_name": keyword }},
                                { "match": { "text": keyword}}
                            ]
                    }
            },
                "highlight" : {
                    "fields" : {
                        "text" : {}
                    }
                }
            }
            weeknote_body = {
                "query": {
                   "bool": {
                            "should": [
                                { "match": { "future_view": keyword }},
                                { "match": { "content": keyword}}
                            ]
                    }
            },
                "highlight" : {
                    "fields" : {
                        "text" : {}
                    }
                }
            }

            report_results = es.search(index=index_name_report, body=body)
            weeknote_results = es.search(index=index_name_weeknote, body=weeknote_body)
            '''
            results_list將會回傳es的搜尋結果
            如果未搜尋前這個list會是空值(不顯示任何一筆)
            '''
            for i in range(len(report_results["hits"]["hits"] )):
                report_results_list.append(report_results["hits"]["hits"][i].get('_source'))
            for i in range(len(weeknote_results["hits"]["hits"] )):
                weeknote_results_list.append(weeknote_results["hits"]["hits"][i].get('_source'))
            return render_template('searchbykeyword.html', user=current_user, ES=report_results_list, week=weeknote_results_list, form=form)
        else:
            return render_template('searchbykeyword.html', user=current_user, ES=report_results_list, week=weeknote_results_list, form=form)
    
    @app.route('/searchbykeyword_2',methods=['GET','POST'])
    @login_required
    def searchbykeyword_2():
        index_name_report = "index_name_keyword2"
        index_name_weeknote = "index_name_weeknote"
        form = SearchForm(request.form)
        report_results_list = []
        weeknote_results_list = []

        if (request.method=='POST'):
            keyword =request.form['keyword']
            
            body = {
                "query": {
                   "bool": {
                            "should": [
                                { "match": { "com_name": keyword }},
                                { "match": { "text": keyword}}
                            ]
                    }
            },
                "highlight" : {
                    "fields" : {
                        "text" : {}
                    }
                }
            }
            weeknote_body = {
                "query": {
                   "bool": {
                            "should": [
                                { "match": { "future_view": keyword }},
                                { "match": { "content": keyword}}
                            ]
                    }
            },
                "highlight" : {
                    "fields" : {
                        "text" : {}
                    }
                }
            }

            report_results = es.search(index=index_name_report, body=body)
            weeknote_results = es.search(index=index_name_weeknote, body=weeknote_body)
            '''
            results_list將會回傳es的搜尋結果
            如果未搜尋前這個list會是空值(不顯示任何一筆)
            '''
            for i in range(len(report_results["hits"]["hits"] )):
                report_results_list.append(report_results["hits"]["hits"][i].get('_source'))
            for i in range(len(weeknote_results["hits"]["hits"] )):
                weeknote_results_list.append(weeknote_results["hits"]["hits"][i].get('_source'))
            return render_template('searchbykeyword_2.html', user=current_user, ES=report_results_list, week=weeknote_results_list, form=form)
        else:
            return render_template('searchbykeyword_2.html', user=current_user, ES=report_results_list, week=weeknote_results_list, form=form)
        

    @app.route('/searchbykeyword_full', methods=['GET','POST'])
    @login_required
    def searchbykeyword_full():
        index_name_report = "index_name_fulltext"
        index_name_weeknote = "index_name_weeknote"
        form = SearchForm(request.form)
        report_results_list = []
        weeknote_results_list = []

        if (request.method=='POST'):
            keyword =request.form['keyword']
            
            body = {
                "query": {
                   "bool": {
                            "should": [
                                { "match": { "com_name": keyword }},
                                { "match": { "text": keyword}}
                            ]
                    }
            },
                "highlight" : {
                    "fields" : {
                        "text" : {}
                    }
                }
            }
            weeknote_body = {
                "query": {
                   "bool": {
                            "should": [
                                { "match": { "future_view": keyword }},
                                { "match": { "content": keyword}}
                            ]
                    }
            },
                "highlight" : {
                    "fields" : {
                        "text" : {}
                    }
                }
            }

            report_results = es.search(index=index_name_report, body=body)
            weeknote_results = es.search(index=index_name_weeknote, body=weeknote_body)

            for i in range(len(report_results["hits"]["hits"] )):
                hightlight_list = []
                results_dict = report_results["hits"]["hits"][i].get('_source')
                try:
                    for j in range(len(report_results["hits"]["hits"][i].get('highlight').get('text'))):
                        hightlight_list.append(report_results["hits"]["hits"][i].get('highlight').get('text')[j])
                except:
                    hightlight_list.append(report_results["hits"]["hits"][i].get('_source').get('text'))
                results_dict['high_light'] = hightlight_list
                report_results_list.append(results_dict)
            for i in range(len(weeknote_results["hits"]["hits"] )):
                weeknote_results_list.append(weeknote_results["hits"]["hits"][i].get('_source'))
                
            return render_template('searchbykeyword_full.html', user=current_user, ES=report_results_list, week=weeknote_results_list, form=form)
        else:
            return render_template('searchbykeyword_full.html', user=current_user, ES=report_results_list, week=weeknote_results_list, form=form)
    @app.route('/content_table',methods=['GET','POST'])
    @login_required
    def content_table():
        index_name_report = "cf_credit_data_retrieval"
        index_name_weeknote = "cf_credit_data_retrieval"
        form = SearchForm(request.form)
        report_results_list = []
        weeknote_results_list = []


        if (request.method=='POST'):
            request_form = {
                'typein' : request.form['typein'],
                
            }
            
            body={
                'query':{
                    'bool':{
                        "should": [
                                            { "match_phrase": { "com_name": request_form['typein']}},
                                            { "match_phrase": { "text": request_form['typein']}},
                                            
                                        ]
                
                    }
                },
                'highlight':{
                    'fields':{
                        'text':{}
                    }
                },
                'sort':[
                                {
                                    '_score':{'order':'desc'}
                                },
                                {
                                    "doc_date":{'order':'desc'}
                                }
                            ]
            }
           

            report_results = es.search(index=index_name_report, body=body)
            #weeknote_results = es.search(index=index_name_weeknote, body=weeknote_body)
            '''
            results_list將會回傳es的搜尋結果
            如果未搜尋前這個list會是空值(不顯示任何一筆)
            '''
            for i in range(len(report_results["hits"]["hits"] )):
                hightlight_list = []
                results_dict = report_results["hits"]["hits"][i].get('_source')
                try:
                    for j in range(len(report_results["hits"]["hits"][i].get('highlight').get('text'))):
                        hightlight_list.append(report_results["hits"]["hits"][i].get('highlight').get('text')[j])
                except:
                    hightlight_list.append(report_results["hits"]["hits"][i].get('_source').get('text'))
                results_dict['high_light'] = hightlight_list
                report_results_list.append(results_dict)
            #for i in range(len(weeknote_results["hits"]["hits"] )):
                #weeknote_results_list.append(weeknote_results["hits"]["hits"][i].get('_source'))
         
            return render_template('content_table.html', user=current_user, report_posts=report_results_list,report_table = json.dumps(report_results_list))
        else:
            return render_template('content_table.html', user=current_user, report_posts=report_results_list,report_table = json.dumps(report_results_list))

    @app.route('/content_table_log',methods=['GET','POST'])
    @login_required
    def content_table_log():
        if (request.method =='POST'):
            data_received = request.data
        return data_received

    @app.route('/content_table2',methods=['GET','POST'])
    @login_required
    def content_table2():
        index_name_report = "cf_credit_data_retrieval"
        index_name_weeknote = "cf_credit_data_retrieval"
        form = SearchForm(request.form)
        report_results_list = []
        weeknote_results_list = []

        if (request.method=='POST'):
            request_form = {
                'typein' : request.form['typein'],
                'branch' : request.form['branch'],
                'caseid' : request.form['caseid'],
                'category_num' : request.form['category_num']
            }
            
            body={
                'query':{
                    'bool':{
                        "should": [
                                            { "match_phrase": { "com_name": request_form['typein']}},
                                            { "match_phrase": { "text": request_form['typein']}},
                                            { "match_phrase": { "bu_name": request_form["branch"]}},
                                            { "match_phrase": { "business_category": request_form["category_num"]}},
                                            { "match_phrase": { "company_id": request_form['caseid']}}
                                        ]
                
                    }
                },
                'highlight':{
                    'fields':{
                        'text':{}
                    }
                },
                'sort':[
                                {
                                    'doc_date':{'order':'desc'}
                                },
                                {
                                    "_score":{'order':'desc'}
                                }
                            ]
            }
           

            report_results = es.search(index=index_name_report, body=body)
            #weeknote_results = es.search(index=index_name_weeknote, body=weeknote_body)
            '''
            results_list將會回傳es的搜尋結果
            如果未搜尋前這個list會是空值(不顯示任何一筆)
            '''
            for i in range(len(report_results["hits"]["hits"] )):
                hightlight_list = []
                results_dict = report_results["hits"]["hits"][i].get('_source')
                try:
                    for j in range(len(report_results["hits"]["hits"][i].get('highlight').get('text'))):
                        hightlight_list.append(report_results["hits"]["hits"][i].get('highlight').get('text')[j])
                except:
                    hightlight_list.append(report_results["hits"]["hits"][i].get('_source').get('text'))
                results_dict['high_light'] = hightlight_list
                report_results_list.append(results_dict)
            #for i in range(len(weeknote_results["hits"]["hits"] )):
                #weeknote_results_list.append(weeknote_results["hits"]["hits"][i].get('_source'))
         
            return render_template('content_table2.html', user=current_user, report_posts=report_results_list, form=form)
        else:
            return render_template('content_table2.html', user=current_user, report_posts=report_results_list, form=form)

    @app.route('/content_table3',methods=['GET','POST'])
    @login_required
    def content_table3():
        index_name_report = "cf_credit_data_retrieval"
        index_name_weeknote = "cf_credit_data_retrieval"
        form = SearchForm(request.form)
        report_results_list = []
        weeknote_results_list = []

        if (request.method=='POST'):
            request_form = {
                'typein' : request.form['typein'],
                'branch' : request.form['branch'],
                'caseid' : request.form['caseid'],
                'category_num' : request.form['category_num']
            }
            
            body={
                'query':{
                    'bool':{
                        "should": [
                                            { "match_phrase": { "com_name": request_form['typein']}},
                                            { "match_phrase": { "text": request_form['typein']}},
                                            { "match_phrase": { "bu_name": request_form["branch"]}},
                                            { "match_phrase": { "business_category": request_form["category_num"]}},
                                            { "match_phrase": { "company_id": request_form['caseid']}}
                                        ]
                
                    }
                },
                'highlight':{
                    'fields':{
                        'text':{}
                    }
                },
                'sort':[
                                {
                                    'doc_date':{'order':'desc'}
                                },
                                {
                                    "_score":{'order':'desc'}
                                }
                            ]
            }
           

            report_results = es.search(index=index_name_report, body=body)
            #weeknote_results = es.search(index=index_name_weeknote, body=weeknote_body)
            '''
            results_list將會回傳es的搜尋結果
            如果未搜尋前這個list會是空值(不顯示任何一筆)
            '''
            for i in range(len(report_results["hits"]["hits"] )):
                hightlight_list = []
                results_dict = report_results["hits"]["hits"][i].get('_source')
                try:
                    for j in range(len(report_results["hits"]["hits"][i].get('highlight').get('text'))):
                        hightlight_list.append(report_results["hits"]["hits"][i].get('highlight').get('text')[j])
                except:
                    hightlight_list.append(report_results["hits"]["hits"][i].get('_source').get('text'))
                results_dict['high_light'] = hightlight_list
                report_results_list.append(results_dict)
            #for i in range(len(weeknote_results["hits"]["hits"] )):
                #weeknote_results_list.append(weeknote_results["hits"]["hits"][i].get('_source'))
         
            return render_template('content_table3.html', user=current_user, report_posts=report_results_list, form=form)
        else:
            return render_template('content_table3.html', user=current_user, report_posts=report_results_list, form=form)
####  setup routes  ####




####  setup routes  ####





####  setup routes  ####
@app.route("/login", methods=["GET", "POST"])
def login():
    # clear the inital flash message
    session.clear()
    if request.method == 'GET':
        return render_template('login.html')

    # get the form data
    username = request.form['username']
    password = request.form['password']

    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    # query the user
    registered_user = User.query.filter_by(username=username).first()

    # check_password_hash檢查hash過的密碼是否一致，回傳True/False。
    if registered_user is None or bcrypt.check_password_hash(registered_user.password, password) == False:
        flash('Invalid Username/Password')
        return render_template('login.html')

    # login the user
    login_user(registered_user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('content_table'))


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        session.clear()
        return render_template('register.html')

    # get the data from our form
    password = request.form['password']
    conf_password = request.form['confirm-password']
    username = request.form['username']
    email = request.form['email']

    # make sure the password match
    if conf_password != password:
        flash("Passwords do not match")
        return render_template('register.html')

    # check if it meets the right complexity
    check_password = password_check(password)

    # generate error messages if it doesnt pass
    if True in check_password.values():
        for k,v in check_password.items():
            if str(v) is "True":
                flash(k)

        return render_template('register.html')

    # hash the password for storage
    pw_hash = bcrypt.generate_password_hash(password)

    # create a user, and check if its unique
    user = User(username, pw_hash, email)
    u_unique = user.unique()

    # add the user
    if u_unique == 0:
        db.session.add(user)
        db.session.commit()
        flash("Account Created")
        return redirect(url_for('login'))

    # else error check what the problem is
    elif u_unique == -1:
        flash("Email address already in use.")
        return render_template('register.html')

    elif u_unique == -2:
        flash("Username already in use.")
        return render_template('register.html')

    else:
        flash("Username and Email already in use.")
        return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

####  end routes  ####

# required function for loading the right user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# check password complexity
def password_check(password):

    # calculating the length
    length_error = len(password) <= 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for lowercase
    character_error = re.search(r"[a-zA-Z]", password) is None

    ret = {
        'Password is less than 8 characters' : length_error,
        'Password does not contain a number' : digit_error,
        'Password does not contain a english character' : character_error,
    }

    return ret


if __name__ == "__main__":
	app.run(host='0.0.0.0')
