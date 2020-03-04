from PyQt5.QtWidgets import QMessageBox
from core import get_pan, save_pans
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
        self._j_view.setText(val)
    
    def _update_view(self, pan):
        self.pansi = pan.pansi
        self.yozi = pan.yozi
        self.jomun = pan.jomun
        self.pannum = "{} ({}/{})".format(pan.num, self._pans_idx+1, len(self._pans))

    def input_handler(self, txt_input):
        txt = txt_input.toPlainText()
        if txt[-1] == '\n':
            nums = txt.split(',')
            nums = [n.lstrip().rstrip() for n in nums]
            if len(nums) == 0:
                self.pansi = ""
                self.yozi = ""
                self.jomun = ""
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
