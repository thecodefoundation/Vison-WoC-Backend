import pandas as pd
import psycopg2
from psycopg2 import Error
import os

try:
    connection = psycopg2.connect(user = "postgres",
                              password = "Ayush3186",
                              host = "127.0.0.1",
                              port = "5432",
                              database = "vison_demo_indexdb")

    cursor = connection.cursor()
    # print ( connection.get_dsn_parameters(),"\n")
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

    # creating table
    create_table_query = '''CREATE TABLE image_index
          (ID SERIAL PRIMARY KEY     NOT NULL,
          image_id           text    NOT NULL,
          image_url         text
          ); '''
    
    cursor.execute(create_table_query)
    connection.commit()

    # adding columns
    for label in labels:
	    add_column = "ALTER TABLE image_index ADD COLUMN {} INT;".format(label.replace(" ", "_"))
	    cursor.execute(add_column)
	    connection.commit()

except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while creating PostgreSQL table", error)

finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
