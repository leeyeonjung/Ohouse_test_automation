# Standard library
import os
import base64
import logging 
from datetime import datetime
from pathlib import Path

# Third-party libraries
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

log = logging.getLogger(__name__)


# 📱 Device Configuration
devices = [
    # Device 1
    pytest.param(
        {"udid": "emulator-5554", "systemPort": 8200, "server_url": "http://127.0.0.1:4723"},  # 기기 설정 정보
        id="emulator-5554"  # 테스트 식별자
    ),
    # Device 2
    pytest.param(
        {"udid": "emulator-5556", "systemPort": 8201, "server_url": "http://127.0.0.1:4725"},  # 기기 설정 정보
        id="emulator-5556"  # 테스트 식별자
    ),
]


# 📱 Appium Driver 설정
@pytest.fixture(params=devices)  # 각 기기에 대해 테스트 실행
def wd(request):
    """Appium WebDriver 인스턴스 생성 및 설정
    
    Args:
        request: pytest fixture request 객체
        
    Yields:
        webdriver.Remote: Appium WebDriver 인스턴스
    """
    options = UiAutomator2Options()  # Android UiAutomator2 옵션 객체 생성

    options.platform_name = "Android"  # 플랫폼 설정

    options.udid = request.param["udid"]  # 기기 식별자 설정

    options.system_port = request.param["systemPort"]  # 시스템 포트 설정

    options.app_package = "net.bucketplace"  # 앱 패키지명 설정

    options.app_activity = "se.ohou.screen.splash.SplashActivity"  # 시작 액티비티 설정

    options.app_wait_activity = "se.ohou.screen.intro.IntroActivity, se.ohou.screen.splash.SplashActivity, *"  # 대기할 액티비티 목록

    options.auto_grant_permissions = True  # 권한 자동 승인

    options.no_reset = False  # 앱 데이터 초기화 O (테스트 간 데이터 초기화)

    options.full_reset = False  # 앱 전체 재설치 X (앱 재설치하지 않음)

    driver = webdriver.Remote(request.param["server_url"], options=options)  # Appium 서버에 연결하여 WebDriver 생성

    driver.implicitly_wait(10)  # 암시적 대기 시간 설정 (10초)

    yield driver  # WebDriver 인스턴스 반환

    driver.quit()  # 테스트 종료 후 WebDriver 종료


# 🎥 Test Video Recording Fixture
@pytest.fixture(autouse=True)  # 모든 테스트에 자동으로 적용 (비디오 녹화 불필요시 autouse=False 변경하여 사용 가능)
def record_video(request, wd):
    """테스트 실행 화면을 동영상으로 녹화
    
    Args:
        request: pytest fixture request 객체
        wd: Appium WebDriver 인스턴스
        
    Yields:
        None: 테스트 실행 중 녹화 진행
    """
    # 테스트 스크립트 파일명 추출
    file_name = Path(request.node.fspath).stem

    # 기기 식별자 추출 및 파일명에 사용 가능한 형태로 변환
    raw_device_id = wd.capabilities.get("udid") or wd.capabilities.get("deviceUDID") or "unknown_device"  # 기기 ID 가져오기
    device_id = str(raw_device_id).replace(":", "_").replace("/", "_").replace("\\", "_")  # 특수문자 제거

    # 실행 시간 가져오기 (config에서 가져오거나 현재 시간 사용)
    execution_time = getattr(request.config, '_execution_time', None)
    if execution_time is None:
        execution_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # 저장 디렉토리 경로 생성: Result/{실행 시간}/video-reports/{device_id}/{테스트 파일명}/
    save_dir = Path(__file__).resolve().parents[0] / "Result" / execution_time / "video-reports" / device_id / file_name
    os.makedirs(save_dir, exist_ok=True)  # 저장 디렉토리 생성

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # 현재 시간을 타임스탬프 형식으로 변환

    test_name = request.node.originalname or request.node.name  # 테스트 함수명 가져오기

    safe_name = "".join(c for c in test_name if c.isalnum() or c in ("_", "-"))  # 파일명에 사용 가능한 문자만 추출

    save_path = save_dir / f"{safe_name}_{timestamp}.mp4"  # 저장할 파일 경로 생성

    wd.start_recording_screen()  # 화면 녹화 시작

    yield  # 테스트 실행

    video_raw = wd.stop_recording_screen()  # 화면 녹화 중지

    with open(save_path, "wb") as f:  # 비디오 파일 저장
        f.write(base64.b64decode(video_raw))  # Base64 디코딩하여 파일에 저장

    log.info(f"[VIDEO] {device_id} → {safe_name} 실행 동영상 저장 완료 → {save_path}")  # 저장 완료 로그 출력


# 📊 pytest 실행 시 항상 HTML Report 자동 생성
def pytest_configure(config):
    """pytest 설정 시 HTML 리포트 경로 자동 설정
    
    Args:
        config: pytest 설정 객체
    """
    # 실행 시간 생성 및 config에 저장 (세션 전체에서 동일한 값 사용)
    execution_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config._execution_time = execution_time
    
    # --html 옵션 없어도 자동으로 HTML 리포트 생성
    if not getattr(config.option, "htmlpath", None):  # HTML 리포트 경로가 설정되지 않았으면
        report_dir = Path(__file__).resolve().parents[0] / "Result" / execution_time / "test-reports"  # 리포트 저장 디렉토리 경로 생성
        report_dir.mkdir(parents=True, exist_ok=True)  # 리포트 저장 디렉토리 생성

        report_path = report_dir / f"report_{execution_time}.html"  # 리포트 파일 경로 생성

        # pytest 옵션에 경로 주입
        config.option.htmlpath = str(report_path)  # HTML 리포트 저장 경로 설정
        config.option.self_contained_html = True  # 자체 포함 HTML 리포트 생성 (외부 CSS/JS 없이)