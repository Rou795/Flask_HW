from typing import Type

import flask
from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Session, User, Ad
from schema import CreateUser, UpdateUser, CreateAd, UpdateAd

app = Flask("app")
bcrypt = Bcrypt(app)

# функция хэширования пароля
def hash_password(password: str) -> str:
    password = password.encode()
    return bcrypt.generate_password_hash(password).decode()

# проверка пароля
def check_password(password: str, hashed: str) -> bool:
    password = password.encode()
    hashed = hashed.encode()
    return bcrypt.check_password_hash(hashed, password)


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response

# методы получения информации о пользователях и объявлениях

def get_user_by_id(user_id: int):
    user = request.session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


def get_ad_by_id(ad_id: int):
    ad = request.session.query(Ad).get(ad_id)
    if ad is None:
        raise HttpError(404, "advertisement not found")
    return ad

# добавлять пользователей и объявлений
def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "user already exists")


def add_ad(ad: Ad):
    try:
        request.session.add(ad)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "ad already exists")


def validate_json(json_data: dict, schema_class: Type[CreateUser] | Type[UpdateUser] | Type[CreateAd] | Type[UpdateAd]):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)

# метод авторизации
def avtorization(password: str, user_id: str):
    if password is not None:
        return check_password(password, get_user_by_id(user_id).password)
    else:
        return False


class UserView(MethodView):

    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        return jsonify(user.dict)

    def post(self):
        user_data = validate_json(request.json, CreateUser)
        user_data["password"] = hash_password(user_data["password"])
        user = User(**user_data)
        add_user(user)
        return jsonify(user.dict)

    def patch(self, user_id: int):
        user_data = validate_json(request.json, UpdateUser)
        if "password" in user_data:
            user_data["password"] = hash_password(user_data["password"])
        user = get_user_by_id(user_id)
        for field, value in user_data.items():
            setattr(user, field, value)
        add_user(user)
        return jsonify(user.dict)


class AdView(MethodView):

    def get(self, ad_id: int):
        password = request.headers.get("authorization")
        user_id = get_ad_by_id(ad_id).user_id
        if avtorization(password, user_id):
            user = get_ad_by_id(ad_id)
            return jsonify(user.dict)
        else:
            raise HttpError(402, "Bad avtorization")

    def post(self):
        ad_data = validate_json(request.json, CreateAd)
        password = request.headers.get("authorization")
        user_id = ad_data.get('user_id')
        if avtorization(password, user_id):
            ad = Ad(**ad_data)
            add_ad(ad)
            return jsonify(ad.dict)
        else:
            raise HttpError(402, "Bad avtorization")

    def patch(self, ad_id: int):
        ad_data = validate_json(request.json, UpdateAd)
        password = request.headers.get("authorization")
        user_id = get_ad_by_id(ad_id).user_id
        if avtorization(password, user_id):
            ad = get_ad_by_id(ad_id)
            for field, value in ad_data.items():
                setattr(ad, field, value)
            add_ad(ad)
            return jsonify(ad.dict)
        else:
            raise HttpError(402, "Bad avtorization")

    def delete(self, ad_id):
        ad = get_ad_by_id(ad_id)
        password = request.headers.get("authorization")
        user_id = get_ad_by_id(ad_id).user_id
        if avtorization(password, user_id):
            request.session.delete(ad)
            request.session.commit()
            return jsonify({"status": "deleted"})
        else:
            raise HttpError(402, "Bad avtorization")


user_view = UserView.as_view("user_view")
ad_view = AdView.as_view("ad_view")

app.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule(
    "/ad/<int:ad_id>", view_func=ad_view, methods=["GET", "PATCH", "DELETE"]
)

app.add_url_rule("/user", view_func=user_view, methods=["POST"])
app.add_url_rule("/ad", view_func=ad_view, methods=["POST"])

if __name__ == "__main__":
    app.run()
