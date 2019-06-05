import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import psycopg2
import viewCarsInfo
import brandEdit
import colorEdit
import typeEdit
import modelEdit


class ASCRA(QtWidgets.QMainWindow, viewCarsInfo.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.updBrandBtn.clicked.connect(self.updBrand)
        self.addBrandBtn.clicked.connect(self.addBrand)
        self.delBrandBtn.clicked.connect(self.delBrand)
        self.updColorBtn.clicked.connect(self.updColor)
        self.addColorBtn.clicked.connect(self.addColor)
        self.delColorBtn.clicked.connect(self.delColor)
        self.updTypeBtn.clicked.connect(self.updType)
        self.addTypeBtn.clicked.connect(self.addType)
        self.delTypeBtn.clicked.connect(self.delType)
        self.updModelBtn.clicked.connect(self.updModel)
        self.addModelBtn.clicked.connect(self.addModel)
        self.delModelBtn.clicked.connect(self.delModel)
        self.tabWidget.tabBarClicked.connect(self.getData)

        labels = ['ID', 'Цвет']
        self.carColorTable.verticalHeader().hide()
        self.carColorTable.setColumnCount(len(labels))
        self.carColorTable.setColumnWidth(0, 25)
        self.carColorTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.carColorTable.setHorizontalHeaderLabels(labels)

        labels = ['ID', 'Тип ТС']
        self.carTypeTable.verticalHeader().hide()
        self.carTypeTable.setColumnCount(len(labels))
        self.carTypeTable.setColumnWidth(0, 25)
        self.carTypeTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.carTypeTable.setHorizontalHeaderLabels(labels)

        labels = ['ID', 'Марка']
        self.carBrandTable.verticalHeader().hide()
        self.carBrandTable.setColumnCount(len(labels))
        self.carBrandTable.setColumnWidth(0, 25)
        self.carBrandTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.carBrandTable.setHorizontalHeaderLabels(labels)

        labels = ['ID', 'Марка', 'Модель', 'Тип']
        self.carModelTable.verticalHeader().hide()
        self.carModelTable.setColumnCount(len(labels))
        self.carModelTable.setColumnWidth(0, 25)
        self.carModelTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.carModelTable.setHorizontalHeaderLabels(labels)

        self.getDataBrand()
        self.getDataType()
        self.getDataColor()
        self.getDataModel()

    def getDataBrand(self):
        self.carBrandTable.setRowCount(0)
        conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                port="5432")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM car_brands ORDER BY id ASC ')
        for row in cursor:
            tableRow = self.carBrandTable.rowCount()
            self.carBrandTable.setRowCount(tableRow + 1)
            self.carBrandTable.setItem(tableRow, 0, QTableWidgetItem(str(row[0])))
            self.carBrandTable.setItem(tableRow, 1, QTableWidgetItem(row[1]))
        cursor.close()
        conn.close()

    def getDataType(self):
        self.carTypeTable.setRowCount(0)
        conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                port="5432")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM car_types ORDER BY id ASC ')
        for row in cursor:
            tableRow = self.carTypeTable.rowCount()
            self.carTypeTable.setRowCount(tableRow + 1)
            self.carTypeTable.setItem(tableRow, 0, QTableWidgetItem(str(row[0])))
            self.carTypeTable.setItem(tableRow, 1, QTableWidgetItem(row[1]))
        cursor.close()
        conn.close()

    def getDataColor(self):
        self.carColorTable.setRowCount(0)
        conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                port="5432")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM car_colors ORDER BY id ASC ')
        for row in cursor:
            tableRow = self.carColorTable.rowCount()
            self.carColorTable.setRowCount(tableRow + 1)
            self.carColorTable.setItem(tableRow, 0, QTableWidgetItem(str(row[0])))
            self.carColorTable.setItem(tableRow, 1, QTableWidgetItem(row[1]))
        cursor.close()
        conn.close()

    def getDataModel(self):
        self.carModelTable.setRowCount(0)
        conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                port="5432")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM car_models
            INNER JOIN car_brands AS brand_name ON
            car_models.brand = brand_name.id
            INNER JOIN car_types AS type_name ON
            car_models.type = type_name.id
            ORDER BY car_models.id ASC 
        ''')
        for row in cursor:
            tableRow = self.carModelTable.rowCount()
            self.carModelTable.setRowCount(tableRow + 1)
            self.carModelTable.setItem(tableRow, 0, QTableWidgetItem(str(row[0])))
            self.carModelTable.setItem(tableRow, 1, QTableWidgetItem(str(row[5])))
            self.carModelTable.setItem(tableRow, 2, QTableWidgetItem(row[2]))
            self.carModelTable.setItem(tableRow, 3, QTableWidgetItem(str(row[7])))
        cursor.close()
        conn.close()

    def updBrand(self):
        selectedRow = self.carBrandTable.currentRow()
        selectedItem = self.carBrandTable.item(selectedRow, 0)
        selectedId = QTableWidgetItem(selectedItem)
        itemId = selectedId.text()
        selectedItem = self.carBrandTable.item(selectedRow, 1)
        selectedId = QTableWidgetItem(selectedItem)
        itemName = selectedId.text()
        window = BrandDialog(str(itemName), itemId, True)
        window.exec_()
        self.getDataBrand()

    def addBrand(self):
        window = BrandDialog("", 0, False)
        window.exec_()
        self.getDataBrand()

    def delBrand(self):
        selectedRow = self.carBrandTable.currentRow()
        selectedItem = self.carBrandTable.item(selectedRow, 0)
        selectedId = QTableWidgetItem(selectedItem)
        itemId = selectedId.text()
        if int(itemId) > 0:
            conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                    port="5432")
            cursor = conn.cursor()
            query = "DELETE FROM car_brands WHERE id = " + itemId
            cursor.execute(query)
            cursor.close()
            conn.commit()
            conn.close()
            self.getDataBrand()

    def updColor(self):

        selectedRow = self.carColorTable.currentRow()
        selectedItem = self.carColorTable.item(selectedRow, 0)
        selectedId = QTableWidgetItem(selectedItem)
        itemId = selectedId.text()

        selectedItem = self.carColorTable.item(selectedRow, 1)
        selectedId = QTableWidgetItem(selectedItem)
        itemName = selectedId.text()

        window = ColorDialog(str(itemName), itemId, True)
        window.exec_()
        self.getDataColor()

    def addColor(self):
        window = ColorDialog("", 0, False)
        window.exec_()
        self.getDataColor()

    def delColor(self):
        selectedRow = self.carColorTable.currentRow()
        selectedItem = self.carColorTable.item(selectedRow, 0)
        selectedId = QTableWidgetItem(selectedItem)
        itemId = selectedId.text()
        if int(itemId) > 0:
            conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                    port="5432")
            cursor = conn.cursor()
            query = "DELETE FROM car_colors WHERE id = " + itemId
            cursor.execute(query)
            cursor.close()
            conn.commit()
            conn.close()
            self.getDataColor()

    def updModel(self):

        # открытие подключения
        conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                port="5432")
        cursor = conn.cursor()

        # берем айдишник
        selectedRow = self.carModelTable.currentRow()
        selectedItem = self.carModelTable.item(selectedRow, 0)
        selectedId = QTableWidgetItem(selectedItem)
        itemId = selectedId.text()

        # берем название
        selectedItem = self.carModelTable.item(selectedRow, 2)
        selectedId = QTableWidgetItem(selectedItem)
        itemName = selectedId.text()

        # берем тип
        selectedItem = self.carModelTable.item(selectedRow, 3)
        selectedId = QTableWidgetItem(selectedItem)
        query = "SELECT id FROM car_types WHERE name = '" + selectedId.text() + "'"
        cursor.execute(query)
        resultString = cursor.fetchone()
        itemType = int(resultString[0])

        # берем марку
        selectedItem = self.carModelTable.item(selectedRow, 1)
        selectedId = QTableWidgetItem(selectedItem)
        query = "SELECT id FROM car_brands WHERE name = '" + selectedId.text() + "'"
        cursor.execute(query)
        resultString = cursor.fetchone()
        itemBrand = int(resultString[0])

        cursor.close()
        conn.close()

        window = ModelDialog(str(itemName), itemId, True, itemType, itemBrand)
        window.exec_()
        self.getDataModel()

    def addModel(self):
        window = ModelDialog("", 0, False, 0, 0)
        window.exec_()
        self.getDataModel()

    def delModel(self):
        selectedRow = self.carModelTable.currentRow()
        selectedItem = self.carModelTable.item(selectedRow, 0)
        selectedId = QTableWidgetItem(selectedItem)
        itemId = selectedId.text()
        if int(itemId) > 0:
            conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                    port="5432")
            cursor = conn.cursor()
            query = "DELETE FROM car_models WHERE id = " + itemId
            cursor.execute(query)
            cursor.close()
            conn.commit()
            conn.close()
            self.getDataModel()

    def updType(self):

        selectedRow = self.carTypeTable.currentRow()
        selectedItem = self.carTypeTable.item(selectedRow, 0)
        selectedId = QTableWidgetItem(selectedItem)
        itemId = selectedId.text()

        selectedItem = self.carTypeTable.item(selectedRow, 1)
        selectedId = QTableWidgetItem(selectedItem)
        itemName = selectedId.text()

        window = TypeDialog(str(itemName), itemId, True)
        window.exec_()
        self.getDataType()

    def addType(self):
        window = TypeDialog("", 0, False)
        window.exec_()
        self.getDataType()

    def delType(self):
        selectedRow = self.carTypeTable.currentRow()
        selectedItem = self.carTypeTable.item(selectedRow, 0)
        selectedId = QTableWidgetItem(selectedItem)
        itemId = selectedId.text()
        if int(itemId) > 0:
            conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                    port="5432")
            cursor = conn.cursor()
            query = "DELETE FROM car_types WHERE id = " + itemId
            cursor.execute(query)
            cursor.close()
            conn.commit()
            conn.close()
            self.getDataType()

    def getData(self):
        self.getDataBrand()


class BrandDialog(QtWidgets.QDialog, brandEdit.Ui_Dialog):

    id = 0
    editMode = False

    def __init__(self, text, inputId, edit):
        super().__init__()
        self.setupUi(self)

        self.editMode = edit
        self.id = inputId
        self.lineEdit.setText(text)
        self.buttonBox.accepted.connect(self.execQuery)

    def execQuery(self):
        conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                port="5432")
        cursor = conn.cursor()
        if self.editMode:
            query = "UPDATE car_brands SET name = '"+self.lineEdit.text()+"' WHERE id = "+self.id
        else:
            query = "INSERT INTO car_brands (name) VALUES ('"+self.lineEdit.text()+"')"
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()


class ColorDialog(QtWidgets.QDialog, colorEdit.Ui_Dialog):

    id = 0
    editMode = False

    def __init__(self, text, inputId, edit):
        super().__init__()
        self.setupUi(self)

        self.editMode = edit
        self.id = inputId
        self.lineEdit.setText(text)
        self.buttonBox.accepted.connect(self.execQuery)

    def execQuery(self):
        conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                port="5432")
        cursor = conn.cursor()
        if self.editMode:
            query = "UPDATE car_colors SET name = '"+self.lineEdit.text()+"' WHERE id = "+self.id
        else:
            query = "INSERT INTO car_colors (name) VALUES ('"+self.lineEdit.text()+"')"
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()


class TypeDialog(QtWidgets.QDialog, typeEdit.Ui_Dialog):

    id = 0
    editMode = False

    def __init__(self, text, inputId, edit):
        super().__init__()
        self.setupUi(self)

        self.editMode = edit
        self.id = inputId
        self.lineEdit.setText(text)
        self.buttonBox.accepted.connect(self.execQuery)

    def execQuery(self):
        conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                port="5432")
        cursor = conn.cursor()
        if self.editMode:
            query = "UPDATE car_types SET name = '"+self.lineEdit.text()+"' WHERE id = "+self.id
        else:
            query = "INSERT INTO car_types (name) VALUES ('"+self.lineEdit.text()+"')"
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()


class ModelDialog(QtWidgets.QDialog, modelEdit.Ui_Dialog):

    id = 0
    type = 0
    brand = 0
    editMode = False

    def __init__(self, text, inputId, edit, inputType, inputBrand):
        super().__init__()
        self.setupUi(self)

        self.editMode = edit
        self.id = inputId
        self.type = inputType
        self.brand = inputBrand
        self.lineEdit.setText(text)

        conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                port="5432")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM car_types ORDER BY id ASC ')
        i = 0
        target = -1
        for row in cursor:
            self.comboBox.addItem(str(row[1]))
            if str(row[0]) == self.id:
                target = i
            i += 1
        self.comboBox.setCurrentIndex(target)
        cursor.execute('SELECT * FROM car_brands ORDER BY id ASC ')
        i = 0
        target = -1
        for row in cursor:
            self.comboBox_2.addItem(str(row[1]))
            if str(row[0]) == self.id:
                target = i
            i += 1
        self.comboBox_2.setCurrentIndex(target)
        cursor.close()
        conn.close()
        self.buttonBox.accepted.connect(self.execQuery)
        self.comboBox.activated[str].connect(self.onComboActivated)
        self.comboBox_2.activated[str].connect(self.onCombo2Activated)


    def onComboActivated(self, text):
        conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                port="5432")
        cursor = conn.cursor()
        query= "SELECT id FROM car_types WHERE name = '" + text + "'"
        cursor.execute(query)
        resultString = cursor.fetchone()
        self.type = int(resultString[0])
        cursor.close()
        conn.close()

    def onCombo2Activated(self, text):
        conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                port="5432")
        cursor = conn.cursor()
        query = "SELECT id FROM car_brands WHERE name = '" + text + "'"
        cursor.execute(query)
        resultString = cursor.fetchone()
        self.brand = int(resultString[0])
        cursor.close()
        conn.close()

    def execQuery(self):
        conn = psycopg2.connect(dbname='cvpsu', user='postgres', password='GalaxyNote101', host='localhost',
                                port="5432")
        cursor = conn.cursor()
        query = ""
        if self.editMode:
            query = "UPDATE car_models SET model = '" + self.lineEdit.text() + "', brand = " + str(self.brand) + ", type = " + str(self.type) + " WHERE id = " + str(self.id)
        else:
            query = "INSERT INTO car_models (model,brand,type) VALUES ('"+self.lineEdit.text()+"'," + str(self.brand) + "," + str(self.type) + ")"
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ASCRA()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()