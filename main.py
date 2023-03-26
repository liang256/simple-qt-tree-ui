import sys
from PySide6 import QtCore, QtGui, QtWidgets

class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent=None):
        super(TreeWidgetItem, self).__init__(parent)
        self.setExpanded(True)
        self.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        self.setCheckState(0, QtCore.Qt.Unchecked)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.setHeaderLabels(['Title'])
        self.treeWidget.setColumnWidth(0, 200)

        self.add_button = QtWidgets.QPushButton('Add')
        self.add_button.clicked.connect(self.add_item)

        self.delete_button = QtWidgets.QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete_item)

        self.list_button = QtWidgets.QPushButton('List Selections')
        self.list_button.clicked.connect(self.list_selections)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.treeWidget)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.list_button)
        main_layout.addLayout(button_layout)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.item_counter = 0

    def add_item(self):
        parent = self.treeWidget.currentItem()
        if not parent:
            parent = self.treeWidget.invisibleRootItem()
        item = TreeWidgetItem(parent)
        item.setText(0, f'Item {self.item_counter}')
        self.item_counter += 1
        self.treeWidget.setCurrentItem(item)

    def delete_item(self):
        item = self.treeWidget.currentItem()
        if item:
            (item.parent() or self.treeWidget.invisibleRootItem()).removeChild(item)

    def list_selections(self):
        selections = []
        root = self.treeWidget.invisibleRootItem()
        for i in range(root.childCount()):
            child = root.child(i)
            if child.checkState(0) == QtCore.Qt.Checked:
                selections.append(child.text(0))
        print('Selections:', selections)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
