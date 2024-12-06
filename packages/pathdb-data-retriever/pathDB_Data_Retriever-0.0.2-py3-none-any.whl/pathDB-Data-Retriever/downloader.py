import sys
from PyQt5.QtWidgets import QApplication
from pathDB_Data_Retriever.gui import PathologyDownloadManager  # Import from your new package

def main():
    app = QApplication(sys.argv)
    ex = PathologyDownloadManager()
    ex.show()
    sys.exit(app.exec_())
