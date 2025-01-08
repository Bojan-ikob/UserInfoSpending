from flask import Flask, request, jsonify, render_template
from extensions import db
from flask_migrate import Migrate
from models import UserInfo, UserSpending

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_vouchers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = UserInfo.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add_user_spending', methods=['POST'])
def add_user_spending():
    data = request.get_json()
    user_spending = UserSpending(user_id=data['user_id'], year=data['year'], money_spent=data['money_spent'])
    db.session.add(user_spending)
    db.session.commit()
    return jsonify(user_spending.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)
