#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from view_eventBridge import EventBridge
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
        input_layout.addWidget(QLabel("판례번호"))
        input_layout.addWidget(self.txt_input)

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
            lambda: self.handler.input_handler(self.txt_input)
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

