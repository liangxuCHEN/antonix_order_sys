from flask_restful import Resource, reqparse
from __init__ import *
from dbhelper import User
from order import OrderListAPI

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(FullName=username_or_token).first()
        #TODO: 后面就不要
        if user:
            user.hash_password()
            if not user.verify_password(password):
                return False
        else:
            return False

    print(user.to_json())

    return True

@app.route('/api/test')
@auth.login_required
def api_root():
    return 'Hi %s Welcome, app for order system opened now! ' % auth.username()



class UserAPI(Resource):
    def __init__(self):
        # ------修改密码-------
        self.reqparser_put = reqparse.RequestParser()
        self.reqparser_put.add_argument("CustomerID", location="json")
        self.reqparser_put.add_argument("PassWord", location="json")
        self.reqparser_put.add_argument("new_password", location="json")
        # ------登录---------
        self.reqparser_post = reqparse.RequestParser()
        self.reqparser_post.add_argument("FullName", location="json")
        self.reqparser_post.add_argument("PassWord", location="json")
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

        # print(user.to_json())
        content = {}
        token = user.generate_auth_token()
        content['token'] = token.decode('ascii')
        content['CustomerID'] = user.CustomerID
        content['CustomerNo'] = user.CustomerNo
        return {"message": "OK", "data": content, "status": 200}, 200


api.add_resource(UserAPI, '/api/v1/open/user', endpoint='client.user')
api.add_resource(OrderListAPI, '/api/v1/order_list', endpoint='client.order_list')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)