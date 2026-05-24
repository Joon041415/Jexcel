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
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QComboBox,
    QLabel,
    QAbstractItemView,
    QMenu,
    QStatusBar,
    QFrame,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QFont, QColor, QCursor


# ──────────────────────────────────────────────
#  색상 팔레트 (홈페이지 참고)
# ──────────────────────────────────────────────
COLORS = {
    "bg":          "#0d0d0d",
    "surface":     "#141414",
    "surface2":    "#1a1a1a",
    "border":      "#2a2a2a",
    "border2":     "#333333",
    "accent":      "#00e5a0",   # 에메랄드 포인트
    "accent_dim":  "#00b37a",
    "text":        "#e8e8e8",
    "text_dim":    "#888888",
    "text_muted":  "#555555",
    "danger":      "#ff4d6d",
    "danger_dim":  "#cc2244",
    "header_bg":   "#111111",
}

STYLESHEET = f"""
/* ── 전체 기본 ── */
QWidget {{
    background-color: {COLORS['bg']};
    color: {COLORS['text']};
    font-family: 'Pretendard', 'Noto Sans KR', 'Segoe UI', sans-serif;
    font-size: 13px;
}}

/* ── 메인 윈도우 ── */
QMainWindow {{
    background-color: {COLORS['bg']};
}}

/* ── 버튼 ── */
QPushButton {{
    background-color: {COLORS['surface2']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border2']};
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 500;
    min-width: 72px;
}}
QPushButton:hover {{
    background-color: {COLORS['border2']};
    border-color: {COLORS['text_dim']};
}}
QPushButton:pressed {{
    background-color: {COLORS['border']};
}}

/* 강조 버튼 (저장) */
QPushButton#btn_save {{
    background-color: {COLORS['accent']};
    color: #000000;
    border: none;
    font-weight: 700;
}}
QPushButton#btn_save:hover {{
    background-color: {COLORS['accent_dim']};
}}

/* 위험 버튼 (삭제) */
QPushButton#btn_delete {{
    background-color: transparent;
    color: {COLORS['danger']};
    border: 1px solid {COLORS['danger_dim']};
}}
QPushButton#btn_delete:hover {{
    background-color: {COLORS['danger_dim']};
    color: white;
}}

/* ── 콤보박스 ── */
QComboBox {{
    background-color: {COLORS['surface2']};
    border: 1px solid {COLORS['border2']};
    border-radius: 4px;
    padding: 5px 10px;
    min-width: 120px;
    color: {COLORS['text']};
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS['surface2']};
    border: 1px solid {COLORS['border2']};
    selection-background-color: {COLORS['border2']};
}}

/* ── 테이블 ── */
QTableWidget {{
    background-color: {COLORS['surface']};
    gridline-color: {COLORS['border']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    selection-background-color: #1a3a2a;
    selection-color: {COLORS['accent']};
    alternate-background-color: {COLORS['surface2']};
}}
QTableWidget::item {{
    padding: 4px 8px;
    border: none;
}}
QTableWidget::item:selected {{
    background-color: #1a3a2a;
    color: {COLORS['accent']};
}}

QHeaderView::section {{
    background-color: {COLORS['header_bg']};
    color: {COLORS['text_dim']};
    padding: 6px 8px;
    border: none;
    border-right: 1px solid {COLORS['border']};
    border-bottom: 1px solid {COLORS['border']};
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}
QHeaderView::section:hover {{
    background-color: {COLORS['surface2']};
    color: {COLORS['text']};
}}

/* ── 스크롤바 ── */
QScrollBar:vertical {{
    background: {COLORS['surface']};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['border2']};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {COLORS['text_dim']};
}}
QScrollBar:horizontal {{
    background: {COLORS['surface']};
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: {COLORS['border2']};
    border-radius: 4px;
    min-width: 30px;
}}
QScrollBar::add-line, QScrollBar::sub-line {{ border: none; background: none; }}

/* ── 상태바 ── */
QStatusBar {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_dim']};
    border-top: 1px solid {COLORS['border']};
    font-size: 11px;
    padding: 2px 8px;
}}

/* ── 구분선 ── */
QFrame#separator {{
    background-color: {COLORS['border']};
    max-height: 1px;
}}

/* ── 컨텍스트 메뉴 ── */
QMenu {{
    background-color: {COLORS['surface2']};
    border: 1px solid {COLORS['border2']};
    border-radius: 6px;
    padding: 4px;
}}
QMenu::item {{
    padding: 6px 20px;
    border-radius: 3px;
}}
QMenu::item:selected {{
    background-color: {COLORS['border2']};
    color: {COLORS['accent']};
}}
QMenu::separator {{
    height: 1px;
    background-color: {COLORS['border']};
    margin: 4px 8px;
}}

/* ── 레이블 ── */
QLabel#lbl_sheet {{
    color: {COLORS['text_dim']};
    font-size: 11px;
}}
"""


class FooterBar(QWidget):
    """홈페이지 스타일 푸터"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(52)
        self.setObjectName("footer")
        self.setStyleSheet(f"""
            QWidget#footer {{
                background-color: {COLORS['surface']};
                border-top: 1px solid {COLORS['border']};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        # 왼쪽: 브랜드
        brand = QLabel("JOON · Excel Editor")
        brand.setStyleSheet(f"""
            color: {COLORS['text_dim']};
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 1.5px;
        """)

        # 가운데 여백
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # 오른쪽: 이메일 링크
        email_label = QLabel(
            '<a href="mailto:lotus031315@gmail.com" '
            'style="color: #00e5a0; text-decoration: none; '
            'font-size: 12px; font-weight: 500;">'
            '✉&nbsp;&nbsp;lotus031315@gmail.com</a>'
        )
        email_label.setOpenExternalLinks(True)
        email_label.setTextInteractionFlags(
            Qt.TextBrowserInteraction
        )
        email_label.setCursor(QCursor(Qt.PointingHandCursor))

        # 구분점
        dot = QLabel("·")
        dot.setStyleSheet(f"color: {COLORS['text_muted']}; margin: 0 10px;")

        # 홈페이지 링크
        web_label = QLabel(
            '<a href="https://joon041415.github.io/" '
            'style="color: #888888; text-decoration: none; '
            'font-size: 12px;">'
            'Portfolio ↗</a>'
        )
        web_label.setOpenExternalLinks(True)
        web_label.setTextInteractionFlags(
            Qt.TextBrowserInteraction
        )
        web_label.setCursor(QCursor(Qt.PointingHandCursor))

        layout.addWidget(brand)
        layout.addWidget(spacer)
        layout.addWidget(email_label)
        layout.addWidget(dot)
        layout.addWidget(web_label)


class ExcelEditor(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Editor")
        self.resize(1300, 780)

        self.file_path = None
        self.df = pd.DataFrame()
        self.loading_table = False

        self.init_ui()
        self.update_status()

    # ── UI 구성 ──────────────────────────────

    def init_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── 툴바 ──
        toolbar = QWidget()
        toolbar.setFixedHeight(52)
        toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['surface']};
                border-bottom: 1px solid {COLORS['border']};
            }}
        """)
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(12, 0, 12, 0)
        tb_layout.setSpacing(8)

        # 앱 타이틀
        title = QLabel("Excel Editor")
        title.setStyleSheet(f"""
            color: {COLORS['accent']};
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 0.5px;
            padding-right: 16px;
        """)

        self.open_btn = QPushButton("📂  열기")
        self.open_btn.clicked.connect(self.open_excel)

        self.new_btn = QPushButton("＋  새 파일")
        self.new_btn.clicked.connect(self.new_file)

        self.save_btn = QPushButton("💾  저장")
        self.save_btn.setObjectName("btn_save")
        self.save_btn.clicked.connect(self.save_excel)

        self.save_as_btn = QPushButton("다른 이름으로")
        self.save_as_btn.clicked.connect(self.save_as_excel)

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.VLine)
        sep1.setStyleSheet(f"background:{COLORS['border2']}; max-width:1px; margin: 10px 4px;")

        self.add_row_btn = QPushButton("＋ 행")
        self.add_row_btn.clicked.connect(
            lambda: self.insert_row(self.table.currentRow())
        )

        self.delete_row_btn = QPushButton("－ 행")
        self.delete_row_btn.setObjectName("btn_delete")
        self.delete_row_btn.clicked.connect(self.delete_selected_rows)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.VLine)
        sep2.setStyleSheet(f"background:{COLORS['border2']}; max-width:1px; margin: 10px 4px;")

        lbl_sheet = QLabel("시트")
        lbl_sheet.setObjectName("lbl_sheet")

        self.sheet_combo = QComboBox()
        self.sheet_combo.currentIndexChanged.connect(self.change_sheet)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        for w in [title, self.open_btn, self.new_btn, self.save_btn,
                  self.save_as_btn, sep1,
                  self.add_row_btn, self.delete_row_btn, sep2,
                  lbl_sheet, self.sheet_combo, spacer]:
            tb_layout.addWidget(w)

        # ── 테이블 영역 ──
        table_container = QWidget()
        table_container.setStyleSheet(f"background:{COLORS['bg']};")
        tc_layout = QVBoxLayout(table_container)
        tc_layout.setContentsMargins(12, 10, 12, 10)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.verticalHeader().setDefaultSectionSize(28)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.itemChanged.connect(self.cell_changed)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

        # 더블클릭으로 열 너비 자동 조정
        self.table.horizontalHeader().sectionDoubleClicked.connect(
            self.table.resizeColumnToContents
        )

        tc_layout.addWidget(self.table)

        # ── 상태바 ──
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # ── 푸터 ──
        footer = FooterBar()

        root_layout.addWidget(toolbar)
        root_layout.addWidget(table_container)
        root_layout.addWidget(footer)

    # ── 파일 작업 ─────────────────────────────

    def open_excel(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "엑셀 파일 선택", "",
            "Excel Files (*.xlsx *.xls)"
        )
        if not path:
            return
        self.file_path = path
        try:
            excel = pd.ExcelFile(path)
            self.sheet_combo.blockSignals(True)
            self.sheet_combo.clear()
            self.sheet_combo.addItems(excel.sheet_names)
            self.sheet_combo.blockSignals(False)
            self.load_sheet(excel.sheet_names[0])
            self.setWindowTitle(f"Excel Editor — {path.split('/')[-1].split(chr(92))[-1]}")
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))

    def new_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "새 파일 저장 위치", "새파일.xlsx",
            "Excel Files (*.xlsx)"
        )
        if not path:
            return
        self.file_path = path
        self.df = pd.DataFrame(columns=["A", "B", "C"])
        empty_wb = pd.ExcelWriter(path, engine="openpyxl")
        self.df.to_excel(empty_wb, sheet_name="Sheet1", index=False)
        empty_wb.close()
        self.sheet_combo.blockSignals(True)
        self.sheet_combo.clear()
        self.sheet_combo.addItems(["Sheet1"])
        self.sheet_combo.blockSignals(False)
        self.load_sheet("Sheet1")
        self.setWindowTitle(f"Excel Editor — {path.split('/')[-1]}")

    # ── 시트 ──────────────────────────────────

    def load_sheet(self, sheet_name):
        try:
            self.loading_table = True
            self.df = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
                dtype=object
            )
            self.table.clear()
            rows, cols = len(self.df.index), len(self.df.columns)
            self.table.setRowCount(rows)
            self.table.setColumnCount(cols)
            self.table.setHorizontalHeaderLabels(
                [str(c) for c in self.df.columns]
            )
            for r in range(rows):
                for c in range(cols):
                    val = self.df.iat[r, c]
                    text = "" if pd.isna(val) else str(val)
                    item = QTableWidgetItem(text)
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    self.table.setItem(r, c, item)
            self.table.resizeColumnsToContents()
            self.loading_table = False
            self.update_status()
        except Exception as e:
            self.loading_table = False
            QMessageBox.critical(self, "오류", str(e))

    def change_sheet(self):
        name = self.sheet_combo.currentText()
        if name:
            self.load_sheet(name)

    # ── 셀 편집 ───────────────────────────────

    def cell_changed(self, item):
        if self.loading_table:
            return
        r, c, text = item.row(), item.column(), item.text()
        self.df.iat[r, c] = None if text == "" else self.convert_value(text)
        self.update_status()

    def convert_value(self, value):
        try:
            if value.isdigit():
                return int(value)
            return float(value)
        except Exception:
            return value

    # ── 행 조작 ───────────────────────────────

    def insert_row(self, row):
        if row < 0:
            row = self.table.rowCount()
        cols = len(self.df.columns)
        upper, lower = self.df.iloc[:row], self.df.iloc[row:]
        empty = pd.DataFrame([[None] * cols], columns=self.df.columns)
        self.df = pd.concat([upper, empty, lower], ignore_index=True)
        self.table.insertRow(row)
        for c in range(cols):
            item = QTableWidgetItem("")
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.table.setItem(row, c, item)
        self.update_status()

    def delete_selected_rows(self):
        """다중 행 삭제 지원"""
        rows = sorted(
            set(idx.row() for idx in self.table.selectedIndexes()),
            reverse=True
        )
        if not rows:
            QMessageBox.warning(self, "선택 필요", "삭제할 행을 선택하세요.")
            return
        confirm = QMessageBox.question(
            self, "행 삭제",
            f"{len(rows)}개 행을 삭제할까요?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return
        for r in rows:
            self.table.removeRow(r)
            self.df = self.df.drop(self.df.index[r]).reset_index(drop=True)
        self.update_status()

    # ── 컨텍스트 메뉴 ─────────────────────────

    def show_context_menu(self, position):
        menu = QMenu()
        add_above = menu.addAction("⬆  위에 행 추가")
        add_below = menu.addAction("⬇  아래에 행 추가")
        menu.addSeparator()
        del_action = menu.addAction("🗑  행 삭제")

        action = menu.exec(self.table.viewport().mapToGlobal(position))
        row = self.table.currentRow()

        if action == add_above:
            self.insert_row(row)
        elif action == add_below:
            self.insert_row(row + 1)
        elif action == del_action:
            self.delete_selected_rows()

    # ── 저장 ──────────────────────────────────

    def save_excel(self):
        if self.df.empty and self.file_path is None:
            return
        if self.file_path is None:
            self.save_as_excel()
            return
        self._write_excel(self.file_path)

    def save_as_excel(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "다른 이름으로 저장", "",
            "Excel Files (*.xlsx)"
        )
        if not path:
            return
        self.file_path = path
        self._write_excel(path)
        self.setWindowTitle(f"Excel Editor — {path.split('/')[-1]}")

    def _write_excel(self, path):
        try:
            sheet_name = self.sheet_combo.currentText() or "Sheet1"
            with pd.ExcelWriter(
                path, engine="openpyxl", mode="a",
                if_sheet_exists="replace"
            ) as writer:
                self.df.to_excel(writer, sheet_name=sheet_name, index=False)
            self.status_bar.showMessage("✓  저장 완료", 3000)
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", str(e))

    # ── 상태바 ────────────────────────────────

    def update_status(self):
        rows = len(self.df.index) if not self.df.empty else 0
        cols = len(self.df.columns) if not self.df.empty else 0
        file_name = (
            self.file_path.split("/")[-1].split("\\")[-1]
            if self.file_path else "파일 없음"
        )
        self.status_bar.showMessage(
            f"  {file_name}   │   {rows}행 × {cols}열"
        )


# ──────────────────────────────────────────────
#  엔트리포인트
# ──────────────────────────────────────────────

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = ExcelEditor()
    window.show()
    sys.exit(app.exec())
