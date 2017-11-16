from PyQt5.QtWidgets import QApplication, QDialog
from gui import *
import sys

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = QDialog()
	ui = Ui_Dialog(app)
	ui.setupUi(window)

	window.show()
	sys.exit(app.exec_())
