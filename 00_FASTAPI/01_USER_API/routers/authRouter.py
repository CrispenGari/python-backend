from fastapi import APIRouter, Body, Header, status

from fastapi.responses import JSONResponse
from  models import User
from  db import SessionDep
from argon2 import PasswordHasher
from sqlmodel import select, or_
from typing import Annotated
from  utils import encode_jwt, validate_email, validate_name, validate_password, validate_username, generate_otp, decode_jwt
from argon2.exceptions import VerifyMismatchError
from  mail import send_email


verificationEmailTemplate = """
<div>
  <h1>Hi, {fullName}</h1>
  <p>
    We have detected that you want to create an account with us using the email
    address <b>{email}</b>. Please click the following link to verify if
    it's you, or
    <em
      >YOU CAN IGNORE THIS EMAIL IF YOU DIDN'T INTENT TO CREATE AN ACCOUNT USING
      THIS EMAIL.</em
    >
  </p>
  <p>
    <a href="{verificationLink}">VERIFY EMAIL</a>
  </p>
  <b>Kind Regard</b>
  <p>Developers</p>
</div>
"""

hasher = PasswordHasher()
authRouter = APIRouter(prefix="/api/v1/auth")

# logout

@authRouter.post("/logout")
def logout(
    authorization: Annotated[str | None, Header()] = None, session: SessionDep = None
):
    try:
        if authorization is None:
            return JSONResponse({"error": "You are not authorized.", 'jwt': None}, status_code=status.HTTP_401_UNAUTHORIZED)
        _, jwt = authorization.split(" ")
        payload = decode_jwt(jwt)
        if payload is None:
            return JSONResponse({"error": "You are not authorized.", 'jwt': None}, status_code=status.HTTP_401_UNAUTHORIZED)
        me = session.get(User, payload["id"])
        me.loggedIn = False
        session.add(me)
        session.commit()
        session.refresh(me)
        return JSONResponse({"jwt": None, "error": None}, status_code=200)
    except Exception:
        return JSONResponse(
            {"error": "You are not authorized.", 'jwt': None}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# verify ->


@authRouter.get("/verify/{otp}")
def verify(otp: str,
             authorization: Annotated[str | None, Header()] = None, session: SessionDep = None):
    try:
        if authorization is None:
            return JSONResponse({"error": "You are not authorized.", 'jwt': None}, status_code=status.HTTP_401_UNAUTHORIZED)
        _, jwt = authorization.split(" ")
        payload = decode_jwt(jwt)
        if payload is None:
            return JSONResponse({"error": "You are not authorized.", 'jwt': None}, status_code=status.HTTP_401_UNAUTHORIZED)
        
        me = session.get(User, payload["id"])

        if me.verificationToken != otp:
            return JSONResponse({"error": "Invalid verification token.", 'jwt': None}, status_code=status.HTTP_401_UNAUTHORIZED)
        
        me.loggedIn = True
        me.verificationToken = '000000'
        me.verified = True
        session.add(me)
        session.commit()
        session.refresh(me)
        jwt = encode_jwt({"email": me.email, "id": me.id})
        return JSONResponse({"jwt": jwt, "error": None}, status_code=200)
    except Exception:
        return JSONResponse(
            {"error": "You are not authorized.", 'jwt': None}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@authRouter.post("/register")
def register(user: User, session: SessionDep):
    # validation
    if validate_username(user.username.strip().lower()) is False:
        return JSONResponse(
            {"error": "The username is invalid.", "jwt": None}, status_code=200
        )
    if validate_email(user.email.strip().lower()) is False:
        return JSONResponse(
            {"error": "The email address is invalid.", "jwt": None}, status_code=200
        )
    if validate_name(user.firstName.strip()) is False:
        return JSONResponse(
            {"error": "The first name is invalid.", "jwt": None}, status_code=200
        )
    if validate_name(user.lastName.strip()) is False:
        return JSONResponse(
            {"error": "The last name is invalid.", "jwt": None}, status_code=200
        )
    if validate_password(user.password.strip()) is False:
        return JSONResponse(
            {"error": "The password must contain at least one letter, one number and one special character.", "jwt": None}, status_code=200
        )
    otp = generate_otp()
    hashedPassword = hasher.hash(user.password.strip())
    user.verificationToken = otp
    user.password = hashedPassword
    user.username = user.username.strip().lower()
    user.email = user.email.strip().lower()
    user.firstName = user.firstName.strip().capitalize()
    user.lastName = user.lastName.strip().capitalize()
    me = session.exec(
        select(User).where(User.username == user.username.strip().lower())
    ).first()
    if me:
        return JSONResponse(
            {"error": "The username is already in use.", "jwt": None}, status_code=200
        )
    me = session.exec(
        select(User).where(User.email == user.email.strip().lower())
    ).first()
    if me:
        return JSONResponse(
            {"error": "The email is already in use.", "jwt": None}, status_code=200
        )
    session.add(user)
    session.commit()
    session.refresh(user)
    jwt = encode_jwt({"email": user.email, "id": user.id})
    # send email with otp to the user
    # 
    verificationLink = f'http://127.0.0.1:8000/api/v1/auth/verify/{otp}'
    send_email("Verify Email", user.email, verificationEmailTemplate.format(
        fullName = f'{user.firstName} {user.lastName}',
        email = user.email,
        verificationLink = verificationLink
    ))
    return JSONResponse({"jwt": jwt, "error": None}, status_code=200)

@authRouter.post("/login")
def login(
    usernameOrEmail: Annotated[str, Body()],
    password: Annotated[str, Body()],
    session: SessionDep,
):
    me = session.exec(
        select(User).where(
            or_(
                User.username == usernameOrEmail.strip().lower(),
                User.email == usernameOrEmail.strip().lower(),
            ),
        )
    ).first()
    if me is None:
        return JSONResponse(
            {"error": "Invalid username or email address.", "jwt": None},
            status_code=200,
        )
    try:
        hasher.verify(me.password, password.strip())
    except VerifyMismatchError:
        return JSONResponse(
            {"error": "Invalid account password.", "jwt": None}, status_code=200
        )
    me.loggedIn = True
    session.add(me)
    session.commit()
    session.refresh(me)
    jwt = encode_jwt({"email": me.email, "id": me.id})
    return JSONResponse({"jwt": jwt, "error": None}, status_code=200)
