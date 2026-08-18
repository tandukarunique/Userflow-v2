import os


class Config:
    BASE_URL = "https://stagingv2.chatboq.com/"
    AUTH_ME_URL = "https://api.stagingv2.chatboq.com/api/v1/auth/me"
    # The application's authentication cookie name.
    AUTH_COOKIE_NAME = "session_uuid"
    # Used as the default session UUID and local saved-session filename.
    AUTH_SESSION_ID = "a8998f2e-046b-44f2-98b0-c49cb55d3402"

    VALID_EMAIL = "hello@sharklasers.com"
    VALID_PASSWORD = "Thacha098!"
    INVALID_EMAIL = "invalid@example.com"
    INVALID_PASSWORD = "wrongpassword"

    DEFAULT_TIMEOUT = 900000
    SHORT_TIMEOUT = 5000
    LONG_TIMEOUT = 60000
    
    

    HEADLESS = os.getenv("CHATBOQ_HEADLESS", "false").lower() == "true"
    SLOW_MO = 500
