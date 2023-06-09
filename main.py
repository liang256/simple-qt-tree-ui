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
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget.currentItemChanged.connect(self.highlight_current_selection)
        self.treeWidget.itemChanged.connect(self.check_child_items)

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
        item.setCheckState(0, QtCore.Qt.Unchecked)
        item.setText(0, f'Item {self.item_counter}')
        self.item_counter += 1

    def delete_item(self):
        item = self.treeWidget.currentItem()
        if item:
            (item.parent() or self.treeWidget.invisibleRootItem()).removeChild(item)

    def list_selections(self):
        selections = []
        self.traverse_tree(self.treeWidget.invisibleRootItem(), selections)
        print('Selections:', selections)

    def traverse_tree(self, item, selections):
        if item.checkState(0) == QtCore.Qt.Checked:
            selections.append(item.text(0))
        for i in range(item.childCount()):
            child = item.child(i)
            self.traverse_tree(child, selections)

    def highlight_current_selection(self, current, prev):
        self.highlight_item(prev, False)
        self.highlight_item(current, True)

    def highlight_item(self, item, highlight):
        font = item.font(0)
        if highlight:
            font.setBold(True)
        else:
            font.setBold(False)
        item.setFont(0, font)

    def check_child_items(self, item):
        if item.checkState(0) == QtCore.Qt.Checked:
            for i in range(item.childCount()):
                child = item.child(i)
                child.setCheckState(0, QtCore.Qt.Checked)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
