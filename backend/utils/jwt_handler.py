import jwt
import datetime
from config import Config

def create_token(user_id):

    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

    return token