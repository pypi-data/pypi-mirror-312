"""
This module provides helper functions for user management and generating PDF labels.

Functions:
    - update_last_active_time: Updates the last active time and active status of a user.
    - inactive_idle_users_after: Marks users as inactive if they have been idle for a specified number of minutes.
    - label_view: Generates a PDF label based on a formatted string (currently not implemented).
"""

from datetime import datetime, timedelta
from .table_operations import DBTableOperations
from .constants import TZ, USER_STATE_ACTIVE, USER_STATE_INACTIVE, current_datetime

TABLE_USER = "User"

def update_last_active_time(user_id):
    """
    Updates the last active time and active status of a user in the database.

    Args:
        user_id (int): The ID of the user whose information is to be updated.

    This function sets the `is_active` field to 1 (active) and updates the `last_active` field
    with the current date and time for the specified user.
    """
    last_active = current_datetime()
    update_data = {"is_active": 1, "last_active": last_active}
    operation = DBTableOperations()
    operation.update(table_name=TABLE_USER, data=update_data, id=user_id)

def inactive_idle_users_after(minutes):
    """
    Marks users as inactive if they have been idle for a specified number of minutes.

    Args:
        minutes (int): The number of minutes of inactivity after which users should be marked as inactive.

    This function calculates the target time based on the current time minus the specified number
    of minutes. It then updates the `is_active` field to inactive for users who have been idle
    longer than the calculated target time.
    """
    target_time = datetime.now().astimezone(TZ) - timedelta(minutes=minutes)
    target_time = target_time.strftime("%Y-%m-%d %H:%M:%S")
    query = (
        "UPDATE "
        + TABLE_USER
        + " SET is_active = "
        + str(USER_STATE_INACTIVE)
        + " WHERE is_active = "
        + str(USER_STATE_ACTIVE)
        + " AND last_active < "
        + "'"
        + target_time
        + "'"
        + " ;"
    )
    operation = DBTableOperations()
    operation.update_complex(query)

def label_view(fmt_string):
    """
    Generates a PDF label based on a formatted string (currently not implemented).

    Args:
        fmt_string (str): A formatted string defining the layout and content of the PDF label.

    Returns:
        str: An empty string as the function implementation is not yet complete.

    Note:
        The function currently returns an empty string and does not perform any operations.
        The intended functionality is to create a PDF label based on the `fmt_string` parameter.
    """
    # lines = fmt_string.split('\n')
    # w, h = float(lines[0].split(',')[1]), float(lines[0].split(',')[2])
    # doc = fitz.open()
    # page = doc.newPage(0, width=w, height=h+10)
    # for line in lines[1:-1]:
    #     elements = line.split(',')
    #     if elements[0] == 'TB' and elements[10] == 'DATA':
    #         write_text(page, elements[1], elements[2], elements[12])

    #     elif elements[0] == 'TB' and elements[10] == 'TEXT':
    #         write_text(page, elements[1], elements[2], elements[11])

    #     elif elements[0] == 'L':
    #         write_line(page, elements[1], elements[2],
    #                    elements[3], elements[4])

    #     # elif elements[0] == 'B':
    #     #     img = open("barcode.png", "rb").read()
    #     #     write_img(doc, page, elements[1], elements[2], elements[3], elements[4], img)

    #     # elif elements[0] == 'QR':
    #     #     img = open("qrcode.png", "rb").read()
    #     #     write_img(doc, page, elements[1], elements[2], elements[3], elements[4], img)

    # pdf_string = base64.b64encode(doc.tobytes())
    pdf_string = ""
    return pdf_string
    