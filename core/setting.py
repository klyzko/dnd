from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Response,Request,Depends,HTTPException
from typing import Optional, Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


