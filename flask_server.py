from flask import Flask, jsonify, request
from flask import abort
import database_model as dm
from database_model import db,app, User, Depository
import os


db.create_all()
@app.route('/depositories', methods=['GET'])
def get_neighbor_dep():
    if 'username' in request.args:
        us = User.query.get(request.args['username'])
        if (not us):
            message = 'user does not exist'
            return message_handler(status=404, info=message)
        else:
            result = Depository.query.all()
            js = [dm.depdict(i) for i in result]
            return jsonify(js)


@app.route('/depositories/check', methods=['GET'])
def check():
    dep = Depository.query.get(request.args['id'])
    if dep.chkcode == request.args['chkcode']:
        message = 'OK'
        return message_handler(status = 200, info = message)
    else:
        message = 'checkcode wrong'
        return message_handler(status = 404, info = message)


#@app.route('/depositories/update', methods=['GET'])
#def update_dep():


@app.route('/depositories/checkcode', methods=['GET'])
def get_chkcode():
    if 'username' in request.args and 'id' in request.args:
        us = User.query.get(request.args['username'])
        if (not us):
            message = 'user does not exist'
            return message_handler(status=404, info=message)
        else:
            dm.update_chk(request.args['id'])
            result = Depository.query.get(request.args['id'])
            chkcode = {
                'chkcode': result.chkcode
            }
            return jsonify(chkcode)


@app.route('/user/login', methods=['GET'])
def get_user():
    if 'username' in request.args:
        us = User.query.get(request.args['username'])
        if(not us):
            message = 'user does not exist'
            return message_handler(status = 404, info = message)
        if request.args['passwd'] == us.passwd:
            js = dm.userdict(us)
            return jsonify(js)
        else:
            message = 'Password wrong'
            return message_handler(status = 404, info = message)


@app.route('/user/register', methods=['GET'])
def register_user():
    if 'username' in request.args and 'passwd' in request.args:
        us = User.query.get(request.args['username'])
        if (not us):
            dm.register_user_to_db(request.args['username'], request.args['passwd'])
            return message_handler(status = 200,info = 'register success and we provide 5 yuan for probation')
        else:
            message = 'user has existed'
            return message_handler(status = 404, info = message)


@app.route('/user/pay')
def pay():
    if 'username' in request.args and 'passwd' in request.args:
        us = User.query.get(request.args['username'])
        if (not us):
            message = 'user does not exist'
            return message_handler(status=404, info=message)
        else:
            dm.pay_database(us, request.args['payment'])
            us = User.query.get(us.username)
            message = 'success and your balance is %r' %us.balance
            return message_handler(status = 200, info = message)


def message_handler(error=None, status = 200, info = ''):
    message = {
            'status': status,
            'message': info
    }
    resp = jsonify(message)
    resp.status_code = status
    return resp


if __name__ == '__main__':
    app.run(host = '0.0.0.0')