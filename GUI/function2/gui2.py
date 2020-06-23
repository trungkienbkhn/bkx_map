import sys
sys.path.append("..")

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import app
import psycopg2
import geopandas as gpd
from geopy.geocoders import Nominatim

qtCreatorFile1 = "function2/Near_res.ui"
qtCreatorFile2 = "function2/Direct_near_res.ui"
Ui_MainWindow1, QtBaseClass1 = uic.loadUiType(qtCreatorFile1)
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(qtCreatorFile2)

type = ''
lat = ''
long = ''

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
    def get_top_res(self, type, coordinate):
        self.cur.execute('''select *
                            from res_point
                            where type = '{}'
                            order by st_distance(geom,'POINT({})'::geometry)
                            limit 5'''.format(type, coordinate))
        return self.cur.fetchall()

    def get_top_res_nontype(self, coordinate1, coordinate2):
        self.cur.execute('''select rp. *
                            from res_point as rp, res_point_mbr rpm, 
                            (select idx
                            from res_point_bounding rpb
                            order by rpb.geom <#> 'SRID=4326;POINT({})'::geometry
                            limit 5) rpb1
                            where rpm.idx = rpb1.idx and rp.id = rpm.id
                            order by st_distance(rpm.geom,'POINT({})'::geometry)
                            limit 5'''.format(coordinate1, coordinate2))
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

class Funct2(QtWidgets.QMainWindow, Ui_MainWindow1):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow1.__init__(self)
        self.setupUi(self)
        self.top.clicked.connect(self.top_res)
        self.back.clicked.connect(self.come_back)

    def come_back(self):
        self.main = app.Homepage()
        self.main.show()
        self.close()

    def top_res(self):
        global type, long, lat
        addr = self.location.text()
        geolocator = Nominatim()
        location = geolocator.geocode(addr)
        lat = location.latitude
        long = location.longitude
        type = self.type.currentText()
        self.main = Funct2_result()
        self.main.show()
        self.close()

class Funct2_result(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.back.clicked.connect(self.come_back)
        self.direct.clicked.connect(self.res_direct)
        global type, long, lat
        coordinate = str(lat)+" "+str(long)
        if (type != 'None'):
            a = GetPsql()
            b = a.get_top_res(type, coordinate)
        else:
            a = GetPsql()
            b = a.get_top_res_nontype(coordinate, coordinate)

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
        self.main = Funct2()
        self.main.show()
        self.close()

    def res_direct(self):
        name = self.res.currentText()
        a = GetPsql()
        b = a.get_coordinates(name)
        t = str(b).lstrip("[('POINT(").rstrip("',)]").split(" ")

        global long, lat
        
        df = a.create_route(long,lat,t[0],t[1])
        print(df)
        # addr_save = "/home/kien/Documents/httt địa lý/shp/"+name+".shp"
        # df.to_file(addr_save)
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Success")
        text = "Created file "+name+".shp"
        msg.setText(text)
        msg.exec_()
