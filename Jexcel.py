import sys
import pandas as pd

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QComboBox,
    QLabel,
    QHBoxLayout,
    QAbstractItemView,
    QMenu
)

from PySide6.QtCore import Qt


class ExcelEditor(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Excel Editor")
        self.resize(1300, 750)

        self.file_path = None
        self.df = pd.DataFrame()

        # 테이블 로딩 중 이벤트 방지
        self.loading_table = False

        self.init_ui()

    def init_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()

        # 상단 버튼
        top_layout = QHBoxLayout()

        self.open_btn = QPushButton("엑셀 열기")
        self.open_btn.clicked.connect(self.open_excel)

        self.save_btn = QPushButton("저장")
        self.save_btn.clicked.connect(self.save_excel)

        self.add_row_btn = QPushButton("행 추가")
        self.add_row_btn.clicked.connect(
            lambda: self.insert_row(
                self.table.currentRow()
            )
        )

        self.delete_row_btn = QPushButton("행 삭제")
        self.delete_row_btn.clicked.connect(
            self.delete_selected_row
        )

        self.sheet_combo = QComboBox()
        self.sheet_combo.currentIndexChanged.connect(
            self.change_sheet
        )

        top_layout.addWidget(self.open_btn)
        top_layout.addWidget(self.save_btn)
        top_layout.addWidget(self.add_row_btn)
        top_layout.addWidget(self.delete_row_btn)
        top_layout.addWidget(QLabel("시트"))
        top_layout.addWidget(self.sheet_combo)

        main_layout.addLayout(top_layout)

        # 테이블
        self.table = QTableWidget()

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.itemChanged.connect(
            self.cell_changed
        )

        # 우클릭 메뉴
        self.table.setContextMenuPolicy(
            Qt.CustomContextMenu
        )

        self.table.customContextMenuRequested.connect(
            self.show_context_menu
        )

        main_layout.addWidget(self.table)

        central.setLayout(main_layout)

    # 엑셀 열기
    def open_excel(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "엑셀 파일 선택",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if not file_path:
            return

        self.file_path = file_path

        try:

            excel = pd.ExcelFile(file_path)

            self.sheet_combo.blockSignals(True)

            self.sheet_combo.clear()
            self.sheet_combo.addItems(
                excel.sheet_names
            )

            self.sheet_combo.blockSignals(False)

            self.load_sheet(
                excel.sheet_names[0]
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "오류",
                str(e)
            )

    # 시트 로드
    def load_sheet(self, sheet_name):

        try:

            self.loading_table = True

            self.df = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
                dtype=object
            )

            self.table.clear()

            rows = len(self.df.index)
            cols = len(self.df.columns)

            self.table.setRowCount(rows)
            self.table.setColumnCount(cols)

            self.table.setHorizontalHeaderLabels(
                [str(col) for col in self.df.columns]
            )

            for row in range(rows):
                for col in range(cols):

                    value = self.df.iat[row, col]

                    if pd.isna(value):
                        text = ""
                    else:
                        text = str(value)

                    item = QTableWidgetItem(text)

                    item.setFlags(
                        item.flags() |
                        Qt.ItemIsEditable
                    )

                    self.table.setItem(
                        row,
                        col,
                        item
                    )

            self.table.resizeColumnsToContents()

            self.loading_table = False

        except Exception as e:
            QMessageBox.critical(
                self,
                "오류",
                str(e)
            )

    # 시트 변경
    def change_sheet(self):

        sheet_name = self.sheet_combo.currentText()

        if sheet_name:
            self.load_sheet(sheet_name)

    # 셀 수정
    def cell_changed(self, item):

        if self.loading_table:
            return

        row = item.row()
        col = item.column()

        text = item.text()

        if text == "":
            self.df.iat[row, col] = None
            return

        converted = self.convert_value(text)

        self.df.iat[row, col] = converted

    # 문자열 자동 타입 변환
    def convert_value(self, value):

        try:

            # int
            if value.isdigit():
                return int(value)

            # float
            return float(value)

        except:
            return value

    # 행 삽입
    def insert_row(self, row):

        if row < 0:
            row = self.table.rowCount()

        cols = len(self.df.columns)

        upper = self.df.iloc[:row]
        lower = self.df.iloc[row:]

        empty = pd.DataFrame(
            [[None] * cols],
            columns=self.df.columns
        )

        self.df = pd.concat(
            [upper, empty, lower],
            ignore_index=True
        )

        self.table.insertRow(row)

        for col in range(cols):

            item = QTableWidgetItem("")

            item.setFlags(
                item.flags() |
                Qt.ItemIsEditable
            )

            self.table.setItem(
                row,
                col,
                item
            )

    # 행 삭제
    def delete_selected_row(self, row=None):

        if row is None:
            row = self.table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "선택 필요",
                "삭제할 행 선택"
            )

            return

        self.table.removeRow(row)

        self.df = self.df.drop(
            self.df.index[row]
        ).reset_index(drop=True)

    # 우클릭 메뉴
    def show_context_menu(self, position):

        menu = QMenu()

        add_action = menu.addAction(
            "행 추가"
        )

        delete_action = menu.addAction(
            "행 삭제"
        )

        action = menu.exec(
            self.table.viewport().mapToGlobal(
                position
            )
        )

        row = self.table.currentRow()

        if action == add_action:
            self.insert_row(row)

        elif action == delete_action:
            self.delete_selected_row(row)

    # 저장
    def save_excel(self):

        if self.df.empty:
            return

        try:

            sheet_name = self.sheet_combo.currentText()

            with pd.ExcelWriter(
                self.file_path,
                engine="openpyxl",
                mode="a",
                if_sheet_exists="replace"
            ) as writer:

                self.df.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=False
                )

            QMessageBox.information(
                self,
                "완료",
                "저장 완료"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "저장 오류",
                str(e)
            )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # 다크모드 스타일
    app.setStyleSheet("""

    QWidget {
        background-color: #1e1e1e;
        color: white;
        font-size: 13px;
    }

    QPushButton {
        background-color: #333333;
        border: 1px solid #555;
        padding: 6px;
    }

    QPushButton:hover {
        background-color: #444444;
    }

    QTableWidget {
        background-color: #252526;
        gridline-color: #444;
    }

    QHeaderView::section {
        background-color: #333333;
        padding: 5px;
        border: 1px solid #444;
    }

    """)

    window = ExcelEditor()
    window.show()

    sys.exit(app.exec())