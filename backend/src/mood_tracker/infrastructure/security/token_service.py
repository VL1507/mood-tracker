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
        self.token_repository = token_repository
        self.algorithm = jwt_config.ALGORITHM
        self.secret_key = jwt_config.SECRET_KEY
        self.access_exp = jwt_config.ACCESS_EXPIRE_SECONDS
        self.refresh_exp = jwt_config.REFRESH_EXPIRE_SECONDS

    async def generate_token_pair(self, user_id: UserID) -> TokenPair:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id.value),
            "iat": now,
            "exp": now + timedelta(seconds=self.access_exp),
        }
        access_token = jwt.encode(
            payload=payload,
            key=self.secret_key,
            algorithm=self.algorithm,
        )

        refresh_token = str(uuid4())
        await self.token_repository.save_refresh(
            user_id=user_id,
            refresh_token=refresh_token,
            time_seconds=self.refresh_exp,
        )

        return TokenPair(access=access_token, refresh=refresh_token)

    def verify_access(self, access_token: str) -> bool:
        try:
            jwt.decode(
                jwt=access_token,
                key=self.secret_key,
                algorithms=[
                    self.algorithm,
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
                key=self.secret_key,
                algorithms=[
                    self.algorithm,
                ],
            )
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return UserID.from_str(payload.get("sub"))

    async def verify_refresh(
        self, user_id: UserID, refresh_token: str
    ) -> bool:
        return await self.token_repository.check_refresh(
            user_id=user_id, refresh_token=refresh_token
        )

    async def revoke_refresh(
        self, user_id: UserID, refresh_token: str
    ) -> None:
        await self.token_repository.delete_refresh(
            user_id=user_id, refresh_token=refresh_token
        )
