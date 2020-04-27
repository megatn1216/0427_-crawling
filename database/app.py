import os
import pymysql
from datetime import datetime
import time
from flask import Flask, render_template
from flask import request, redirect, abort, session, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import requests

app = Flask(__name__, 
            static_folder="static",
            template_folder="views")
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.secret_key = 'sookbun'

db = pymysql.connect(
    user='root',
    passwd='kt10149422',
    host='localhost',
    db='stock',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)




# ///////////////////////////////////
@app.route("/useradd", methods=['GET', 'POST'])
def useradd():
    message =''
    id = ''
    if request.method == 'POST':
        cursor = db.cursor()
        cursor.execute(f"""
            select id, name, password from author 
            where name = '{request.form['id']}'""")
        user = cursor.fetchone()
        if user is None:
            message = "회원이 아닙니다. 사용 가능합니다."
            id = f"{request.form['id']}"
            print(id)
        else:
            message = "id가 중복됩니다. 다른 id를 입력하세요."
            id = ''


        message=f"""<script>		
                alert('{message}');
                document.getElementById('id').value = '{id}';
                </script>"""
                # document.getElementById('id').value = ''{id}'';
                # $(document).ready(function(){
                #     $()
                # })
        

    return render_template('useradd.html', message=message, dup_id = id)


def get_menu():
    cursor = db.cursor()
    cursor.execute(f"select id, title, price, market_price, volume, time, author_id from interests where author_id= {session['user']['id']}")
    menu = [f"<tr><td><input type='checkbox' name='check{row['id']}'</td><td><a href='/{row['title']}'>{row['title']}</td><td>{row['price']}</td> <td>{row['market_price']}</td> <td>{row['volume']}</td> <td>{row['time']}</td></a></tr>"
            for row in cursor.fetchall()]
    # print(type('\n'.join(menu)))

    tableN = '\n'.join(menu)

    tableN = '<table border="1" bordercolor=black ><thead><tr><th>Check</th><th>종목</th><th>가격</th><th>시가총액</th><th>거래량</th><th>시간</th></tr></thead>' + tableN + '</table>'
    return tableN

@app.route("/", methods=['GET', 'POST'])
def index():    
#     title = 'Welcome ' + session['user']['name'] if 'user' in session else 'Welcome'
        
#     content = 'Welcome Python Class...'
#     return render_template('template.html',
#                            id="",
#                            title=title,
#                            content=content,
#                            menu=get_menu())
    message = ""
    if request.method == 'POST':
        cursor = db.cursor()
        cursor.execute(f"""
            select id, name, password from author 
            where name = '{request.form['id']}'""")
        user = cursor.fetchone()
        
        if user is None:
            message = "<p>회원이 아닙니다.</p>"
        else:
            cursor.execute(f"""
            select id, name, password from author 
            where name = '{request.form['id']}' and 
                  password = SHA2('{request.form['pw']}', 256)""")
            user = cursor.fetchone()
            print(user)
            if user is None:
                message = "<p>패스워드를 확인해 주세요</p>"
            else:
                # 로그인 성공시 리스트
                session['user'] = user
                return redirect("/main")
    
    return render_template('login.html', 
                           message=message
                           )

# @app.route("/delete", methods=['GET', 'POST'])
# def delete():
#     if request.method == 'POST':

#     return pass


@app.route("/main", methods=['GET', 'POST'])
def main():    
    
    if request.method == 'POST':
        cursor = db.cursor()
        uid = request.form['uid']
        passw = request.form['pw']
        print("id : ",uid, "pw: ", passw)
        cursor.execute(f"select * from author where name ='{uid}'")

        user = cursor.fetchone()
        if user is None:
            sql = f"""insert into author (name, password)
                    values ('{uid}',
                    SHA2('{passw}', 256))"""
            
            cursor.execute(sql)
            db.commit()
            message=f"""<script>		
                alert('가입 완료되었습니다.');
                </script>"""
            return render_template('login.html', message=message)
        else:
            message=f"""<script>		
                alert('중복된 ID입니다. ID 중복확인을 하세요.');
                </script>"""
            return render_template('useradd.html', message=message, dup_id = "")

        # print(passw)
        # print(uid)

    # title = 'Welcome ' + session['user']['name'] if 'user' in session else 'Welcome'    
    # content = 'Welcome Python Class...'

    return render_template('main.html',
                        #    id=session['user']['name'],
                        #    title=title,
                        #    content=content,
                           menu=get_menu())

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        cursor = db.cursor() 

        stock_name = request.form['title']

        # print(stock_name)
        # print(os.getcwd() +'\chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(os.getcwd() +'\chromedriver.exe', options=options)
        driver.implicitly_wait(3)
        url = f"https://www.naver.com"
        driver.get(url)

        driver.find_element_by_xpath('//*[@id="query"]').clear()
        driver.find_element_by_xpath('//*[@id="query"]').send_keys(stock_name)
        driver.find_element_by_xpath('//*[@id="search_btn"]').click()
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        vl = soup.select(".vl")[0].get_text()
        regex_volume = re.compile("거래량 (.+)")
        volume = regex_volume.findall(vl)[0]
        
        pcp = soup.select(".pcp")[0].get_text()
        regex_pcp = re.compile("전일종가 (.+)")
        closingPrice = regex_pcp.findall(pcp)[0]

        mc = soup.select(".mc")[0].get_text()
        regex_mc = re.compile("시가 총액 (.+)")
        marketCap = regex_mc.findall(mc)[0]

        print("거래량", volume)
        print("전일종가", closingPrice)
        print("시가총액", marketCap)


        sql = f"""
            insert into interests (title, price, market_price, volume, time, author_id)
            values ('{stock_name}', '{closingPrice}', '{marketCap}', '{volume}',
                    '{datetime.now()}', '{session['user']['id']}')
        """
        cursor.execute(sql)
        db.commit()

        return redirect('/main')
    
    return render_template('create.html', 
                           message='', 
                           menu=get_menu())


@app.route("/<title>")
def content(title):
    # print(title)
    url = f"https://search.naver.com/search.naver?ie=UTF-8&query={title}&sm=chr_hty"
    page = requests.get(url)
    
    soup = BeautifulSoup(page.text, 'html.parser')
    
    site=soup.select("#main_pack > div.nsite.section._nsiteBase > ul > li > dl > dt > span.url_area > a")[0].get_text()
    print(1)
    # infoTable=soup.select('#main_pack > div.nsite.section._nsiteBase > ul > li > dl > dt > span.url_area > a')[0].get_text()
    # for e in soup.select("#main_pack > div.news.section._prs_nws_all > ul > li > dl > dt > _sp_each_title")[0].get_text():
    #     print("*" * 100)
    #     print(e)
    # print(soup.select("#main_pack > div.news.section._prs_nws_all > ul > li > dl > dt > a")[0].get_text())
    # print(news)
    # news
    
    newslistN=[]
    # newslist=''
    for i in range(20):
        try:
            infoTable=soup.select(f'#sp_nws_all{i} > dl > dt > a')[0].get_text()
            infoTable2=soup.select(f'#sp_nws_all{i} > dl > dt > a')[0].attrs['href']
            # newslistN.append(infoTable)
            if 'http' in infoTable2:
                # print(infoTable)
                print(infoTable2)
                news = f"<li><a href='{infoTable2}' target='_black'>{infoTable}</a></li>"
                # print(news)
                newslistN.append(news)

                # newslist = '\n'.join(newslistN)
        except:
            pass

    print('\n'.join(newslistN))            

    # print("newslist")    
    # print(newslist)
    # print("newslist")
    #뉴스확인
    # for item in listN:
    #     print(item)
    # 

    # 테이블에 있을 경우 (db 인서트)
    


    # 테이블에 없을 경우 (db 업데이트)




    return render_template('stock_info.html',
                           title=title,
                           site=site,
                           news='\n'.join(newslistN)
                           )





























# @app.route("/delete/<id>")
# def delete(id):
#     cursor = db.cursor()
#     cursor.execute(f"delete from interests where id='{id}'")
#     db.commit()
    
#     return redirect("/")



# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     message = ""
#     if request.method == 'POST':
#         cursor = db.cursor()
#         cursor.execute(f"""
#             select id, name, profile, password from author 
#             where name = '{request.form['id']}'""")
#         user = cursor.fetchone()
        
#         if user is None:
#             message = "<p>회원이 아닙니다.</p>"
#         else:
#             cursor.execute(f"""
#             select id, name, profile, password from author 
#             where name = '{request.form['id']}' and 
#                   password = SHA2('{request.form['pw']}', 256)""")
#             user = cursor.fetchone()
            
#             if user is None:
#                 message = "<p>패스워드를 확인해 주세요</p>"
#             else:
#                 # 로그인 성공에는 메인으로
#                 session['user'] = user
#                 return redirect("/")
    
#     return render_template('login.html', 
#                            message=message, 
#                            menu=get_menu())

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route("/favicon.ico")
def favicon():
    return abort(404)

@app.route("/dbtest")
def dbtest():
    cursor = db.cursor()
    cursor.execute("select * from interests")
    return str(cursor.fetchall())

######################
## restful API

# @app.route("/api/author", methods=['get', 'post'])
# def author_list():
#     cursor = db.cursor()
    
#     if request.method == 'GET':
#         cursor.execute("select * from author")    
#         return jsonify(cursor.fetchall())
#     elif request.method == 'POST':
#         sql = f"""insert into author (name, profile, password)
#                   values ('{request.form['name']}', '{request.form['profile']}',
#                   SHA2('{request.form['password']}', 256))"""
#         cursor.execute(sql)
#         db.commit()
        
#         return jsonify({"success": True})
    
#     return abort(405)

# @app.route("/api/author/<author_id>", methods=['get', 'put', 'delete'])
# def author(author_id):
#     cursor = db.cursor()
    
#     if request.method == 'GET':
#         cursor.execute(f"select * from author where id = {author_id}")
#         author = cursor.fetchone()

#         if author:
#             return jsonify(author)
#         else:
#             return abort(404)

#     elif request.method == 'PUT':
#         sql = f"""update author set
#                   name = '{request.form['name']}',
#                   profile = '{request.form['profile']}',
#                   password = SHA2('{request.form['password']}', 256)
#                   where id = '{author_id}'"""
#         cursor.execute(sql)
#         db.commit()
#         return jsonify({"success": True})
    
#     elif request.method == 'DELETE':
#         cursor.execute(f"delete from author where id = '{author_id}'")
#         db.commit()
#         return jsonify({"success": True})
    
#     return abort(405)

# @app.route("/api/interests")
# @app.route("/api/author/<author_id>/interests")
# def interests_list(author_id=None):
#     cursor = db.cursor()
    
#     if author_id is None:
#         cursor.execute("select * from interests")
#     else:
#         cursor.execute(f"""select A.id, A.title, A.description, A.created, A.author_id
#                            from interests A, author B 
#                            where A.author_id = B.id and B.id = '{author_id}'""")    
#     return jsonify(cursor.fetchall())

app.run(port=8007)