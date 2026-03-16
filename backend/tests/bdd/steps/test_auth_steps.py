from __future__ import annotations

from pytest_bdd import given, parsers, scenario, then, when

from httpx import AsyncClient

from src.main import app

BASE = "http://test"


@scenario("../features/auth.feature", "Register a new user")
def test_register() -> None:
    pass


@scenario("../features/auth.feature", "Login with valid credentials")
def test_login() -> None:
    pass


@scenario("../features/auth.feature", "Login with invalid credentials")
def test_login_invalid() -> None:
    pass


# ---------- steps ----------

@given("I have valid registration data", target_fixture="reg_data")
def valid_reg_data() -> dict:
    return {"email": "test@example.com", "password": "Str0ngP@ss"}


@given("a registered user exists", target_fixture="reg_data")
async def registered_user() -> dict:
    data = {"email": "existing@example.com", "password": "Str0ngP@ss"}
    async with AsyncClient(app=app, base_url=BASE) as client:
        await client.post("/api/v1/auth/register", json=data)
    return data


@when(parsers.parse('I send a POST request to "{url}"'), target_fixture="response")
async def post_request(url: str, reg_data: dict) -> dict:
    async with AsyncClient(app=app, base_url=BASE) as client:
        resp = await client.post(url, json=reg_data)
    return {"status": resp.status_code, "body": resp.json()}


@when(parsers.parse('I send a POST request to "{url}" with valid credentials'), target_fixture="response")
async def post_login_valid(url: str, reg_data: dict) -> dict:
    async with AsyncClient(app=app, base_url=BASE) as client:
        resp = await client.post(url, json=reg_data)
    return {"status": resp.status_code, "body": resp.json()}


@when(parsers.parse('I send a POST request to "{url}" with wrong password'), target_fixture="response")
async def post_login_wrong(url: str, reg_data: dict) -> dict:
    async with AsyncClient(app=app, base_url=BASE) as client:
        resp = await client.post(url, json={**reg_data, "password": "wrong"})
    return {"status": resp.status_code, "body": resp.json()}


@then(parsers.parse("the response status code should be {code:d}"))
def check_status(response: dict, code: int) -> None:
    assert response["status"] == code


@then("the response should contain a user id")
def check_user_id(response: dict) -> None:
    assert "id" in response["body"]


@then("the response should contain an access token")
def check_access_token(response: dict) -> None:
    assert "access_token" in response["body"]
