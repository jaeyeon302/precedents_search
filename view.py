#-*- coding:utf-8 -*-
import sys
from core import get_pan, save_pans
from PyQt5.QtWidgets import *

class EventBridge():
    def __init__(self,
                pannum_view, 
                pansi_view, yozi_view, jomun_view):
        self._pn_view = pannum_view
        self._p_view = pansi_view
        self._y_view = yozi_view
        self._j_view = jomun_view
        self._pans_idx = 0
        self._pans = []

    @property
    def pannum(self):
        return self._pn_view.text()
    
    @pannum.setter
    def pannum(self, val):
        self._pn_view.setText(val)
    
    @property
    def pansi(self):
        return self._p_view.toPlainText()

    @pansi.setter
    def pansi(self, val):
        self._p_view.setText(val)

    @property
    def yozi(self):
        return self._y_view.toPlainText()
    
    @yozi.setter
    def yozi(self, val):
        self._y_view.setText(val)

    @property
    def jomun(self):
        return self._j_view.toPlainText()
    
    @jomun.setter
    def jomun(self, val):
        return self._j_view.setText(val)
    
    def _update_view(self, pan):
        self.pansi = pan.pansi
        self.yozi = pan.yozi
        self.jomun = pan.jomun
        self.pannum = "{} ({}/{})".format(pan.num, self._pans_idx+1, len(self._pans))

    def input_handler(self, txt_input, progress_bar):
        txt = txt_input.toPlainText()
        if txt[-1] == '\n':
            nums = txt.split(',')
            nums = [n.lstrip().rstrip() for n in nums]
            if len(nums) == 0:
                self.pansi = ""
                self.yozi = ""
                self.jomun = ""
            count = 0
            progress_bar.setValue(count)
            unit = progress_bar.maximum()/len(nums)
            self._pans = []
            for num in nums:
                self._pans.append(get_pan(num))
                count += unit
                progress_bar.setValue(count)
            self._pans = [get_pan(num) for num in nums]
            self._update_view(self._pans[0])
            txt_input.setPlainText(txt.lstrip().rstrip())

    def prev_btn_handler(self):
        if self._pans_idx > 0:
            self._pans_idx -= 1
            self._update_view(self._pans[self._pans_idx])

    def next_btn_handler(self):
        if len(self._pans) > self._pans_idx + 1:
            self._pans_idx += 1
            self._update_view(self._pans[self._pans_idx])
    
    def save_btn_handler(self, pansi_check, yozi_check, jomun_check):
        nums = [p.num for p in self._pans]
        ofilename = "./{}".format(nums)
        if pansi_check: ofilename += "_판시사항"
        if yozi_check: ofilename += "_판결요지"
        if jomun_check: ofilename += "_참조조문"
        ofilename += ".docx"
        save_pans(self._pans, ofilename, pansi_check, yozi_check, jomun_check)
        alert = QMessageBox()
        alert.setText("{} 저장되었습니다".format(ofilename))
        alert.exec_()  

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.handler = EventBridge(
            self.pannum_view,
            self.pansi_view, self.yozi_view, self.jomun_view
        )
        self.register_handler()
    
    def setup_ui(self):
        base_layout = QHBoxLayout()

        lv_layout = QVBoxLayout()
        rv_layout = QVBoxLayout()

        result_layout = QVBoxLayout()
        self.pannum_view = QLabel("판례번호")
        self.pansi_view = QTextBrowser()
        self.yozi_view = QTextBrowser()
        self.jomun_view = QTextBrowser()
        result_layout.addWidget(self.pannum_view)
        result_layout.addWidget(QLabel("판시사항"))
        result_layout.addWidget(self.pansi_view)
        result_layout.addWidget(QLabel("판결요지"))
        result_layout.addWidget(self.yozi_view)
        result_layout.addWidget(QLabel("참조조문"))
        result_layout.addWidget(self.jomun_view)
        
        control_layout = QHBoxLayout()
        self.prev_btn = QPushButton("이전")
        self.next_btn = QPushButton("다음")
        control_layout.addWidget(self.prev_btn)
        control_layout.addWidget(self.next_btn)

        lv_layout.addLayout(result_layout)
        lv_layout.addLayout(control_layout)

        input_layout = QVBoxLayout()
        self.txt_input = QPlainTextEdit()
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        input_layout.addWidget(QLabel("판례번호"))
        input_layout.addWidget(self.txt_input)
        input_layout.addWidget(self.progress_bar)

        export_layout = QVBoxLayout()
        self.pansi_check = QCheckBox("판시사항")
        self.yozi_check = QCheckBox("판결요지")
        self.jomun_check = QCheckBox("참조조문")
        self.save_btn = QPushButton("저장")
        export_layout.addWidget(QLabel("내보내기"))
        export_layout.addWidget(self.pansi_check)
        export_layout.addWidget(self.yozi_check)
        export_layout.addWidget(self.jomun_check)
        export_layout.addWidget(self.save_btn)

        rv_layout.addLayout(input_layout)
        rv_layout.addLayout(export_layout)

        base_layout.addLayout(lv_layout)
        base_layout.addLayout(rv_layout)
        self.setLayout(base_layout)

    def register_handler(self):
        self.txt_input.textChanged.connect(
            lambda: self.handler.input_handler(self.txt_input, self.progress_bar)
        )
        self.prev_btn.clicked.connect(
            self.handler.prev_btn_handler
        )
        self.next_btn.clicked.connect(
            self.handler.next_btn_handler
        )
        self.save_btn.clicked.connect(
            lambda: self.handler.save_btn_handler(
                self.pansi_check.isChecked(),
                self.yozi_check.isChecked(),
                self.jomun_check.isChecked()
            )
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())
