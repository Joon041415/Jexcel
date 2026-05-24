import sys, re, math, os
import pandas as pd

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QTableWidget,
    QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QComboBox, QLabel,
    QAbstractItemView, QMenu, QStatusBar, QFrame,
    QSizePolicy, QDialog, QLineEdit, QDialogButtonBox,
    QScrollArea, QCheckBox, QColorDialog, QSpinBox,
    QDoubleSpinBox, QGroupBox, QGridLayout, QSplitter,
    QHeaderView,
)
from PySide6.QtCore import Qt, QSize, QTimer, QMimeData, QPoint
from PySide6.QtGui import (
    QCursor, QKeySequence, QShortcut, QColor, QBrush,
    QFont, QClipboard, QGuiApplication,
)

# ══════════════════════════════════════════════════
#  팔레트
# ══════════════════════════════════════════════════
C = {
    "bg":          "#0d0d0d",
    "surface":     "#141414",
    "surface2":    "#1a1a1a",
    "border":      "#2a2a2a",
    "border2":     "#333333",
    "accent":      "#00e5a0",
    "accent_dim":  "#00b37a",
    "accent_bg":   "#0d2e22",
    "accent_bg2":  "#0a2019",
    "text":        "#e8e8e8",
    "text_dim":    "#888888",
    "text_muted":  "#555555",
    "danger":      "#ff4d6d",
    "danger_dim":  "#cc2244",
    "header_bg":   "#111111",
    "formula_bg":  "#0e1a12",
    "freeze_line": "#00e5a0",
    "filter_on":   "#003322",
}

STYLESHEET = f"""
QWidget {{
    background-color:{C['bg']};
    color:{C['text']};
    font-family:'Pretendard','Noto Sans KR','Segoe UI',sans-serif;
    font-size:13px;
}}
QMainWindow {{ background-color:{C['bg']}; }}

/* ── 버튼 ── */
QPushButton {{
    background-color:{C['surface2']}; color:{C['text']};
    border:1px solid {C['border2']}; border-radius:4px;
    padding:5px 12px; font-size:12px; font-weight:500; min-width:60px;
}}
QPushButton:hover  {{ background-color:{C['border2']}; border-color:{C['text_dim']}; }}
QPushButton:pressed {{ background-color:{C['border']}; }}
QPushButton#btn_save {{
    background-color:{C['accent']}; color:#000; border:none; font-weight:700;
}}
QPushButton#btn_save:hover {{ background-color:{C['accent_dim']}; }}
QPushButton#btn_delete {{
    background-color:transparent; color:{C['danger']};
    border:1px solid {C['danger_dim']};
}}
QPushButton#btn_delete:hover {{ background-color:{C['danger_dim']}; color:white; }}
QPushButton#fn_btn {{
    background-color:{C['formula_bg']}; color:{C['accent']};
    border:1px solid #1a3a2a; border-radius:3px;
    padding:3px 8px; font-size:11px; font-weight:600; min-width:44px;
    font-family:'Consolas','Courier New',monospace;
}}
QPushButton#fn_btn:hover {{ background-color:#0f2d20; border-color:{C['accent_dim']}; }}
QPushButton#filter_active {{
    background-color:{C['filter_on']}; color:{C['accent']};
    border:1px solid {C['accent_dim']}; border-radius:3px;
    padding:1px 5px; font-size:10px; font-weight:700; min-width:0px;
}}

/* ── Formula Bar ── */
QLineEdit#formula_bar {{
    background-color:{C['formula_bg']};
    border:1px solid #1a3a2a;
    border-radius:0px;
    padding:4px 10px;
    color:{C['text']};
    font-family:'Consolas','Courier New',monospace;
    font-size:13px;
    selection-background-color:{C['accent_bg']};
}}
QLineEdit#formula_bar:focus {{ border-color:{C['accent']}; }}

/* ── 셀 주소 박스 ── */
QLineEdit#cell_ref {{
    background-color:{C['surface2']};
    border:1px solid {C['border2']};
    border-radius:3px; padding:4px 8px;
    color:{C['accent']};
    font-family:'Consolas','Courier New',monospace;
    font-size:12px; font-weight:700;
    min-width:64px; max-width:80px;
}}

/* ── 콤보박스 ── */
QComboBox {{
    background-color:{C['surface2']}; border:1px solid {C['border2']};
    border-radius:4px; padding:5px 10px; min-width:100px; color:{C['text']};
}}
QComboBox::drop-down {{ border:none; width:18px; }}
QComboBox QAbstractItemView {{
    background-color:{C['surface2']}; border:1px solid {C['border2']};
    selection-background-color:{C['border2']};
}}

/* ── 테이블 ── */
QTableWidget {{
    background-color:{C['surface']}; gridline-color:{C['border']};
    border:none; alternate-background-color:{C['surface2']};
    selection-background-color:{C['accent_bg']}; selection-color:{C['accent']};
}}
QTableWidget::item {{ padding:2px 6px; border:none; }}
QTableWidget::item:selected {{
    background-color:{C['accent_bg']}; color:{C['accent']};
}}
QHeaderView::section {{
    background-color:{C['header_bg']}; color:{C['text_dim']};
    padding:5px 6px; border:none;
    border-right:1px solid {C['border']}; border-bottom:1px solid {C['border']};
    font-size:11px; font-weight:600; letter-spacing:0.3px;
}}
QHeaderView::section:hover {{
    background-color:{C['surface2']}; color:{C['text']};
}}

/* ── 스크롤바 ── */
QScrollBar:vertical   {{ background:{C['surface']}; width:7px; border-radius:4px; }}
QScrollBar:horizontal {{ background:{C['surface']}; height:7px; border-radius:4px; }}
QScrollBar::handle:vertical,QScrollBar::handle:horizontal {{
    background:{C['border2']}; border-radius:4px; min-height:20px; min-width:20px;
}}
QScrollBar::handle:vertical:hover,QScrollBar::handle:horizontal:hover {{
    background:{C['text_dim']};
}}
QScrollBar::add-line,QScrollBar::sub-line {{ border:none; background:none; }}

/* ── 입력창 ── */
QLineEdit {{
    background-color:{C['surface2']}; border:1px solid {C['border2']};
    border-radius:4px; padding:5px 8px; color:{C['text']};
}}
QLineEdit:focus {{ border-color:{C['accent']}; }}

/* ── 다이얼로그 ── */
QDialog {{ background-color:{C['surface']}; }}
QGroupBox {{
    border:1px solid {C['border2']}; border-radius:4px;
    margin-top:8px; padding-top:8px; color:{C['text_dim']};
    font-size:11px;
}}
QGroupBox::title {{ subcontrol-origin:margin; left:8px; color:{C['text_dim']}; }}
QCheckBox {{ spacing:6px; }}
QCheckBox::indicator {{
    width:14px; height:14px; border:1px solid {C['border2']};
    border-radius:3px; background:{C['surface2']};
}}
QCheckBox::indicator:checked {{
    background:{C['accent']}; border-color:{C['accent']};
}}

/* ── 상태바 ── */
QStatusBar {{
    background-color:{C['surface']}; color:{C['text_dim']};
    border-top:1px solid {C['border']}; font-size:11px; padding:2px 8px;
}}

/* ── 메뉴 ── */
QMenu {{
    background-color:{C['surface2']}; border:1px solid {C['border2']};
    border-radius:6px; padding:4px;
}}
QMenu::item {{ padding:6px 20px; border-radius:3px; }}
QMenu::item:selected {{ background-color:{C['border2']}; color:{C['accent']}; }}
QMenu::separator {{ height:1px; background:{C['border']}; margin:4px 8px; }}

/* ── 함수 패널 ── */
QWidget#fn_panel {{
    background-color:{C['formula_bg']};
    border-bottom:1px solid #1a3a2a;
}}
QLabel#fn_result {{
    color:{C['accent']}; font-family:'Consolas','Courier New',monospace;
    font-size:12px; padding:0 6px;
}}
QLabel#fn_title {{
    color:{C['text_muted']}; font-size:10px; font-weight:600;
    letter-spacing:1px; padding:0 3px;
}}
"""

# ══════════════════════════════════════════════════
#  수식 엔진
# ══════════════════════════════════════════════════
COL_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def col_letter_to_idx(s):
    """'A'→0, 'B'→1, 'AA'→26 …"""
    s = s.upper()
    result = 0
    for ch in s:
        result = result * 26 + (ord(ch) - ord('A') + 1)
    return result - 1

def idx_to_col_letter(n):
    s = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = COL_LETTERS[r] + s
    return s

def parse_cell_ref(ref, base_row=0, base_col=0):
    """'B3' → (row_idx, col_idx).  상대참조만 지원."""
    m = re.fullmatch(r'([A-Za-z]+)(\d+)', ref.strip())
    if not m:
        return None
    return int(m.group(2)) - 1, col_letter_to_idx(m.group(1))

def parse_range_ref(ref):
    """'A1:C3' → list of (r,c)"""
    m = re.fullmatch(r'([A-Za-z]+\d+):([A-Za-z]+\d+)', ref.strip())
    if not m:
        return None
    r1, c1 = parse_cell_ref(m.group(1))
    r2, c2 = parse_cell_ref(m.group(2))
    return [(r, c) for r in range(r1, r2+1) for c in range(c1, c2+1)]


class FormulaEngine:
    """
    =SUM(A1:B3), =AVERAGE(...), =IF(cond,t,f), =VLOOKUP(...) 등
    엑셀 스타일 수식을 Python으로 평가.
    """

    def __init__(self, get_cell_fn):
        # get_cell_fn(row, col) → raw string value
        self.get_cell = get_cell_fn

    def evaluate(self, formula, cur_row, cur_col):
        if not formula.startswith('='):
            return formula
        expr = formula[1:].strip()
        try:
            result = self._eval_expr(expr, cur_row, cur_col)
            if isinstance(result, float) and result == int(result):
                return str(int(result))
            if isinstance(result, float):
                return f"{result:.10g}"
            return str(result)
        except ZeroDivisionError:
            return "#DIV/0!"
        except Exception:
            return "#ERR!"

    def _eval_expr(self, expr, r, c):
        # 함수 호출 패턴
        m = re.fullmatch(r'([A-Za-z_][A-Za-z0-9_]*)\((.+)\)', expr, re.DOTALL)
        if m:
            fname = m.group(1).upper()
            args_str = m.group(2)
            return self._call_fn(fname, args_str, r, c)
        # 연산자 포함 표현식: 셀 참조 치환 후 eval
        resolved = self._resolve_refs(expr, r, c)
        return self._safe_eval(resolved)

    def _resolve_refs(self, expr, r, c):
        """수식 내 셀 참조(A1, B2 등)를 수치로 치환"""
        def replace_ref(m):
            ref = m.group(0)
            pos = parse_cell_ref(ref)
            if pos is None:
                return ref
            val = self.get_cell(pos[0], pos[1])
            try:
                return str(float(val))
            except Exception:
                return f'"{val}"'
        return re.sub(r'\b[A-Za-z]+\d+\b', replace_ref, expr)

    def _get_range_vals(self, args_str, r, c):
        """범위 또는 개별 셀 목록에서 숫자 값 추출"""
        vals = []
        # 쉼표로 분리된 인자들
        for arg in self._split_args(args_str):
            arg = arg.strip()
            # A1:B3 형태
            cells = parse_range_ref(arg)
            if cells:
                for (rr, cc) in cells:
                    v = self.get_cell(rr, cc)
                    try:
                        vals.append(float(v))
                    except Exception:
                        pass
                continue
            # 단일 셀
            pos = parse_cell_ref(arg)
            if pos:
                v = self.get_cell(pos[0], pos[1])
                try:
                    vals.append(float(v))
                except Exception:
                    pass
                continue
            # 숫자 리터럴
            try:
                vals.append(float(arg))
            except Exception:
                pass
        return vals

    def _split_args(self, s):
        """괄호 깊이를 고려한 쉼표 분리"""
        args, depth, cur = [], 0, []
        for ch in s:
            if ch == '(':
                depth += 1; cur.append(ch)
            elif ch == ')':
                depth -= 1; cur.append(ch)
            elif ch == ',' and depth == 0:
                args.append(''.join(cur)); cur = []
            else:
                cur.append(ch)
        if cur:
            args.append(''.join(cur))
        return args

    def _call_fn(self, fname, args_str, r, c):
        args = self._split_args(args_str)

        if fname == 'SUM':
            return sum(self._get_range_vals(args_str, r, c))
        if fname in ('AVERAGE', 'AVG'):
            v = self._get_range_vals(args_str, r, c)
            return sum(v) / len(v) if v else 0
        if fname == 'COUNT':
            return len(self._get_range_vals(args_str, r, c))
        if fname == 'COUNTA':
            count = 0
            for arg in args:
                arg = arg.strip()
                cells = parse_range_ref(arg)
                if cells:
                    for rr, cc in cells:
                        if self.get_cell(rr, cc).strip():
                            count += 1
                else:
                    pos = parse_cell_ref(arg)
                    if pos and self.get_cell(pos[0], pos[1]).strip():
                        count += 1
            return count
        if fname == 'MAX':
            v = self._get_range_vals(args_str, r, c)
            return max(v) if v else 0
        if fname == 'MIN':
            v = self._get_range_vals(args_str, r, c)
            return min(v) if v else 0
        if fname == 'ABS':
            return abs(float(self._eval_expr(args[0].strip(), r, c)))
        if fname == 'ROUND':
            val = float(self._eval_expr(args[0].strip(), r, c))
            dec = int(self._eval_expr(args[1].strip(), r, c)) if len(args) > 1 else 0
            return round(val, dec)
        if fname == 'SQRT':
            return math.sqrt(float(self._eval_expr(args[0].strip(), r, c)))
        if fname == 'INT':
            return int(float(self._eval_expr(args[0].strip(), r, c)))
        if fname == 'LEN':
            val = self.get_cell(*parse_cell_ref(args[0].strip())) if parse_cell_ref(args[0].strip()) else args[0].strip().strip('"')
            return len(str(val))
        if fname == 'UPPER':
            pos = parse_cell_ref(args[0].strip())
            val = self.get_cell(*pos) if pos else args[0].strip().strip('"')
            return str(val).upper()
        if fname == 'LOWER':
            pos = parse_cell_ref(args[0].strip())
            val = self.get_cell(*pos) if pos else args[0].strip().strip('"')
            return str(val).lower()
        if fname == 'CONCATENATE' or fname == 'CONCAT':
            parts = []
            for a in args:
                a = a.strip()
                pos = parse_cell_ref(a)
                if pos:
                    parts.append(str(self.get_cell(*pos)))
                else:
                    parts.append(str(self._eval_expr(a, r, c)))
            return ''.join(parts)
        if fname == 'IF':
            if len(args) < 2:
                return '#ERR!'
            cond_str = self._resolve_refs(args[0].strip(), r, c)
            cond = bool(self._safe_eval(cond_str))
            if cond:
                return self._eval_expr(args[1].strip(), r, c)
            else:
                return self._eval_expr(args[2].strip(), r, c) if len(args) > 2 else ''
        if fname == 'IFERROR':
            try:
                return self._eval_expr(args[0].strip(), r, c)
            except Exception:
                return self._eval_expr(args[1].strip(), r, c) if len(args) > 1 else ''
        if fname == 'VLOOKUP':
            # VLOOKUP(lookup_value, range, col_index)
            if len(args) < 3:
                return '#ERR!'
            lookup_val = str(self._eval_expr(args[0].strip(), r, c))
            cells = parse_range_ref(args[1].strip())
            col_idx = int(self._eval_expr(args[2].strip(), r, c)) - 1
            if not cells:
                return '#ERR!'
            rows_in_range = sorted(set(rc[0] for rc in cells))
            cols_in_range = sorted(set(rc[1] for rc in cells))
            for row in rows_in_range:
                if str(self.get_cell(row, cols_in_range[0])) == lookup_val:
                    target_col = cols_in_range[col_idx] if col_idx < len(cols_in_range) else cols_in_range[-1]
                    return self.get_cell(row, target_col)
            return '#N/A'
        if fname in ('NOW', 'TODAY'):
            from datetime import datetime
            return datetime.now().strftime('%Y-%m-%d')
        # 미지원 함수
        return f'#NAME?({fname})'

    def _safe_eval(self, expr):
        expr = expr.strip()
        # 문자열 리터럴
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        # 비교 연산자 → Python
        expr = re.sub(r'<>', '!=', expr)
        allowed = {
            'abs': abs, 'round': round, 'int': int, 'float': float,
            'min': min, 'max': max, 'sum': sum, 'len': len,
            'True': True, 'False': False,
        }
        return eval(compile(expr, '<cell>', 'eval'),
                    {"__builtins__": {}}, allowed)


# ══════════════════════════════════════════════════
#  커스텀 테이블
# ══════════════════════════════════════════════════
class SpreadsheetTable(QTableWidget):
    """Enter→아래이동, Ctrl+방향키 이동, Ctrl+C/V 처리"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_win = parent

    def keyPressEvent(self, event):
        key = event.key()
        mods = event.modifiers()

        # ── Enter: 아래 이동 ──
        if key in (Qt.Key_Return, Qt.Key_Enter) and not (mods & Qt.ControlModifier):
            if self.state() == QAbstractItemView.EditingState:
                self.commitData(self.itemDelegate())
                self.closePersistentEditor(self.currentItem())
            r, c = self.currentRow(), self.currentColumn()
            self.setCurrentCell(min(r + 1, self.rowCount() - 1), c)
            self.setFocus()
            return

        # ── Ctrl+C ──
        if key == Qt.Key_C and (mods & Qt.ControlModifier):
            self._copy_selection()
            return

        # ── Ctrl+V ──
        if key == Qt.Key_V and (mods & Qt.ControlModifier):
            self._paste_selection()
            return

        # ── Ctrl+D (Fill Down) ──
        if key == Qt.Key_D and (mods & Qt.ControlModifier):
            if self.main_win:
                self.main_win.fill_down()
            return

        # ── Ctrl+R (Fill Right) ──
        if key == Qt.Key_R and (mods & Qt.ControlModifier):
            if self.main_win:
                self.main_win.fill_right()
            return

        # ── Delete: 선택 셀 내용 삭제 ──
        if key == Qt.Key_Delete and not (mods & Qt.ControlModifier):
            for idx in self.selectedIndexes():
                item = self.item(idx.row(), idx.column())
                if item:
                    item.setText("")
            return

        super().keyPressEvent(event)

    def _copy_selection(self):
        indexes = self.selectedIndexes()
        if not indexes:
            return
        rows = sorted(set(i.row() for i in indexes))
        cols = sorted(set(i.column() for i in indexes))
        grid = []
        for r in rows:
            row_data = []
            for c in cols:
                item = self.item(r, c)
                row_data.append(item.text() if item else "")
            grid.append("\t".join(row_data))
        text = "\n".join(grid)
        QGuiApplication.clipboard().setText(text)
        if self.main_win:
            self.main_win.status_bar.showMessage(
                f"  📋 {len(rows)}행 × {len(cols)}열 복사", 2000
            )

    def _paste_selection(self):
        text = QGuiApplication.clipboard().text()
        if not text:
            return
        start_r = self.currentRow()
        start_c = self.currentColumn()
        rows_data = text.split("\n")
        for dr, row_text in enumerate(rows_data):
            cells = row_text.split("\t")
            for dc, val in enumerate(cells):
                r = start_r + dr
                c = start_c + dc
                if r < self.rowCount() and c < self.columnCount():
                    item = self.item(r, c)
                    if not item:
                        item = QTableWidgetItem("")
                        item.setFlags(item.flags() | Qt.ItemIsEditable)
                        self.setItem(r, c, item)
                    item.setText(val)
        if self.main_win:
            self.main_win.status_bar.showMessage("  📋 붙여넣기 완료", 2000)


# ══════════════════════════════════════════════════
#  필터 다이얼로그
# ══════════════════════════════════════════════════
class FilterDialog(QDialog):
    def __init__(self, col_name, unique_vals, active_filter, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"필터: {col_name}")
        self.setMinimumSize(260, 360)
        self.result_filter = None

        lay = QVBoxLayout(self)
        lay.setSpacing(8)

        # 검색
        self.search = QLineEdit()
        self.search.setPlaceholderText("검색...")
        self.search.textChanged.connect(self._on_search)
        lay.addWidget(self.search)

        # 전체선택
        self.chk_all = QCheckBox("(전체 선택)")
        self.chk_all.setChecked(True)
        self.chk_all.stateChanged.connect(self._toggle_all)
        lay.addWidget(self.chk_all)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background:{C['border']};")
        lay.addWidget(sep)

        # 스크롤 영역에 체크박스 목록
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        inner = QWidget()
        self.inner_lay = QVBoxLayout(inner)
        self.inner_lay.setSpacing(2)
        self.inner_lay.setContentsMargins(4, 4, 4, 4)
        scroll.setWidget(inner)
        lay.addWidget(scroll)

        self.checkboxes = []
        for v in sorted(unique_vals, key=lambda x: str(x)):
            chk = QCheckBox(str(v))
            chk.setChecked(active_filter is None or str(v) in active_filter)
            chk.stateChanged.connect(self._update_all_state)
            self.inner_lay.addWidget(chk)
            self.checkboxes.append((str(v), chk))
        self.inner_lay.addStretch()

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self._accept)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def _on_search(self, text):
        for val, chk in self.checkboxes:
            chk.setVisible(text.lower() in val.lower())

    def _toggle_all(self, state):
        for val, chk in self.checkboxes:
            if chk.isVisible():
                chk.blockSignals(True)
                chk.setChecked(state == Qt.Checked)
                chk.blockSignals(False)

    def _update_all_state(self):
        checked = [chk.isChecked() for _, chk in self.checkboxes if chk.isVisible()]
        self.chk_all.blockSignals(True)
        if all(checked):
            self.chk_all.setCheckState(Qt.Checked)
        elif any(checked):
            self.chk_all.setCheckState(Qt.PartiallyChecked)
        else:
            self.chk_all.setCheckState(Qt.Unchecked)
        self.chk_all.blockSignals(False)

    def _accept(self):
        selected = {val for val, chk in self.checkboxes if chk.isChecked()}
        all_vals = {val for val, _ in self.checkboxes}
        self.result_filter = None if selected == all_vals else selected
        self.accept()


# ══════════════════════════════════════════════════
#  조건부 서식 다이얼로그
# ══════════════════════════════════════════════════
class ConditionalFormatDialog(QDialog):
    def __init__(self, col_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"조건부 서식: {col_name}")
        self.setFixedSize(340, 220)
        self.result = None

        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        grp = QGroupBox("숫자 범위 하이라이트")
        g_lay = QGridLayout(grp)

        g_lay.addWidget(QLabel("최솟값 이상:"), 0, 0)
        self.min_spin = QDoubleSpinBox()
        self.min_spin.setRange(-1e9, 1e9); self.min_spin.setValue(0)
        g_lay.addWidget(self.min_spin, 0, 1)

        g_lay.addWidget(QLabel("최댓값 이하:"), 1, 0)
        self.max_spin = QDoubleSpinBox()
        self.max_spin.setRange(-1e9, 1e9); self.max_spin.setValue(100)
        g_lay.addWidget(self.max_spin, 1, 1)

        g_lay.addWidget(QLabel("배경색:"), 2, 0)
        self.color_btn = QPushButton("선택")
        self._color = QColor("#1a3a2a")
        self.color_btn.setStyleSheet(f"background-color:#1a3a2a;")
        self.color_btn.clicked.connect(self._pick_color)
        g_lay.addWidget(self.color_btn, 2, 1)

        lay.addWidget(grp)

        self.clear_chk = QCheckBox("이 열의 조건부 서식 제거")
        lay.addWidget(self.clear_chk)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self._accept)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def _pick_color(self):
        c = QColorDialog.getColor(self._color, self)
        if c.isValid():
            self._color = c
            self.color_btn.setStyleSheet(f"background-color:{c.name()};")

    def _accept(self):
        if self.clear_chk.isChecked():
            self.result = {"clear": True}
        else:
            self.result = {
                "min": self.min_spin.value(),
                "max": self.max_spin.value(),
                "color": self._color,
            }
        self.accept()


# ══════════════════════════════════════════════════
#  찾기 다이얼로그
# ══════════════════════════════════════════════════
class FindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("찾기")
        self.setFixedSize(340, 110)
        self.parent_window = parent

        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        row = QHBoxLayout()
        row.addWidget(QLabel("검색어:"))
        self.input = QLineEdit()
        self.input.setPlaceholderText("찾을 내용 입력...")
        self.input.returnPressed.connect(self.find_next)
        row.addWidget(self.input)
        lay.addLayout(row)

        btn_row = QHBoxLayout()
        self.find_btn = QPushButton("다음 찾기")
        self.find_btn.clicked.connect(self.find_next)
        close_btn = QPushButton("닫기")
        close_btn.clicked.connect(self.close)
        self.result_lbl = QLabel("")
        self.result_lbl.setStyleSheet(f"color:{C['text_dim']};font-size:11px;")
        btn_row.addWidget(self.result_lbl)
        btn_row.addStretch()
        btn_row.addWidget(self.find_btn)
        btn_row.addWidget(close_btn)
        lay.addLayout(btn_row)

        self._last_row = -1
        self._last_col = -1

    def find_next(self):
        keyword = self.input.text().strip().lower()
        if not keyword:
            return
        table = self.parent_window.table
        rows, cols = table.rowCount(), table.columnCount()
        start_r, start_c = self._last_row, self._last_col + 1

        for r in range(start_r, rows):
            c_start = start_c if r == start_r else 0
            for c in range(c_start, cols):
                item = table.item(r, c)
                if item and keyword in item.text().lower():
                    table.setCurrentCell(r, c)
                    table.scrollToItem(item)
                    self._last_row, self._last_col = r, c
                    self.result_lbl.setText(f"행 {r+1} · 열 {c+1}")
                    return

        for r in range(0, start_r + 1):
            c_end = start_c if r == start_r else cols
            for c in range(0, c_end):
                item = table.item(r, c)
                if item and keyword in item.text().lower():
                    table.setCurrentCell(r, c)
                    table.scrollToItem(item)
                    self._last_row, self._last_col = r, c
                    self.result_lbl.setText(f"행 {r+1} · 열 {c+1} (처음으로)")
                    return

        self.result_lbl.setText("결과 없음")
        self._last_row, self._last_col = -1, -1


# ══════════════════════════════════════════════════
#  푸터
# ══════════════════════════════════════════════════
class FooterBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(44)
        self.setObjectName("footer")
        self.setStyleSheet(f"QWidget#footer{{background:{C['surface']};border-top:1px solid {C['border']};}}")
        lay = QHBoxLayout(self)
        lay.setContentsMargins(20, 0, 20, 0)

        brand = QLabel("JOON · Excel Editor")
        brand.setStyleSheet(f"color:{C['text_muted']};font-size:11px;font-weight:600;letter-spacing:1.5px;")
        spacer = QWidget(); spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        email = QLabel(
            f'<a href="mailto:lotus031315@gmail.com" '
            f'style="color:{C["accent"]};text-decoration:none;font-size:12px;font-weight:500;">'
            f'✉&nbsp;&nbsp;lotus031315@gmail.com</a>'
        )
        email.setOpenExternalLinks(True)
        email.setTextInteractionFlags(Qt.TextBrowserInteraction)
        email.setCursor(QCursor(Qt.PointingHandCursor))

        dot = QLabel("·"); dot.setStyleSheet(f"color:{C['text_muted']};margin:0 8px;")
        web = QLabel(
            f'<a href="https://joon041415.github.io/" '
            f'style="color:{C["text_muted"]};text-decoration:none;font-size:12px;">'
            f'Portfolio ↗</a>'
        )
        web.setOpenExternalLinks(True)
        web.setTextInteractionFlags(Qt.TextBrowserInteraction)
        web.setCursor(QCursor(Qt.PointingHandCursor))

        for w in [brand, spacer, email, dot, web]:
            lay.addWidget(w)


# ══════════════════════════════════════════════════
#  메인 윈도우
# ══════════════════════════════════════════════════
class ExcelEditor(QMainWindow):

    # ── 청크 사이즈 (가상 스크롤) ──
    CHUNK = 200

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Editor")
        self.resize(1400, 860)

        # 데이터
        self.file_path = None
        self.last_dir = ""
        self.df_full = pd.DataFrame()    # 전체 원본
        self.df = pd.DataFrame()         # 현재 시트 (필터 전)
        self.df_view = pd.DataFrame()    # 현재 표시 (필터 후)

        # 수식 저장소: {(row, col): "=SUM(A1:B3)"}
        self.formulas: dict = {}

        # 상태
        self.loading_table = False
        self._undo_stack = []
        self._find_dialog = None

        # 필터: {col_idx: set of allowed string values | None}
        self.col_filters: dict = {}

        # 조건부 서식: {col_idx: {"min":..,"max":..,"color":QColor}}
        self.cond_formats: dict = {}

        # Freeze
        self.freeze_row = 0   # 고정 행 수
        self.freeze_col = 0   # 고정 열 수

        # 가상 스크롤 — 현재 로드된 청크 끝 행
        self._loaded_rows = 0

        # 수식 엔진
        self.engine = FormulaEngine(self._get_raw_cell)

        self.init_ui()
        self._setup_shortcuts()
        self.update_status()

    # ════════════════════════════════════
    #  UI 빌드
    # ════════════════════════════════════
    def init_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        rl = QVBoxLayout(root)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(0)

        rl.addWidget(self._build_toolbar())
        rl.addWidget(self._build_formula_bar())
        rl.addWidget(self._build_fn_panel())
        rl.addWidget(self._build_table_area())
        rl.addWidget(FooterBar())

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    # ── 툴바 ────────────────────────────
    def _build_toolbar(self):
        bar = QWidget()
        bar.setFixedHeight(50)
        bar.setStyleSheet(f"QWidget{{background:{C['surface']};border-bottom:1px solid {C['border']};}}")
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(12, 0, 12, 0)
        lay.setSpacing(5)

        title = QLabel("Excel Editor")
        title.setStyleSheet(f"color:{C['accent']};font-size:14px;font-weight:700;letter-spacing:0.5px;padding-right:10px;")

        self.open_btn    = self._tb_btn("📂 열기",       self.open_excel)
        self.new_btn     = self._tb_btn("＋ 새 파일",    self.new_file)
        self.save_btn    = self._tb_btn("💾 저장",       self.save_excel, obj="btn_save")
        self.save_as_btn = self._tb_btn("다른 이름으로", self.save_as_excel)

        s1 = self._vsep()

        self.add_row_btn = self._tb_btn("＋행", lambda: self.insert_row(self.table.currentRow()))
        self.del_row_btn = self._tb_btn("－행", self.delete_selected_rows, obj="btn_delete")
        self.add_col_btn = self._tb_btn("＋열", lambda: self.insert_col(self.table.currentColumn()))
        self.del_col_btn = self._tb_btn("－열", self.delete_selected_col, obj="btn_delete")

        s2 = self._vsep()

        # Freeze
        self.freeze_btn = self._tb_btn("🔒 고정", self.toggle_freeze)
        self.freeze_btn.setToolTip("현재 셀 기준으로 행/열 고정 (Freeze Pane)")

        s3 = self._vsep()

        lbl = QLabel("시트")
        lbl.setStyleSheet(f"color:{C['text_dim']};font-size:11px;")
        self.sheet_combo = QComboBox()
        self.sheet_combo.currentIndexChanged.connect(self.change_sheet)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        hint = QLabel("Ctrl+S 저장  │  Ctrl+Z 실행취소  │  Ctrl+F 찾기  │  Ctrl+D 아래채우기  │  Ctrl+R 오른쪽채우기")
        hint.setStyleSheet(f"color:{C['text_muted']};font-size:10px;")

        for w in [title, self.open_btn, self.new_btn, self.save_btn, self.save_as_btn,
                  s1, self.add_row_btn, self.del_row_btn,
                  self.add_col_btn, self.del_col_btn, s2,
                  self.freeze_btn, s3,
                  lbl, self.sheet_combo, spacer, hint]:
            lay.addWidget(w)
        return bar

    # ── Formula Bar ─────────────────────
    def _build_formula_bar(self):
        bar = QWidget()
        bar.setFixedHeight(36)
        bar.setStyleSheet(f"QWidget{{background:{C['formula_bg']};border-bottom:1px solid #1a3a2a;}}")
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(8, 0, 8, 0)
        lay.setSpacing(6)

        # 셀 주소 (A1 스타일)
        self.cell_ref_box = QLineEdit("A1")
        self.cell_ref_box.setObjectName("cell_ref")
        self.cell_ref_box.returnPressed.connect(self._cell_ref_navigate)

        # fx 레이블
        fx_lbl = QLabel("ƒx")
        fx_lbl.setStyleSheet(f"color:{C['accent']};font-size:14px;font-weight:700;font-style:italic;padding:0 4px;")

        # 수식/값 입력 바
        self.formula_bar = QLineEdit()
        self.formula_bar.setObjectName("formula_bar")
        self.formula_bar.setPlaceholderText("값 또는 수식 입력 (예: =SUM(A1:B10))")
        self.formula_bar.returnPressed.connect(self._formula_bar_commit)
        self.formula_bar.textEdited.connect(self._formula_bar_edited)

        lay.addWidget(self.cell_ref_box)
        lay.addWidget(fx_lbl)
        lay.addWidget(self.formula_bar, 1)
        return bar

    # ── 함수 패널 ───────────────────────
    def _build_fn_panel(self):
        panel = QWidget()
        panel.setObjectName("fn_panel")
        panel.setFixedHeight(40)
        lay = QHBoxLayout(panel)
        lay.setContentsMargins(10, 0, 10, 0)
        lay.setSpacing(4)

        lbl = QLabel("FUNC"); lbl.setObjectName("fn_title")
        lay.addWidget(lbl); lay.addWidget(self._vsep())

        for name, slot in [
            ("SUM", self._fn_sum), ("AVG", self._fn_avg),
            ("COUNT", self._fn_count), ("MAX", self._fn_max),
            ("MIN", self._fn_min), ("COUNTA", self._fn_counta),
        ]:
            b = QPushButton(name); b.setObjectName("fn_btn")
            b.setFixedHeight(26); b.clicked.connect(slot)
            b.setToolTip(f"선택 열에 {name} 적용")
            lay.addWidget(b)

        lay.addWidget(self._vsep())
        lbl2 = QLabel("SORT"); lbl2.setObjectName("fn_title")
        lay.addWidget(lbl2)
        for name, asc in [("↑ 오름", True), ("↓ 내림", False)]:
            b = QPushButton(name); b.setObjectName("fn_btn")
            b.setFixedHeight(26); b.clicked.connect(lambda _, a=asc: self._sort_by_col(a))
            lay.addWidget(b)

        lay.addWidget(self._vsep())
        dedup = QPushButton("중복제거"); dedup.setObjectName("fn_btn")
        dedup.setFixedHeight(26); dedup.clicked.connect(self._fn_dedup)
        lay.addWidget(dedup)

        lay.addWidget(self._vsep())
        lbl3 = QLabel("결과:"); lbl3.setObjectName("fn_title")
        lay.addWidget(lbl3)
        self.fn_result = QLabel("—"); self.fn_result.setObjectName("fn_result")
        lay.addWidget(self.fn_result)

        lay.addStretch()
        return panel

    # ── 테이블 영역 ─────────────────────
    def _build_table_area(self):
        container = QWidget()
        container.setStyleSheet(f"background:{C['bg']};")
        lay = QVBoxLayout(container)
        lay.setContentsMargins(10, 8, 10, 6)

        self.table = SpreadsheetTable(self)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(24)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.itemChanged.connect(self.cell_changed)
        self.table.currentCellChanged.connect(self._on_cell_selected)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

        # 헤더 더블클릭 → 열 이름 편집
        self.table.horizontalHeader().sectionDoubleClicked.connect(self.edit_column_name)
        # 헤더 우클릭 → 필터/조건부서식 메뉴
        self.table.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.horizontalHeader().customContextMenuRequested.connect(self._header_context_menu)

        # 가상 스크롤: 스크롤 끝 근처에서 추가 로드
        self.table.verticalScrollBar().valueChanged.connect(self._on_scroll)

        self.table.itemSelectionChanged.connect(self._on_selection_changed)

        lay.addWidget(self.table)
        return container

    # ════════════════════════════════════
    #  단축키
    # ════════════════════════════════════
    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+S"),       self).activated.connect(self.save_excel)
        QShortcut(QKeySequence("Ctrl+Shift+S"), self).activated.connect(self.save_as_excel)
        QShortcut(QKeySequence("Ctrl+Z"),       self).activated.connect(self.undo)
        QShortcut(QKeySequence("Ctrl+F"),       self).activated.connect(self.open_find)
        QShortcut(QKeySequence("Ctrl+A"),       self).activated.connect(self.table.selectAll)
        QShortcut(QKeySequence("Ctrl+Return"),  self).activated.connect(
            lambda: self.insert_row(self.table.currentRow() + 1))
        QShortcut(QKeySequence("Ctrl+Up"),    self).activated.connect(lambda: self._jump("up"))
        QShortcut(QKeySequence("Ctrl+Down"),  self).activated.connect(lambda: self._jump("down"))
        QShortcut(QKeySequence("Ctrl+Left"),  self).activated.connect(lambda: self._jump("left"))
        QShortcut(QKeySequence("Ctrl+Right"), self).activated.connect(lambda: self._jump("right"))
        QShortcut(QKeySequence("Ctrl+Home"),  self).activated.connect(lambda: self._goto(0, 0))
        QShortcut(QKeySequence("Ctrl+End"),   self).activated.connect(
            lambda: self._goto(self.table.rowCount()-1, self.table.columnCount()-1))
        QShortcut(QKeySequence("Ctrl+Delete"),self).activated.connect(self.delete_selected_rows)

    # ════════════════════════════════════
    #  셀 이동 헬퍼
    # ════════════════════════════════════
    def _jump(self, direction):
        r, c = self.table.currentRow(), self.table.currentColumn()
        rows, cols = self.table.rowCount(), self.table.columnCount()
        if r < 0 or c < 0:
            return

        def has(rr, cc):
            item = self.table.item(rr, cc)
            return bool(item and item.text())

        if direction == "up":
            if r == 0: return
            if not has(r, c):
                for i in range(r-1, -1, -1):
                    if has(i, c): self._goto(i, c); return
                self._goto(0, c)
            else:
                if not has(r-1, c):
                    for i in range(r-2, -1, -1):
                        if has(i, c): self._goto(i, c); return
                    self._goto(0, c)
                else:
                    t = 0
                    for i in range(r-1, -1, -1):
                        if not has(i, c): t = i+1; break
                    self._goto(t, c)
        elif direction == "down":
            if r == rows-1: return
            if not has(r, c):
                for i in range(r+1, rows):
                    if has(i, c): self._goto(i, c); return
                self._goto(rows-1, c)
            else:
                if not has(r+1, c):
                    for i in range(r+2, rows):
                        if has(i, c): self._goto(i, c); return
                    self._goto(rows-1, c)
                else:
                    t = rows-1
                    for i in range(r+1, rows):
                        if not has(i, c): t = i-1; break
                    self._goto(t, c)
        elif direction == "left":
            if c == 0: return
            if not has(r, c):
                for j in range(c-1, -1, -1):
                    if has(r, j): self._goto(r, j); return
                self._goto(r, 0)
            else:
                if not has(r, c-1):
                    for j in range(c-2, -1, -1):
                        if has(r, j): self._goto(r, j); return
                    self._goto(r, 0)
                else:
                    t = 0
                    for j in range(c-1, -1, -1):
                        if not has(r, j): t = j+1; break
                    self._goto(r, t)
        elif direction == "right":
            if c == cols-1: return
            if not has(r, c):
                for j in range(c+1, cols):
                    if has(r, j): self._goto(r, j); return
                self._goto(r, cols-1)
            else:
                if not has(r, c+1):
                    for j in range(c+2, cols):
                        if has(r, j): self._goto(r, j); return
                    self._goto(r, cols-1)
                else:
                    t = cols-1
                    for j in range(c+1, cols):
                        if not has(r, j): t = j-1; break
                    self._goto(r, t)

    def _goto(self, row, col):
        row = max(0, min(row, self.table.rowCount()-1))
        col = max(0, min(col, self.table.columnCount()-1))
        self.table.setCurrentCell(row, col)
        item = self.table.item(row, col)
        if item:
            self.table.scrollToItem(item)

    # ════════════════════════════════════
    #  Formula Bar 연동
    # ════════════════════════════════════
    def _on_cell_selected(self, row, col, prev_row, prev_col):
        if row < 0 or col < 0:
            return
        col_letter = idx_to_col_letter(col)
        self.cell_ref_box.setText(f"{col_letter}{row + 1}")

        # 수식이 있으면 수식 표시, 없으면 값 표시
        formula = self.formulas.get((row, col), "")
        if formula:
            self.formula_bar.setText(formula)
        else:
            item = self.table.item(row, col)
            self.formula_bar.setText(item.text() if item else "")

    def _formula_bar_edited(self, text):
        """포뮬러 바 입력 중 — 아직 커밋하지 않음"""
        pass

    def _formula_bar_commit(self):
        """포뮬러 바 Enter → 현재 셀에 적용"""
        r, c = self.table.currentRow(), self.table.currentColumn()
        if r < 0 or c < 0:
            return
        text = self.formula_bar.text()
        self.loading_table = True
        item = self.table.item(r, c)
        if not item:
            item = QTableWidgetItem("")
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.table.setItem(r, c, item)

        if text.startswith("="):
            self.formulas[(r, c)] = text
            result = self.engine.evaluate(text, r, c)
            item.setText(result)
            self._update_df_cell(r, c, result)
        else:
            self.formulas.pop((r, c), None)
            item.setText(text)
            self._update_df_cell(r, c, text)

        self.loading_table = False
        # 의존 셀 재계산
        self._recalc_all()
        self.table.setCurrentCell(r + 1, c)

    def _cell_ref_navigate(self):
        """셀 주소 입력 후 Enter → 해당 셀로 이동"""
        ref = self.cell_ref_box.text().strip()
        pos = parse_cell_ref(ref)
        if pos:
            self._goto(pos[0], pos[1])

    # ════════════════════════════════════
    #  수식 재계산
    # ════════════════════════════════════
    def _get_raw_cell(self, row, col):
        """수식 엔진용: 셀의 표시값 반환"""
        if row < 0 or col < 0:
            return ""
        if row >= self.table.rowCount() or col >= self.table.columnCount():
            return ""
        item = self.table.item(row, col)
        return item.text() if item else ""

    def _recalc_all(self):
        """수식이 있는 모든 셀 재계산"""
        if not self.formulas:
            return
        self.loading_table = True
        for (r, c), formula in list(self.formulas.items()):
            if r >= self.table.rowCount() or c >= self.table.columnCount():
                continue
            result = self.engine.evaluate(formula, r, c)
            item = self.table.item(r, c)
            if item:
                item.setText(result)
                self._update_df_cell(r, c, result)
        self.loading_table = False

    def _update_df_cell(self, r, c, value):
        if r < len(self.df_view.index) and c < len(self.df_view.columns):
            converted = self._convert_value(value)
            self.df_view.iat[r, c] = converted
            # df 원본에도 반영
            orig_idx = self.df_view.index[r]
            self.df.at[orig_idx, self.df.columns[c]] = converted

    # ════════════════════════════════════
    #  가상 스크롤 (청크 로딩)
    # ════════════════════════════════════
    def _on_scroll(self, value):
        sb = self.table.verticalScrollBar()
        # 스크롤 90% 이상 도달하면 다음 청크 로드
        if sb.maximum() > 0 and value / sb.maximum() > 0.88:
            self._load_next_chunk()

    def _load_next_chunk(self):
        total = len(self.df_view)
        if self._loaded_rows >= total:
            return
        end = min(self._loaded_rows + self.CHUNK, total)
        self.loading_table = True
        cols = len(self.df_view.columns)
        self.table.setRowCount(end)
        for r in range(self._loaded_rows, end):
            for c in range(cols):
                val = self.df_view.iat[r, c]
                text = "" if pd.isna(val) else str(val)
                item = QTableWidgetItem(text)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.table.setItem(r, c, item)
            self._apply_row_cond_format(r)
        self._apply_freeze_visual()
        self.loading_table = False
        self._loaded_rows = end
        if end < total:
            self.status_bar.showMessage(
                f"  {self._loaded_rows}/{total}행 로드됨 — 스크롤하면 더 불러옵니다", 2000
            )

    def _reload_table_from_df(self):
        """df_view → table 전체 재렌더링 (필터/정렬 후 공통 사용)"""
        was = self.loading_table
        self.loading_table = True
        self.table.clearContents()
        rows, cols = len(self.df_view), len(self.df_view.columns)

        # 청크 첫 배치만 렌더
        first_batch = min(rows, self.CHUNK)
        self.table.setRowCount(first_batch)
        self.table.setColumnCount(cols)
        self.table.setHorizontalHeaderLabels([str(c) for c in self.df_view.columns])

        for r in range(first_batch):
            for c in range(cols):
                val = self.df_view.iat[r, c]
                text = "" if pd.isna(val) else str(val)
                item = QTableWidgetItem(text)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.table.setItem(r, c, item)
            self._apply_row_cond_format(r)

        self.table.resizeColumnsToContents()
        self._apply_freeze_visual()
        self.loading_table = was
        self._loaded_rows = first_batch

        # 수식 재계산
        self._recalc_all()

        # 필터 버튼 업데이트
        self._update_filter_indicators()
        self.update_status()

    # ════════════════════════════════════
    #  필터
    # ════════════════════════════════════
    def _header_context_menu(self, position):
        col = self.table.horizontalHeader().logicalIndexAt(position)
        if col < 0:
            return
        col_name = str(self.df_view.columns[col]) if col < len(self.df_view.columns) else ""
        menu = QMenu()
        filter_action  = menu.addAction(f"🔽  필터 설정: {col_name}")
        clear_filter   = menu.addAction("✕  이 열 필터 제거")
        clear_all      = menu.addAction("✕  전체 필터 제거")
        menu.addSeparator()
        cond_fmt       = menu.addAction(f"🎨  조건부 서식: {col_name}")
        menu.addSeparator()
        rename_action  = menu.addAction("✏  열 이름 수정")
        auto_fit       = menu.addAction("↔  열 너비 자동 맞춤")

        action = menu.exec(self.table.horizontalHeader().mapToGlobal(position))
        if action == filter_action:
            self._show_filter_dialog(col)
        elif action == clear_filter:
            self.col_filters.pop(col, None)
            self._apply_filters()
        elif action == clear_all:
            self.col_filters.clear()
            self._apply_filters()
        elif action == cond_fmt:
            self._show_cond_format_dialog(col)
        elif action == rename_action:
            self.edit_column_name(col)
        elif action == auto_fit:
            self.table.resizeColumnToContents(col)

    def _show_filter_dialog(self, col):
        if col >= len(self.df.columns):
            return
        col_name = str(self.df.columns[col])
        unique_vals = self.df.iloc[:, col].dropna().astype(str).unique().tolist()
        active = self.col_filters.get(col)
        dlg = FilterDialog(col_name, unique_vals, active, self)
        if dlg.exec() == QDialog.Accepted:
            if dlg.result_filter is None:
                self.col_filters.pop(col, None)
            else:
                self.col_filters[col] = dlg.result_filter
            self._apply_filters()

    def _apply_filters(self):
        result = self.df.copy()
        for col_idx, allowed in self.col_filters.items():
            if allowed is not None and col_idx < len(result.columns):
                col_name = result.columns[col_idx]
                result = result[result[col_name].astype(str).isin(allowed)]
        self.df_view = result.reset_index(drop=True)
        self._reload_table_from_df()

    def _update_filter_indicators(self):
        """필터 적용된 헤더에 시각적 표시"""
        for c in range(self.table.columnCount()):
            header_item = self.table.horizontalHeaderItem(c)
            if header_item is None:
                continue
            col_name = header_item.text()
            base_name = col_name.lstrip("▼ ")
            if c in self.col_filters:
                header_item.setText(f"▼ {base_name}")
                header_item.setForeground(QBrush(QColor(C['accent'])))
            else:
                header_item.setText(base_name)
                header_item.setForeground(QBrush(QColor(C['text_dim'])))

    # ════════════════════════════════════
    #  조건부 서식
    # ════════════════════════════════════
    def _show_cond_format_dialog(self, col):
        if col >= len(self.df_view.columns):
            return
        col_name = str(self.df_view.columns[col])
        dlg = ConditionalFormatDialog(col_name, self)
        if dlg.exec() == QDialog.Accepted and dlg.result:
            if dlg.result.get("clear"):
                self.cond_formats.pop(col, None)
            else:
                self.cond_formats[col] = dlg.result
            self._repaint_cond_formats()

    def _apply_row_cond_format(self, row):
        """특정 행에 조건부 서식 적용"""
        for col, fmt in self.cond_formats.items():
            if col >= self.table.columnCount():
                continue
            item = self.table.item(row, col)
            if not item:
                continue
            try:
                val = float(item.text())
                if fmt["min"] <= val <= fmt["max"]:
                    item.setBackground(QBrush(fmt["color"]))
                else:
                    item.setBackground(QBrush(QColor(C['surface'])))
            except (ValueError, TypeError):
                pass

    def _repaint_cond_formats(self):
        for r in range(self.table.rowCount()):
            self._apply_row_cond_format(r)

    # ════════════════════════════════════
    #  Freeze Pane
    # ════════════════════════════════════
    def toggle_freeze(self):
        r, c = self.table.currentRow(), self.table.currentColumn()
        if self.freeze_row == r and self.freeze_col == c:
            # 이미 같은 위치 → 해제
            self.freeze_row = 0
            self.freeze_col = 0
            self.status_bar.showMessage("  🔓 고정 해제", 2000)
        else:
            self.freeze_row = r
            self.freeze_col = c
            self.status_bar.showMessage(
                f"  🔒 {r}행 / {c}열까지 고정", 2000
            )
        self._apply_freeze_visual()

    def _apply_freeze_visual(self):
        """고정 행/열에 시각적 구분선 색 적용"""
        freeze_color = QColor(C['freeze_line'])
        normal_bg_even = QColor(C['surface'])
        normal_bg_odd  = QColor(C['surface2'])

        for r in range(self.table.rowCount()):
            for c in range(self.table.columnCount()):
                item = self.table.item(r, c)
                if item is None:
                    continue
                is_frozen = (r < self.freeze_row) or (c < self.freeze_col)
                if is_frozen and (self.freeze_row > 0 or self.freeze_col > 0):
                    item.setBackground(QBrush(QColor("#0e1f17")))
                    item.setForeground(QBrush(QColor(C['text'])))
                else:
                    # 조건부 서식이 있으면 그걸 우선
                    if c in self.cond_formats:
                        self._apply_row_cond_format(r)
                    # 아니면 기본 배경 복원 (setAlternatingRowColors가 QSS에서 처리)

    # ════════════════════════════════════
    #  AutoFill (Fill Down / Fill Right)
    # ════════════════════════════════════
    def fill_down(self):
        """Ctrl+D: 선택 첫 행 값/수식을 아래 행들에 채우기"""
        indexes = self.table.selectedIndexes()
        if not indexes:
            return
        cols_selected = sorted(set(i.column() for i in indexes))
        rows_selected = sorted(set(i.row() for i in indexes))
        if len(rows_selected) < 2:
            return
        source_row = rows_selected[0]
        for c in cols_selected:
            src_item = self.table.item(source_row, c)
            src_val = src_item.text() if src_item else ""
            src_formula = self.formulas.get((source_row, c), "")
            for r in rows_selected[1:]:
                item = self.table.item(r, c)
                if not item:
                    item = QTableWidgetItem("")
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    self.table.setItem(r, c, item)
                if src_formula:
                    # 수식 행 번호 오프셋 적용
                    offset = r - source_row
                    new_formula = self._offset_formula(src_formula, offset, 0)
                    self.formulas[(r, c)] = new_formula
                    result = self.engine.evaluate(new_formula, r, c)
                    item.setText(result)
                else:
                    item.setText(src_val)
        self._recalc_all()
        self.status_bar.showMessage("  ↓ Fill Down 완료", 2000)

    def fill_right(self):
        """Ctrl+R: 선택 첫 열 값/수식을 오른쪽 열들에 채우기"""
        indexes = self.table.selectedIndexes()
        if not indexes:
            return
        rows_selected = sorted(set(i.row() for i in indexes))
        cols_selected = sorted(set(i.column() for i in indexes))
        if len(cols_selected) < 2:
            return
        source_col = cols_selected[0]
        for r in rows_selected:
            src_item = self.table.item(r, source_col)
            src_val = src_item.text() if src_item else ""
            src_formula = self.formulas.get((r, source_col), "")
            for c in cols_selected[1:]:
                item = self.table.item(r, c)
                if not item:
                    item = QTableWidgetItem("")
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    self.table.setItem(r, c, item)
                if src_formula:
                    offset = c - source_col
                    new_formula = self._offset_formula(src_formula, 0, offset)
                    self.formulas[(r, c)] = new_formula
                    result = self.engine.evaluate(new_formula, r, c)
                    item.setText(result)
                else:
                    item.setText(src_val)
        self._recalc_all()
        self.status_bar.showMessage("  → Fill Right 완료", 2000)

    def _offset_formula(self, formula, row_offset, col_offset):
        """수식 내 셀 참조의 행/열 번호를 오프셋만큼 이동 (상대참조)"""
        def shift_ref(m):
            col_str = m.group(1)
            row_num = int(m.group(2))
            new_row = row_num + row_offset
            new_col_idx = col_letter_to_idx(col_str) + col_offset
            new_col_str = idx_to_col_letter(new_col_idx)
            return f"{new_col_str}{new_row}"
        return re.sub(r'([A-Za-z]+)(\d+)', shift_ref, formula)

    # ════════════════════════════════════
    #  파일 작업
    # ════════════════════════════════════
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
            self.formulas.clear()
            self.col_filters.clear()
            self.cond_formats.clear()
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
        cols = [chr(65 + i) for i in range(10)]
        self.df = pd.DataFrame([[None]*10 for _ in range(10)], columns=cols)
        self.df_view = self.df.copy()
        self.formulas.clear()
        self.col_filters.clear()
        self.cond_formats.clear()
        w = pd.ExcelWriter(path, engine="openpyxl")
        self.df.to_excel(w, sheet_name="Sheet1", index=False)
        w.close()
        self.sheet_combo.blockSignals(True)
        self.sheet_combo.clear()
        self.sheet_combo.addItems(["Sheet1"])
        self.sheet_combo.blockSignals(False)
        self.load_sheet("Sheet1")
        self.setWindowTitle(f"Excel Editor — {path.replace(chr(92),'/').split('/')[-1]}")

    # ════════════════════════════════════
    #  시트 관리
    # ════════════════════════════════════
    def load_sheet(self, sheet_name):
        try:
            self.df = pd.read_excel(self.file_path, sheet_name=sheet_name, dtype=object)
            self.df_view = self.df.copy()
            self.col_filters.clear()
            self._reload_table_from_df()
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))

    def change_sheet(self):
        name = self.sheet_combo.currentText()
        if name:
            self.formulas.clear()
            self.load_sheet(name)

    # ════════════════════════════════════
    #  셀 편집
    # ════════════════════════════════════
    def cell_changed(self, item):
        if self.loading_table:
            return
        r, c = item.row(), item.column()
        text = item.text()

        # 수식 입력 감지
        if text.startswith("="):
            self.formulas[(r, c)] = text
            result = self.engine.evaluate(text, r, c)
            self.loading_table = True
            item.setText(result)
            self.loading_table = False
            self._update_df_cell(r, c, result)
            # formula bar 업데이트
            self.formula_bar.setText(text)
            QTimer.singleShot(0, self._recalc_all)
            return

        # 일반 값
        old_val = self.df_view.iat[r, c] if r < len(self.df_view) and c < len(self.df_view.columns) else None
        self._undo_stack.append((r, c, old_val, self.formulas.get((r, c))))
        if len(self._undo_stack) > 200:
            self._undo_stack.pop(0)

        self.formulas.pop((r, c), None)
        new_val = None if text == "" else self._convert_value(text)
        self._update_df_cell(r, c, new_val if new_val is not None else text)

        # 조건부 서식 재적용
        if c in self.cond_formats:
            self._apply_row_cond_format(r)

        # formula bar 동기화
        self.formula_bar.setText(text)
        self.update_status()

    def undo(self):
        if not self._undo_stack:
            self.status_bar.showMessage("⚠  실행취소 내역 없음", 2000)
            return
        r, c, old_val, old_formula = self._undo_stack.pop()
        self.loading_table = True
        text = "" if old_val is None or (isinstance(old_val, float) and pd.isna(old_val)) else str(old_val)
        item = self.table.item(r, c)
        if item:
            item.setText(text)
        if old_formula:
            self.formulas[(r, c)] = old_formula
        else:
            self.formulas.pop((r, c), None)
        self.loading_table = False
        self._update_df_cell(r, c, old_val)
        self.table.setCurrentCell(r, c)
        self.status_bar.showMessage(f"↩  실행취소 — 행{r+1} 열{c+1}", 2000)

    def _convert_value(self, value):
        try:
            if str(value).isdigit():
                return int(value)
            return float(value)
        except Exception:
            return value

    # ════════════════════════════════════
    #  행/열 조작
    # ════════════════════════════════════
    def insert_row(self, row):
        if row < 0:
            row = self.table.rowCount()
        cols = len(self.df_view.columns)
        upper = self.df_view.iloc[:row]
        lower = self.df_view.iloc[row:]
        empty = pd.DataFrame([[None]*cols], columns=self.df_view.columns)
        self.df_view = pd.concat([upper, empty, lower], ignore_index=True)
        self.df = self.df_view.copy()
        self.table.insertRow(row)
        for c in range(cols):
            item = QTableWidgetItem("")
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.table.setItem(row, c, item)
        self.table.setCurrentCell(row, 0)
        self.update_status()

    def delete_selected_rows(self):
        rows = sorted(set(i.row() for i in self.table.selectedIndexes()), reverse=True)
        if not rows:
            QMessageBox.warning(self, "선택 필요", "삭제할 행을 선택하세요.")
            return
        if len(rows) > 1:
            ans = QMessageBox.question(self, "행 삭제", f"{len(rows)}개 행을 삭제할까요?",
                                       QMessageBox.Yes | QMessageBox.No)
            if ans != QMessageBox.Yes:
                return
        for r in rows:
            self.table.removeRow(r)
            self.df_view = self.df_view.drop(self.df_view.index[r]).reset_index(drop=True)
        self.df = self.df_view.copy()
        self.update_status()

    def insert_col(self, col):
        if col < 0:
            col = self.table.columnCount()
        existing = list(self.df_view.columns)
        new_name = self._unique_col_name("NewCol", existing)
        self.df_view.insert(col, new_name, None)
        self.df = self.df_view.copy()
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
            ans = QMessageBox.question(self, "열 삭제", f"{len(cols)}개 열을 삭제할까요?",
                                       QMessageBox.Yes | QMessageBox.No)
            if ans != QMessageBox.Yes:
                return
        for c in cols:
            self.table.removeColumn(c)
            col_name = self.df_view.columns[c]
            self.df_view = self.df_view.drop(columns=[col_name])
        self.df = self.df_view.copy()
        self.update_status()

    def _unique_col_name(self, base, existing):
        if base not in existing:
            return base
        i = 1
        while f"{base}{i}" in existing:
            i += 1
        return f"{base}{i}"

    # ════════════════════════════════════
    #  열 이름 편집
    # ════════════════════════════════════
    def edit_column_name(self, col_idx):
        current = self.df_view.columns[col_idx] if col_idx < len(self.df_view.columns) else ""
        dlg = QDialog(self)
        dlg.setWindowTitle("열 이름 수정")
        dlg.setFixedSize(320, 110)
        lay = QVBoxLayout(dlg)
        lay.setSpacing(10)
        row = QHBoxLayout()
        row.addWidget(QLabel("새 이름:"))
        inp = QLineEdit(str(current))
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
        if not new_name or new_name == str(current):
            return
        if new_name in [str(c) for c in self.df_view.columns]:
            QMessageBox.warning(self, "중복 이름", f"'{new_name}' 열이 이미 존재합니다.")
            return
        old_name = self.df_view.columns[col_idx]
        self.df_view = self.df_view.rename(columns={old_name: new_name})
        self.df = self.df.rename(columns={old_name: new_name})
        self.loading_table = True
        item = self.table.horizontalHeaderItem(col_idx)
        if item:
            item.setText(new_name)
        else:
            self.table.setHorizontalHeaderItem(col_idx, QTableWidgetItem(new_name))
        self.loading_table = False
        self.status_bar.showMessage(f"  열 이름 변경: '{old_name}' → '{new_name}'", 3000)

    # ════════════════════════════════════
    #  함수 패널 집계
    # ════════════════════════════════════
    def _selected_col_nums(self):
        indexes = self.table.selectedIndexes()
        if not indexes:
            return None, None
        col = indexes[0].column()
        rows = sorted(set(i.row() for i in indexes))
        vals = []
        for r in rows:
            item = self.table.item(r, col)
            if item and item.text():
                try:
                    vals.append(float(item.text()))
                except ValueError:
                    pass
        col_name = self.table.horizontalHeaderItem(col).text() if self.table.horizontalHeaderItem(col) else f"Col{col}"
        return vals, col_name

    def _selected_col_all(self):
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

    def _show_fn(self, label, value):
        if isinstance(value, float) and value == int(value):
            self.fn_result.setText(f"{label} = {int(value):,}")
        elif isinstance(value, float):
            self.fn_result.setText(f"{label} = {value:,.6g}")
        else:
            self.fn_result.setText(f"{label} = {value}")

    def _fn_sum(self):
        v, col = self._selected_col_nums()
        if v is None: self.fn_result.setText("행 선택 필요"); return
        self._show_fn(f"SUM({col})", sum(v))
    def _fn_avg(self):
        v, col = self._selected_col_nums()
        if not v: self.fn_result.setText("숫자 없음"); return
        self._show_fn(f"AVG({col})", sum(v)/len(v))
    def _fn_count(self):
        v, col = self._selected_col_nums()
        if v is None: self.fn_result.setText("행 선택 필요"); return
        self._show_fn(f"COUNT({col})", len(v))
    def _fn_counta(self):
        items, col = self._selected_col_all()
        if items is None: self.fn_result.setText("행 선택 필요"); return
        self._show_fn(f"COUNTA({col})", sum(1 for v in items if v.strip()))
    def _fn_max(self):
        v, col = self._selected_col_nums()
        if not v: self.fn_result.setText("숫자 없음"); return
        self._show_fn(f"MAX({col})", max(v))
    def _fn_min(self):
        v, col = self._selected_col_nums()
        if not v: self.fn_result.setText("숫자 없음"); return
        self._show_fn(f"MIN({col})", min(v))

    def _sort_by_col(self, ascending=True):
        indexes = self.table.selectedIndexes()
        if not indexes:
            self.fn_result.setText("열 선택 필요"); return
        col_idx = indexes[0].column()
        col_name = self.df_view.columns[col_idx]
        self.df_view = self.df_view.sort_values(
            by=col_name, ascending=ascending,
            key=lambda s: pd.to_numeric(s, errors='coerce').fillna(s)
        ).reset_index(drop=True)
        self.df = self.df_view.copy()
        self._reload_table_from_df()
        self.fn_result.setText(f"정렬: {col_name} {'↑' if ascending else '↓'}")

    def _fn_dedup(self):
        before = len(self.df_view)
        self.df_view = self.df_view.drop_duplicates().reset_index(drop=True)
        self.df = self.df_view.copy()
        removed = before - len(self.df_view)
        self._reload_table_from_df()
        self.fn_result.setText(f"중복제거: {removed}행 삭제")

    def _on_selection_changed(self):
        self.fn_result.setText("—")

    # ════════════════════════════════════
    #  저장
    # ════════════════════════════════════
    def save_excel(self):
        if self.file_path is None:
            self.save_as_excel(); return
        self._write_excel(self.file_path)

    def save_as_excel(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "다른 이름으로 저장", self.last_dir, "Excel Files (*.xlsx)")
        if not path:
            return
        self.file_path = path
        self.last_dir = path.replace("\\", "/").rsplit("/", 1)[0]
        self._write_excel(path)
        self.setWindowTitle(f"Excel Editor — {path.replace(chr(92),'/').split('/')[-1]}")

    def _write_excel(self, path):
        try:
            sheet = self.sheet_combo.currentText() or "Sheet1"
            with pd.ExcelWriter(path, engine="openpyxl", mode="a",
                                if_sheet_exists="replace") as writer:
                self.df_view.to_excel(writer, sheet_name=sheet, index=False)
            self.status_bar.showMessage("✓  저장 완료", 3000)
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", str(e))

    # ════════════════════════════════════
    #  찾기
    # ════════════════════════════════════
    def open_find(self):
        if self._find_dialog is None or not self._find_dialog.isVisible():
            self._find_dialog = FindDialog(self)
        self._find_dialog.show()
        self._find_dialog.raise_()
        self._find_dialog.input.setFocus()

    # ════════════════════════════════════
    #  컨텍스트 메뉴
    # ════════════════════════════════════
    def show_context_menu(self, position):
        menu = QMenu()
        add_above  = menu.addAction("⬆  위에 행 추가  [Ctrl+Enter]")
        add_below  = menu.addAction("⬇  아래에 행 추가")
        del_row    = menu.addAction("🗑  행 삭제  [Ctrl+Del]")
        menu.addSeparator()
        add_col_l  = menu.addAction("◀  왼쪽에 열 추가")
        add_col_r  = menu.addAction("▶  오른쪽에 열 추가")
        del_col    = menu.addAction("✂  열 삭제")
        menu.addSeparator()
        fill_d     = menu.addAction("↓  아래 채우기  [Ctrl+D]")
        fill_r     = menu.addAction("→  오른쪽 채우기  [Ctrl+R]")
        menu.addSeparator()
        find_act   = menu.addAction("🔍  찾기  [Ctrl+F]")

        action = menu.exec(self.table.viewport().mapToGlobal(position))
        row = self.table.currentRow()
        col = self.table.currentColumn()

        if action == add_above:   self.insert_row(row)
        elif action == add_below: self.insert_row(row + 1)
        elif action == del_row:   self.delete_selected_rows()
        elif action == add_col_l: self.insert_col(col)
        elif action == add_col_r: self.insert_col(col + 1)
        elif action == del_col:   self.delete_selected_col()
        elif action == fill_d:    self.fill_down()
        elif action == fill_r:    self.fill_right()
        elif action == find_act:  self.open_find()

    # ════════════════════════════════════
    #  상태바
    # ════════════════════════════════════
    def update_status(self):
        rows = len(self.df_view) if not self.df_view.empty else 0
        cols = len(self.df_view.columns) if not self.df_view.empty else 0
        fname = self.file_path.replace("\\", "/").split("/")[-1] if self.file_path else "파일 없음"
        filter_info = f"  │  🔽 {len(self.col_filters)}열 필터" if self.col_filters else ""
        freeze_info = f"  │  🔒 {self.freeze_row}행/{self.freeze_col}열 고정" if (self.freeze_row or self.freeze_col) else ""
        self.status_bar.showMessage(
            f"  {fname}   │   {rows}행 × {cols}열{filter_info}{freeze_info}"
            f"   │   Ctrl+방향키  │  Ctrl+D/R 채우기  │  =수식 입력"
        )

    # ════════════════════════════════════
    #  헬퍼
    # ════════════════════════════════════
    def _tb_btn(self, text, slot, obj=None):
        btn = QPushButton(text)
        if obj: btn.setObjectName(obj)
        btn.clicked.connect(slot)
        return btn

    def _vsep(self):
        sep = QFrame(); sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet(f"background:{C['border2']};max-width:1px;margin:10px 2px;")
        return sep


# ══════════════════════════════════════════════════
#  엔트리포인트
# ══════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = ExcelEditor()
    window.show()
    sys.exit(app.exec())
