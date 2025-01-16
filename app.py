from flask import Flask, request, jsonify
from extensions import db
from models import UserInfo, UserSpending
from pymongo import MongoClient, errors

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_vouchers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from pymongo import MongoClient
from pymongo.server_api import ServerApi

cloud_uri = "mongodb+srv://petkovskibojan8891:f0y4QHEggv8ox8cB@cluster0.iiujb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
cloud_client = MongoClient(cloud_uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
cloud_db = cloud_client["ProjectUserSpending"]
cloud_collection = cloud_db["user_voucher_collection"]

local_uri = "mongodb://localhost:27017/"
local_client = MongoClient(local_uri, serverSelectionTimeoutMS=5000)
local_db = local_client["ProjectUserSpending"]
local_collection = local_db["user_voucher_collection"]

def add_data_to_both(datapoint):
    try:
        if not cloud_collection.find_one({"user_id": datapoint["user_id"]}):
            cloud_collection.insert_one(datapoint)
            print("Data added to cloud MongoDB.")
        else:
            print(f"Data for user_id {datapoint['user_id']} already exists in cloud MongoDB.")
    except errors.PyMongoError as e:
        print(f"Failed to add data to cloud MongoDB: {e}")
    try:
        if not local_collection.find_one({"user_id": datapoint["user_id"]}):
            local_collection.insert_one(datapoint)
            print("Data added to local MongoDB.")
        else:
            print(f"Data for user_id {datapoint['user_id']} already exists in local MongoDB.")
    except errors.PyMongoError as e:
        print(f"Failed to add data to local MongoDB: {e}")


with app.app_context():
    db.create_all()

@app.route("/")
def home_page_view():
    return jsonify("Users spending info home page")

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
    existing_user = UserInfo.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"message": "User with this email already exists."}), 409
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
    try:
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
            for data in users_vouchers:
                add_data_to_both(data)
            message = f"Vneseni {len(users_vouchers)} podatoci vo MongoDB lokalno i na oblak!"
            return jsonify({"message": message, "count": len(users_vouchers)}), 201
        else:
            return jsonify({"message": "Nema korisnici koi go isponuvaat uslovot za da bidat vneseni vo MongoDB"}), 200

    except Exception as e:
        return jsonify({"error": "Nastana greska", "details": str(e)}), 500


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



if __name__ == '__main__':
    app.run(debug=True, port=5001)
