
from api.auth.jwt import token as jwts
from fastapi import Depends, HTTPException,Response
import redis.asyncio as redis
from dependency.depend_redis import get_redis


async def refresh_verifide_token(
                                 response:Response,
                                 red: redis.Redis = Depends(get_redis),
                                 token:str = Depends(jwts.get_token(jwts.typs_token.refresh_token)),
                                 token_refresh:str = Depends(jwts.get_token(jwts.typs_token.refresh_token))
                                 ):
    #checking availability refresh
    if not token_refresh:
        raise HTTPException(status_code=401, detail='Token is empty')
    # check access
    access_token = await jwts.verify_token(token)
    if access_token:
        jti=access_token.get('jti')
        if not await jwts.get_blacklist_token(jti,red):
            return access_token
    # check refresh
    ref = await jwts.verify_token(token_refresh)
    if ref:
        jti=ref.get('jti')
        if not await jwts.get_blacklist_token(jti,red):
            id=ref.get('sub')
            new_access = await jwts.create_access_token(id)
            await jwts.set_cookie(response,new_access,jwts.typs_token.access_token)
            new_verified = await jwts.verify_token(new_access)
            return new_verified.get('sub')
    raise HTTPException(status_code=401, detail='Token is expired')
