"""
This module provides constants and utility functions related to user management and time operations in a Flask application.

Constants:
    - TZ: Timezone object for Asia/Kolkata.
    - USER_TYPE_ADMIN: String constant for the admin user type.
    - USER_TYPE_OPERATOR: String constant for the operator user type.
    - USER_ACCESS_ALLOW: Integer constant indicating access is allowed.
    - USER_ACCESS_DENY: Integer constant indicating access is denied.
    - USER_STATE_ACTIVE: Integer constant indicating the user is active.
    - USER_STATE_INACTIVE: Integer constant indicating the user is inactive.

Functions:
    - get_server_url: Retrieves the server URL from the Flask request.
    - current_datetime: Returns the current date and time in the Asia/Kolkata timezone formatted as "YYYY-MM-DD HH:MM:SS".
"""

from flask import request
from datetime import datetime
import pytz

TZ = pytz.timezone("Asia/Kolkata")

USER_TYPE_ADMIN = "admin"
USER_TYPE_OPERATOR = "operator"

USER_ACCESS_ALLOW = 1
USER_ACCESS_DENY = 0

USER_STATE_ACTIVE = 1
USER_STATE_INACTIVE = 0

def get_server_url():
    """
    Retrieves the server URL from the Flask request.

    Returns:
        str: The URL of the server as specified in the Flask request.

    This function returns the server URL from the `request.host_url`. The URL is determined based on
    the current request context. The function currently does not modify the URL but can be adjusted
    for secure protocol changes if needed.
    """
    SERVER_URL = request.host_url
    # if not SERVER_URL == 'http://127.0.0.1:5000/':
    #     SERVER_URL = SERVER_URL.replace("http://", "https://", 1)
    return SERVER_URL

def current_datetime():
    """
    Returns the current date and time formatted as "YYYY-MM-DD HH:MM:SS" in the Asia/Kolkata timezone.

    Returns:
        str: The current date and time in the Asia/Kolkata timezone.

    The function retrieves the current date and time, formats it to the specified string format, and
    returns it. The timezone used is Asia/Kolkata.
    """
    current_dt = datetime.now().astimezone(TZ).strftime("%Y-%m-%d %H:%M:%S")
    return current_dt
