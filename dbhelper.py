import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from __init__ import db, app


class User(db.Model):
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
    __tablename__ = 'OrderDetailed'
    OrderDetailID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.String)
    ConsumerNo = db.Column(db.String)
    ConsumerColor = db.Column(db.String)
    OrderNo = db.Column(db.String)
    Size = db.Column(db.Integer)
    Count = db.Column(db.Integer)
    TotalMoneyTax = db.Column(db.Float)
    DeliveryTime = db.Column(db.DateTime)

    def to_json(self):
        return {
            "id": self.OrderDetailID,
            "CustomerNo": self.CustomerNo,
            "OrderID": self.OrderID,
            "ConsumerColor": self.ConsumerColor,
            "OrderNo": self.OrderNo,
            "Size": self.Size,
            "Count": self.Count,
            "StyleNo": self.StyleNo,
            "TotalMoneyTax": self.TotalMoneyTax,
            "DeliveryTime": str(self.DeliveryTime),
        }


