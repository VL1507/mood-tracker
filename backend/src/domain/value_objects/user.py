from typing import NewType
from uuid import UUID


UserID = NewType("UserID", UUID)
UserName = NewType("UserName", str)
UserLogin = NewType("UserLogin", str)
HashPassword = NewType("HashPassword", str)
