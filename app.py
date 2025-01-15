from flask import Flask, request, jsonify
from extensions import db, migrate
from models import UserInfo, UserSpending
from pymongo import MongoClient
import os

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_vouchers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

# MongoDB server
# uri = "mongodb+srv://petkovskibojan8891:f0y4QHEggv8ox8cB@cluster0.iiujb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# client = MongoClient(uri, server_api=ServerApi('1'))
# mongo_db = client['UsersInfoSpending']
# users_vouchers_collection = mongo_db['users_vouchers']

# MongoDB lokalno
client = MongoClient("mongodb://localhost:27017/")
mongo_db = client["ProjectUserSpending"]
users_vouchers_collection = mongo_db["user_voucher_collection"]


# with app.app_context():
#     db.create_all()

@app.route("/")
def home_page_view():
    return jsonify("Users spending info")

@app.route('/users', methods=['GET'])
def get_users():
    user_info = UserInfo.query.all()
    return jsonify([user.to_dict() for user in user_info])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = UserInfo.query.get_or_404(id)
    return jsonify(user.to_dict())

@app.route('/user_info', methods = ['POST'])
def add_user():
    data = request.get_json()
    new_user = UserInfo(name = data['name'], email = data['email'], age = data['age'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()),201

@app.route('/user_spending', methods = ['POST'])
def add_spending():
    data = request.get_json()
    new_spending = UserSpending(user_id = data['user_id'], money_spent = data['money_spent'], year = data['year'])
    db.session.add(new_spending)
    db.session.commit()
    return jsonify(new_spending.to_dict()),201

@app.route('/user_spending', methods=['GET'])
def get_user_spending():
    user_spending = UserSpending.query.all()
    spendings_list = [user.to_dict() for user in user_spending]
    return jsonify(spendings_list)

@app.route('/write_to_mongodb', methods=['POST'])
def write_to_mongodb():
    users = UserInfo.query.all()
    users_vouchers = []
    for user in users:
        spendings = UserSpending.query.filter_by(user_id=user.user_id).all()
        total_spent = sum([spending.money_spent for spending in spendings])
        if total_spent > 2000:
            user_data = {
                "user_id": user.user_id,
                "total_spent": total_spent,
            }
            users_vouchers.append(user_data)
    if users_vouchers:
        users_vouchers_collection.insert_many(users_vouchers)
    return jsonify({"message": "Uspesno vneseni podatoci vo MongoDB!", "count": len(users_vouchers)})

@app.route('/total_spent/<int:user_id>', methods=['GET'])
def get_total_spent(user_id):
    spendings = UserSpending.query.filter_by(user_id=user_id).all()
    total_spent = sum([spending.money_spent for spending in spendings])
    return jsonify({"user_id": user_id, "total_spent": total_spent})

@app.route('/average_spending_by_age', methods=['GET'])
def average_spending_by_age():
    age_groups = {
        "18-24": (18, 24),
        "25-30": (25, 30),
        "31-36": (31, 36),
        "37-47": (37, 47),
        ">47": (48, 100)
    }
    average_spending_by_age = {}
    for group, (min_age, max_age) in age_groups.items():
        users_in_group = UserInfo.query.filter(UserInfo.age >= min_age, UserInfo.age <= max_age).all()
        total_spent = 0
        total_users = 0
        for user in users_in_group:
            spendings = UserSpending.query.filter_by(user_id=user.user_id).all()
            total_spent += sum([spending.money_spent for spending in spendings])
            total_users += 1
        if total_users > 0:
            average_spending = total_spent / total_users
            average_spending = round(average_spending, 2)
        else:
            average_spending = 0
        average_spending_by_age[group] = average_spending
    return jsonify(average_spending_by_age)



# if __name__ == '__main__':
#     app.run(debug=True, port=5001)
os.environ['FLASK_APP'] = 'app.py'
if __name__ == '__main__':
    flask_app = os.getenv('FLASK_APP')
    if flask_app:
        print(f"FLASK_APP is set to: {flask_app}")
    else:
        print("FLASK_APP is not set. Please set it using 'export FLASK_APP=app.py' (Linux/Mac) or 'set FLASK_APP=app.py' (Windows).")
    app.run(debug=True, port=5001)