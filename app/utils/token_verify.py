import os
import jwt

from fastapi import HTTPException
from config import DOMAIN, API_AUDIENCE, ISSUER, ALGORITHMS, ACCES_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY, ALGORITHM
from schemas.schemas import TokenResponse

from datetime import datetime, timedelta

def create_access_token(user_email: str) -> str:
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=int(ACCES_TOKEN_EXPIRE_MINUTES)),
        'iat': datetime.utcnow(),
        'scope': 'access_token',
        'email': str(user_email)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, ALGORITHM)


def decode_access_token(encoded_jwt: any) -> str:
    try:
        payload = jwt.decode(jwt=encoded_jwt.credentials, key = JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('email') if payload.get('exp') >= int(ACCES_TOKEN_EXPIRE_MINUTES) else None
    except jwt.InvalidTokenError:
         raise HTTPException(status_code=401, detail='Invalid token')

def encode_refresh_token(user_email: str):
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=int(ACCES_TOKEN_EXPIRE_MINUTES)),
        'iat': datetime.utcnow(),
        'scope': 'refresh_token',
        'email': str(user_email)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, ALGORITHM)


def refresh_token(refresh_token: str) -> str:
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET_KEY, ALGORITHM)
        if payload.get("refresh_token") == "refresh_token":
            user_email = payload.get("user_email")
            new_token = create_access_token(user_email)
            return new_token
        raise HTTPException(status_code=401, detail='Invalid scope for token')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Refresh token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid refresh token')

class VerifyToken():
    """Does all the token verification using PyJWT"""

    def __init__(self, token, permissions=None, scopes=None):
        self.token = token
        self.permissions = permissions
        self.scopes = scopes

        # This gets the JWKS from a given URL and does processing so you can use any of
        # the keys available
        jwks_url = f'https://{DOMAIN}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=ISSUER,
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        if self.scopes:
            result = self._check_claims(payload, 'scope', str, self.scopes.split(' '))
            if result.get("error"):
                return result

        if self.permissions:
            result = self._check_claims(payload, 'permissions', list, self.permissions)
            if result.get("error"):
                return result

        return payload

    def _check_claims(self, payload, claim_name, claim_type, expected_value):

        instance_check = isinstance(payload[claim_name], claim_type)
        result = {"status": "success", "status_code": 200}

        payload_claim = payload[claim_name]

        if claim_name not in payload or not instance_check:
            result["status"] = "error"
            result["status_code"] = 400

            result["code"] = f"missing_{claim_name}"
            result["msg"] = f"No claim '{claim_name}' found in token."
            return result

        if claim_name == 'scope':
            payload_claim = payload[claim_name].split(' ')

        for value in expected_value:
            if value not in payload_claim:
                result["status"] = "error"
                result["status_code"] = 403

                result["code"] = f"insufficient_{claim_name}"
                result["msg"] = (f"Insufficient {claim_name} ({value}). You don't have "
                                 "access to this resource")
                return result
        return result
