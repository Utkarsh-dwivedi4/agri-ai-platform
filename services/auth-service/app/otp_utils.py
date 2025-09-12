import random
import time

# Simple in-memory OTP store: {phone: (otp, expiry_timestamp)}
otp_store = {}

OTP_EXPIRATION_SECONDS = 300  # 5 minutes


def generate_otp(phone: str) -> int:
    otp = random.randint(100000, 999999)
    expiry = time.time() + OTP_EXPIRATION_SECONDS
    otp_store[phone] = (otp, expiry)
    # In production, send OTP by SMS using an SMS gateway here
    print(f"DEBUG: OTP for {phone} is {otp}")  # For testing
    return otp


def verify_otp(phone: str, otp: int) -> bool:
    if phone not in otp_store:
        return False
    stored_otp, expiry = otp_store[phone]
    if time.time() > expiry:
        del otp_store[phone]
        return False
    if stored_otp == otp:
        del otp_store[phone]
        return True
    return False
