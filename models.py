from extensions import db

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    age = db.Column(db.Integer)

    spendings = db.relationship('UserSpending', backref='user', lazy=True)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'spendings': [spending.to_dict() for spending in self.spendings]
        }


class UserSpending(db.Model):
    __tablename__ = 'user_spending'
    # id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'),primary_key=True)
    money_spent = db.Column(db.Float)
    year = db.Column(db.Integer)

    def to_dict(self):
        return {
            # 'id':self.id,
            'user_id':self.user_id,
            'money_spent': self.money_spent,
            'year': self.year
        }

