from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
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
    __tablename__ = 'OrderV'
    OrderID = db.Column(db.Integer, primary_key=True)
    CustomerNo = db.Column(db.String)
    TotalMoneyTax = db.Column(db.Float)
    OrderNo = db.Column(db.String)
    QuarterName = db.Column(db.String)
    FStatusName = db.Column(db.String)
    ClothesName = db.Column(db.String)
    FollowEmpName = db.Column(db.String)
    OrderDate = db.Column(db.DateTime)

    def to_json(self):
            return {
                "id": self.OrderID,
                "CustomerNo": self.CustomerNo,
                "TotalMoneyTax": self.TotalMoneyTax,
                "OrderNo": self.OrderNo,
                "FStatusName": self.FStatusName,
                "QuarterName": self.QuarterName,
                "ClothesName": self.ClothesName,
                "FollowEmpName": self.FollowEmpName,
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