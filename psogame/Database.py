import mysql.connector

class Database:
    def __init__(self) -> None:
        self.isOnline = True
        self.customColor = (0,0,0)
        self.cameraZoom = 3
        try:
            self.cnn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database = "DarkChasmPSOO"
            )
            self.c = self.cnn.cursor()
        except:
            self.isOnline = False
            print("database not reached")
    def insertRank(self,name,time):
        if self.isOnline:
            add_rank = ("INSERT INTO rank "
                "(id,name, time) "
                "VALUES (null,%s, %s)")
            data_rank = (name, time)
            self.c.execute(add_rank, data_rank)
            self.cnn.commit()
        
    def setColor(self,newColor):
        self.customColor = newColor
    
    def getColor(self):
        return self.customColor

    def closeDB(self):
        self.c.close()
        self.cnn.close()
    
    def set_sprite_scale(self,newZoom):
        self.cameraZoom = newZoom
    
    def get_sprite_scale(self):
        return self.cameraZoom

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
