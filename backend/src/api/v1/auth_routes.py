from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import DbSession
from src.api.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from src.application.user.commands import LoginCommand, RegisterUserCommand
from src.application.user.handlers import LoginHandler, RegisterUserHandler
from src.domain.user.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from src.infrastructure.persistence.user_repo import SqlAlchemyUserRepository

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, session: DbSession) -> UserResponse:
    repo = SqlAlchemyUserRepository(session)
    handler = RegisterUserHandler(repo)
    try:
        user = await handler.handle(RegisterUserCommand(email=body.email, password=body.password))
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return UserResponse(id=user.id, email=user.email.value, is_active=user.is_active)


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, session: DbSession) -> TokenResponse:
    repo = SqlAlchemyUserRepository(session)
    handler = LoginHandler(repo)
    try:
        token = await handler.handle(LoginCommand(email=body.email, password=body.password))
    except InvalidCredentialsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=token)
