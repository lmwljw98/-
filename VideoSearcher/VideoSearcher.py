import requests
import json
import webbrowser
import sys
from PyQt5.QtWidgets import *

mediaCode_list = []
mediaFre_list = []
base_url = "http://cjpiporigin.myskcdn.com/VOD/"


class myGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.kwd = QLineEdit()
        self.result = QListWidget()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setSizeConstraint(QLayout.SetFixedSize)

        search = QPushButton("Search")

        search.clicked.connect(self.searchMediaCode)
        self.result.doubleClicked.connect(self.searchProgramCode)

        grid.addWidget(self.kwd, 1, 1)
        grid.addWidget(self.result, 2, 1, 6, 6)
        grid.addWidget(search, 1, 6)

        self.setLayout(grid)
        self.setWindowTitle("TVing Video Searcher")
        self.show()

    def searchMediaCode(self):
        try:
            keyword = self.kwd.text()
            self.result.clear()
            mediaCode_list.clear()
            mediaFre_list.clear()
            params = {'kwd': keyword, 'pageSize': 1000}
            mediaCode_request = requests.get('http://search.tving.com:8080/search/getFind.jsp', params=params)
            mediaCode = json.loads(mediaCode_request.text)

            for i in range(len(mediaCode['vodBCRsb']['dataList'])):
                self.result.addItem(
                    mediaCode['vodBCRsb']['dataList'][i]['mast_nm'].replace("#@$", "").replace("$#@", "") + " "
                    + mediaCode['vodBCRsb']['dataList'][i]['frequency'] + "화")
                mediaCode_list.append(mediaCode['vodBCRsb']['dataList'][i]['epi_cd'])
                mediaFre_list.append(mediaCode['vodBCRsb']['dataList'][i]['frequency'])

        except:
            errorWindow = QMessageBox.warning(self, 'Error', 'Nothing found.', QMessageBox.Ok,
                                              QMessageBox.Ok)

    def searchProgramCode(self):
        try:
            second_params = {'mediaCode': mediaCode_list[self.result.currentRow()], 'info': 'Y'}
            programCode_request = requests.get('http://api.tving.com/v1/media/stream/info', params=second_params)
            programCode = json.loads(programCode_request.text)

            realCode = programCode['body']['content']['info']['program']['enm_code']
            fre_number = mediaFre_list[self.result.currentRow()]

            final_url = base_url + realCode + "/" + realCode + "_" + fre_number + ".mp4"

            webbrowser.open(final_url)
            return final_url
        except:
            errorWindow = QMessageBox.warning(self, 'Error', 'May this program is not in TVing.', QMessageBox.Ok,
                                              QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = myGUI()
    sys.exit(app.exec_())
