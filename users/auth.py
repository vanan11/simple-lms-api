from datetime import datetime, timedelta
from jose import jwt, JWTError
from ninja.security import HttpBearer
from django.contrib.auth.models import User

# 🔐 CONFIG
SECRET_KEY = "secret123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# 🔑 CREATE TOKEN
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 🔓 DECODE TOKEN
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# 🛡️ AUTH BEARER (INI YANG ERROR TADI)
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        payload = decode_token(token)

        if not payload:
            return None

        try:
            user = User.objects.get(id=payload["user_id"])
            return user
        except User.DoesNotExist:
            return None