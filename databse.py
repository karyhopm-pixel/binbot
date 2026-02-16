users = {}

def get_or_create_user(user_id):
    if user_id not in users:
        users[user_id] = {"credits": 10}
    return users[user_id]

def get_user_credits(user_id):
    return users.get(user_id, {}).get("credits", 10)

def update_user_credits(user_id, amount):
    if user_id in users:
        users[user_id]["credits"] += amount
