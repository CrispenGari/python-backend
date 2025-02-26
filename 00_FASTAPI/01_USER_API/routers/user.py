from fastapi import APIRouter, Header, status, Body, Query, UploadFile

from models import User
from db import SessionDep
from typing import Annotated, Literal
from fastapi.responses import JSONResponse
from sqlmodel import select, and_
from utils import (
    validate_email,
    validate_name,
    validate_password,
    validate_username,
    decode_jwt,
)
from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher

hasher = PasswordHasher()
userRouter = APIRouter(prefix="/api/v1/user")


def collect_fields_from_users(user: User):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "verified": user.verified,
        "loggedIn": user.loggedIn,
        "avatar": user.avatar,
        "createdAt": str(user.createdAt),
        "updatedAt": str(user.updatedAt),
    }


# Bearer authorization
@userRouter.get("/me")
def me(
    authorization: Annotated[str | None, Header()] = None, session: SessionDep = None
):
    try:
        if authorization is None:
            return JSONResponse({"me": None}, status_code=status.HTTP_401_UNAUTHORIZED)

        _, jwt = authorization.split(" ")
        payload = decode_jwt(jwt)
        if payload is None:
            return JSONResponse({"me": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        me = session.get(User, payload["id"])
        me = collect_fields_from_users(me)
        return JSONResponse({"me": me}, status_code=status.HTTP_200_OK)
    except Exception:
        return JSONResponse(
            {"me": None}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@userRouter.get("/users")
def all(session: SessionDep):
    try:
        users = session.exec(select(User)).all()
        users = [collect_fields_from_users(u) for u in users]
        return JSONResponse(users, status_code=status.HTTP_200_OK)
    except Exception:
        return JSONResponse([], status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


ORDER = Literal["desc", "asc"]


@userRouter.get("/")
def users(
    session: SessionDep,
    firstName: Annotated[str | None, Query()] = None,
    lastName: Annotated[str | None, Query()] = None,
    page: Annotated[int | None, Query()] = None,
    per_page: Annotated[int | None, Query()] = None,
    order: Annotated[ORDER, Query()] = "asc",
):
    # page=2&per_page=2
    #
    try:
        offset = None if per_page is None or page is None else (page - 1) * per_page
        lastName = lastName.strip().capitalize() if lastName is not None else None
        firstName = firstName.strip().capitalize() if firstName is not None else None
        order = User.id.desc() if order == "desc" else User.id.asc()

        if firstName is not None and lastName is not None:
            users = session.exec(
                select(User)
                .where(and_(User.firstName == firstName, User.lastName == lastName))
                .offset(offset)
                .limit(per_page)
                .order_by(order)
            ).all()
        elif firstName is not None and lastName is None:
            users = session.exec(
                select(User)
                .where(User.firstName == firstName)
                .offset(offset)
                .limit(per_page)
                .order_by(order)
            ).all()
        elif firstName is None and lastName is not None:
            users = session.exec(
                select(User)
                .where(User.lastName == lastName)
                .offset(offset)
                .limit(per_page)
                .order_by(order)
            ).all()
        else:
            users = session.exec(
                select(User).offset(offset).limit(per_page).order_by(order)
            ).all()
        users = [collect_fields_from_users(u) for u in users]
        return JSONResponse(
            users
            if offset is None
            else {
                "offset": offset,
                "limit": per_page,
                "pageNumber": page,
                "users": users,
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        return JSONResponse([], status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@userRouter.get("/{id}")
def user(id: int, session: SessionDep):
    try:
        me = session.get(User, id)
        me = collect_fields_from_users(me)
        return JSONResponse(me, status_code=status.HTTP_200_OK)
    except Exception:
        return JSONResponse(None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@userRouter.delete("/{id}")
def delete_user(id: int, session: SessionDep):
    me = session.get(User, id)
    if me is None:
        return JSONResponse(
            {"error": f"The user with id '{id}' does not exists"}, status_code=200
        )
    session.delete(me)
    session.commit()
    return JSONResponse(
        {"message": f"The user with id '{id}' was deleted."},
        status_code=status.HTTP_200_OK,
    )


@userRouter.put("/{id}")
def update_user(
    id: int,
    session: SessionDep,
    password: Annotated[str | None, Body()] = None,
    firstName: Annotated[str | None, Body()] = None,
    username: Annotated[str | None, Body()] = None,
    email: Annotated[str | None, Body()] = None,
    lastName: Annotated[str | None, Body()] = None,
):
    me = session.get(User, id)
    if me is None:
        return JSONResponse(
            {"error": f"The user with id '{id}' does not exists"}, status_code=200
        )
    if username is not None and validate_username(username.strip().lower()) is False:
        return JSONResponse({"error": "The username is invalid."}, status_code=200)
    if email is not None and validate_email(email.strip().lower()) is False:
        return JSONResponse({"error": "The email address is invalid."}, status_code=200)
    if firstName is not None and validate_name(firstName.strip()) is False:
        return JSONResponse({"error": "The first name is invalid."}, status_code=200)
    if lastName is not None and validate_name(lastName.strip()) is False:
        return JSONResponse({"error": "The last name is invalid."}, status_code=200)
    if password is not None and validate_password(password.strip()) is False:
        return JSONResponse(
            {
                "error": "The password must contain at least one letter, one number and one special character."
            },
            status_code=200,
        )
    if password is not None:
        try:
            hasher.verify(me.password, password.strip())
            return JSONResponse(
                {"error": "You can not set your new password as old password."},
                status_code=200,
            )
        except VerifyMismatchError:
            pass
    if username is not None:
        username_taken = session.exec(
            select(User).where(User.username == username.strip().lower())
        ).first()
        if username_taken:
            return JSONResponse(
                {"error": "The username is already in use.", "jwt": None},
                status_code=200,
            )
    if email is not None:
        email_taken = session.exec(
            select(User).where(User.email == email.strip().lower())
        ).first()
        if email_taken:
            return JSONResponse(
                {"error": "The email is already in use.", "jwt": None}, status_code=200
            )
    me.password = hasher.hash(password.strip()) if password is not None else me.password
    me.username = username.strip().lower() if username is not None else me.username
    me.email = email.strip().lower() if email is not None else me.email
    me.firstName = (
        firstName.strip().capitalize() if firstName is not None else me.firstName
    )
    me.lastName = lastName.strip().capitalize() if lastName is not None else me.lastName

    session.add(me)
    session.commit()
    session.refresh(me)
    me = collect_fields_from_users(me)
    return JSONResponse(me, status_code=status.HTTP_200_OK)


@userRouter.patch("/update-profile")
def update_avatar(
    avatar: UploadFile,
    authorization: Annotated[str | None, Header()] = None,
    session: SessionDep = None,
):
    try:
        if authorization is None:
            return JSONResponse(
                {"success": False, "url": None},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        _, jwt = authorization.split(" ")
        payload = decode_jwt(jwt)
        if payload is None:
            return JSONResponse(
                {"success": False, "url": None},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        me = session.get(User, payload["id"])
        if me is None:
            return JSONResponse(
                {"success": False, "url": None},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        # hello.jpge
        ext = avatar.filename.split(".")[-1]
        save_name = f"storage/{str(me.id)}-avatar.{ext}"
        # print(avatar)
        with open(save_name, "wb+") as file_object:
            file_object.write(avatar.file.read())

        avatar = f"http://127.0.0.1:8000/{save_name}"
        me.avatar = avatar
        session.add(me)
        session.commit()
        session.refresh(me)
        return JSONResponse(
            {"success": False, "url": me.avatar}, status_code=status.HTTP_200_OK
        )
    except Exception:
        return JSONResponse(
            {"success": False, "url": None},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
