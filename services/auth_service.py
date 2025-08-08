import requests
import logging
import traceback
from typing import Optional, Dict
from fastapi import HTTPException
from requests.exceptions import Timeout, RequestException
from email_validator import validate_email as validate, EmailNotValidError

# Configure logger to record errors
logging.basicConfig(level=logging.ERROR)

# Fixed URLs for authentication on the MapBiomas API
LOGIN_URL = "https://api.mapbiomas.org/auth/login"
SIGNUP_URL = "https://plataforma.alerta.mapbiomas.org/sign-up"

def _clean_email(email: str) -> str:
    """
    Removes whitespace and converts the email to lowercase.
    """
    return email.strip().lower()

def _validate_email(email: str) -> bool:
    """
    Validates the email format using the `email-validator` package.
    """
    try:
        validate(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False

def signup_user() -> Dict[str, str]:
    """
    Returns the redirect URL for user registration on the MapBiomas website.
    """
    return {
        "message": "User creation must be done on the MapBiomas website.",
        "redirect_url": SIGNUP_URL
    }

def login_user(email: str, password: str) -> Optional[str]:
    """
    Authenticates a user on the MapBiomas Fogo API using the provided credentials.
    """
    email = _clean_email(email)

    if not _validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format.")

    payload = {"email": email, "password": password}

    try:
        response = requests.post(LOGIN_URL, json=payload, timeout=5)
        response.raise_for_status()

        if response.status_code == 200:
            token = response.json().get("data", {}).get("token")
            if token:
                return token
            else:
                raise HTTPException(status_code=500, detail="Token not found in the API response.")
        else:
            return None

    except Timeout:
        raise HTTPException(status_code=504, detail="Request to MapBiomas API timed out.")

    except RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to MapBiomas API: {e}")

    except HTTPException:
        raise  # Allows custom HTTPExceptions to propagate

    except Exception as e:
        logging.error(f"Unexpected error during login: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An unexpected internal error occurred.")

    return None
