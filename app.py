from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import operator
import jwt
import hashlib

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.vwj3mqc.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

SECRET_KEY = 'SPARTA'

@app.route('/')
def home():
        return render_template('index.html')


@app.route('/register')
def register():
    return render_template('regist.html')

@app.route('/main')
def main():
    token_receive = request.cookies.get('mytoken')


    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        userinfo = db.users.find_one({'id': payload['id']}, {'_id': 0})
        nickname = userinfo['nick']
    except jwt.ExpiredSignatureError:
        return render_template('index.html', msg='로그인 시간이 만료되었습니다.')
    except jwt.exceptions.DecodeError:

      return render_template('index.html', msg='로그인 정보가 존재하지 않습니다')

    first = list(db.reviews.find({'number':'1'}, {'_id': False}))
    second = list(db.reviews.find({'number': '2'}, {'_id': False}))
    third = list(db.reviews.find({'number': '3'}, {'_id': False}))
    fourth = list(db.reviews.find({'number': '4'}, {'_id': False}))
    fifth = list(db.reviews.find({'number': '5'}, {'_id': False}))
    sixth = list(db.reviews.find({'number': '6'}, {'_id': False}))
    seventh = list(db.reviews.find({'number': '7'}, {'_id': False}))
    first_star = 0
    second_star = 0
    third_star = 0
    fourth_star = 0
    fifth_star = 0
    sixth_star = 0
    seventh_star = 0
    first_total= 0
    second_total= 0
    third_total = 0
    fourth_total = 0
    fifth_total = 0
    sixth_total = 0
    seventh_total = 0
    
    for i in first:
        first_star += int(i['star'])
    if len(first) != 0 :
        first_total = first_star / len(first)

    for i in second:
        second_star += int(i['star'])
    if len(second) != 0 :
        second_total = second_star/len(second)

    for i in third:
        third_star += int(i['star'])
    if len(third) != 0:
        third_total = third_star/len(third)

    for i in fourth:
        fourth_star += int(i['star'])
    if len(fourth) != 0:
        fourth_total = fourth_star/len(fourth)
    for i in fifth:
        fifth_star += int(i['star'])
    if len(fifth) != 0:
        fifth_total = fifth_star/len(fifth)

    for i in sixth:
        sixth_star += int(i['star'])
    if len(sixth) != 0:
        sixth_total = sixth_star/len(sixth)

    for i in seventh:
        seventh_star += int(i['star'])
    if len(seventh) != 0:
        seventh_total = seventh_star/len(seventh)

    star_assemble = {'1': first_total, '2': second_total, '3': third_total, '4': fourth_total, '5': fifth_total, '6': sixth_total, '7': seventh_total}
    star_reassemble = sorted(star_assemble.items(), key=operator.itemgetter(1), reverse=True)


    return render_template('main.html', nick=nickname, first=star_reassemble[0][0],first_star=star_reassemble[0][1], second=star_reassemble[1][0], second_star= star_reassemble[1][1], third=star_reassemble[2][0], third_star= star_reassemble[2][1], fourth=star_reassemble[3][0],  fourth_star= star_reassemble[3][1], fifth=star_reassemble[4][0], fifth_star= star_reassemble[4][1], sixth=star_reassemble[5][0], sixth_star= star_reassemble[5][1], seventh = star_reassemble[6][0], seventh_star = star_reassemble[6][1])


@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.users.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})

@app.route('/api/in', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.users.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:

        payload = {
         'id': id_receive,
       # 'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
                }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/sign_up/check_dup_id', methods=['POST'])
def check_dup_id():
    userid_receive = request.form['userid_give']
    exists = bool(db.users.find_one({"id": userid_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/sign_up/check_dup_nick', methods=['POST'])
def check_dup_nick():
    usernick_receive = request.form['usernick_give']
    exists = bool(db.users.find_one({"nick": usernick_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    userid_receive = request.form['userid_give']
    password_receive = request.form['password_give']
    usernick_receive = request.form['usernick_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "id": userid_receive,
        "pw": password_hash,
        "nick": usernick_receive,
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route("/reviews/get", methods=["POST"])
def review_get():
 number_recive = request.form['number_give']
 review_list=list(db.reviews.find({'number': number_recive},{'_id':False}))
 return jsonify({'reviews':review_list})

@app.route("/reviews/post", methods=["POST"])
def web_review_post():
        number_receive = request.form['number_give']
        title_receive = request.form['title_give']
        image_receive = request.form['image_give']
        star_receive = request.form['star_give']
        comment_receive = request.form['comment_give']
        doc = { 'number': number_receive,
                'title': title_receive,
                'image': image_receive,
                'star': star_receive,
                'comment': comment_receive
        }
        db.reviews.insert_one(doc)
        return jsonify({'msg': '리뷰 완료'})

@app.route('/detail')
def detail():
    token_receive = request.cookies.get('mytoken')
    numtoken_receive = request.cookies.get('numtoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        payload2 = jwt.decode(numtoken_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        userinfo = db.users.find_one({'id': payload['id']}, {'_id': 0})
        nickname = userinfo['nick']
        number = payload2['num']
    except jwt.ExpiredSignatureError:
        return render_template('index.html', msg='로그인 시간이 만료되었습니다.')
    except jwt.exceptions.DecodeError:
        # return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
        return render_template('index.html', msg='입력 정보가 존재하지 않습니다')

    return render_template('detail.html', nick=nickname, number=number)

@app.route('/api/detail', methods=['POST'])
def todetail():
        num_receive = request.form['num_give']

        payload2 = {
                'num': num_receive
        }

        token = jwt.encode(payload2, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)