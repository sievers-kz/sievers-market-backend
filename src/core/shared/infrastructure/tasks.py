from enum import Enum


class TaskNames(str, Enum):
    SEND_OTP_EMAIL = "send_otp_email"
    SEND_OTP_PASSWORD_RESET = "send_otp_password_reset"
    SEND_OTP_CHANGE_EMAIL = "send_otp_change_email"
