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
            USE {self.db_name};
            INSERT INTO user_info VALUES ('{"', '".join(values)}')
        """)

        self.sql.commit()
