import mysql.connector

class Database:
    def __init__(self) -> None:
        self.cnn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = "DarkChasmPSOO"
        )
        self.c = self.cnn.cursor()

    def insertRank(self,name,time):
        add_rank = ("INSERT INTO rank "
              "(id,name, time) "
              "VALUES (null,%s, %s)")
        data_rank = (name, time)
        self.c.execute(add_rank, data_rank)
        self.cnn.commit()
    

    def closeDB(self):
        self.c.close()
        self.cnn.close()

#create database darkchasmpsooo;
#use darkchasmpsoo;# MySQL não retornou nenhum registo.
#CREATE TABLE rank(
#id int NOT null	AUTO_INCREMENT,
#name varchar(45) not null,
#time varchar(45) not null,
#    PRIMARY KEY (id)
#
#);# MySQL não retornou nenhum registo.
#
