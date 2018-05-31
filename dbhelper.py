from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from datetime import date, datetime, timedelta
from __init__ import db, app


class User(db.Model):
    """
    用户信息，包括客户和供应商
    """
    __tablename__ = 'Customer'
    CustomerID = db.Column(db.Integer, primary_key=True)
    AccountName = db.Column(db.Unicode(None))
    CustomerType = db.Column(db.Unicode(None))   # 0:客户，292:供应商
    FullName = db.Column(db.Unicode(None))
    PassWord = db.Column(db.Unicode(None))
    CustomerNo = db.Column(db.Unicode(None))

    def get_CustomerNo(self):
        return self.CustomerNo

    def get_CustomerID(self):
        return self.CustomerID

    def to_json(self):
        return {
            "id": self.CustomerID,
            "AccountName": self.AccountName,
            "FullName": self.FullName,
            "CustomerType": self.CustomerType,
            "CustomerNo": self.CustomerNo,
        }

    def generate_auth_token(self, expiration=60*60*6):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.CustomerID})

    def hash_password(self):
        self.password_hash = generate_password_hash(self.PassWord)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired

        except BadSignature:
            return None  # invalid token

        user = User.query.get(data['id'])
        return user


class Order(db.Model):
    """
    客户的订单
    """
    __tablename__ = 'Order'
    OrderID = db.Column(db.Integer, primary_key=True)
    CustomerNo = db.Column(db.String(50))
    TotalMoneyTax = db.Column(db.Float)
    OrderNo = db.Column(db.String(50))
    Quarter = db.Column(db.Integer)
    FStatus = db.Column(db.Integer)
    ClothType = db.Column(db.Integer)
    FollowEmp = db.Column(db.Integer)
    IsRelease = db.Column(db.Integer)
    Class = db.Column(db.Integer)
    OrderDate = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, *args,  **kwargs):
        #TODO:临时订单号生产，以后可能不要
        today = date.today()
        datetime_today = datetime.strptime(str(today), '%Y-%m-%d')
        count = len(Order.query.filter(
            Order.OrderDate >= datetime_today,
            Order.OrderDate <= datetime_today + timedelta(days=1)
        ).all()) + 1
        # 暂时设定默认值
        self.OrderNo = "OR%s%s" % (datetime_today.strftime('%Y%m%d'), '{:0>4}'.format(count))
        self.FStatus = 0      # 未审批
        self.IsRelease = 0    # 预备单
        self.TotalMoneyTax = 0
        self.Class = 144      # 销售下单

        super(Order, self).__init__(*args, **kwargs)

    def to_json(self):

            self.order_detail = OrderDetailed.query.filter_by(OrderID=self.OrderID).all()
            self.FStatusName = Dictionaries.query.filter_by(DictionariesID=self.FStatus).first()
            self.QuarterName = Dictionaries.query.filter_by(DictionariesID=self.Quarter).first()
            self.ClothesName = Dictionaries.query.filter_by(DictionariesID=self.ClothType).first()
            self.FollowEmpName = Employee.query.filter_by(EmployeeID=self.FollowEmp).first()
            self.ClassName = Dictionaries.query.filter_by(DictionariesID=self.Class).first()

            return {
                "id": self.OrderID,
                "CustomerNo": self.CustomerNo,
                "TotalMoneyTax": self.TotalMoneyTax,
                "OrderNo": self.OrderNo,
                "FStatusName": self.FStatusName.get_name() if self.FStatusName else "",
                "QuarterName": self.QuarterName.get_name() if self.QuarterName else "",
                "ClothesName": self.ClothesName.get_name() if self.ClothesName else "",
                "FollowEmpName": self.FollowEmpName.get_name() if self.FollowEmpName else "",
                "ClassName": self.ClassName.get_name() if self.ClassName else "",
                "IsRelease": "正式订单" if self.IsRelease > 0 else "预备订单",
                "order_detail": [e.to_json() for e in self.order_detail],
                "OrderDate": str(self.OrderDate),
            }

class OrderDetailed(db.Model):
    """
    客户订单明细：　包含每一张单的产品明细
    """
    __tablename__ = 'OrderDetailed'
    OrderDetailID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.String)
    ConsumerColor = db.Column(db.String)
    ConsumerNo = db.Column(db.String)
    OrderNo = db.Column(db.String)
    Size = db.Column(db.Integer)
    Count = db.Column(db.Integer)
    TotalMoneyTax = db.Column(db.Float)
    DeliveryTime = db.Column(db.DateTime)

    def to_json(self):
        return {
            "id": self.OrderDetailID,
            "OrderID": self.OrderID,
            "ConsumerColor": self.ConsumerColor,
            "OrderNo": self.OrderNo,
            "Size": self.Size,
            "Count": self.Count,
            "ConsumerNo": self.ConsumerNo,
            "TotalMoneyTax": self.TotalMoneyTax,
            "DeliveryTime": str(self.DeliveryTime),
        }


class Archives(db.Model):
    """
    TODO:后面或许表会变或者做视图,，或者添加状态识别哪些样衣可以下单
    样衣
    """
    __tablename__ = 'Archives'
    ArchivesID = db.Column(db.Integer, primary_key=True)
    Code = db.Column(db.String)
    ClothesNo = db.Column(db.String)
    CmpColorNo = db.Column(db.String)
    ArchivesTypes = db.Column(db.String)
    ArchivesType = db.Column(db.String)
    StyleNo = db.Column(db.String)
    Sizes = db.Column(db.String)
    ClothesTypeID = db.Column(db.Integer)
    FStatus = db.Column(db.Integer)
    IsDelete = db.Column(db.Integer)
    CreateTime = db.Column(db.DateTime)

    def to_json(self):
        pictures = Picture.query.filter_by(ClothesPictureID=self.ArchivesID)
        return {
            "id": self.ArchivesID,
            "Code": self.Code,
            "ClothesNo": self.ClothesNo,
            "CmpColorNo": self.CmpColorNo,
            "Sizes": self.Sizes,
            "ClothesTypeID": self.ClothesTypeID,
            "ArchivesTypes": self.ArchivesTypes,
            "ArchivesType": self.ArchivesType,
            "StyleNo": self.StyleNo,
            "pictures": [e.to_json() for e in pictures]
        }

class Picture(db.Model):
    """
    TODO:后面或许表会变或者做视图,，
    样衣图片
    """
    __tablename__ = 'Picture'
    PictureID = db.Column(db.Integer, primary_key=True)
    BarCode = db.Column(db.String)
    PicName = db.Column(db.String)
    ClothesPictureID = db.Column(db.String)
    URL = db.Column(db.String)


    def to_json(self):
        return {
            "id": self.PictureID,
            "BarCode": self.BarCode,
            "PicName": self.PicName,
            "ClothesPictureID": self.ClothesPictureID,
            "URL": self.URL
        }


class Dictionaries(db.Model):
    """
    字典解释
    """
    __tablename__ = 'Dictionaries'
    DictionariesID = db.Column(db.Integer, primary_key=True)
    DicName = db.Column(db.String)
    Rmarks = db.Column(db.String)

    def get_name(self):
        return self.DicName

    def to_json(self):
        return {
            "id": self.DictionariesID,
            "DicName": self.DicName,
            "Rmarks": self.Rmarks,
        }

class Employee(db.Model):
    """
    企业员工        
    """
    __tablename__ = 'Employee'
    EmployeeID = db.Column(db.Integer, primary_key=True)
    EmpName = db.Column(db.String)
    Mobile = db.Column(db.String)

    def get_name(self):
        return self.EmpName

    def to_json(self):
        return {
            "id": self.DictionariesID,
            "EmpName": self.EmpName,
            "Mobile": self.Mobile,
        }

