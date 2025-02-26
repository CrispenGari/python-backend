import jwt
import re
from random import randint


SECRETE = '696650d131f129a8fa46b72a8eaa491c0b0dccd5f14cb026dcc48e884578cafc1ac3b92aa856f88a33de20dc0916808c0f97a194b8376f1e9a8c3223'


def generate_otp()->str:
    return str(randint(100000, 999999))

def decode_jwt(token: str) -> dict | None:
    p = jwt.decode(token, SECRETE, algorithms=["HS256"])
    return p

def encode_jwt(payload: dict)->str:
    t = jwt.encode(payload, SECRETE, algorithm="HS256")
    return t

# username1@gmail.cm
def validate_email(email: str) -> bool:
    regex = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return regex.match(email) is not None


def validate_username(username: str) -> bool:
    regex = re.compile('^(?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$')
    return regex.match(username) is not None

def validate_password(password: str) -> bool:
    # Minimum eight characters, at least one letter, one number and one special character:
    regex = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
    return regex.match(password) is not None

def validate_name(name: str) -> bool:
    regex = re.compile("^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$")
    return regex.match(name) is not None
