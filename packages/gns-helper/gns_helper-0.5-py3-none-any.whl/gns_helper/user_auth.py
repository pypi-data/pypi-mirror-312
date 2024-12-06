"""
User Management and Authentication API Module

This module provides API endpoints for user management and authentication. 
It includes functionalities for user sign-up, sign-in, token refresh, 
sign-out, user updates, and user deletions. Access to these APIs is 
controlled via JWT (JSON Web Tokens).

Dependencies:
- JWT for token-based authentication
- Logging for tracking operations
- Database operations for CRUD actions

APIs:
- sign_up: Registers a new user in the system.
- sign_in: Authenticates a user and provides access and refresh tokens.
- update_scale: Updates the application scale configuration.
- token_refresh: Refreshes the JWT access token.
- sign_out: Logs out the user and updates their status.
- get_all_users: Retrieves a list of all users with their details.
- update_user: Updates user information and access levels.
- delete_user: Deletes a user from the system.
"""
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from flask import request
import hashlib
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import pymysql
from .config import logger
from .custom_decorators import handle_exceptions
from .constants import (
    USER_ACCESS_ALLOW,
    USER_ACCESS_DENY,
    USER_STATE_ACTIVE,
    USER_STATE_INACTIVE,
    USER_TYPE_ADMIN,
)
from .table_operations import (
    DBTableOperations,
    Validation,
    is_ref_exist
    )
from .views_helper_functions import update_last_active_time
import pymysql
from dbutils.pooled_db import PooledDB

BLOCK_SIZE = 32
TABLE_USER = "User"


from .set_db_name import get_config

class UserAuth:
    def __init__(self):
        config = get_config()
        db_config = config.get('development', config['default'])  # Assuming 'development' environment

        self.pool = PooledDB(
            creator=pymysql,
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['username'],
            password=db_config['password'],
            database=db_config['database'],
            blocking=False,
            maxconnections=100,
        )
        self.encryption_key = b"1234567890123456"  # This key should be stored securely

    
    def encrypt(self, plaintext, key=None):
        key = key if key else self.encryption_key
        cipher = AES.new(key, AES.MODE_ECB)
        return base64.b64encode(
            cipher.encrypt(pad(plaintext.encode("utf-8"), BLOCK_SIZE))
        ).decode("utf-8")

    def decrypt(self, ciphertext, key=None):
        key = key if key else self.encryption_key
        cipher = AES.new(key, AES.MODE_ECB)
        return unpad(cipher.decrypt(base64.b64decode(ciphertext)), BLOCK_SIZE).decode(
            "utf-8"
        )
        
    @handle_exceptions
    @jwt_required(refresh=True)
    def token_refresh(self):
        current_user_id = get_jwt_identity()  # Gets Identity from JWT
        query = (
            "SELECT is_active FROM "
            + TABLE_USER
            + " WHERE id = "
            + str(current_user_id)
            + ";"
        )
        #print("user",current_user_id)
        user = DBTableOperations().fetch_one(query)
        #print("******* user ******",user)
        if user["is_active"] == USER_STATE_ACTIVE:
            new_token = create_access_token(identity=current_user_id, fresh=False)
            return {"success": True, "access_token": new_token}
        else:
            return {"success": False}
    
    @handle_exceptions
    def sign_up(self):
        data = request.get_json()
        col_list = ["username", "email", "mobile"]
        is_exist = Validation().is_record_exist(data, TABLE_USER, col_list)
        if is_exist:
            return {
                "success": False,
                "message": "User already exists with this Username, Email, or Mobile!"
            }
        password = data["password"]
        data["password"] = self.encrypt(password)
        user = DBTableOperations()
        user.create(table_name=TABLE_USER, data=data)
        return {"success": True, "message": "User Created Successfully!"}

    @handle_exceptions
    def sign_in(self):
        data = request.get_json()
        username_or_email = data["username_or_email"]
        password = data["password"]

        query = (
            f"SELECT * FROM {TABLE_USER} WHERE username = '{username_or_email}' OR email = '{username_or_email}';"
        )
        print("query-------------------------------",query)
        conn = self.pool.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        user = cursor.fetchone()
        print("user",user)
        
        if not user:
            return {"success": False, "message": "User doesn't exist!"}

        if (user["username"] == username_or_email or user["email"] == username_or_email) and \
                (user["password"] == self.encrypt(password)):
            if user["user_access"] != 1:
                return {
                    "success": False,
                    "message": "Your access is denied. Please contact Admin!"
                }

            refresh_token = create_refresh_token(identity=user["id"])
            access_token = create_access_token(identity=user["id"], fresh=True)
            update_last_active_time(user_id=user["id"])

            return {
                "success": True,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_type": user["user_type"],
                "name": user["name"],
                "username": user["username"],
                "email": user["email"],
                "gender": user["gender"],
            }
        return {"success": False, "message": "Invalid credentials!"}

    @handle_exceptions
    @jwt_required()
    def get_all_users(self):
        operation = DBTableOperations()
        query = f"SELECT * FROM {TABLE_USER} ORDER BY id DESC;"
        data = operation.fetch(query)
        for i in range(len(data)):
            data[i]["password"] = self.decrypt(data[i]["password"])  # Decrypt passwords
        return {"success": True, "data": data}

    @handle_exceptions
    @jwt_required()
    def update_user(self):
        data = request.get_json()
        user_access = data["user_access"]
        user_type = data["user_type"]
        print("update user !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",data)

        if user_type == USER_TYPE_ADMIN and user_access == USER_ACCESS_DENY:
            query = f"SELECT * FROM {TABLE_USER} WHERE user_type = {USER_TYPE_ADMIN} AND user_access = {USER_ACCESS_ALLOW};"
            admin_users = DBTableOperations().fetch(query)
            if len(admin_users) < 2:
                return {
                    "success": False,
                    "message": "Only one ADMIN remains. Can't deny access for this user."
                }

        if user_access == USER_ACCESS_DENY:
            data["is_active"] = USER_STATE_INACTIVE

        col_list = ["username", "email", "mobile"]
        is_exist = Validation().is_record_exist(data, TABLE_USER, col_list, is_update=True)
        if is_exist:
            return {
                "success": False,
                "message": "User already exists with this Username, Email, or Mobile!"
            }

        user_id = data.pop("id")
        if "password" in data:
            password = data["password"]
            data["password"] = self.encrypt(password)
        
        operation = DBTableOperations()
        operation.update(table_name=TABLE_USER, data=data, id=user_id)
        return {"success": True, "message": "User updated successfully!"}
    
    @handle_exceptions
    @jwt_required(refresh=True)
    def sign_out(self):
        current_user_id = get_jwt_identity()  # Gets Identity from JWT
        update_data = {"is_active": 0}
        operation = DBTableOperations()
        operation.update(table_name=TABLE_USER, data=update_data, id=current_user_id)
        return {"success": True}

    @handle_exceptions
    @jwt_required()
    def delete_user(self):
        data = request.get_json()
        user_id = data["id"]
        user_type = data["user_type"]
        if user_type == USER_TYPE_ADMIN:
            query = (
                "SELECT * FROM "
                + TABLE_USER
                + " WHERE user_type = "
                + str(USER_TYPE_ADMIN)
                + " ;"
            )
            admin_users = DBTableOperations().fetch(query)
            if len(admin_users) < 2:
                return {
                    "success": False,
                    "message": "Only one ADMIN remains. So can't DELETE this user.",
                }
        user_id = data["id"]
        is_exist = is_ref_exist(TABLE_USER, col_nm="formula", id=user_id)
        if is_exist:
            return {
                "success": False,
                "message": "This Username created some Data. So can't delete. If you want to delete then first delete all the data which is made by this user !!!",
            }
        operation = DBTableOperations()
        query = "DELETE FROM " + TABLE_USER + " WHERE id = " + str(user_id) + ";"
        operation.delete(query)
        return {"success": True, "message": "User Deleted Successfully !!!"}