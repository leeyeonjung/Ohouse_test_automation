# 📱 오늘의집 로그인 테스트 자동화 프로젝트
---

*Appium · Python · Pytest 기반의 모바일 로그인 테스트 자동화 구현 과제 (Android 코드 포함)*

---

## 🧩 Overview
이 프로젝트는 **Appium + Pytest 기반의 Android UI 자동화 프레임워크**를 활용하여  
**오늘의집(Ohouse)** 앱의 로그인 및 메인 페이지 진입 과정을 검증하는 **Android 코드 기반 테스트 자동화 과제**입니다.

- 테스트 결과는 **HTML Report**로 시각화됩니다.
- 각 테스트 함수의 실행 과정은 **동영상으로 기록**되어 디버깅 및 리포트에 활용됩니다.  
- **SSIM 기반 이미지 비교**로 UI 요소의 정확성을 검증합니다.  
- **소셜 로그인 세션 존재 여부**에 따라 테스트를 분리 실행합니다.  
- **Appium Inspector를 통해 실제 Android 코드 요소를 기반으로 Locator 및 Action 구현**하였습니다.
---

## 🔍 Key Features

### ✅ **소셜 로그인 테스트**
- 카카오, 네이버, 페이스북, 애플, 이메일 로그인을 검증합니다.  
- 세션 존재 여부에 따라 테스트를 구분 (`@pytest.mark.session_exist`, `@pytest.mark.session_none`).

### ✅ **Pytest 기반 모듈화 구조**
- `conftest.py`를 통한 **Appium WebDriver 관리 및 공통 fixture 정의**
- Page Object Model(POM) 패턴 적용  
- 공통 유틸리티(`control_image.py`)를 통한 이미지 비교 로직 모듈화  

### ✅ **결과 리포트 자동화**
- 실행 시마다 타임스탬프 기반 폴더(`tests/Result/{실행 시간}/`) 생성  
  - 📊 **HTML Report** — 테스트 결과 시각화  
  - 🎥 **Video Report** — 실행 과정 자동 녹화  
  - 🖼️ **Image Report** — UI 비교 스크린샷 자동 저장  

### ✅ **UI 이미지 비교 검증**
- SSIM(Structural Similarity Index) 기반 유사도 비교  
- 로그인 화면 주요 요소(로고, 버튼 등)의 정확도 검증  

---

## ⚙️ Tech Stack
| 구분 | 사용 기술 |
|------|------------|
| Test Framework | **Pytest**, **Appium**, **uiautomator2** |
| Language | **Python 3.x** |
| Report | **pytest-html**, **Video Recording** |
| Device | **Android Emulator / Physical Device** |
| Image Comparison | **SSIM (scikit-image)** |

---

## 🏗️ Project Structure
```
Ohouse_test_automation/
├── test_data.py.example                      # 테스트 계정 정보 템플릿
├── pytest.ini                                # Pytest 설정 및 마커 정의
├── requirements.txt                          # 의존성 패키지 목록
├── testcase_excel/                           # 테스트 케이스 관리 파일
│   └── Ohouse.xlsm
│
├── tests/
│   ├── conftest.py                           # WebDriver, Report, Fixture 설정
│   │
│   ├── original_image/                       # 기준 이미지 (Baseline)
│   │   ├── logo_image.png
│   │   ├── login_button_kakao.png
│   │   └── ...
│   │
│   ├── src/
│   │   ├── common_util/                      # 공통 유틸리티
│   │   │   └── control_image.py              # SSIM 이미지 비교 함수
│   │   ├── locaters/                         # Locator 정의
│   │   │   └── login_page_locaters.py
│   │   └── pages/                            # Page Object 정의
│   │       └── login_page.py
│   │
│   ├── testcase/                             # 실제 테스트 시나리오
│   │   └── test_login_page.py
│   │
│   └── Result/                               # 테스트 실행 결과
│       └── {실행 시간}/
│           ├── image/{device_id}/{test_file}/
│           ├── test-reports/report_{timestamp}.html
│           └── video-reports/{device_id}/{test_file}/
```

---

## 🔐 Test Data 관리

### `test_data.py`
- 실제 로그인에 사용할 **계정 정보**를 별도로 관리합니다.  
- 보안상의 이유로 `.gitignore`에 등록되어 GitHub에는 포함되지 않습니다.  
- 저장소 클론 후 `test_data.py.example` 파일을 복사하여 `test_data.py`로 만들고 실제 계정 정보를 입력하세요:

```bash
# 저장소 클론 후 최초 설정
cp test_data.py.example test_data.py
# 또는 Windows PowerShell
Copy-Item test_data.py.example test_data.py
```

그 후 `test_data.py` 파일에 실제 테스트 계정 정보를 입력하세요.

---

## 🏷️ Pytest Markers

### 마커 정의
| 마커 | 설명 |
|------|------|
| `@pytest.mark.session_exist` | 기기 내 로그인 세션이 존재하는 경우 |
| `@pytest.mark.session_none` | 세션이 존재하지 않아 신규 로그인해야 하는 경우 |

### 실행 예시
```bash
# 세션 존재 테스트만 실행
pytest -m session_exist -v

# 세션 없음 테스트만 실행
pytest -m session_none -v

# 세션 존재 테스트 제외 실행
pytest -m "not session_exist" -v
```

---

## ▶️ Run Locally

### 1️⃣ 환경 설정
```bash
pip install -r requirements.txt
```

### 2️⃣ 테스트 계정 등록
1. `test_data.py.example` 파일을 복사하여 `test_data.py` 생성:
   ```bash
   # Linux/Mac
   cp test_data.py.example test_data.py
   
   # Windows PowerShell
   Copy-Item test_data.py.example test_data.py
   ```
2. `test_data.py` 파일에 실제 테스트 계정 정보를 입력합니다.

### 3️⃣ 테스트 실행
```bash
# 전체 테스트 실행
pytest -v

# 특정 테스트 파일만 실행
pytest -v tests/testcase/test_login_page.py

# 마커 기반 테스트 실행
pytest -m session_exist -v

# 로그 레벨 INFO로 실행
pytest --log-cli-level=INFO -v
```

### 4️⃣ 결과 확인
- 📊 **HTML Report:** `tests/Result/{실행 시간}/test-reports/report_{timestamp}.html`  
- 🎥 **Video Report:** `tests/Result/{실행 시간}/video-reports/{device_id}/{테스트 파일명}/`  
- 🖼️ **Image Report:** `tests/Result/{실행 시간}/image/{device_id}/{테스트 파일명}/login_screen/`  

---

## 📋 Test Cases
모든 테스트 케이스는  `testcase_excel/Ohouse.xlsm` 파일에서 관리됩니다.  
(자동화 구현 여부, 기기 상태, 기대결과 등 포함)

---

## 💡 주요 기능 설명

### 🧱 Page Object Model
- `LoginPage` 클래스는 로그인 화면의 모든 동작(입력, 클릭, 화면 캡처 등)을 캡슐화합니다.  
- `login_page_locaters.py`는 UI 요소의 locator를 중앙에서 관리합니다.

### 🖼️ 이미지 비교 (SSIM)
- `control_image.py`를 통해 기준 이미지와 테스트 캡처를 비교  
- 유사도를 백분율로 계산하여 UI의 시각적 정확성 검증

### 🎥 비디오 녹화
- 각 테스트 함수 실행 과정이 자동으로 녹화되어  
  실패 케이스의 디버깅 및 리포트 활용이 용이합니다.

### 🕓 실행 시간 기반 결과 관리
- 테스트 실행 시점(`datetime.now()`)을 기준으로 결과 폴더를 생성  
- 한 번의 실행에 포함된 모든 산출물(HTML, Video, Image)을 동일 타임스탬프 하에 저장  

---

## 🔧 Configuration

### `pytest.ini`
- 커스텀 마커 정의 (`session_exist`, `session_none`)  
- 테스트 경로, 로그 레벨 등 공통 실행 설정  

### `conftest.py`
- Appium WebDriver 초기화  
- 디바이스 및 세션 설정  
- HTML 리포트 / 비디오 녹화 fixture 정의  

---

## 📝 Notes
- `test_data.py`는 `.gitignore`에 반드시 포함되어 있어 push되지 않습니다.  
- 저장소 클론 후 `test_data.py.example`를 복사하여 `test_data.py`를 생성하세요.  
- 테스트 실행 전 Appium Server가 정상 구동 중인지 확인하세요.  
- Emulator 및 실제 기기 모두에서 실행 가능합니다.  
