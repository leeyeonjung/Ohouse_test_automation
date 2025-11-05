# tests/testcase/test_login_page.py

# Standard library
import re

# Third-party libraries
import pytest
import pytest_check as check

# Local modules
from tests.src.pages.login_page import LoginPage
from test_data import TEST_ACCOUNTS


# Test Cases
def test_login_screen(wd, request):
    """로그인 화면 진입"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    results = page.capture_and_compare_images(request)  # 로그인 화면 이미지 캡처 및 유사도 비교

    for img_name, similarity in results.items():  # 각 이미지별 유사도 검증
        # Assertions: 로그인 화면 요소 확인 (오늘의 집, 3초만에 빠른 회원가입, 카카오톡으로 계속하기, 네이버 페이스북 애플, 이메일로 로그인 | 이메일로 가입, 로그인에 문제가 있으신가요?, 비회원 주문하기)
        check.greater_equal(similarity, 85.0, f"{img_name} 이미지 유사도가 85% 이상이어야 합니다.")


@pytest.mark.session_exist
def test_kakao_login_success_with_session(wd):
    """기기 내 카카오 로그인 세션 존재 시 등록된 회원의 로그인 성공하는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_login("kakao")  # 카카오 로그인 버튼 클릭

    page.wait_for_main_activity()
    
    # Assertions: 로그인 성공 후 메인 페이지 노출
    check.equal(page.get_current_activity(), "se.ohou.screen.main.MainActivity", "current activity is not main activity")


@pytest.mark.session_none
def test_kakao_login_webview(wd):
    """기기 내 카카오 로그인 세션이 없을 때 카카오 로그인 페이지로 이동되는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_login("kakao")  # 카카오 로그인 버튼 클릭

    page.switch_to_webview()  # 웹뷰 컨텍스트로 전환

    # Assertions: 웹뷰 카카오 로그인 페이지 노출
    check.equal(wd.title, "Kakao Account", "title is not Kakao Account")


@pytest.mark.session_exist
def test_naver_login_success_with_session(wd):
    """기기 내 네이버 로그인 세션 존재 시 등록된 회원의 로그인 성공하는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_login("naver")  # 네이버 로그인 버튼 클릭

    page.wait_for_main_activity()

    # Assertions: 로그인 성공 후 메인 페이지 노출
    check.equal(page.get_current_activity(), "se.ohou.screen.main.MainActivity", "current activity is not main activity")


@pytest.mark.session_none
def test_naver_login_webview(wd):
    """기기 내 네이버 로그인 세션이 없을 때 네이버 로그인 페이지로 이동되는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_login("naver")  # 네이버 로그인 버튼 클릭

    page.switch_to_webview()  # 웹뷰 컨텍스트로 전환

    # Assertions: 웹뷰 네이버 로그인 페이지 노출
    check.equal(wd.title, "네이버 : 로그인", "title is not 네이버 : 로그인")


@pytest.mark.session_exist
def test_facebook_login_success_with_session(wd):
    """기기 내 페이스북 로그인 세션 존재 시 등록된 회원의 로그인 성공하는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_login("facebook")  # 페이스북 로그인 버튼 클릭

    page.wait_for_main_activity()
    
    # Assertions: 로그인 성공 후 메인 페이지 노출
    check.equal(page.get_current_activity(), "se.ohou.screen.main.MainActivity", "current activity is not main activity")


@pytest.mark.session_none
def test_facebook_login_webview(wd):
    """기기 내 페이스북 로그인 세션이 없을 때 페이스북 로그인 페이지로 이동되는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_login("facebook")  # 페이스북 로그인 버튼 클릭

    page.switch_to_webview()  # 웹뷰 컨텍스트로 전환

    # Assertions: 웹뷰 페이스북 로그인 페이지 노출
    check.equal(wd.title, "Log into Facebook | Facebook", "title is not Log into Facebook | Facebook")


@pytest.mark.session_exist
def test_apple_login_success_with_session(wd):
    """기기 내 애플 로그인 세션 존재 시 등록된 회원의 로그인 성공하는지 확인"""
    """ios 디바이스에서만 테스트 가능"""
    
    page = LoginPage(wd)  # LoginPage 객체 생성
    platform = page.get_device_platform()
    if platform == "Android":
        check.skip("Android 디바이스에서는 애플 로그인 기능을 테스트할 수 없습니다.")

    """실제 ios 디바이스에서는 메인 페이지로 이동하지만
    android 디바이스에서는 애플 로그인 기능을 테스트할 수 없기 때문에 테스트는 skip하고 결과는 주석처리함"""
    # page.click_login("apple")  # 애플 로그인 버튼 클릭
    # page.wait_for_main_activity()
    
    # # Assertions: 로그인 성공 후 메인 페이지 노출
    # check.equal(page.get_current_activity(), "se.ohou.screen.main.MainActivity", "current activity is not main activity")


@pytest.mark.session_none
def test_apple_login(wd):
    """기기 내 애플 로그인 세션이 없을 때 애플 로그인 페이지로 이동되는지 확인"""
    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_login("apple")  # 애플 로그인 버튼 클릭
    apple_account = page.apple_login_text()

    # Assertions: 애플 계정 텍스트에 'Apple'이 포함되어야 함
    check.equal( "Apple" in apple_account, True, "Apple is not in the title")


def test_email_login_success(wd):
    """유효 ID·PW로 로그인 시 등록된 회원의 로그인 성공하는지 확인"""
    valid_account = TEST_ACCOUNTS['email'][0]  # 유효한 이메일 계정 정보 가져오기

    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_login("email")  # 이메일 로그인 버튼 클릭

    page.input_email(valid_account['email'])  # 이메일 입력

    page.input_password(valid_account['password'])  # 비밀번호 입력

    page.click_login_confirm()  # 로그인 확인 버튼 클릭

    page.wait_for_main_activity()

    # Assertions: 메인 페이지로 이동
    check.equal(page.get_current_activity(), "se.ohou.screen.main.MainActivity", "current activity is not main activity")


def test_email_login_fail_with_invalid_email(wd):
    """비유효 ID· 유효 PW로 로그인 시 등록된 회원의 로그인 성공하는지 확인"""
    invalid_email_account = TEST_ACCOUNTS['email'][1]  # 유효하지 않은 이메일 계정 정보 가져오기

    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_login("email")  # 이메일 로그인 버튼 클릭

    login_activity_before = page.get_current_activity()  # 로그인 전 activity 저장

    page.input_email(invalid_email_account['email'])  # 유효하지 않은 이메일 입력

    page.input_password(invalid_email_account['password'])  # 비밀번호 입력

    page.click_login_confirm()  # 로그인 확인 버튼 클릭

    toast = page.get_toast_message()  # 토스트 메시지 가져오기

    pattern = r"^10번 실패하면 10분간 로그인이 제한돼요\. \(\d+/10\)$"  # 정규식을 사용하여 토스트 메시지 패턴 정의

    # Assertions: "10번 실패하면 10분간 로그인이 제한되요 (n/10)" 의 toast 메시지가 노출됨
    check.is_true(bool(re.match(pattern, toast)), "toast message is not the expected message")

    # Assertions: 현재 페이지 유지 (화면 이동 없음)
    check.equal(page.get_current_activity(), login_activity_before, "current activity is not the same as the login activity before")


def test_email_login_fail_with_invalid_password(wd):
    """유효 ID· 비유효 PW로 로그인 시 등록된 회원의 로그인 성공하는지 확인"""
    invalid_password_account = TEST_ACCOUNTS['email'][2]  # 유효하지 않은 비밀번호 계정 정보 가져오기

    page = LoginPage(wd)  # LoginPage 객체 생성

    page.click_login("email")  # 이메일 로그인 버튼 클릭

    login_activity_before = page.get_current_activity()  # 로그인 전 activity 저장

    page.input_email(invalid_password_account['email'])  # 이메일 입력

    page.input_password(invalid_password_account['password'])  # 유효하지 않은 비밀번호 입력

    page.click_login_confirm()  # 로그인 확인 버튼 클릭

    toast = page.get_toast_message()  # 토스트 메시지 가져오기

    pattern = r"^10번 실패하면 10분간 로그인이 제한돼요\. \(\d+/10\)$"  # 정규식을 사용하여 토스트 메시지 패턴 정의

    # Assertions: "10번 실패하면 10분간 로그인이 제한되요 (n/10)" 의 toast 메시지가 노출됨
    check.is_true(bool(re.match(pattern, toast)), "toast message is not the expected message")

    # Assertions: 현재 페이지 유지 (화면 이동 없음)
    check.equal(page.get_current_activity(), login_activity_before, "current activity is not the same as the login activity before")
