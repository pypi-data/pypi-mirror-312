"""
This module provides classes and methods for performing various database operations, 
including CRUD operations, barcode data handling, and zero data management.

Classes:
    - DBTableOperations: Handles basic CRUD operations for database tables.
    - Preprocessing: Prepares SQL queries for database operations.
    - Validation: Validates the existence of records in the database.
    - BarcodeDataModel: Manages operations related to barcode data.
    - ZeroDataModel: Manages operations for handling zero configurations in the database.

Functions:
    - is_ref_exist: Checks if a reference exists in a database table.
"""
import yaml
import os
import pymysql
from dbutils.pooled_db import PooledDB
from .set_db_name import get_config
        
class DBTableOperations:
    """
    Class for performing database operations such as insert, update, delete, and fetch.
    @Auther:
    """
    connection = None
    cursor = None

    def __init__(self):
        """
        Initializes the database connection and cursor.
        @Auther:
        
        """
        config = get_config()
        db_config = config.get('development', config['default'])  # Assuming 'development' environment

        pool = PooledDB(
            creator=pymysql,
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['username'],
            password=db_config['password'],
            database=db_config['database'],
            blocking=False,
            maxconnections=100,
        )

        # Initialization
        #self.connection = sqlite3.connect(DATABASE_NAME)
        self.connection = pool.connection()
        # self.connection = self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.row_factory = lambda c, r: dict(
            [(col[0], r[idx]) for idx, col in enumerate(c.description)]
        )
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        #self.cursor = self.cursor.execute("PRAGMA foreign_keys = ON")

    def create(self, table_name, data):
        """
        Inserts a new record into the specified table.

        Parameter:
            table_name (str): Name of the table.
            data (dict): Dictionary containing column names and values.

        Returns:
            int: ID of the inserted row.
        @Auther:
        """
        # Prepare query
        query = Preprocessing().prepare_insert_query(table_name, data)
        # Execute query
        print(query)
        self.cursor.execute(query)
        inserted_row_id = self.cursor.lastrowid
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        return inserted_row_id

    def select_product(self):
        """
        Selects all records from the ProductInfo table.

        Returns:
            list: List of dictionaries containing the fetched records.
        @Auther:
        """
        #query = Preprocessing().prepare_insert_query(table_name, data)
        query = "select * from ProductInfo"
        # Execute query
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        print(data)
        self.cursor.close()
        self.connection.close()
        return data


    def update(self, table_name, data, **conditional_param):
        """
        Updates records in the specified table based on the conditional parameters.

        Parameter:
            table_name (str): Name of the table.
            data (dict): Dictionary containing column names and values to update.
            conditional_param (dict): Dictionary containing column names and values for the condition.
        @Auther:
        """
        query = Preprocessing().prepare_update_query(
            table_name, data, conditional_param
        )
        # Execute query
        self.cursor.execute(query)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def update_complex(self, query):
        """
        Executes a complex update query.

        Parameter:
            query (str): The SQL query to execute.
        @Auther:
        """
        # Execute query
        self.cursor.execute(query)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def fetch(self, query):
        """
        Fetches multiple records based on the query.

        Parameter:
            query (str): The SQL query to execute.

        Returns:
            list: List of dictionaries containing the fetched records.
        @Auther:
        """
        # Start to Fetch
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        #self.cursor.close()
        #self.connection.close()
        return data

    def fetch_one(self, query):
        """
        Fetches a single record based on the query.

        Parameter:
            query (str): The SQL query to execute.

        Returns:
            dict: Dictionary containing the fetched record.
        @Auther:
        """
        # Start to Fetch Single Record
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        self.cursor.close()
        self.connection.close()
        return data

    def delete(self, query):
        """
        Deletes records based on the query.

        Parameter:
            query (str): The SQL query to execute.
        @Auther:
        """
        # Delete Records
        self.cursor.execute(query)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


class Preprocessing:
    """
    Class for preparing SQL queries for various database operations.
    @Auther:
    """
    def __init__(self):
        pass

    def prepare_insert_query(self, table_name, data):
        """
        Prepares an SQL insert query.

        Parameter:
            table_name (str): Name of the table.
            data (dict): Dictionary containing column names and values.

        Returns:
            str: Prepared SQL insert query.
        @Auther:
        """
        # Prepare Fields & Values
        fields = (str(list(data.keys()))[1:-1]).replace("'", "")
        values = str(list(data.values()))[1:-1]

        # Prepare Query
        query = (
            "INSERT INTO " + table_name + " (" + fields + ") VALUES (" + values + ");"
        )
        print("query",query)
        return query

    def prepare_update_query(self, table_name, data, conditional_param):
        """
        Prepares an SQL update query.

        Parameter:
            table_name (str): Name of the table.
            data (dict): Dictionary containing column names and values to update.
            conditional_param (dict): Dictionary containing column names and values for the condition.

        Returns:
            str: Prepared SQL update query.
        @Auther:
        """
        # Prepare Condition String
        if not len(conditional_param) == 1:
            raise TypeError("update() requires three argumnts.")
        key = list(conditional_param.keys())[0]
        value = list(conditional_param.values())[0]
        #print("key",key)
        #print("value",value)
        if type(value) == int or type(value) == float:
            condition = key + "=" + str(value)
        else:
            condition = key + "='" + str(value) + "'"

        # Prepare Updated Values String
        fields = list(data.keys())
        values = list(data.values())
        
        print("fields",fields)
        print("values",values)

        updated_values = (
            "".join(
                [
                    fields[i] + "=(" + str(values[i]) + "), "
                    if type(values[i]) == int or type(values[i]) == float
                    else fields[i] + "=('" + str(values[i]) + "'), "
                    for i in range(len(fields))
                ]
            )
            .strip()
            .rstrip(",")
        )

        # Prepare Query
        query = (
            "UPDATE "
            + table_name
            + " SET "
            + updated_values
            + " WHERE "
            + condition
            + ";"
        )

        return query


class Validation:
    """
    Class for validating records in the database.
    """
    def __init__(self):
        pass

    """
        Checks if a record exists in the database based on specified conditions.

        Parameter:
            data (dict): Dictionary containing column names and values.
            table_name (str): Name of the table.
            col_list (list): List of column names used in the filter.
            all_unique (bool): Whether all columns should be unique.
            is_update (bool): Whether it's an update operation.

        Returns:
            bool: True if the record exists, False otherwise.
        @Auther:
    """
    def is_record_exist(
        self, data, table_name, col_list, all_unique=False, is_update=False
    ):
        """
        col_list : list of column names which are used in filter
        all_unique = False : at least one column should be UNIQUE
        all_unique = True : all columns should be UNIQUE
        is_update = False : record exist with current id
        is_update = True : record exist other than current id
        """
        if all_unique is False:
            condition = "OR"
        elif all_unique is True:
            condition = "AND"
        else:
            raise Exception("all_unique should be True or False.")

        filter_str = ""
        for col in col_list:
            filter_str += f" {col} = '{data[col]}' {condition}"
        filter_str = filter_str.strip()
        filter_str = filter_str.rstrip(condition)
        if is_update is False:
            query = f"SELECT * FROM {table_name} WHERE {filter_str};"
        elif is_update is True:
            query = (
                f"SELECT * FROM {table_name} WHERE ({filter_str}) AND id<>{data['id']}"
            )
        else:
            raise Exception('data should contain "id".')

        record = DBTableOperations().fetch_one(query)
        if record is not None:
            return True
        else:
            return False


def is_ref_exist(table_name, col_nm, id):
    """
    Checks if a reference exists in the database.

    Parameter:
        table_name (str): Name of the table.
        col_nm (str): Column name.
        id (int): ID to check.

    Returns:
        bool: True if the reference exists, False otherwise.
    @Auther:
    """
    query = f"SELECT * FROM {table_name} WHERE {col_nm}={id};"
    record = DBTableOperations().fetch_one(query)
    if record is not None:
        return True
    else:
        return False

class BarcodeDataModel:
    """
    Class for handling barcode data operations.
    """
    connection = None
    cursor = None

    def __init__(self) -> None:
        config = get_config()
        db_config = config.get('development', config['default'])  # Assuming 'development' environment

        pool = PooledDB(
            creator=pymysql,
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['username'],
            password=db_config['password'],
            database=db_config['database'],
            blocking=False,
            maxconnections=100,
        )
        self.connection = pool.connection()
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def compare(self, value):
        """
        Compares the barcode value with product codes in the database.

        Parameter:
            value (str): Barcode value to compare.

        Returns:
            dict: JSON response indicating success and data or failure message.
        @Auther:
        """
        print("------------------------------------  from barcode data model -------------------------------------------")
        print("barcode value",value)
        # compare value with product code 
        # if matches -> return product info 
        query = "Select * from ProductInfo where product_code='{value}'"
        response = self.cursor.execute(query)
        print("-------------------------------- fetched row for given barcode ------------------------",response)
        
        if (len(response)==0):
            return {"success": False, "message": "no data found!"}
        else:
            return {"success": True, "data": response , "message":"success"}

        
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

class ZeroDataModel:
    """
    Class for handling zero data operations.
    """
    connection = None
    cursor = None

    def __init__(self) -> None:
        """
        Initializes the database connection and cursor for zero configuration operations.
        """
        config = get_config()
        db_config = config.get('development', config['default'])  # Assuming 'development' environment

        pool = PooledDB(
            creator=pymysql,
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['username'],
            password=db_config['password'],
            database=db_config['database'],
            blocking=False,
            maxconnections=100,
        )
        self.connection = pool.connection()
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def update_zero(self, value):
        """
        Updates the zero value in the SystemConfig table.

        Parameter:
            value (str): Value to update.

        Returns:
            dict: JSON response indicating success and data or failure message.
        @Auther:
        """
        print("------------------------------------  from zero data model -------------------------------------------")
        print("zero value",value)
        # compare value with product code 
        # if matches -> return product info 
        query = "Select * from SystemConfig where is_zero ='{value}'"
        response = self.cursor.execute(query)
        print("-------------------------------- fetched row for given barcode ------------------------",response)
        
        if (len(response)==0):
            return {"success": False, "message": "no data found!"}
        else:
            return {"success": True, "data": response , "message":"success"}