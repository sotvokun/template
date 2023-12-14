from typing import Optional, Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


_oauth2_password = OAuth2PasswordBearer(tokenUrl="token")


inject_oauth2_password = _oauth2_password

OAuthD = Annotated[Optional[str], Depends(inject_oauth2_password)]