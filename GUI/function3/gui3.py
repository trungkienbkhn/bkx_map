import sys
sys.path.append("..")

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import app
import psycopg2
import geopandas as gpd
from geopy.geocoders import Nominatim

qtCreatorFile1 = "function3/Filter.ui"
qtCreatorFile2 = "function3/Direct.ui"
Ui_MainWindow1, QtBaseClass1 = uic.loadUiType(qtCreatorFile1)
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(qtCreatorFile2)

name = ''
street = ''
min = ''
max = ''
open_h = ''
close_h = ''
type = ''

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
    def search_res(self, key):
        self.cur.execute('''select *
                            from res_point
                            where name like '%{}%' '''.format(key))
        return self.cur.fetchall()

    def get_res_1(self, open, close, min, max):
        self.cur.execute('''select *
                            from res_point
                            where opening_ho <= {} and closing_ho >= {}
                            and min_price >= {} and max_price <= {}'''.format(open, close, min, max))
        return self.cur.fetchall()

    def get_res_2(self, open, close, min, max, type):
        self.cur.execute('''select *
                            from res_point
                            where opening_ho <= {} and closing_ho >= {}
                            and min_price >= {} and max_price <= {}
                            and type like '%{}%' '''.format(open, close, min, max, type))
        return self.cur.fetchall()

    def get_res_3(self, open, close, min, max, street):
        self.cur.execute('''select *
                            from res_point
                            where opening_ho <= {} and closing_ho >= {}
                            and min_price >= {} and max_price <= {}
                            and addr_stree = '{}' '''.format(open, close, min, max, street))
        return self.cur.fetchall()

    def get_res_4(self, open, close, min, max, street, type):
        self.cur.execute('''select *
                            from res_point
                            where opening_ho <= {} and closing_ho >= {}
                            and min_price >= {} and max_price <= {}
                            and addr_stree = '{}' 
                            and type like '%{}%' '''.format(open, close, min, max, street, type))
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

class Funct3(QtWidgets.QMainWindow, Ui_MainWindow1):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow1.__init__(self)
        self.setupUi(self)
        self.filter.clicked.connect(self.res)
        self.back.clicked.connect(self.come_back)
        self.search.clicked.connect(self.search_res)

    def come_back(self):
        self.main = app.Homepage()
        self.main.show()
        self.close()

    def res(self):
        global street, open_h, close_h, min, max, type
        street = self.address.currentText()
        open_h = self.open.currentText()
        close_h = self.close_h.currentText()
        min = self.min.currentText()
        max = self.max.currentText()
        type = self.type.currentText()
        self.main = Funct3_result()
        self.main.show()
        self.close()
    
    def search_res(self):
        global name
        name = self.name.text()
        self.main = Funct3_search()
        self.main.show()
        self.close()

class Funct3_search(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.back.clicked.connect(self.come_back)
        self.direct.clicked.connect(self.res_direct)
        global name
        a = GetPsql()
        b = a.search_res(name)
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
        self.main = Funct3()
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

class Funct3_result(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        global street, open_h, close_h, min, max, type
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.back.clicked.connect(self.come_back)
        self.direct.clicked.connect(self.res_direct)
        if (open_h == "None"):
            open_h = 11
        else:
            open_h = int(open_h.rstrip("h"))
        if (close_h == "None"):
            close_h = 15
        else:
            close_h = int(close_h.rstrip("h"))
        if (min == "None"):
            min = 0
        else:
            min = int(min.rstrip("K"))
        if (max == "None"):
            max = 500
        else:
            max = int(max.rstrip("K"))
        a = GetPsql()
        street = street.lstrip("Đường").lstrip(" ")
        if (street == "None"):
            if (type == "None"):
                b = a.get_res_1(open_h,close_h,min,max)
            else:
                b = a.get_res_2(open_h,close_h,min,max,type)
        else:
            if (type == "None"):
                b = a.get_res_3(open_h,close_h,min,max,street)
            else:
                b = a.get_res_4(open_h,close_h,min,max,street,type)
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
        self.main = Funct3()
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
