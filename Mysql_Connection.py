import mysql.connector
from mysql.connector import Error


class MySqlConnection:

    def __init__(self, db_user, db_password, db_name):
        try:
            self.connection = mysql.connector.connect(host='localhost',
                                                      database=f'{db_name}',
                                                      user=f'{db_user}',
                                                      password=f'{db_password}')
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Connection successfully")

        except Error as e:
            print("Error while connecting to MySQL", e)

    def add_parameters(self, matricule=None, anomaly=None, speed=None, _long=None, lat=None, id_user=None):
        """
                    Define the parameters
        :param matricule:
        :param anomaly:
        :param speed:
        :param _long:
        :param lat:
        :param id_user:
        :return:
        """
        query = """INSERT INTO parameters(Matricule, Anomalie, Vitesse, Longitude, Latitude, Date_Heure, id_user) VALUES 
                                                (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP,%s) """
        recordTuple = (matricule, anomaly, speed, _long, lat, id_user)
        try:
            self.cursor.execute(query, recordTuple)
            self.connection.commit()
            print("Record inserted successfully")

        except Error as e:
            print("Error while connecting to MySQL", e)

        finally:
            if (self.connection.is_connected()):
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")

