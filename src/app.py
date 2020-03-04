import sys
from PyQt5.QtWidgets import QApplication
from view import MyWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())