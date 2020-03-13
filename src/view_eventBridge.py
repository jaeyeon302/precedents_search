import os
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit
from core import get_pan, save_pans


class EventBridge():
    def __init__(self, view_instance):
        self.view = view_instance
        self._pn_view = view_instance.pannum_view
        self._p_view = view_instance.pansi_view
        self._y_view = view_instance.yozi_view
        self._j_view = view_instance.jomun_view
        self._r_view = view_instance.refpan_view
        self._a_view = view_instance.allcon_view
        self._pans_idx = 0
        self._pans = []

    @property
    def pannum(self):
        return self.view.pannum_view.text()

    @pannum.setter
    def pannum(self, val):
        self.view.pannum_view.setText(val)

    @property
    def pansi(self):
        return self.view.pansi_view.toPlainText()

    @pansi.setter
    def pansi(self, val):
        self.view.pansi_view.setText(val)

    @property
    def yozi(self):
        return self.view.yozi_view.toPlainText()

    @yozi.setter
    def yozi(self, val):
        self.view.yozi_view.setText(val)

    @property
    def jomun(self):
        return self.view.jomun_view.toPlainText()

    @jomun.setter
    def jomun(self, val):
        self.view.jomun_view.setText(val)

    @property
    def refpan(self):
        self.view.refpan_view.toPlainText()

    @refpan.setter
    def refpan(self, val):
        self.view.refpan_view.setText(val)

    @property
    def allcon(self):
        self.view.allcon_view.toPlainText()

    @allcon.setter
    def allcon(self, val):
        self.view.allcon_view.setText(val)

    def _update_view(self, pan):
        self.pansi = pan.pansi
        self.yozi = pan.yozi
        self.jomun = pan.jomun
        self.refpan = pan.refpan
        self.allcon = pan.allcon
        self.pannum = "{} ({}/{})".format(pan.num,
                                          self._pans_idx+1, len(self._pans))

    def input_handler(self):
        txt = self.view.txt_input.toPlainText()
        if txt[-1] == '\n':
            nums = txt.split(',')
            nums = [n.lstrip().rstrip() for n in nums]
            if len(nums) == 0:
                self.pansi = ""
                self.yozi = ""
                self.jomun = ""
            self._pans = [get_pan(num) for num in nums]
            self._update_view(self._pans[0])
            self.view.txt_input.setPlainText(txt.lstrip().rstrip())

    def prev_btn_handler(self):
        if self._pans_idx > 0:
            self._pans_idx -= 1
            self._update_view(self._pans[self._pans_idx])

    def next_btn_handler(self):
        if len(self._pans) > self._pans_idx + 1:
            self._pans_idx += 1
            self._update_view(self._pans[self._pans_idx])

    def save_btn_handler(self):
        nums = [p.num for p in self._pans]
        pansi_check = self.view.pansi_check.isChecked()
        yozi_check = self.view.yozi_check.isChecked()
        jomun_check = self.view.jomun_check.isChecked()
        refpan_check = self.view.refpan_check.isChecked()
        allcon_check = self.view.allcon_check.isChecked()
        text, okPressed = QInputDialog.getText(
            self.view, "내보내기", "파일 이름 : ", QLineEdit.Normal, "")
        if okPressed and text != "":
            ofilename = "./{}".format(text)
            if pansi_check:
                ofilename += "_판시사항"
            if yozi_check:
                ofilename += "_판결요지"
            if jomun_check:
                ofilename += "_참조조문"
            if refpan_check:
                ofilename += "_참조판례"
            if allcon_check:
                ofilename += "_전문"
            ofilename += ".docx"
            save_pans(self._pans, ofilename, pansi_check, yozi_check,
                      jomun_check, refpan_check, allcon_check)
            alert = QMessageBox()
            ofilename = os.path.abspath(ofilename)
            alert.setText("{} 저장되었습니다".format(ofilename))
            alert.exec_()
