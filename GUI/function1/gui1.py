import sys
sys.path.append("..")

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import app
import psycopg2
import geopandas as gpd
from geopy.geocoders import Nominatim

qtCreatorFile = "function1/Direct.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class GetPsql:
    # Connect to databse
    conn = psycopg2.connect(user = "postgres",
                            password = "s",
                            host = "localhost",
                            port = "5432",
                            database = "bkx")

    def __init__(self):
        self.cur = self.getdb()

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def getdb(self):
        return self.conn.cursor()

    # Query from database
    def get_all_res(self):
        self.cur.execute('''select *
                            from res_point''')
        return self.cur.fetchall()

    def get_coordinates(self, name):
        self.cur.execute('''select ST_AsText(geom)
                            from res_point
                            where name = '{}' '''.format(name))
        return self.cur.fetchall()

    def create_route(self, long1, lat1, long2, lat2):
        conn = psycopg2.connect(database = "bkx", user = "postgres", password = "s", host = "localhost", port = "5432")
        sql = "SELECT (route.geom) FROM (SELECT geom FROM pgr_fromCtoD('roads',"+str(long1)+","+str(lat1)+","+str(long2)+","+str(lat2)+") ORDER BY seq) AS route;"
        df = gpd.GeoDataFrame.from_postgis(sql, conn, geom_col='geom' )
        return df

class Funct1(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.back.clicked.connect(self.come_back)
        self.direct.clicked.connect(self.res_direct)
        a = GetPsql()
        b = a.get_all_res()
        for i in range(0, len(b)):
            self.result.setItem(i, 0, QtWidgets.QTableWidgetItem(str(b[i][1])))
            if (str(b[i][3]) != "None"):
                addr = "Số "+b[i][2]+", ngõ "+str(b[i][3])+", đường "+b[i][4]+", quận "+b[i][5]+", "+b[i][6]
            else:
                addr = "Số "+b[i][2]+", đường "+b[i][4]+", quận "+b[i][5]+", "+b[i][6]
            self.result.setItem(i, 1, QtWidgets.QTableWidgetItem(addr))
            t = str(b[i][7]).split(".")
            if (b[i][7] == 0):
                open = "0h"
            else: 
                if (t[1][0] == "5"):
                    open = t[0]+"h"+"30"
                elif (t[1][0] == "1"):
                    open = t[0]+"h"+"15"
                elif(t[1][0] == "7"):
                    open = t[0]+"h"+"45"
                else:
                    open = t[0]+"h"

            t = str(b[i][8]).split(".")
            if (b[i][8] == 0):
                close = "0h"
            else: 
                if (t[1][0] == "5"):
                    close = t[0]+"h"+"30"
                elif (t[1][0] == "1"):
                    close = t[0]+"h"+"15"
                elif(t[1][0] == "7"):
                    close = t[0]+"h"+"45"
                else:
                    close = t[0]+"h"

            self.result.setItem(i, 2, QtWidgets.QTableWidgetItem(open))
            self.result.setItem(i, 3, QtWidgets.QTableWidgetItem(close))
            price = str(b[i][10])+"-"+str(b[i][11])+"K"
            self.result.setItem(i, 4, QtWidgets.QTableWidgetItem(price))
            self.result.setItem(i, 5, QtWidgets.QTableWidgetItem(str(b[i][9])))
            self.result.setRowCount(len(b))
            self.result.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        for i in range(0, len(b)):
            self.res.addItem(b[i][1])

    def come_back(self):
        self.main = app.Homepage()
        self.main.show()
        self.close()

    def res_direct(self):
        name = self.res.currentText()
        a = GetPsql()
        b = a.get_coordinates(name)
        t = str(b).lstrip("[('POINT(").rstrip("',)]").split(" ")

        addr = self.location.text()
        geolocator = Nominatim()
        location = geolocator.geocode(addr)
        lat = location.latitude
        long = location.longitude
        
        df = a.create_route(long,lat,t[0],t[1])
        addr_save = "/home/kien/Documents/httt địa lý/shp/"+name+".shp"
        df.to_file(addr_save)
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Success")
        text = "Created file "+name+".shp"
        msg.setText(text)
        x = msg.exec_()

#48 Tạ Quang Bửu Hai Bà Trưng Hà Nội
