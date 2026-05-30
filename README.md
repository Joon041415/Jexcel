# Excel Editor

> 🇰🇷 한국어 &nbsp;|&nbsp; 🇺🇸 [English](#english) &nbsp;|&nbsp; 🇯🇵 [日本語](#japanese)

---

<a name="korean"></a>
# 🇰🇷 한국어

## 개요

Python 기반 경량 엑셀 에디터. 수식 엔진, 필터, 조건부 서식, Freeze Pane을 내장하며
별도 오피스 설치 없이 `.xlsx` / `.xls` 파일을 열고 편집·저장할 수 있습니다.

```
Excel Editor
├── Formula Bar (수식 입력/표시)
├── 함수 패널 (SUM / AVG / COUNT / MAX / MIN / COUNTA)
├── 필터 · 조건부 서식 · Freeze Pane
├── Ctrl+C/V · Fill Down/Right · 자동 재계산
└── 가상 스크롤 (대용량 청크 로딩)
```

---

## 설치

### 요구 사항

| 항목 | 버전 |
|------|------|
| Python | 3.10 이상 |
| PySide6 | 6.5 이상 |
| pandas | 2.0 이상 |
| openpyxl | 3.1 이상 |

### 의존성 설치

```bash
pip install PySide6 pandas openpyxl
```

### 실행

```bash
python excel_editor.py
```

### 간략 실행 bat

excel.bat 메모장 작성
```
@echo off
py "파일위치\excel_editor.py"
```


---

## 기능

### 파일 관리
| 기능 | 설명 |
|------|------|
| 열기 | `.xlsx` / `.xls` 파일 열기 |
| 새 파일 | 10×10 빈 시트로 새 파일 생성 |
| 저장 | 현재 파일에 덮어쓰기 저장 |
| 다른 이름으로 저장 | 새 경로로 저장 |
| 마지막 경로 기억 | 열기·저장 다이얼로그가 마지막 디렉토리를 기억 |
| 다중 시트 | 시트 콤보박스로 전환 |

### 수식 (Formula)
셀에 `=` 로 시작하는 수식을 입력하면 즉시 계산되며, 참조 셀 변경 시 **자동 재계산**합니다.

```
=SUM(A1:C10)          범위 합계
=AVERAGE(B1:B20)      평균
=IF(A1>100,"초과","이하")  조건 분기
=VLOOKUP(D1,A1:C10,2) 수직 검색
=IFERROR(A1/B1,"오류") 오류 처리
=CONCAT(A1,"-",B1)    문자 결합
=ROUND(A1,2)          반올림
=LEN(A1)              문자 수
=UPPER(A1)            대문자 변환
=TODAY()              오늘 날짜
```

> **제한:** 절대참조(`$A$1`) 미지원. 순환참조 감지 없음.

### 편집
| 기능 | 방법 |
|------|------|
| 셀 편집 | 셀 클릭 후 입력 |
| Enter | 편집 완료 후 아래 셀로 이동 |
| 열 이름 수정 | 헤더 더블클릭 |
| 행 추가 | `＋행` 버튼 또는 우클릭 메뉴 |
| 행 삭제 | `－행` 버튼 또는 선택 후 `Ctrl+Delete` |
| 열 추가 | `＋열` 버튼 또는 우클릭 메뉴 |
| 열 삭제 | `－열` 버튼 또는 우클릭 메뉴 |
| 다중 선택 | `Shift` / `Ctrl` 클릭 |

### 단축키

| 단축키 | 기능 |
|--------|------|
| `Ctrl+S` | 저장 |
| `Ctrl+Shift+S` | 다른 이름으로 저장 |
| `Ctrl+Z` | 실행 취소 (최대 200단계) |
| `Ctrl+F` | 찾기 |
| `Ctrl+A` | 전체 선택 |
| `Ctrl+C` | 복사 (다중 셀 지원) |
| `Ctrl+V` | 붙여넣기 |
| `Ctrl+D` | 아래 채우기 (Fill Down) |
| `Ctrl+R` | 오른쪽 채우기 (Fill Right) |
| `Ctrl+Enter` | 아래에 새 행 추가 |
| `Ctrl+Delete` | 선택 행 삭제 |
| `Ctrl+↑↓←→` | 데이터 블록 끝으로 이동 |
| `Ctrl+Home` | 첫 번째 셀 (A1) |
| `Ctrl+End` | 마지막 데이터 셀 |
| `Delete` | 선택 셀 내용 삭제 |

### 필터
- 헤더 우클릭 → **필터 설정**
- 고유값 목록에서 체크박스로 표시할 값 선택
- 필터 적용 시 헤더에 `▼` 표시
- 필터 적용 중에도 저장 가능 (표시된 행만 저장)

### 조건부 서식
- 헤더 우클릭 → **조건부 서식**
- 숫자 범위(최솟값 ~ 최댓값)와 배경색 지정
- 열 단위 적용

### Freeze Pane (행/열 고정)
1. 고정하려는 위치의 셀 선택
2. 툴바 **🔒 고정** 버튼 클릭
3. 선택 셀 기준으로 행/열 고정 (시각적 음영 표시)
4. 같은 버튼으로 고정 해제

### 가상 스크롤 (대용량 파일)
- 최초 200행만 렌더링
- 스크롤이 하단 88% 이상 도달하면 다음 200행 자동 로드
- 수만 행 파일도 UI 응답 유지

---

## 라이선스

본 소프트웨어는 **MIT License** 로 배포됩니다.

### 사용 허가
- ✅ 개인적 사용
- ✅ 소스 코드 수정
- ✅ 비상업적 배포
- ✅ 교육·연구 목적
- ✅ 포트폴리오·데모 용도

### 사용 불가
- ❌ 상업적 판매 목적의 재배포 (라이선스 고지 없이)
- ❌ PySide6 라이브러리 자체를 상업 제품에 번들링할 경우 Qt 상업 라이선스 별도 필요
- ❌ 본 소프트웨어를 자신의 저작물로 허위 표기
- ❌ 라이선스 고지문 제거

### 사용 라이브러리 라이선스

| 라이브러리 | 라이선스 | 고지 |
|-----------|---------|------|
| PySide6 | LGPL v3 | Copyright © The Qt Company |
| pandas | BSD 3-Clause | Copyright © pandas contributors |
| openpyxl | MIT | Copyright © openpyxl contributors |
| Python | PSF License | Copyright © Python Software Foundation |

> **상업 판매 목적이라면:** PySide6의 LGPL 조건에 따라 Qt 상업 라이선스 취득을 권장합니다.
> 자세한 내용은 [Qt Licensing](https://www.qt.io/licensing/) 을 참고하세요.

---

## 연락처

- **이메일:** [lotus031315@gmail.com](mailto:lotus031315@gmail.com)
- **포트폴리오:** [https://joon041415.github.io/](https://joon041415.github.io/)

---
---

<a name="english"></a>
# 🇺🇸 English

## Overview

A lightweight Excel editor built with Python. Features a built-in formula engine, column filters, conditional formatting, and Freeze Pane — no Office installation required. Opens, edits, and saves `.xlsx` / `.xls` files.

```
Excel Editor
├── Formula Bar (formula input & display)
├── Function Panel (SUM / AVG / COUNT / MAX / MIN / COUNTA)
├── Filter · Conditional Formatting · Freeze Pane
├── Ctrl+C/V · Fill Down/Right · Auto Recalculation
└── Virtual Scroll (chunk-based loading for large files)
```

---

## Installation

### Requirements

| Item | Version |
|------|---------|
| Python | 3.10+ |
| PySide6 | 6.5+ |
| pandas | 2.0+ |
| openpyxl | 3.1+ |

### Install Dependencies

```bash
pip install PySide6 pandas openpyxl
```

### Run

```bash
python excel_editor.py
```

### Build Executable (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "ExcelEditor" excel_editor.py
# Generates dist/ExcelEditor.exe
```

---

## Features

### File Management
| Feature | Description |
|---------|-------------|
| Open | Open `.xlsx` / `.xls` files |
| New File | Create a new 10×10 blank sheet |
| Save | Overwrite save to current file |
| Save As | Save to a new path |
| Last Directory Memory | Open/save dialogs remember the last directory |
| Multi-Sheet | Switch sheets via combo box |

### Formulas
Enter a formula starting with `=` in any cell. Values **auto-recalculate** when referenced cells change.

```
=SUM(A1:C10)           Sum of range
=AVERAGE(B1:B20)       Average
=IF(A1>100,"Over","OK") Conditional branch
=VLOOKUP(D1,A1:C10,2)  Vertical lookup
=IFERROR(A1/B1,"ERR")  Error handling
=CONCAT(A1,"-",B1)     String concatenation
=ROUND(A1,2)           Round to decimal
=LEN(A1)               String length
=UPPER(A1)             Uppercase
=TODAY()               Today's date
```

> **Limitations:** Absolute references (`$A$1`) are not supported. No circular reference detection.

### Editing
| Action | How |
|--------|-----|
| Edit cell | Click cell and type |
| Enter key | Confirm edit and move to cell below |
| Rename column | Double-click header |
| Add row | `＋Row` button or right-click menu |
| Delete row | `－Row` button or select + `Ctrl+Delete` |
| Add column | `＋Col` button or right-click menu |
| Delete column | `－Col` button or right-click menu |
| Multi-select | `Shift` / `Ctrl` + click |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save |
| `Ctrl+Shift+S` | Save As |
| `Ctrl+Z` | Undo (up to 200 steps) |
| `Ctrl+F` | Find |
| `Ctrl+A` | Select All |
| `Ctrl+C` | Copy (multi-cell supported) |
| `Ctrl+V` | Paste |
| `Ctrl+D` | Fill Down |
| `Ctrl+R` | Fill Right |
| `Ctrl+Enter` | Insert new row below |
| `Ctrl+Delete` | Delete selected rows |
| `Ctrl+↑↓←→` | Jump to end of data block |
| `Ctrl+Home` | Go to first cell (A1) |
| `Ctrl+End` | Go to last data cell |
| `Delete` | Clear selected cell contents |

### Filter
- Right-click header → **Filter**
- Check/uncheck values from the unique value list
- Header shows `▼` when filter is active
- Save while filtered exports only visible rows

### Conditional Formatting
- Right-click header → **Conditional Formatting**
- Set numeric range (min ~ max) and highlight color
- Applied per column

### Freeze Pane
1. Select the cell at the freeze boundary
2. Click **🔒 Freeze** in the toolbar
3. Rows/columns above and to the left are frozen (shown with shading)
4. Click again to unfreeze

### Virtual Scroll (Large Files)
- Only the first 200 rows are rendered on load
- Next 200 rows load automatically when scroll reaches 88% of the way down
- Handles files with tens of thousands of rows without UI freezing

---

## License

This software is distributed under the **MIT License**.

### Permitted
- ✅ Personal use
- ✅ Modifying source code
- ✅ Non-commercial distribution
- ✅ Educational and research use
- ✅ Portfolio and demo use

### Not Permitted
- ❌ Commercial redistribution without license notice
- ❌ Bundling PySide6 into a commercial product without a Qt commercial license
- ❌ Claiming this software as your own without attribution
- ❌ Removing license notices

### Third-Party Library Licenses

| Library | License | Notice |
|---------|---------|--------|
| PySide6 | LGPL v3 | Copyright © The Qt Company |
| pandas | BSD 3-Clause | Copyright © pandas contributors |
| openpyxl | MIT | Copyright © openpyxl contributors |
| Python | PSF License | Copyright © Python Software Foundation |

> **For commercial sale:** Qt commercial license acquisition is recommended under the LGPL v3 terms of PySide6.
> See [Qt Licensing](https://www.qt.io/licensing/) for details.

---

## Contact

- **Email:** [lotus031315@gmail.com](mailto:lotus031315@gmail.com)
- **Portfolio:** [https://joon041415.github.io/](https://joon041415.github.io/)

---
---

<a name="japanese"></a>
# 🇯🇵 日本語

## 概要

Python ベースの軽量 Excel エディター。数式エンジン、フィルター、条件付き書式、Freeze Pane を内蔵し、Office のインストール不要で `.xlsx` / `.xls` ファイルを開いて編集・保存できます。

```
Excel Editor
├── Formula Bar（数式の入力・表示）
├── 関数パネル（SUM / AVG / COUNT / MAX / MIN / COUNTA）
├── フィルター・条件付き書式・Freeze Pane
├── Ctrl+C/V・Fill Down/Right・自動再計算
└── 仮想スクロール（大容量チャンク読み込み）
```

---

## インストール

### 動作環境

| 項目 | バージョン |
|------|-----------|
| Python | 3.10 以上 |
| PySide6 | 6.5 以上 |
| pandas | 2.0 以上 |
| openpyxl | 3.1 以上 |

### 依存関係のインストール

```bash
pip install PySide6 pandas openpyxl
```

### 起動

```bash
python excel_editor.py
```

### 実行ファイルのビルド（Windows）

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "ExcelEditor" excel_editor.py
# dist/ExcelEditor.exe が生成されます
```

---

## 機能

### ファイル管理
| 機能 | 説明 |
|------|------|
| 開く | `.xlsx` / `.xls` ファイルを開く |
| 新規作成 | 10×10 の空シートで新規ファイルを作成 |
| 保存 | 現在のファイルに上書き保存 |
| 名前を付けて保存 | 新しいパスに保存 |
| 最終ディレクトリの記憶 | 開く・保存ダイアログが最後のフォルダーを記憶 |
| マルチシート | コンボボックスでシートを切り替え |

### 数式（Formula）
セルに `=` で始まる数式を入力すると即座に計算され、参照セルの変更時に**自動再計算**されます。

```
=SUM(A1:C10)           範囲の合計
=AVERAGE(B1:B20)       平均
=IF(A1>100,"超過","以下") 条件分岐
=VLOOKUP(D1,A1:C10,2)  垂直検索
=IFERROR(A1/B1,"エラー") エラー処理
=CONCAT(A1,"-",B1)     文字列結合
=ROUND(A1,2)           四捨五入
=LEN(A1)               文字数
=UPPER(A1)             大文字変換
=TODAY()               今日の日付
```

> **制限事項:** 絶対参照（`$A$1`）は未対応。循環参照の検出なし。

### 編集操作
| 操作 | 方法 |
|------|------|
| セルの編集 | セルをクリックして入力 |
| Enter キー | 編集確定後、下のセルへ移動 |
| 列名の変更 | ヘッダーをダブルクリック |
| 行の追加 | `＋行` ボタンまたは右クリックメニュー |
| 行の削除 | `－行` ボタンまたは選択後 `Ctrl+Delete` |
| 列の追加 | `＋列` ボタンまたは右クリックメニュー |
| 列の削除 | `－列` ボタンまたは右クリックメニュー |
| 複数選択 | `Shift` / `Ctrl` + クリック |

### キーボードショートカット

| ショートカット | 機能 |
|--------------|------|
| `Ctrl+S` | 保存 |
| `Ctrl+Shift+S` | 名前を付けて保存 |
| `Ctrl+Z` | 元に戻す（最大 200 ステップ） |
| `Ctrl+F` | 検索 |
| `Ctrl+A` | 全選択 |
| `Ctrl+C` | コピー（複数セル対応） |
| `Ctrl+V` | 貼り付け |
| `Ctrl+D` | 下方向へのフィル（Fill Down） |
| `Ctrl+R` | 右方向へのフィル（Fill Right） |
| `Ctrl+Enter` | 下に新規行を挿入 |
| `Ctrl+Delete` | 選択行を削除 |
| `Ctrl+↑↓←→` | データブロックの端へ移動 |
| `Ctrl+Home` | 最初のセル（A1）へ移動 |
| `Ctrl+End` | 最後のデータセルへ移動 |
| `Delete` | 選択セルの内容を削除 |

### フィルター
- ヘッダーを右クリック → **フィルター設定**
- 一意の値リストからチェックボックスで表示する値を選択
- フィルター適用中はヘッダーに `▼` が表示
- フィルター適用中でも保存可能（表示行のみ保存）

### 条件付き書式
- ヘッダーを右クリック → **条件付き書式**
- 数値の範囲（最小値〜最大値）と背景色を指定
- 列単位で適用

### Freeze Pane（行・列の固定）
1. 固定したい境界のセルを選択
2. ツールバーの **🔒 固定** ボタンをクリック
3. 選択セルの上・左が固定される（シェーディングで視覚的に表示）
4. 同じボタンで固定解除

### 仮想スクロール（大容量ファイル）
- 初回読み込み時は最初の 200 行のみレンダリング
- スクロールが下端の 88% に達すると次の 200 行を自動読み込み
- 数万行のファイルでも UI の応答を維持

---

## ライセンス

本ソフトウェアは **MIT License** のもとで配布されます。

### 許可される使用
- ✅ 個人的な使用
- ✅ ソースコードの改変
- ✅ 非商業的な配布
- ✅ 教育・研究目的での使用
- ✅ ポートフォリオ・デモ用途

### 禁止される使用
- ❌ ライセンス表記なしでの商業的な再配布
- ❌ Qt 商用ライセンスなしで PySide6 を商業製品にバンドルすること
- ❌ 本ソフトウェアを自分の著作物として偽って表示すること
- ❌ ライセンス表記の削除

### 使用ライブラリのライセンス

| ライブラリ | ライセンス | 表記 |
|-----------|-----------|------|
| PySide6 | LGPL v3 | Copyright © The Qt Company |
| pandas | BSD 3-Clause | Copyright © pandas contributors |
| openpyxl | MIT | Copyright © openpyxl contributors |
| Python | PSF License | Copyright © Python Software Foundation |

> **商業販売を目的とする場合:** PySide6 の LGPL v3 の条件に従い、Qt 商用ライセンスの取得を推奨します。
> 詳細は [Qt Licensing](https://www.qt.io/licensing/) をご参照ください。

---

## 連絡先

- **メール:** [lotus031315@gmail.com](mailto:lotus031315@gmail.com)
- **ポートフォリオ:** [https://joon041415.github.io/](https://joon041415.github.io/)
