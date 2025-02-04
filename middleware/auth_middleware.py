from typing import Annotated, Union
from fastapi import HTTPException, Header
import requests


AUTH_PREFIX = 'Bearer '
USER_INFO_URL = "https://api.clientvenue.com/v1/user/me"


async def verify_token_middleware(authorization : Annotated[Union[str, None] , Header()] = None )-> dict:  
    auth_exception = HTTPException(
        status_code = 401,
        detail = {"message":"Invalid Authentication Credentials"}
    )
   
    if not authorization:
        raise auth_exception
    
    token = authorization

    if not token or not token.startswith(AUTH_PREFIX):
        raise HTTPException(detail={"error": "Unauthorized"}, status_code=401)

    try:
        response = requests.get(
            USER_INFO_URL, 
            headers={"Authorization": authorization}
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Invalid or expired token")

        user_data = response.json()
        return user_data
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Error verifying token")
    
