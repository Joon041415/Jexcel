import sys
import pandas as pd

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QTableWidget,
    QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QComboBox, QLabel,
    QAbstractItemView, QMenu, QStatusBar, QFrame,
    QSizePolicy, QDialog, QLineEdit, QDialogButtonBox,
    QToolButton, QScrollArea,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor, QKeySequence, QShortcut, QColor, QBrush

# ─────────────────────────────────────────
#  팔레트
# ─────────────────────────────────────────
C = {
    "bg":         "#0d0d0d",
    "surface":    "#141414",
    "surface2":   "#1a1a1a",
    "border":     "#2a2a2a",
    "border2":    "#333333",
    "accent":     "#00e5a0",
    "accent_dim": "#00b37a",
    "accent_bg":  "#0d2e22",   # 선택 음영 배경
    "accent_bg2": "#0a2019",   # 교대행 선택 음영
    "text":       "#e8e8e8",
    "text_dim":   "#888888",
    "text_muted": "#555555",
    "danger":     "#ff4d6d",
    "danger_dim": "#cc2244",
    "header_bg":  "#111111",
    "fn_bg":      "#101a15",   # 함수 패널 배경
}

STYLESHEET = f"""
QWidget {{
    background-color: {C['bg']};
    color: {C['text']};
    font-family: 'Pretendard', 'Noto Sans KR', 'Segoe UI', sans-serif;
    font-size: 13px;
}}
QMainWindow {{ background-color: {C['bg']}; }}

/* ── 버튼 기본 ── */
QPushButton {{
    background-color: {C['surface2']};
    color: {C['text']};
    border: 1px solid {C['border2']};
    border-radius: 4px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
    min-width: 64px;
}}
QPushButton:hover  {{ background-color: {C['border2']}; border-color: {C['text_dim']}; }}
QPushButton:pressed {{ background-color: {C['border']}; }}

QPushButton#btn_save {{
    background-color: {C['accent']}; color: #000;
    border: none; font-weight: 700;
}}
QPushButton#btn_save:hover {{ background-color: {C['accent_dim']}; }}

QPushButton#btn_delete {{
    background-color: transparent;
    color: {C['danger']};
    border: 1px solid {C['danger_dim']};
}}
QPushButton#btn_delete:hover {{ background-color: {C['danger_dim']}; color: white; }}

/* ── 함수 패널 버튼 ── */
QPushButton#fn_btn {{
    background-color: {C['fn_bg']};
    color: {C['accent']};
    border: 1px solid #1a3a2a;
    border-radius: 3px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 600;
    min-width: 50px;
    font-family: 'Consolas', 'Courier New', monospace;
}}
QPushButton#fn_btn:hover {{
    background-color: #0f2d20;
    border-color: {C['accent_dim']};
}}

/* ── 콤보박스 ── */
QComboBox {{
    background-color: {C['surface2']};
    border: 1px solid {C['border2']};
    border-radius: 4px;
    padding: 5px 10px;
    min-width: 110px;
    color: {C['text']};
}}
QComboBox::drop-down {{ border: none; width: 18px; }}
QComboBox QAbstractItemView {{
    background-color: {C['surface2']};
    border: 1px solid {C['border2']};
    selection-background-color: {C['border2']};
}}

/* ── 테이블 ── */
QTableWidget {{
    background-color: {C['surface']};
    gridline-color: {C['border']};
    border: 1px solid {C['border']};
    border-radius: 4px;
    alternate-background-color: {C['surface2']};
    selection-background-color: {C['accent_bg']};
    selection-color: {C['accent']};
}}
QTableWidget::item {{ padding: 3px 8px; border: none; }}
QTableWidget::item:selected {{
    background-color: {C['accent_bg']};
    color: {C['accent']};
    border-left: 2px solid {C['accent']};
}}
QTableWidget::item:alternate:selected {{
    background-color: {C['accent_bg2']};
}}

QHeaderView::section {{
    background-color: {C['header_bg']};
    color: {C['text_dim']};
    padding: 6px 8px;
    border: none;
    border-right: 1px solid {C['border']};
    border-bottom: 1px solid {C['border']};
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.5px;
}}
QHeaderView::section:hover {{
    background-color: {C['surface2']};
    color: {C['text']};
}}

/* ── 스크롤바 ── */
QScrollBar:vertical   {{ background:{C['surface']}; width:7px; border-radius:4px; }}
QScrollBar:horizontal {{ background:{C['surface']}; height:7px; border-radius:4px; }}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
    background:{C['border2']}; border-radius:4px; min-height:24px; min-width:24px;
}}
QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {{
    background:{C['text_dim']};
}}
QScrollBar::add-line, QScrollBar::sub-line {{ border:none; background:none; }}

/* ── 찾기 입력창 ── */
QLineEdit {{
    background-color: {C['surface2']};
    border: 1px solid {C['border2']};
    border-radius: 4px;
    padding: 5px 8px;
    color: {C['text']};
}}
QLineEdit:focus {{ border-color: {C['accent']}; }}

/* ── 다이얼로그 ── */
QDialog {{
    background-color: {C['surface']};
}}
QDialogButtonBox QPushButton {{
    min-width: 60px;
}}

/* ── 상태바 ── */
QStatusBar {{
    background-color: {C['surface']};
    color: {C['text_dim']};
    border-top: 1px solid {C['border']};
    font-size: 11px; padding: 2px 8px;
}}

/* ── 컨텍스트 메뉴 ── */
QMenu {{
    background-color: {C['surface2']};
    border: 1px solid {C['border2']};
    border-radius: 6px; padding: 4px;
}}
QMenu::item {{ padding: 6px 20px; border-radius: 3px; }}
QMenu::item:selected {{ background-color: {C['border2']}; color: {C['accent']}; }}
QMenu::separator {{ height:1px; background:{C['border']}; margin:4px 8px; }}

/* ── 함수 패널 컨테이너 ── */
QWidget#fn_panel {{
    background-color: {C['fn_bg']};
    border-bottom: 1px solid #1a3a2a;
}}
QLabel#fn_result {{
    color: {C['accent']};
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    padding: 0 8px;
}}
QLabel#fn_title {{
    color: {C['text_muted']};
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    padding: 0 4px;
}}
"""


# ─────────────────────────────────────────
#  찾기 다이얼로그
# ─────────────────────────────────────────
class FindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("찾기")
        self.setFixedSize(340, 110)
        self.parent_window = parent

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        row = QHBoxLayout()
        row.addWidget(QLabel("검색어:"))
        self.input = QLineEdit()
        self.input.setPlaceholderText("찾을 내용 입력...")
        self.input.returnPressed.connect(self.find_next)
        row.addWidget(self.input)
        layout.addLayout(row)

        btn_row = QHBoxLayout()
        self.find_btn = QPushButton("다음 찾기")
        self.find_btn.clicked.connect(self.find_next)
        close_btn = QPushButton("닫기")
        close_btn.clicked.connect(self.close)
        self.result_lbl = QLabel("")
        self.result_lbl.setStyleSheet(f"color:{C['text_dim']}; font-size:11px;")
        btn_row.addWidget(self.result_lbl)
        btn_row.addStretch()
        btn_row.addWidget(self.find_btn)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

        self._last_row = -1
        self._last_col = -1

    def find_next(self):
        keyword = self.input.text().strip().lower()
        if not keyword:
            return
        table = self.parent_window.table
        rows = table.rowCount()
        cols = table.columnCount()

        # 현재 위치 이후부터 순환 탐색
        start_r = self._last_row
        start_c = self._last_col + 1

        for r in range(start_r, rows):
            c_start = start_c if r == start_r else 0
            for c in range(c_start, cols):
                item = table.item(r, c)
                if item and keyword in item.text().lower():
                    table.setCurrentCell(r, c)
                    table.scrollToItem(item)
                    self._last_row = r
                    self._last_col = c
                    self.result_lbl.setText(f"행 {r+1} · 열 {c+1}")
                    return

        # 처음부터 다시
        for r in range(0, start_r + 1):
            c_end = start_c if r == start_r else cols
            for c in range(0, c_end):
                item = table.item(r, c)
                if item and keyword in item.text().lower():
                    table.setCurrentCell(r, c)
                    table.scrollToItem(item)
                    self._last_row = r
                    self._last_col = c
                    self.result_lbl.setText(f"행 {r+1} · 열 {c+1} (처음으로)")
                    return

        self.result_lbl.setText("결과 없음")
        self._last_row = -1
        self._last_col = -1


# ─────────────────────────────────────────
#  푸터
# ─────────────────────────────────────────
class FooterBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(46)
        self.setObjectName("footer")
        self.setStyleSheet(f"""
            QWidget#footer {{
                background-color: {C['surface']};
                border-top: 1px solid {C['border']};
            }}
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        brand = QLabel("JOON · Excel Editor")
        brand.setStyleSheet(f"color:{C['text_muted']}; font-size:11px; font-weight:600; letter-spacing:1.5px;")

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        email = QLabel(
            f'<a href="mailto:lotus031315@gmail.com" '
            f'style="color:{C["accent"]}; text-decoration:none; font-size:12px; font-weight:500;">'
            f'✉&nbsp;&nbsp;lotus031315@gmail.com</a>'
        )
        email.setOpenExternalLinks(True)
        email.setTextInteractionFlags(Qt.TextBrowserInteraction)
        email.setCursor(QCursor(Qt.PointingHandCursor))

        dot = QLabel("·")
        dot.setStyleSheet(f"color:{C['text_muted']}; margin:0 10px;")

        web = QLabel(
            f'<a href="https://joon041415.github.io/" '
            f'style="color:{C["text_muted"]}; text-decoration:none; font-size:12px;">'
            f'Portfolio ↗</a>'
        )
        web.setOpenExternalLinks(True)
        web.setTextInteractionFlags(Qt.TextBrowserInteraction)
        web.setCursor(QCursor(Qt.PointingHandCursor))

        for w in [brand, spacer, email, dot, web]:
            layout.addWidget(w)


# ─────────────────────────────────────────
#  Enter → 아래 이동을 보장하는 커스텀 테이블
# ─────────────────────────────────────────
class ExcelTable(QTableWidget):
    """QTableWidget 서브클래스 — 편집 완료 후 Enter 시 아래 셀 이동"""

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Return, Qt.Key_Enter):
            # 편집 중이면 먼저 커밋
            if self.state() == QAbstractItemView.EditingState:
                self.commitData(self.itemDelegate())
                self.closePersistentEditor(self.currentItem())
            r = self.currentRow()
            c = self.currentColumn()
            next_r = min(r + 1, self.rowCount() - 1)
            self.setCurrentCell(next_r, c)
            # 편집 상태 해제 보장
            self.setFocus()
        else:
            super().keyPressEvent(event)



class ExcelEditor(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Editor")
        self.resize(1340, 800)
        self.file_path = None
        self.last_dir = ""             # 마지막으로 열었던 디렉토리
        self.df = pd.DataFrame()
        self.loading_table = False
        self._undo_stack = []          # (row, col, old_value)
        self._find_dialog = None
        self.init_ui()
        self._setup_shortcuts()
        self.update_status()

    # ══════════════════════════════════════
    #  UI 구성
    # ══════════════════════════════════════
    def init_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_toolbar())
        root_layout.addWidget(self._build_fn_panel())
        root_layout.addWidget(self._build_table_area())
        root_layout.addWidget(FooterBar())

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    # ── 툴바 ──────────────────────────────
    def _build_toolbar(self):
        bar = QWidget()
        bar.setFixedHeight(50)
        bar.setStyleSheet(f"QWidget{{background:{C['surface']};border-bottom:1px solid {C['border']};}}")
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(12, 0, 12, 0)
        lay.setSpacing(6)

        title = QLabel("Excel Editor")
        title.setStyleSheet(f"color:{C['accent']};font-size:14px;font-weight:700;letter-spacing:0.5px;padding-right:12px;")

        self.open_btn    = self._tb_btn("📂 열기",       self.open_excel)
        self.new_btn     = self._tb_btn("＋ 새 파일",    self.new_file)
        self.save_btn    = self._tb_btn("💾 저장",       self.save_excel, obj="btn_save")
        self.save_as_btn = self._tb_btn("다른 이름으로", self.save_as_excel)

        sep1 = self._vsep()

        self.add_row_btn = self._tb_btn("＋ 행", lambda: self.insert_row(self.table.currentRow()))
        self.del_row_btn = self._tb_btn("－ 행", self.delete_selected_rows, obj="btn_delete")
        self.add_col_btn = self._tb_btn("＋ 열", lambda: self.insert_col(self.table.currentColumn()))
        self.del_col_btn = self._tb_btn("－ 열", self.delete_selected_col, obj="btn_delete")

        sep2 = self._vsep()

        lbl = QLabel("시트")
        lbl.setStyleSheet(f"color:{C['text_dim']};font-size:11px;")
        self.sheet_combo = QComboBox()
        self.sheet_combo.currentIndexChanged.connect(self.change_sheet)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # 단축키 힌트 레이블
        hint = QLabel("Ctrl+S 저장  │  Ctrl+Z 실행취소  │  Ctrl+F 찾기  │  Ctrl+↑↓←→ 데이터 끝으로")
        hint.setStyleSheet(f"color:{C['text_muted']};font-size:10px;letter-spacing:0.3px;")

        for w in [title, self.open_btn, self.new_btn, self.save_btn, self.save_as_btn,
                  sep1, self.add_row_btn, self.del_row_btn,
                  self.add_col_btn, self.del_col_btn, sep2,
                  lbl, self.sheet_combo, spacer, hint]:
            lay.addWidget(w)
        return bar

    # ── 함수 패널 ─────────────────────────
    def _build_fn_panel(self):
        panel = QWidget()
        panel.setObjectName("fn_panel")
        panel.setFixedHeight(42)
        lay = QHBoxLayout(panel)
        lay.setContentsMargins(12, 0, 12, 0)
        lay.setSpacing(6)

        lbl = QLabel("FUNCTIONS")
        lbl.setObjectName("fn_title")
        lay.addWidget(lbl)

        sep = self._vsep()
        lay.addWidget(sep)

        # 자주 쓰는 집계 함수
        fns = [
            ("SUM",    self._fn_sum),
            ("AVG",    self._fn_avg),
            ("COUNT",  self._fn_count),
            ("COUNTA", self._fn_counta),
            ("MAX",    self._fn_max),
            ("MIN",    self._fn_min),
        ]
        for name, slot in fns:
            btn = QPushButton(name)
            btn.setObjectName("fn_btn")
            btn.setFixedHeight(28)
            btn.clicked.connect(slot)
            btn.setToolTip(f"선택된 열에 {name} 적용")
            lay.addWidget(btn)

        sep2 = self._vsep()
        lay.addWidget(sep2)

        # 정렬
        sort_lbl = QLabel("SORT")
        sort_lbl.setObjectName("fn_title")
        lay.addWidget(sort_lbl)

        self.sort_asc_btn = QPushButton("↑ 오름차순")
        self.sort_asc_btn.setObjectName("fn_btn")
        self.sort_asc_btn.setFixedHeight(28)
        self.sort_asc_btn.clicked.connect(lambda: self._sort_by_col(ascending=True))

        self.sort_desc_btn = QPushButton("↓ 내림차순")
        self.sort_desc_btn.setObjectName("fn_btn")
        self.sort_desc_btn.setFixedHeight(28)
        self.sort_desc_btn.clicked.connect(lambda: self._sort_by_col(ascending=False))

        lay.addWidget(self.sort_asc_btn)
        lay.addWidget(self.sort_desc_btn)

        sep3 = self._vsep()
        lay.addWidget(sep3)

        # 중복 제거
        dedup_btn = QPushButton("중복 제거")
        dedup_btn.setObjectName("fn_btn")
        dedup_btn.setFixedHeight(28)
        dedup_btn.clicked.connect(self._fn_dedup)
        lay.addWidget(dedup_btn)

        sep4 = self._vsep()
        lay.addWidget(sep4)

        # 결과 표시
        result_lbl_title = QLabel("결과:")
        result_lbl_title.setObjectName("fn_title")
        lay.addWidget(result_lbl_title)

        self.fn_result = QLabel("—")
        self.fn_result.setObjectName("fn_result")
        lay.addWidget(self.fn_result)

        lay.addStretch()
        return panel

    # ── 테이블 영역 ───────────────────────
    def _build_table_area(self):
        container = QWidget()
        container.setStyleSheet(f"background:{C['bg']};")
        lay = QVBoxLayout(container)
        lay.setContentsMargins(12, 8, 12, 8)

        self.table = ExcelTable()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(26)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.itemChanged.connect(self.cell_changed)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        # 헤더 더블클릭 → 열 너비 자동 맞춤(단일 클릭) / 이름 편집(더블클릭)
        self.table.horizontalHeader().sectionDoubleClicked.connect(
            self.edit_column_name
        )
        # 선택 변경 시 함수 결과 초기화
        self.table.itemSelectionChanged.connect(self._on_selection_changed)

        lay.addWidget(self.table)
        return container

    # ══════════════════════════════════════
    #  단축키 설정
    # ══════════════════════════════════════
    def _setup_shortcuts(self):
        # 저장
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.save_excel)
        # 다른 이름으로 저장
        QShortcut(QKeySequence("Ctrl+Shift+S"), self).activated.connect(self.save_as_excel)
        # 실행취소
        QShortcut(QKeySequence("Ctrl+Z"), self).activated.connect(self.undo)
        # 찾기
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.open_find)
        # 전체 선택
        QShortcut(QKeySequence("Ctrl+A"), self).activated.connect(self.table.selectAll)
        # 행 추가
        QShortcut(QKeySequence("Ctrl+Return"), self).activated.connect(
            lambda: self.insert_row(self.table.currentRow() + 1)
        )
        # Ctrl+방향키 — 데이터 끝으로 점프
        QShortcut(QKeySequence("Ctrl+Up"),    self).activated.connect(lambda: self._jump("up"))
        QShortcut(QKeySequence("Ctrl+Down"),  self).activated.connect(lambda: self._jump("down"))
        QShortcut(QKeySequence("Ctrl+Left"),  self).activated.connect(lambda: self._jump("left"))
        QShortcut(QKeySequence("Ctrl+Right"), self).activated.connect(lambda: self._jump("right"))
        # Ctrl+Home / Ctrl+End
        QShortcut(QKeySequence("Ctrl+Home"), self).activated.connect(
            lambda: self._goto(0, 0)
        )
        QShortcut(QKeySequence("Ctrl+End"), self).activated.connect(
            lambda: self._goto(self.table.rowCount()-1, self.table.columnCount()-1)
        )
        # Delete — 선택 행 삭제
        QShortcut(QKeySequence("Ctrl+Delete"), self).activated.connect(self.delete_selected_rows)

    def _jump(self, direction):
        """Ctrl+방향키: 엑셀과 동일한 동작
        - 현재 셀이 비어있으면 → 다음 데이터 있는 셀로
        - 현재 셀에 데이터 있으면 → 연속 블록 끝까지 이동, 끝이면 다음 데이터 있는 셀로
        """
        r = self.table.currentRow()
        c = self.table.currentColumn()
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        if r < 0 or c < 0:
            return

        def has_data(rr, cc):
            item = self.table.item(rr, cc)
            return bool(item and item.text())

        if direction == "up":
            if r == 0:
                return
            if not has_data(r, c):
                # 비어있음 → 위로 올라가며 첫 데이터 셀
                for i in range(r - 1, -1, -1):
                    if has_data(i, c):
                        self._goto(i, c); return
                self._goto(0, c)
            else:
                # 데이터 있음 → 블록 끝(위쪽) 찾기
                if not has_data(r - 1, c):
                    # 바로 위가 비어있으면 → 다음 데이터 블록 위로 점프
                    for i in range(r - 2, -1, -1):
                        if has_data(i, c):
                            self._goto(i, c); return
                    self._goto(0, c)
                else:
                    # 연속 블록 위쪽 끝까지
                    target = 0
                    for i in range(r - 1, -1, -1):
                        if not has_data(i, c):
                            target = i + 1; break
                    self._goto(target, c)

        elif direction == "down":
            if r == rows - 1:
                return
            if not has_data(r, c):
                for i in range(r + 1, rows):
                    if has_data(i, c):
                        self._goto(i, c); return
                self._goto(rows - 1, c)
            else:
                if not has_data(r + 1, c):
                    for i in range(r + 2, rows):
                        if has_data(i, c):
                            self._goto(i, c); return
                    self._goto(rows - 1, c)
                else:
                    target = rows - 1
                    for i in range(r + 1, rows):
                        if not has_data(i, c):
                            target = i - 1; break
                    self._goto(target, c)

        elif direction == "left":
            if c == 0:
                return
            if not has_data(r, c):
                for j in range(c - 1, -1, -1):
                    if has_data(r, j):
                        self._goto(r, j); return
                self._goto(r, 0)
            else:
                if not has_data(r, c - 1):
                    for j in range(c - 2, -1, -1):
                        if has_data(r, j):
                            self._goto(r, j); return
                    self._goto(r, 0)
                else:
                    target = 0
                    for j in range(c - 1, -1, -1):
                        if not has_data(r, j):
                            target = j + 1; break
                    self._goto(r, target)

        elif direction == "right":
            if c == cols - 1:
                return
            if not has_data(r, c):
                for j in range(c + 1, cols):
                    if has_data(r, j):
                        self._goto(r, j); return
                self._goto(r, cols - 1)
            else:
                if not has_data(r, c + 1):
                    for j in range(c + 2, cols):
                        if has_data(r, j):
                            self._goto(r, j); return
                    self._goto(r, cols - 1)
                else:
                    target = cols - 1
                    for j in range(c + 1, cols):
                        if not has_data(r, j):
                            target = j - 1; break
                    self._goto(r, target)

    def _goto(self, row, col):
        row = max(0, min(row, self.table.rowCount() - 1))
        col = max(0, min(col, self.table.columnCount() - 1))
        self.table.setCurrentCell(row, col)
        self.table.scrollToItem(self.table.item(row, col))

    # ══════════════════════════════════════
    #  함수 기능
    # ══════════════════════════════════════
    def _selected_col_values(self):
        """선택된 행들의 현재 열 숫자 값 추출"""
        indexes = self.table.selectedIndexes()
        if not indexes:
            return None, None
        col = indexes[0].column()
        rows = sorted(set(i.row() for i in indexes))
        values = []
        for r in rows:
            item = self.table.item(r, col)
            if item and item.text():
                try:
                    values.append(float(item.text()))
                except ValueError:
                    pass
        col_name = self.table.horizontalHeaderItem(col).text() if self.table.horizontalHeaderItem(col) else f"Col{col}"
        return values, col_name

    def _selected_col_all(self):
        """선택된 행들의 현재 열 전체 셀(빈칸 포함) 추출"""
        indexes = self.table.selectedIndexes()
        if not indexes:
            return None, None
        col = indexes[0].column()
        rows = sorted(set(i.row() for i in indexes))
        items = []
        for r in rows:
            item = self.table.item(r, col)
            items.append(item.text() if item else "")
        col_name = self.table.horizontalHeaderItem(col).text() if self.table.horizontalHeaderItem(col) else f"Col{col}"
        return items, col_name

    def _show_fn_result(self, label, value):
        if isinstance(value, float) and value == int(value):
            self.fn_result.setText(f"{label} = {int(value):,}")
        elif isinstance(value, float):
            self.fn_result.setText(f"{label} = {value:,.4f}".rstrip('0').rstrip('.'))
        else:
            self.fn_result.setText(f"{label} = {value}")

    def _fn_sum(self):
        vals, col = self._selected_col_values()
        if vals is None:
            return self._fn_result_warn()
        self._show_fn_result(f"SUM({col})", sum(vals))

    def _fn_avg(self):
        vals, col = self._selected_col_values()
        if not vals:
            return self._fn_result_warn()
        self._show_fn_result(f"AVG({col})", sum(vals) / len(vals))

    def _fn_count(self):
        vals, col = self._selected_col_values()
        if vals is None:
            return self._fn_result_warn()
        self._show_fn_result(f"COUNT({col})", len(vals))

    def _fn_counta(self):
        items, col = self._selected_col_all()
        if items is None:
            return self._fn_result_warn()
        count = sum(1 for v in items if v.strip() != "")
        self._show_fn_result(f"COUNTA({col})", count)

    def _fn_max(self):
        vals, col = self._selected_col_values()
        if not vals:
            return self._fn_result_warn()
        self._show_fn_result(f"MAX({col})", max(vals))

    def _fn_min(self):
        vals, col = self._selected_col_values()
        if not vals:
            return self._fn_result_warn()
        self._show_fn_result(f"MIN({col})", min(vals))

    def _fn_dedup(self):
        if self.df.empty:
            return
        before = len(self.df)
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        after = len(self.df)
        removed = before - after
        self._reload_table_from_df()
        self._show_fn_result("중복제거", f"{removed}행 삭제 → {after}행 남음")

    def _sort_by_col(self, ascending=True):
        indexes = self.table.selectedIndexes()
        if not indexes:
            self.fn_result.setText("열을 선택하세요")
            return
        col_idx = indexes[0].column()
        col_name = self.df.columns[col_idx]
        self.df = self.df.sort_values(
            by=col_name, ascending=ascending,
            key=lambda s: pd.to_numeric(s, errors='coerce').fillna(s)
        ).reset_index(drop=True)
        self._reload_table_from_df()
        direction = "오름차순" if ascending else "내림차순"
        self.fn_result.setText(f"정렬: {col_name} {direction}")

    def _fn_result_warn(self):
        self.fn_result.setText("행을 선택하세요")

    def _on_selection_changed(self):
        self.fn_result.setText("—")
        # 상태바에 선택 행 수 표시
        rows = set(i.row() for i in self.table.selectedIndexes())
        if len(rows) > 1:
            self._update_status_selection(len(rows))

    # ══════════════════════════════════════
    #  파일 작업
    # ══════════════════════════════════════
    def open_excel(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "엑셀 파일 선택", self.last_dir,
            "Excel Files (*.xlsx *.xls)"
        )
        if not path:
            return
        self.file_path = path
        self.last_dir = path.replace("\\", "/").rsplit("/", 1)[0]
        try:
            excel = pd.ExcelFile(path)
            self.sheet_combo.blockSignals(True)
            self.sheet_combo.clear()
            self.sheet_combo.addItems(excel.sheet_names)
            self.sheet_combo.blockSignals(False)
            self.load_sheet(excel.sheet_names[0])
            fname = path.replace("\\", "/").split("/")[-1]
            self.setWindowTitle(f"Excel Editor — {fname}")
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))

    def new_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "새 파일 저장 위치", self.last_dir + "/새파일.xlsx",
            "Excel Files (*.xlsx)"
        )
        if not path:
            return
        self.file_path = path
        self.last_dir = path.replace("\\", "/").rsplit("/", 1)[0]
        # 10x10 빈 시트
        cols = [chr(65 + i) for i in range(10)]   # A~J
        self.df = pd.DataFrame(
            [[None] * 10 for _ in range(10)],
            columns=cols
        )
        w = pd.ExcelWriter(path, engine="openpyxl")
        self.df.to_excel(w, sheet_name="Sheet1", index=False)
        w.close()
        self.sheet_combo.blockSignals(True)
        self.sheet_combo.clear()
        self.sheet_combo.addItems(["Sheet1"])
        self.sheet_combo.blockSignals(False)
        self.load_sheet("Sheet1")
        self.setWindowTitle(f"Excel Editor — {path.replace(chr(92),'/').split('/')[-1]}")

    # ══════════════════════════════════════
    #  시트 관리
    # ══════════════════════════════════════
    def load_sheet(self, sheet_name):
        try:
            self.loading_table = True
            self.df = pd.read_excel(
                self.file_path, sheet_name=sheet_name, dtype=object
            )
            self._reload_table_from_df()
            self.loading_table = False
            self.update_status()
        except Exception as e:
            self.loading_table = False
            QMessageBox.critical(self, "오류", str(e))

    def _reload_table_from_df(self):
        """df → table 재렌더링 (정렬/중복제거 후 공통 사용)"""
        was_loading = self.loading_table
        self.loading_table = True
        rows, cols = len(self.df.index), len(self.df.columns)
        self.table.clear()
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)
        self.table.setHorizontalHeaderLabels([str(c) for c in self.df.columns])
        for r in range(rows):
            for c in range(cols):
                val = self.df.iat[r, c]
                text = "" if pd.isna(val) else str(val)
                item = QTableWidgetItem(text)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.table.setItem(r, c, item)
        self.table.resizeColumnsToContents()
        self.loading_table = was_loading
        self.update_status()

    def change_sheet(self):
        name = self.sheet_combo.currentText()
        if name:
            self.load_sheet(name)

    # ══════════════════════════════════════
    #  셀 편집 / 실행취소
    # ══════════════════════════════════════
    def cell_changed(self, item):
        if self.loading_table:
            return
        r, c = item.row(), item.column()
        old_val = self.df.iat[r, c]
        text = item.text()
        new_val = None if text == "" else self.convert_value(text)
        self._undo_stack.append((r, c, old_val))
        if len(self._undo_stack) > 100:
            self._undo_stack.pop(0)
        self.df.iat[r, c] = new_val
        self.update_status()

    def undo(self):
        if not self._undo_stack:
            self.status_bar.showMessage("⚠  실행취소할 내역이 없습니다", 2000)
            return
        r, c, old_val = self._undo_stack.pop()
        self.df.iat[r, c] = old_val
        self.loading_table = True
        text = "" if old_val is None or (isinstance(old_val, float) and pd.isna(old_val)) else str(old_val)
        item = self.table.item(r, c)
        if item:
            item.setText(text)
        self.loading_table = False
        self.table.setCurrentCell(r, c)
        self.status_bar.showMessage(f"↩  실행취소 — 행{r+1} 열{c+1}", 2000)

    def convert_value(self, value):
        try:
            if value.isdigit():
                return int(value)
            return float(value)
        except Exception:
            return value

    # ══════════════════════════════════════
    #  행 조작
    # ══════════════════════════════════════
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
        self.table.setCurrentCell(row, 0)
        self.update_status()

    def delete_selected_rows(self):
        rows = sorted(
            set(idx.row() for idx in self.table.selectedIndexes()),
            reverse=True
        )
        if not rows:
            QMessageBox.warning(self, "선택 필요", "삭제할 행을 선택하세요.")
            return
        if len(rows) > 1:
            ans = QMessageBox.question(
                self, "행 삭제", f"{len(rows)}개 행을 삭제할까요?",
                QMessageBox.Yes | QMessageBox.No
            )
            if ans != QMessageBox.Yes:
                return
        for r in rows:
            self.table.removeRow(r)
            self.df = self.df.drop(self.df.index[r]).reset_index(drop=True)
        self.update_status()

    # ── 열 조작 ───────────────────────────────
    def insert_col(self, col):
        """현재 열 왼쪽에 새 열 삽입"""
        if col < 0:
            col = self.table.columnCount()
        # 헤더 이름 생성 (기존 이름과 겹치지 않게)
        existing = list(self.df.columns)
        new_name = self._unique_col_name("NewCol", existing)
        self.df.insert(col, new_name, None)
        self.table.insertColumn(col)
        self.table.setHorizontalHeaderItem(col, QTableWidgetItem(new_name))
        for r in range(self.table.rowCount()):
            item = QTableWidgetItem("")
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.table.setItem(r, col, item)
        self.update_status()

    def delete_selected_col(self):
        indexes = self.table.selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, "선택 필요", "삭제할 열의 셀을 선택하세요.")
            return
        cols = sorted(set(i.column() for i in indexes), reverse=True)
        if len(cols) > 1:
            ans = QMessageBox.question(
                self, "열 삭제", f"{len(cols)}개 열을 삭제할까요?",
                QMessageBox.Yes | QMessageBox.No
            )
            if ans != QMessageBox.Yes:
                return
        for c in cols:
            self.table.removeColumn(c)
            col_name = self.df.columns[c]
            self.df = self.df.drop(columns=[col_name])
        self.update_status()

    def _unique_col_name(self, base, existing):
        if base not in existing:
            return base
        i = 1
        while f"{base}{i}" in existing:
            i += 1
        return f"{base}{i}"

    # ══════════════════════════════════════
    #  찾기
    # ══════════════════════════════════════
    def open_find(self):
        if self._find_dialog is None or not self._find_dialog.isVisible():
            self._find_dialog = FindDialog(self)
        self._find_dialog.show()
        self._find_dialog.raise_()
        self._find_dialog.input.setFocus()

    # ══════════════════════════════════════
    #  컨텍스트 메뉴
    # ══════════════════════════════════════
    def show_context_menu(self, position):
        menu = QMenu()
        add_above   = menu.addAction("⬆  위에 행 추가  [Ctrl+Enter]")
        add_below   = menu.addAction("⬇  아래에 행 추가")
        del_row     = menu.addAction("🗑  행 삭제  [Ctrl+Del]")
        menu.addSeparator()
        add_col_l   = menu.addAction("◀  왼쪽에 열 추가")
        add_col_r   = menu.addAction("▶  오른쪽에 열 추가")
        del_col     = menu.addAction("✂  열 삭제")
        menu.addSeparator()
        find_action = menu.addAction("🔍  찾기  [Ctrl+F]")

        action = menu.exec(self.table.viewport().mapToGlobal(position))
        row = self.table.currentRow()
        col = self.table.currentColumn()

        if action == add_above:
            self.insert_row(row)
        elif action == add_below:
            self.insert_row(row + 1)
        elif action == del_row:
            self.delete_selected_rows()
        elif action == add_col_l:
            self.insert_col(col)
        elif action == add_col_r:
            self.insert_col(col + 1)
        elif action == del_col:
            self.delete_selected_col()
        elif action == find_action:
            self.open_find()

    # ══════════════════════════════════════
    #  저장
    # ══════════════════════════════════════
    def save_excel(self):
        if self.file_path is None:
            self.save_as_excel()
            return
        self._write_excel(self.file_path)

    def save_as_excel(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "다른 이름으로 저장", self.last_dir, "Excel Files (*.xlsx)"
        )
        if not path:
            return
        self.file_path = path
        self.last_dir = path.replace("\\", "/").rsplit("/", 1)[0]
        self._write_excel(path)
        self.setWindowTitle(f"Excel Editor — {path.replace(chr(92),'/').split('/')[-1]}")

    def _write_excel(self, path):
        try:
            sheet = self.sheet_combo.currentText() or "Sheet1"
            with pd.ExcelWriter(
                path, engine="openpyxl", mode="a",
                if_sheet_exists="replace"
            ) as writer:
                self.df.to_excel(writer, sheet_name=sheet, index=False)
            self.status_bar.showMessage("✓  저장 완료", 3000)
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", str(e))

    # ══════════════════════════════════════
    #  상태바
    # ══════════════════════════════════════
    def update_status(self):
        rows = len(self.df.index) if not self.df.empty else 0
        cols = len(self.df.columns) if not self.df.empty else 0
        fname = (
            self.file_path.replace("\\", "/").split("/")[-1]
            if self.file_path else "파일 없음"
        )
        self.status_bar.showMessage(
            f"  {fname}   │   {rows}행 × {cols}열"
            f"   │   Ctrl+방향키: 데이터 끝으로   │   Ctrl+F: 찾기   │   Ctrl+Z: 실행취소"
        )

    def _update_status_selection(self, count):
        self.status_bar.showMessage(
            f"  {count}행 선택됨   │   함수 버튼으로 집계하거나 Ctrl+Del로 삭제",
            3000
        )

    # ══════════════════════════════════════
    #  열 이름 편집
    # ══════════════════════════════════════
    def edit_column_name(self, col_idx):
        """헤더 더블클릭 → 열 이름 인라인 수정 다이얼로그"""
        current_name = self.df.columns[col_idx] if col_idx < len(self.df.columns) else ""

        dlg = QDialog(self)
        dlg.setWindowTitle("열 이름 수정")
        dlg.setFixedSize(320, 110)

        lay = QVBoxLayout(dlg)
        lay.setSpacing(10)

        row = QHBoxLayout()
        row.addWidget(QLabel("새 이름:"))
        inp = QLineEdit(str(current_name))
        inp.selectAll()
        row.addWidget(inp)
        lay.addLayout(row)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        lay.addWidget(btns)

        inp.setFocus()
        inp.returnPressed.connect(dlg.accept)

        if dlg.exec() != QDialog.Accepted:
            return

        new_name = inp.text().strip()
        if not new_name or new_name == str(current_name):
            return

        # 중복 체크
        existing = [str(c) for c in self.df.columns]
        if new_name in existing:
            QMessageBox.warning(self, "중복 이름", f"'{new_name}' 열이 이미 존재합니다.")
            return

        # df 컬럼 이름 변경
        old_name = self.df.columns[col_idx]
        self.df = self.df.rename(columns={old_name: new_name})

        # 헤더 위젯 업데이트
        self.loading_table = True
        item = self.table.horizontalHeaderItem(col_idx)
        if item:
            item.setText(new_name)
        else:
            self.table.setHorizontalHeaderItem(col_idx, QTableWidgetItem(new_name))
        self.loading_table = False

        self.status_bar.showMessage(f"  열 이름 변경: '{old_name}' → '{new_name}'", 3000)

    # ══════════════════════════════════════
    #  헬퍼
    # ══════════════════════════════════════
    def _tb_btn(self, text, slot, obj=None):
        btn = QPushButton(text)
        if obj:
            btn.setObjectName(obj)
        btn.clicked.connect(slot)
        return btn

    def _vsep(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet(f"background:{C['border2']}; max-width:1px; margin:10px 2px;")
        return sep


# ─────────────────────────────────────────
#  엔트리포인트
# ─────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = ExcelEditor()
    window.show()
    sys.exit(app.exec())
