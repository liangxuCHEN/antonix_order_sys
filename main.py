from flask_restful import Resource, reqparse
from flask import g
from __init__ import *
from dbhelper import User
from order import OrderListAPI, OrderDetailListAPI, ArchivesListAPI


@auth.verify_password
def verify_password(username_or_token, password):
    # TODO:后面不要password, 只保留token
    # TODO:根据权限返回用户
    """
    这是验证权限
    :param username_or_token: 
    :param password: 
    :return: 
    """
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(FullName=username_or_token).first()
        if user:
            user.hash_password()
            if not user.verify_password(password):
                g.user = None
                return False
        else:
            g.user = None
            return False

    g.user = user
    return True

@app.route('/api/test')
@auth.login_required
def api_root():
    return 'Hi %s Welcome, app for order system opened now! ' % auth.username()



class UserAPI(Resource):
    def __init__(self):
        # ------修改密码-------
        self.reqparser_put = reqparse.RequestParser()
        self.reqparser_put.add_argument("CustomerID")
        self.reqparser_put.add_argument("PassWord")
        self.reqparser_put.add_argument("new_password")
        # ------登录---------
        self.reqparser_post = reqparse.RequestParser()
        self.reqparser_post.add_argument("FullName")
        self.reqparser_post.add_argument("PassWord")
        super(UserAPI, self).__init__()

    def put(self):
        args = self.reqparser_put.parse_args()
        for value in args.values():
            if value is None:
                return {"message": "缺少参数", "data": "", "status": 500}, 200

        user = User.query.get(args.CustomerID)
        user.hash_password()
        if not user.verify_password(args.PassWord):
            return {"message": "旧密码不对", "data": "", "status": 500}, 200

        user.PassWord =  args.new_password
        db.session.commit()

        content = {}
        token = user.generate_auth_token()
        content['token'] = token.decode('ascii')
        content['CustomerID'] = user.CustomerID
        content['CustomerNo'] = user.CustomerNo
        return {"message": "OK", "data": content, "status": 200}

    def post(self):
        required = self.reqparser_post.parse_args()
        for value in required.values():
            if value is None:
                return {"message": "value required not found", "data": "", "status": 500}, 200

        user = User.query.filter_by(FullName=required.FullName).first()
        if user:
            user.hash_password()
            if not user.verify_password(required.PassWord):
                return {"message": "密码不对", "data": "", "status": 500}, 200
        else:
            return {"message": "用户不存在", "data": "", "status": 500}, 200

        content = {}
        token = user.generate_auth_token()
        content['token'] = token.decode('ascii')
        content['CustomerID'] = user.CustomerID
        content['CustomerNo'] = user.CustomerNo
        return {"message": "OK", "data": content, "status": 200}, 200


# API 设定
api.add_resource(UserAPI, '/api/v1/open/user', endpoint='client.user')
api.add_resource(OrderListAPI, '/api/v1/order_list', endpoint='client.order_list')
api.add_resource(OrderDetailListAPI, '/api/v1/order_detail_list', endpoint='client.Order_detail_list')
api.add_resource(ArchivesListAPI, '/api/v1/archives_list', endpoint='client.archives_list')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)