from extensions import db



class UserInfo(db.Model):
    __tablename__ = 'user_info'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    age = db.Column(db.Integer)

    # Врска со таблицата user_spending
    spendings = db.relationship('UserSpending', backref='user', lazy=True)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'spendings': [spending.to_dict() for spending in self.spendings]  # Додај ги трошоците
        }


class UserSpending(db.Model):
    __tablename__ = 'user_spending'
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'), primary_key=True)
    money_spent = db.Column(db.Float)
    year = db.Column(db.Integer)

    def to_dict(self):
        return {
            'user_id':self.user_id,
            'money_spent': self.money_spent,
            'year': self.year
        }





# class UserInfo(db.Model):
#     __tablename__ = 'user_info'
#
#     user_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     age = db.Column(db.Integer, nullable=False)
#
#
#     def to_dict(self):
#         user_spendings = UserSpending.query.filter_by(user_id=self.user_id).all()
#         spendings_list = [{"money_spent": spending.money_spent, "year": spending.year} for spending in user_spendings]
#
#         return {
#             'user_id':self.user_id,
#             'name':self.name,
#             'email':self.email,
#             'age':self.age,
#             'spendings': spendings_list
#
#         }
#
# class UserSpending(db.Model):
#     __tablename__ = "user_spending"
#
#     user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'), primary_key = True)
#     money_spent = db.Column(db.Float, nullable = False, default = 0.0)
#     year = db.Column(db.Integer, nullable = False)
#     user = db.relationship('UserInfo', backref=db.backref('spending', lazy=True))
#     def to_dict(self):
#         return {
#             'user_id':self.user_id,
#             'money_spent':self.money_spent,
#             'year':self.year
#
#         }

