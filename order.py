from flask_restful import Resource, reqparse
from flask import g, request
from dbhelper import Order, OrderDetailed, Archives, Employee
from __init__ import auth, db


class OrderListAPI(Resource):
    method_decorators = [auth.login_required]
    def __init__(self):
        # ------获取订单-------
        self.reqparser_get = reqparse.RequestParser()
        self.reqparser_get.add_argument("FStatus")
        self.reqparser_get.add_argument("Quarter")
        self.reqparser_get.add_argument("ClothType")
        self.reqparser_get.add_argument("begin_date")
        self.reqparser_get.add_argument("end_date")
        self.reqparser_get.add_argument("page", type=int)
        self.reqparser_get.add_argument("per_page", type=int)

        # ------新增订单--------
        self.reqparser_post = reqparse.RequestParser()
        self.reqparser_post.add_argument("order_details", type=list, location='json')
        self.reqparser_post.add_argument("FollowEmpName", location='json')

        super(OrderListAPI, self).__init__()

    def get(self):
        args = self.reqparser_get.parse_args()
        if g.user:
            CustomerNo = g.user.get_CustomerNo()
            if not CustomerNo:
                return {"message": "TOKEN已经过期，请重新登录", "data": "", "status": 501}, 200
        else:
            return {"message": "TOKEN已经过期，请重新登录", "data": "", "status": 501}, 200

        print(CustomerNo)

        query = Order.query.filter_by(CustomerNo=CustomerNo)
        if args.FStatus:
            query = query.filter(Order.FStatus==args.FStatus)
        if args.Quarter:
            query = query.filter(Order.Quarter==args.Quarter)
        if args.ClothType:
            query = query.filter(Order.ClothType==args.ClothType)

        if args.begin_date:
            query = query.filter(Order.OrderDate >= args.begin_date)
        if args.end_date:
            query = query.filter(Order.OrderDate <= args.end_date)
        #排序
        query = query.order_by(db.desc(Order.OrderDate))

        if args.page and args.per_page:
            entities = query.paginate(args.page, args.per_page).items
        else:
            entities = query.all()

        return {"message": "ok", "data": [e.to_json() for e in entities], "status": 200}, 200

    def post(self):
        """
        新增订单
        :return: 
        """
        # return {"message": "暂不开放", "data": "", "status": 200}, 200
        # try:
        print('========POST==========')

        #args = self.reqparser_post.parse_args()
        #
        print(request.args)
        print(request.data)
        print(request.json)
        #
        # if args.FollowEmpName:
        #     FollowEmp = Employee.query.filter_by(EmpName=args.FollowEmpName).first()
        #     if FollowEmp:
        #         args['FollowEmp'] = FollowEmp
        #
        # del (args['FollowEmpName'])
        #
        # if not args.order_details:
        #     return {"message": "缺少参数", "data": "", "status": 501}, 200


        order_details = request.json['order_details']
        # for item in order_details:
        #     print(type(item))
        #     for k,v in item.items():
        #         print(k,v)

        # del(args['order_details'])

        # args['CustomerNo'] = g.user.get_CustomerNo()

        #TODO:暂时没有数据表存，后面再保存，现在返回处理的数据结果
        # order = Order(**args)
        # db.session.add(order)
        # db.session.commit()

        #print(order.to_json())
        return {"message": "返回输入数据，检验是否与输入相符", "data": {'order':order_details, 'customerNo': g.user.get_CustomerNo()}, "status": 200}, 200


class OrderDetailListAPI(Resource):
    method_decorators = [auth.login_required]

    def __init__(self):
        # ------获取订单明细-------
        self.reqparser_get = reqparse.RequestParser()
        self.reqparser_get.add_argument("OrderID")

        super(OrderDetailListAPI, self).__init__()

    def get(self):
        args = self.reqparser_get.parse_args()
        if not args.OrderID:
            return {"message": "缺少参数", "data": "", "status": 501}, 200

        query = OrderDetailed.query.filter_by(OrderID=args.OrderID)
        #排序
        query = query.order_by(db.desc(OrderDetailed.DeliveryTime))

        entities = query.all()

        return {"message": "ok", "data": [e.to_json() for e in entities], "status": 200}, 200


class ArchivesListAPI(Resource):
    method_decorators = [auth.login_required]

    def __init__(self):
        # ------获取样衣列表明细-------
        self.reqparser_get = reqparse.RequestParser()
        self.reqparser_get.add_argument("ClothesTypeID")
        self.reqparser_get.add_argument("Sizes")
        self.reqparser_get.add_argument("page", type=int)
        self.reqparser_get.add_argument("per_page", type=int)

        super(ArchivesListAPI, self).__init__()


    def get(self):
        args = self.reqparser_get.parse_args()
        query = Archives.query

        if args.ClothesTypeID:
            query = query.filter(Archives.ClothesTypeID==args.ClothesTypeID)
        if args.Sizes:
            query = query.filter(Archives.Sizes==args.Sizes)

        # 排序
        query = query.order_by(db.desc(Archives.CreateTime))

        if args.page and args.per_page:
            entities = query.paginate(args.page, args.per_page).items
        else:
            entities = query.all()


        return {"message": "ok", "data": [e.to_json() for e in entities], "status": 200}, 200