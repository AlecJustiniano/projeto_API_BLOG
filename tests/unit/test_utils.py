from src.utils import eleva_quadrado, require_role
import pytest
from http import HTTPStatus


@pytest.mark.parametrize("test_input,expected", [(2, 4), (10, 100), (6, 36)])
def test_eleva_quadrado_sucesso(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected


def test_requires_role_success(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"

    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)

    decorated_function = require_role("admin")(lambda: "success")
    result = decorated_function()
    assert result == "success"


def test_requires_role_fail(mocker):
#O que é fornecido
    mock_user = mocker.Mock()
    mock_user.role.name = "normal"

    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)
#O que executa
    decorated_function = require_role("admin")(lambda: "success")
    result = decorated_function()
#resultado
    assert result == ({"message": "User dont have acess."}, HTTPStatus.FORBIDDEN)
