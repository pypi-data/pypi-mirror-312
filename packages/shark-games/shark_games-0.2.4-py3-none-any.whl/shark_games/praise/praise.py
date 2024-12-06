import random

def main(user_info:dict):
    user_name = user_info["name"]
    user_mention = "@" + user_info["username"]
    if user_info["host"]:
        user_mention += "@" +  user_info["host"]
    praise_list = [
        f"You are such a cutie, {user_name}",
        f"*pats {user_name}*",
        f"*hugs {user_name}*",
        f"You look so good today {user_name}!"
    ]
    return user_mention + " " + random.choice(praise_list)