from typing import Optional

from fastapi import Header, HTTPException


async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="API Key is missing")

    # Tu można dodać właściwą weryfikację klucza API
    # Na razie przyjmujemy przykładowy klucz
    if x_api_key != "test_api_key":
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return x_api_key
