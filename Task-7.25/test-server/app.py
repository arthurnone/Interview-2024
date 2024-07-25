from flask import Flask, request
from flask_cors import CORS
import random
import datetime

app = Flask(__name__)
CORS(app)

user_template = {
    "id": None,
    "name": "",
    "username": "",
    "email": "",
    "phone": "",
    "website": "",
    "company": "",
    "dateJoined": "",
}

names = ["Wang", "ワン", "王"]
email = "root@wangpeifeng.com"
website = "wangpeifeng.com"
email_domain = "wangpeifeng.com"


def generate_user(count):
    name = random.choice(names)
    username = name + str(random.randint(10000, 99999))
    email = f"{name}@{email_domain}"
    phone = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    website = f"www.test-{count}.com"
    company = f"test-{random.randint(1000, 9999)}"
    date_joined = datetime.datetime.now() + datetime.timedelta(days=random.randint(-5, 5))
    date_joined_str = date_joined.strftime("%Y/%m/%d")

    return {
        "id": count,
        "avatar": f"https://i.pravatar.cc/300?u=wang-{count}",
        "name": f"{name} {count}",
        "username": username,
        "email": email,
        "phone": phone,
        "website": website,
        "company": company,
        "dateJoined": date_joined_str,
    }


@app.route('/api/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_user():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        user_data = []
        start = (page-1)*10 + 1
        end = start + 10
        for i in range(start, end):
            user_data.append(generate_user(i))
        return {
            "users": user_data,
            "page": {
                "page": page,
                "total": 1000
            },
            "status": "success"
        }
    else:
        data = request.get_json(force=True)
        if not data["id"]:
            date_joined = datetime.datetime.now() + datetime.timedelta(days=random.randint(-5, 5))
            date_joined_str = date_joined.strftime("%Y/%m/%d")
            data["id"] = random.randint(10000, 99999)
            data["dateJoined"] = date_joined_str
        return {
            "user": data,
            "status": "success"
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10001)
