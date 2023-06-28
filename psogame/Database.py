import sqlite3

class Database:
    def __init__(self) -> None:
        self.isOnline = True
        self.customColor = [0,0,0]
        self.cameraZoom = 3
        self.rankAmount = 0
        try:
            self.cnn = sqlite3.connect("database.db")
            self.c = self.cnn.cursor()
            print("database reached")
            
            self.c.execute("CREATE TABLE if not exists rank(name varchar(45),time decimal(4,3),gold int(10))")
            self.cnn.commit()   


            self.rankAmount = self.c.execute("select count(*) from rank").fetchone()[0]
            
        except:
            #self.isOnline = False
            print("database not reached")
    def insertRank(self,name,time,points):
        if self.isOnline:
            name,time,points = str(name),str(time),str(points)
            self.c.execute("INSERT INTO rank VALUES('"+name+"', "+time+","+points+")")
            self.cnn.commit()
            self.getRanksAll()
            self.updateRankAmount()
    
    def updateRankAmount(self):
        self.rankAmount = self.c.execute("select count(*) from rank").fetchone()[0]
    
    def getRanksAll(self):
        if self.isOnline:
            if self.rankAmount > 4:
                ranks = self.c.execute("SELECT * FROM rank ORDER BY time,gold ASC LIMIT 5")
            else:
                ranks = self.c.execute("SELECT * FROM rank ORDER BY time,gold ASC")
            self.cnn.commit()
            return ranks.fetchall()
           

    def delAll(self):
        self.c.execute("DELETE FROM rank")
        self.cnn.commit()
        
    def setColor(self,newColor):
        self.customColor = newColor
    
    def getColor(self):
        if len(self.customColor) == 3:
            self.customColor.append(255)
        return self.customColor

    def closeDB(self):
        self.cnn.close()
    
    def set_sprite_scale(self,newZoom):
        self.cameraZoom = newZoom
    
    def get_sprite_scale(self):
        return self.cameraZoom