from flask import Blueprint, request
from src.app import Role, db
from http import HTTPStatus
app = Blueprint("role", __name__, url_prefix="/roles")


def create_role():
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created!"}, HTTPStatus.CREATED


def _list_roles():
    query = db.select(Role)
    roles = db.session.execute(query).scalars()
    return [
        {
            "role_id": role.id,
            "role_name": role.name,
        }
        for role in roles
    ]


@app.route("/", methods=["GET", "POST"])
def list_or_create_role():
    if request.method == "POST":
        create_role()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return _list_roles()
