# tests/src/pages/login_page.py

# Standard library
import logging
from datetime import datetime
from pathlib import Path

# Third-party libraries
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Local modules
from tests.src.common_util.control_image import compare
import tests.src.locaters.login_page_locaters as loc


log = logging.getLogger(__name__)


class LoginPage:
    def __init__(self, wd):
        """LoginPage 클래스 초기화
        
        Args:
            wd: WebDriver 인스턴스
        """
        self.wd = wd


    def get_device_id(self):
        """디바이스 ID 반환
        
        Returns:
            str: 디바이스의 UDID 값
        """
        return self.wd.capabilities.get("udid")


    def get_current_activity(self):
        """현재 앱의 액티비티 이름 반환
        
        Returns:
            str: 현재 액티비티 이름 (예: "se.ohou.screen.main.MainActivity")
        """
        return self.wd.current_activity


    def click_social_login(self, provider):
        """소셜 로그인 버튼 클릭
        
        Args:
            provider (str): 로그인 제공자 ("kakao", "naver", "facebook", "apple", "email")
        """
        locator = getattr(loc, f"login_button_{provider}")
        message = f"{provider}로 로그인 버튼 클릭"
        
        WebDriverWait(self.wd, 10).until(
            EC.element_to_be_clickable((By.ID, locator))
        ).click()
        log.info(message)


    def input_email(self, email):
        """이메일 입력 필드에 이메일 주소 입력
        
        Args:
            email (str): 입력할 이메일 주소
        """
        self.wd.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("이메일")').send_keys(email)


    def input_password(self, password):
        """비밀번호 입력 필드에 비밀번호 입력
        
        Args:
            password (str): 입력할 비밀번호
        """
        self.wd.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("비밀번호")').send_keys(password)


    def click_login_confirm(self):
        """로그인 확인 버튼 클릭"""
        self.wd.find_element(By.ID, "net.bucketplace:id/loginButton").click()
        log.info("로그인 버튼 클릭")


    def get_toast_message(self):
        """로그인 제한 토스트 메시지 가져오기
        
        Returns:
            str: 토스트 메시지 텍스트 (예: "10번 실패하면 10분간 로그인이 제한돼요. (1/10)")
        """
        toast_locator = (AppiumBy.XPATH, '//*[contains(@text, "로그인이 제한돼요")]')
        element = WebDriverWait(self.wd, 5).until(EC.presence_of_element_located(toast_locator))
        return element.text


    # 웹뷰 관련
    def wait_for_webview_context(self):
        """웹뷰 컨텍스트가 준비될 때까지 대기
        
        Returns:
            list: 웹뷰 컨텍스트 리스트 (예: ["WEBVIEW_chrome"])
        """
        def context_ready(wd):
            contexts = wd.contexts
            return "NATIVE_APP" in contexts and any("WEBVIEW" in ctx for ctx in contexts)
        WebDriverWait(self.wd, 30).until(context_ready)
        return [ctx for ctx in self.wd.contexts if "WEBVIEW" in ctx]


    def switch_to_webview(self):
        """웹뷰 컨텍스트로 전환"""
        webviews = self.wait_for_webview_context()
        self.wd.switch_to.context(webviews[0])
        log.info(f"웹뷰 컨텍스트로 전환: {webviews[0]}")


    def capture_and_compare_images(self, request):
        """로그인 화면의 주요 요소들을 캡처하고 원본 이미지와 유사도 비교
        
        Args:
            request: pytest request 객체
        
        Returns:
            dict: 이미지 이름과 유사도(%)를 담은 딕셔너리
        """
        # 테스트 파일명 추출 및 test_ 접두사 제거
        test_file_name = Path(request.node.fspath).stem
        test_file_name = test_file_name.replace("test_", "")

        # 실행 시간 가져오기 (request.config에서 가져오거나 현재 시간 사용)
        execution_time = getattr(request.config, '_execution_time', None)
        if execution_time is None:
            execution_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        device_id = self.get_device_id()
        original_dir = Path(__file__).resolve().parents[2] / "original_image"
        
        result_dir = Path(__file__).resolve().parents[2] / "Result" / execution_time / "image" / device_id / test_file_name / "login_screen"
        result_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        mapping = {
            "logo_image.png": loc.logo_image,
            "guide_image.png": loc.guide_image,
            "login_button_kakao.png": loc.login_button_kakao,
            "login_button_naver.png": loc.login_button_naver,
            "login_button_facebook.png": loc.login_button_facebook,
            "login_button_apple.png": loc.login_button_apple,
            "login_button_email.png": loc.login_button_email,
            "login_button_email_signup.png": loc.login_button_email_signup,
            "login_button_customer_service.png": loc.login_button_customer_service,
            "login_button_anonymous_order_check.png": loc.login_button_anonymous_order_check,
        }

        results = {}
        for img_name, locator in mapping.items():
            element = WebDriverWait(self.wd, 10).until(EC.presence_of_element_located((By.ID, locator)))
            current_path = result_dir / f"{img_name.replace('.png', '')}_current_{timestamp}.png"
            element.screenshot(str(current_path))
            similarity = compare(str(original_dir / img_name), str(current_path))
            results[img_name] = similarity
            log.debug(f"[유사도 비교] {img_name}: {similarity}%")
        return results
