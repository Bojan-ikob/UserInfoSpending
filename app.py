from flask import Flask, request, jsonify, render_template
from extensions import db
from models import UserInfo

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_vouchers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    # db.drop_all()
    db.create_all()


@app.route("/")
def home_page_view():
    users = UserInfo.query.all()
    return jsonify([user.to_dict() for user in users])


if __name__ == '__main__':
    app.run(debug=True)