
from flask import Flask, request, jsonify, render_template
from extensions import db
from models import UserInfo, UserSpending

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_vouchers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/users', methods=['GET'])
def get_users():
    user_info = UserInfo.query.all()
    return jsonify([user.to_dict() for user in user_info])


@app.route('/user_spending', methods=['GET'])
def get_user_spending():
    user_spending = UserSpending.query.all()
    return jsonify([user.to_dict() for user in user_spending])



if __name__ == '__main__':
    app.run(debug=True)
