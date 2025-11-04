# tests/testcase/test_login_page.py

# Standard library
import re

# Third-party libraries
import pytest
import pytest_check as check
import logging
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC    
from selenium.webdriver.support.ui import WebDriverWait
log = logging.getLogger(__name__)

# Local modules
from tests.src.pages.login_page import LoginPage
from test_data import TEST_ACCOUNTS


# Test Cases
def test_login_screen(wd, request):
    """로그인 화면 진입"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    results = page.capture_and_compare_images(request)  # 로그인 화면 이미지 캡처 및 유사도 비교

    for img_name, similarity in results.items():  # 각 이미지별 유사도 검증
        # 기대 결과: 로그인 화면 요소 확인 (오늘의 집, 3초만에 빠른 회원가입, 카카오톡으로 계속하기, 네이버 페이스북 애플, 이메일로 로그인 | 이메일로 가입, 로그인에 문제가 있으신가요?, 비회원 주문하기)
        check.greater_equal(similarity, 85.0, f"{img_name} 이미지 유사도가 85% 이상이어야 합니다.")


@pytest.mark.session_exist
def test_kakao_login_success_with_session(wd):
    """기기 내 카카오 로그인 세션 존재 시 등록된 회원의 로그인 성공하는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_social_login("kakao")  # 카카오 로그인 버튼 클릭

    # 기대 결과: 로그인 성공 후 메인 페이지 노출
    check.equal(page.get_current_activity(), "se.ohou.screen.main.MainActivity")


@pytest.mark.session_none
def test_kakao_login_webview(wd):
    """기기 내 카카오 로그인 세션이 없을 때 카카오 로그인 페이지로 이동되는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_social_login("kakao")  # 카카오 로그인 버튼 클릭

    page.switch_to_webview()  # 웹뷰 컨텍스트로 전환

    # 기대 결과: 웹뷰 카카오 로그인 페이지 노출
    check.equal(wd.title, "Kakao Account")


@pytest.mark.session_exist
def test_naver_login_success_with_session(wd):
    """기기 내 네이버 로그인 세션 존재 시 등록된 회원의 로그인 성공하는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_social_login("naver")  # 네이버 로그인 버튼 클릭

    # 기대 결과: 로그인 성공 후 메인 페이지 노출
    check.equal(page.get_current_activity(), "se.ohou.screen.main.MainActivity")


@pytest.mark.session_none
def test_naver_login_webview(wd):
    """기기 내 네이버 로그인 세션이 없을 때 네이버 로그인 페이지로 이동되는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_social_login("naver")  # 네이버 로그인 버튼 클릭

    page.switch_to_webview()  # 웹뷰 컨텍스트로 전환

    # 기대 결과: 웹뷰 네이버 로그인 페이지 노출
    check.equal(wd.title, "네이버 : 로그인")


@pytest.mark.session_exist
def test_facebook_login_success_with_session(wd):
    """기기 내 페이스북 로그인 세션 존재 시 등록된 회원의 로그인 성공하는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_social_login("facebook")  # 페이스북 로그인 버튼 클릭

    # 기대 결과: 로그인 성공 후 메인 페이지 노출
    check.equal(page.get_current_activity(), "se.ohou.screen.main.MainActivity")


@pytest.mark.session_none
def test_facebook_login_webview(wd):
    """기기 내 페이스북 로그인 세션이 없을 때 페이스북 로그인 페이지로 이동되는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_social_login("facebook")  # 페이스북 로그인 버튼 클릭

    page.switch_to_webview()  # 웹뷰 컨텍스트로 전환

    # 기대 결과: 웹뷰 페이스북 로그인 페이지 노출
    check.equal(wd.title, "Log into Facebook | Facebook")


@pytest.mark.session_exist
def test_apple_login_success_with_session(wd):
    """기기 내 애플 로그인 세션 존재 시 등록된 회원의 로그인 성공하는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_social_login("apple")  # 애플 로그인 버튼 클릭

    # 기대 결과: 로그인 성공 후 메인 페이지 노출
    check.not_equal(page.get_current_activity(), "se.ohou.screen.intro.IntroActivity")


@pytest.mark.session_none
def test_apple_login_webview(wd):
    """기기 내 애플 로그인 세션이 없을 때 애플 로그인 페이지로 이동되는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_social_login("apple")  # 애플 로그인 버튼 클릭
    apple_account = page.apple_login_text()

    # 기대 결과: 애플 계정 텍스트에 'Apple'이 포함되어야 함
    check.is_true( "Apple" in apple_account, f"애플 계정 텍스트에 'Apple'이 포함되어야 합니다. (현재: {apple_account})" )


def test_email_login_success(wd):
    """유효 ID·PW로 로그인 시 등록된 회원의 로그인 성공하는지 확인"""
    valid_account = TEST_ACCOUNTS['email'][0]  # 유효한 이메일 계정 정보 가져오기

    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_social_login("email")  # 이메일 로그인 버튼 클릭

    page.input_email(valid_account['email'])  # 이메일 입력

    page.input_password(valid_account['password'])  # 비밀번호 입력

    page.click_login_confirm()  # 로그인 확인 버튼 클릭

    # 기대 결과: 메인 페이지로 이동
    check.equal(page.get_current_activity(), "se.ohou.screen.main.MainActivity")


def test_email_login_fail_with_invalid_email(wd):
    """비유효 ID· 유효 PW로 로그인 시 등록된 회원의 로그인 성공하는지 확인"""
    invalid_email_account = TEST_ACCOUNTS['email'][1]  # 유효하지 않은 이메일 계정 정보 가져오기

    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_social_login("email")  # 이메일 로그인 버튼 클릭

    login_activity_before = page.get_current_activity()  # 로그인 전 activity 저장

    page.input_email(invalid_email_account['email'])  # 유효하지 않은 이메일 입력

    page.input_password(invalid_email_account['password'])  # 비밀번호 입력

    page.click_login_confirm()  # 로그인 확인 버튼 클릭

    toast = page.get_toast_message()  # 토스트 메시지 가져오기

    pattern = r"^10번 실패하면 10분간 로그인이 제한돼요\. \(\d+/10\)$"  # 토스트 메시지 패턴 정의

    # 기대 결과: "10번 실패하면 10분간 로그인이 제한되요 (n/10)" 의 toast 메시지가 노출됨
    check.is_true(bool(re.match(pattern, toast)))

    # 기대 결과: 현재 페이지 유지 (화면 이동 없음)
    check.equal(page.get_current_activity(), login_activity_before)


def test_email_login_fail_with_invalid_password(wd):
    """유효 ID· 비유효 PW로 로그인 시 등록된 회원의 로그인 성공하는지 확인"""
    invalid_password_account = TEST_ACCOUNTS['email'][2]  # 유효하지 않은 비밀번호 계정 정보 가져오기

    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_social_login("email")  # 이메일 로그인 버튼 클릭

    login_activity_before = page.get_current_activity()  # 로그인 전 activity 저장

    page.input_email(invalid_password_account['email'])  # 이메일 입력

    page.input_password(invalid_password_account['password'])  # 유효하지 않은 비밀번호 입력

    page.click_login_confirm()  # 로그인 확인 버튼 클릭

    toast = page.get_toast_message()  # 토스트 메시지 가져오기

    pattern = r"^10번 실패하면 10분간 로그인이 제한돼요\. \(\d+/10\)$"  # 토스트 메시지 패턴 정의

    # 기대 결과: "10번 실패하면 10분간 로그인이 제한되요 (n/10)" 의 toast 메시지가 노출됨
    check.is_true(bool(re.match(pattern, toast)))

    # 기대 결과: 현재 페이지 유지 (화면 이동 없음)
    check.equal(page.get_current_activity(), login_activity_before)
