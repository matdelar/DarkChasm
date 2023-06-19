import sqlite3

class Database:
    def __init__(self) -> None:
        self.isOnline = True
        self.customColor = (0,0,0)
        self.cameraZoom = 3
        self.rankAmount = 0
        try:
            self.cnn = sqlite3.connect("database.db")
            self.c = self.cnn.cursor()
            print("database reached")
            self.rankAmount = self.c.execute("select count(*) from rank").fetchone()[0]
            try:
                self.c.execute("CREATE TABLE rank(name,time)")
            except:
                pass
        except:
            self.isOnline = False
            print("database not reached")
    def insertRank(self,name,time):
        if self.isOnline:
            name,time = str(name),str(time)
            self.c.execute("INSERT INTO rank VALUES('"+name+"', '"+time+"')")
            self.cnn.commit()
            self.getRanksAll()
            self.updateRankAmount()
    
    def updateRankAmount(self):
        self.rankAmount = self.c.execute("select count(*) from rank").fetchone()[0]
    
    def getRanksAll(self):
        if self.isOnline:
            ranks = self.c.execute("SELECT * FROM RANK")
            self.cnn.commit()
            return ranks.fetchall()
    
    def delAll(self):
        self.c.execute("DELETE FROM rank")
        self.cnn.commit()
        
    def setColor(self,newColor):
        self.customColor = newColor
    
    def getColor(self):
        return self.customColor

    def closeDB(self):
        self.cnn.close()
    
    def set_sprite_scale(self,newZoom):
        self.cameraZoom = newZoom
    
    def get_sprite_scale(self):
        return self.cameraZoom