import PyQt5


class CheckConnectivity(PyQt5.QtCore.QObject):
    def __init__(self, *args, **kwargs):
        PyQt5.QtCore.QObject.__init__(self, *args, **kwargs)
        url = PyQt5.QtCore.QUrl("https://www.google.com/")
        req = PyQt5.QtNetwork.QNetworkRequest(url)
        self.net_manager = PyQt5.QtNetwork.QNetworkAccessManager()
        self.res = self.net_manager.get(req)
        self.res.finished.connect(self.processRes)
        self.res.error.connect(self.processErr)
        self.msg = PyQt5.QtWidgets.QMessageBox()

    @PyQt5.QtCore.pyqtSlot()
    def processRes(self):
        if self.res.bytesAvailable():
            self.msg.information(None, "Info", "You are connected to the Internet.")
        self.res.deleteLater()

    @PyQt5.QtCore.pyqtSlot(PyQt5.QtNetwork.QNetworkReply.NetworkError)
    def processErr(self, code):
        self.msg.critical(None, "Info", "You are not connected to the Internet.")
        print(code)