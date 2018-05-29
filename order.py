from flask_restful import Resource, reqparse
from dbhelper import Order, OrderDetailed, Archives, Picture
from __init__ import auth, db


class OrderListAPI(Resource):
    method_decorators = [auth.login_required]
    def __init__(self):
        # ------获取订单-------
        self.reqparser_get = reqparse.RequestParser()
        self.reqparser_get.add_argument("CustomerNo")
        self.reqparser_get.add_argument("FStatusName")
        self.reqparser_get.add_argument("QuarterName")
        self.reqparser_get.add_argument("ClothesName")
        self.reqparser_get.add_argument("begin_date")
        self.reqparser_get.add_argument("end_date")
        self.reqparser_get.add_argument("page", type=int)
        self.reqparser_get.add_argument("per_page", type=int)

        super(OrderListAPI, self).__init__()

    def get(self):
        args = self.reqparser_get.parse_args()
        if not args.CustomerNo:
            return {"message": "缺少参数", "data": "", "status": 501}, 200

        query = Order.query.filter_by(CustomerNo=args.CustomerNo)
        if args.FStatusName:
            query = query.filter(Order.FStatusName==args.FStatusName)
        if args.QuarterName:
            query = query.filter(Order.QuarterName==args.QuarterName)
        if args.ClothesName:
            query = query.filter(Order.ClothesName==args.ClothesName)

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