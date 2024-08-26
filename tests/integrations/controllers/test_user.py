from http import HTTPStatus
from src.app import User, db, Role
from sqlalchemy import func

def test_get_user_success(client):
    #given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="Jonh-doe", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()
    #when
    response = client.get(f"/users/{user.id}")
    #then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"id": user.id, "username": user.username}


def test_get_user_not_found(client):
    #given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user_id = 1
    #when
    response = client.get(f"/users/{user_id}")
    #then
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_list_users(client, access_token):
    #given
    user = db.session.execute(db.select(User).where(User.username == "Jonh-doe")).scalar()

    response = client.post('/auth/login', json={"username": user.username,
                                                "password": user.password})
    access_token = response.json["access_token"]
    #when

    response = client.get("/users/", headers={"Authorization": f"Bearer {access_token}"})

    #then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "identity": user.username,
        "users": [
                {
                    "role": {
                            "id": user.role.id,
                            "name": user.role.name,
                    },
                    "user_id": user.id,  # Aqui, use 'user_id' em vez de 'id'
                    "username": user.username
                }
        ]
    }


def test_create_users(client, access_token):
    #given
    
    role_id = db.session.execute(db.select(Role.id).where(Role.name == "admin")).scalar()
    payload = {"username": "Alec", "password": "248mudar", "role_id": role_id}
    #when
    response = client.post("/users/", json=payload, headers={"Authorization": f"Bearer {access_token}"})

    #then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "User created!"}
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2
