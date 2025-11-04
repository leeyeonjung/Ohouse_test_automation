# 📱 오늘의 집 로그인 테스트 자동화 프로젝트
---

## 🧩 Overview
이 프로젝트는 **Appium, Python, Pytest**를 이용하여  
**오늘의 집** 앱의 로그인 완료와 메인페이지 진입을 자동화 테스트한 프로젝트입니다.

- 테스트 결과는 **HTML Report** 형태로 시각화됩니다.  
- 각 테스트 함수의 실행 과정은 **동영상으로 기록**되어 디버깅 및 검증에 활용할 수 있습니다.  
- **이미지 비교**를 통해 UI 요소의 정확성을 검증합니다.  
- **소셜 로그인 세션 존재 여부**에 따라 테스트를 분리하여 실행할 수 있습니다.  

---

## 🔍 Key Features

### **소셜 로그인 테스트**
- 기기 내 세션 존재 여부에 따라 marker로 테스트 분리 (`@pytest.mark.session_exist`, `@pytest.mark.session_none`)

### **Pytest 기반 모듈화 구조**
- `conftest.py`에서 **Appium 드라이버 관련 fixture 정의 및 관리**
- Page Object Model 패턴 적용
- 공통 유틸리티 모듈화

### **HTML Report & Video Recording**
- 결과는 `Result/{실행 시간}/` 하위 폴더에 생성됩니다.  
  - 📊 **HTML Report** → `Result/{실행 시간}/test-reports/`  
    - 전체 테스트 결과가 **시각화된 HTML 형태로 저장**됩니다.  
  - 🎥 **Video Report** → `Result/{실행 시간}/video-reports/`  
    - 각 테스트 함수의 **실행 과정이 동영상으로 기록**됩니다.  
  - 🖼️ **Image Report** → `Result/{실행 시간}/image/`  
    - 테스트 함수에서 인식한 이미지가 **기기 및 테스트 파일별 PNG 파일로 저장**됩니다.

### **이미지 비교 검증**
- SSIM 기반 이미지 유사도 비교
- 로그인 화면의 주요 UI 요소 검증 (로고, 가이드, 버튼 등)

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
├── test_data.py                                    # 테스트 계정 정보 (Git에 push되지 않음)
├── pytest.ini                                      # Pytest 설정 및 커스텀 마커 정의
├── requirements.txt                                # Python 의존성 패키지 목록
│
├── tests/
│   ├── conftest.py                                 # pytest 전역 설정 및 driver fixture 정의
│   │                                               # - Appium WebDriver 설정
│   │                                               # - 비디오 녹화 fixture
│   │                                               # - HTML 리포트 자동 생성
│   │
│   ├── original_image/                             # 기준 이미지 (Baseline Images)
│   │   ├── logo_image.png
│   │   ├── guide_image.png
│   │   ├── login_button_kakao.png
│   │   ├── login_button_naver.png
│   │   ├── login_button_facebook.png
│   │   ├── login_button_apple.png
│   │   ├── login_button_email.png
│   │   └── ...
│   │
│   ├── src/
│   │   ├── common_util/                            # 공통 유틸리티 모듈
│   │   │   └── control_image.py                    # SSIM 기반 이미지 비교 유틸리티
│   │   │
│   │   ├── locaters/                               # 요소 Locators 정의
│   │   │   └── login_page_locaters.py              # 로그인 화면 locator 정의
│   │   │
│   │   └── pages/                                  # Page Object 정의
│   │       └── login_page.py                       # 로그인 화면 Page Object
│   │
│   └── testcase/                                   # 실제 테스트 시나리오 및 검증 로직
│       └── test_login_page.py                      # 로그인 기능 테스트
│
└── Result/                                         # 테스트 실행 결과 저장 폴더
    └── {실행 시간}/                                # 예: 2025-11-04_17-25-30
        ├── image/                                  # 캡처 이미지 저장
        │   └── {device_id}/                        # 예: emulator-5554
        │       └── {테스트 파일명}/                # 예: login_page
        │           └── {함수명}/
        │               └── {이미지명}_current_{timestamp}.png
        ├── test-reports/                           # pytest HTML 리포트
        │   └── report_{실행 시간}.html
        └── video-reports/                          # 테스트 실행 녹화 영상
            └── {device_id}/                        # 예: emulator-5554
                └── {테스트 파일명}/                # 예: test_login_page
                    └── {함수명}_{timestamp}.mp4
```

---

## 🔐 Test Data 관리

### test_data.py
- 테스트 계정 정보를 관리하는 파일입니다.
- 최초 예시를 제외 후에는 `.gitignore`에 포함되어 있어 Git에 push되지 않습니다.
- 실제 테스트 계정 정보를 입력하여 사용하세요.
```

---

## 🏷️ Pytest Markers

### 커스텀 마커 사용
```bash
# 세션 존재 테스트만 실행
pytest -m session_exist

# 세션 없음 테스트만 실행
pytest -m session_none

# 세션 존재 테스트 제외
pytest -m "not session_exist"
```

### 마커 정의
- `@pytest.mark.session_exist`: 기기 내 소셜 로그인 세션이 존재하는 경우
- `@pytest.mark.session_none`: 기기 내 소셜 로그인 세션이 없는 경우

---

## ▶️ Run Locally

### 1️⃣ 환경 설정
```bash
# 필수 패키지 설치
pip install -r requirements.txt
```

### 2️⃣ 테스트 계정 설정
`test_data.py` 파일에 실제 테스트 계정 정보를 입력하세요.

### 3️⃣ 테스트 실행
```bash
# 전체 테스트 실행
pytest -v

# 특정 테스트 파일 실행
pytest -v tests/testcase/test_login_page.py

# 특정 마커로 테스트 실행
pytest -m session_exist -v

# 로그 레벨 INFO로 실행
pytest --log-cli-level=INFO -v
```

### 4️⃣ 결과 확인
- 📊 **HTML Report:** `Result/{실행 시간}/test-reports/report_{실행 시간}.html`
- 🎥 **Video Report:** `Result/{실행 시간}/video-reports/{device_id}/{테스트 파일명}/`
- 🖼️ **Image Report:** `Result/{실행 시간}/image/{테스트 파일명}/{device_id}/login_screen/`

---

## 📋 Test Cases

테스트 케이스 상세 내용은 `testcase_excel/Ohouse.xlsm` 파일에 정의되어 있습니다.

---

## 💡 주요 기능 설명

### Page Object Model
- `LoginPage` 클래스: 로그인 화면의 모든 동작을 메서드로 캡슐화
- `login_page_locaters.py`: UI 요소 locator 중앙 관리

### 이미지 비교
- SSIM (Structural Similarity Index) 알고리즘 사용
- 기준 이미지와 캡처 이미지의 유사도를 백분율로 계산

### 비디오 녹화
- 각 테스트 함수 실행 과정을 자동으로 녹화
- 테스트 실패 시 디버깅에 활용

### 실행 시간 기반 결과 관리
- pytest 실행 시작 시 생성된 타임스탬프를 기준으로 모든 결과물을 동일한 폴더에 저장
- 한 번의 실행에서 생성된 모든 결과물을 쉽게 추적 가능

---

## 🔧 Configuration

### pytest.ini
- 커스텀 마커 정의
- 테스트 실행 옵션 설정

### conftest.py
- Appium WebDriver 설정
- 디바이스 구성
- 비디오 녹화 fixture
- HTML 리포트 자동 생성

---

## 📝 Notes
- `test_data.py`는 `.gitignore`에 포함되어 있어 Git에 push되지 않습니다.
- 실제 테스트 계정 정보는 반드시 `test_data.py`에 입력하세요.
- 테스트 실행 시 conftest.py에 설정된된 Appium Server가 실행 중이어야 합니다.