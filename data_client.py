from utils.sql import SafeSQL
from utils.logging import path_log

from constants import SQL_CONFIG


class DataClient:

    def __init__(self):

        try:

            # Pop the database name from the config map
            self.db_name = SQL_CONFIG.pop('database')

            # Establish a SafeSQL connection
            self.sql = SafeSQL(**SQL_CONFIG, verbose=True)

            print("MySQL Connection Successful.")

        except Exception as err:
            path_log('MySQL Connection Failed', err)

    def save_user_info(self, user_info):

        print(f"User Info: {user_info}")

        values = [
            user_info['email'],
            user_info['first_name'],
            user_info['last_name'],
            user_info['phone_number'],
            user_info['zipcode'],
            user_info['state']
        ]

        self.sql.run(f"""

            -- Initialize and use database
            CREATE DATABASE IF NOT EXISTS {self.db_name};
            USE {self.db_name};

            -- Initialize table if it doesn't already exist
            CREATE TABLE IF NOT EXISTS user_info (
                email VARCHAR(50) PRIMARY KEY,
                first_name VARCHAR(30) NOT NULL,
                last_name VARCHAR(30) NOT NULL,
                phone_number CHAR(10) NOT NULL,
                zipcode CHAR(5) NOT NULL,
                state CHAR(2) NOT NULL
            );

            -- Insert user info into table as record
            INSERT INTO user_info VALUES ('{"', '".join(values)}')

        """)

        self.sql.commit()
