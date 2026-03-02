from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt

from mood_tracker.config import JWT
from mood_tracker.domain.repositories import ITokenRepository
from mood_tracker.domain.security import ITokenService
from mood_tracker.domain.value_objects import TokenPair, UserID


class TokenService(ITokenService):
    def __init__(
        self, token_repository: ITokenRepository, jwt_config: JWT
    ) -> None:
        self._token_repository = token_repository
        self._algorithm = jwt_config.ALGORITHM
        self._secret_key = jwt_config.SECRET_KEY
        self._access_exp = jwt_config.ACCESS_EXPIRE_SECONDS
        self._refresh_exp = jwt_config.REFRESH_EXPIRE_SECONDS

    async def generate_token_pair(self, user_id: UserID) -> TokenPair:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id.value),
            "iat": now,
            "exp": now + timedelta(seconds=self._access_exp),
        }
        access_token = jwt.encode(
            payload=payload,
            key=self._secret_key,
            algorithm=self._algorithm,
        )

        refresh_token = str(uuid4())

        await self._token_repository.save_refresh(
            user_id=user_id,
            refresh_token=refresh_token,
            time_seconds=self._refresh_exp,
        )

        return TokenPair(access=access_token, refresh=refresh_token)

    def verify_access(self, access_token: str) -> bool:
        try:
            jwt.decode(
                jwt=access_token,
                key=self._secret_key,
                algorithms=[
                    self._algorithm,
                ],
            )
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        return True

    def decode_access(self, access_token: str) -> UserID | None:
        try:
            payload = jwt.decode(
                jwt=access_token,
                key=self._secret_key,
                algorithms=[
                    self._algorithm,
                ],
            )
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        sub = payload.get("sub")
        if sub is None:
            return None
        return UserID.from_str(sub)

    async def verify_refresh(self, refresh_token: str) -> bool:
        return await self._token_repository.check_refresh(
            refresh_token=refresh_token
        )

    async def revoke_refresh(self, refresh_token: str) -> None:
        await self._token_repository.delete_refresh(
            refresh_token=refresh_token
        )

    async def revoke_all_refresh(self, user_id: UserID) -> None:
        await self._token_repository.revoke_all_refresh(user_id=user_id)

    async def get_user_id_by_refresh(
        self, refresh_token: str
    ) -> UserID | None:
        return await self._token_repository.get_user_id_by_refresh(
            refresh_token=refresh_token
        )
