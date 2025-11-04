"""
테스트 계정 데이터 관리 파일

⚠️ 주의: 이 파일은 .gitignore에 포함되어 있어 Git에 push되지 않습니다.
실제 계정 정보를 입력하여 사용하세요.

사용 예시:
    from test_data import TEST_ACCOUNTS
    
    # 이메일 계정 사용
    email_account = TEST_ACCOUNTS['email'][0]
    email = email_account['email']
    password = email_account['password']
    
    # 카카오 계정 사용
    kakao_account = TEST_ACCOUNTS['kakao'][0]
    kakao_id = kakao_account['id']
    kakao_password = kakao_account['password']
"""

# ============================================
# 예시 데이터 (주석 처리)
# ============================================
# TEST_ACCOUNTS = {
#     'email': [
#         {
#             'name': '테스트 계정 1',
#             'email': 'test1@example.com',
#             'password': 'TestPassword123!',
#             'description': '일반 테스트용 계정'
#         },
#         {
#             'name': '테스트 계정 2',
#             'email': 'test2@example.com',
#             'password': 'TestPassword456!',
#             'description': '회원가입 테스트용 계정'
#         },
#     ],
#     'kakao': [
#         {
#             'name': '카카오 테스트 계정 1',
#             'id': 'kakao_test1@kakao.com',
#             'password': 'KakaoPassword123!',
#             'description': '카카오 로그인 테스트용'
#         },
#     ],
#     'naver': [
#         {
#             'name': '네이버 테스트 계정 1',
#             'id': 'naver_test1@naver.com',
#             'password': 'NaverPassword123!',
#             'description': '네이버 로그인 테스트용'
#         },
#     ],
#     'facebook': [
#         {
#             'name': '페이스북 테스트 계정 1',
#             'email': 'facebook_test1@facebook.com',
#             'password': 'FacebookPassword123!',
#             'description': '페이스북 로그인 테스트용'
#         },
#     ],
#     'apple': [
#         {
#             'name': '애플 테스트 계정 1',
#             'apple_id': 'apple_test1@icloud.com',
#             'password': 'ApplePassword123!',
#             'description': '애플 로그인 테스트용'
#         },
#     ],
# }

# ============================================
# 실제 테스트 계정 데이터 (여기에 입력하세요)
# ============================================
TEST_ACCOUNTS = {
    'email': [
#         {
#             'name': '테스트 계정 1',
#             'email': 'test1@example.com',
#             'password': 'TestPassword123!',
#             'description': '일반 테스트용 계정'
#         },
    ],
    'kakao': [
        # {
        #     'name': '계정 이름',
        #     'id': '카카오 계정 ID',
        #     'password': '카카오 비밀번호',
        #     'description': '계정 설명'
        # },
    ],
    'naver': [
        # {
        #     'name': '계정 이름',
        #     'id': '네이버 계정 ID',
        #     'password': '네이버 비밀번호',
        #     'description': '계정 설명'
        # },
    ],
    'facebook': [
        # {
        #     'name': '계정 이름',
        #     'email': '페이스북 이메일',
        #     'password': '페이스북 비밀번호',
        #     'description': '계정 설명'
        # },
    ],
    'apple': [
        # {
        #     'name': '계정 이름',
        #     'apple_id': '애플 ID',
        #     'password': '애플 비밀번호',
        #     'description': '계정 설명'
        # },
    ],
}

