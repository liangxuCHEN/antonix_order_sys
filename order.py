from flask_restful import Resource, reqparse
from dbhelper import Order, OrderDetailed
from __init__ import auth, db


class OrderListAPI(Resource):
    method_decorators = [auth.login_required]
    def __init__(self):
        # ------获取订单-------
        self.reqparser_get = reqparse.RequestParser()
        self.reqparser_get.add_argument("CustomerNo")
        self.reqparser_get.add_argument("FStatus")
        self.reqparser_get.add_argument("page")
        self.reqparser_get.add_argument("per_page")

        super(OrderListAPI, self).__init__()

    def get(self):
        args = self.reqparser_get.parse_args()
        if not args.CustomerNo:
            return {"message": "缺少参数", "data": "", "status": 501}, 200

        query = Order.query.filter_by(CustomerNo=args.CustomerNo)
        if args.FStatus:
            query = query.filter(FStatus=args.FStatus)
        #排序
        query = query.order_by(db.desc(Order.OrderDate))

        if args.page and args.per_page:
            entities = query.paginate(args.page, args.per_page).items
        else:
            entities = query.all()

        return {"message": "ok", "data": [e.to_json() for e in entities], "status": 200}, 200
    # def put(self):
    #     args = self.reqparser.parse_args()
    #     for value in args.values():
    #         if value is None:
    #             return {"message": "缺少参数", "data": "", "status": 500}, 200
    #
    #     user = Order.query.get(args.CustomerID)
    #     user.hash_password()
    #     if not user.verify_password(args.PassWord):
    #         return {"message": "旧密码不对", "data": "", "status": 500}, 200
    #
    #     user.PassWord =  args.new_password
    #     db.session.commit()
    #
    #     content = {}
    #     token = user.generate_auth_token()
    #     content['token'] = token.decode('ascii')
    #     content['CustomerID'] = user.CustomerID
    #     return {"message": "OK", "data": content, "status": 200}
    #
    # def post(self):
    #     required = self.reqparser_post.parse_args()
    #     for value in required.values():
    #         if value is None:
    #             return {"message": "value required not found", "data": "", "status": 500}, 200
    #
    #     user = User.query.filter_by(FullName=required.FullName).first()
    #     if user:
    #         user.hash_password()
    #         if not user.verify_password(required.PassWord):
    #             return {"message": "密码不对", "data": "", "status": 500}, 200
    #     else:
    #         return {"message": "用户不存在", "data": "", "status": 500}, 200
    #
    #     # print(user.to_json())
    #     content = {}
    #     token = user.generate_auth_token()
    #     content['token'] = token.decode('ascii')
    #     content['CustomerID'] = user.CustomerID
    #     return {"message": "OK", "data": content, "status": 200}, 200




