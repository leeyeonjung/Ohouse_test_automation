# Third-party libraries
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

def compare(img1, img2):
    """
    두 이미지의 유사도를 SSIM 기반으로 계산하여 0~100 점수 반환
    img1: 원본 이미지 (str 경로 또는 PIL.Image 객체)
    img2: 비교할 이미지 (str 경로 또는 PIL.Image 객체)
    """
    # 문자열 경로면 열기
    if isinstance(img1, str):
        img1 = Image.open(img1)
    if isinstance(img2, str):
        img2 = Image.open(img2)

    # RGB로 변환 (JPG/PNG 채널 차이 제거)
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    # 원본(img1) 기준으로 세로를 통일하고 가로는 양쪽 crop
    w1, h1 = img1.size  # 원본
    w2, h2 = img2.size  # 비교 대상
    
    # 원본의 세로(h1)를 기준으로 통일
    target_h = h1
    
    # 원본의 가로/세로 비율 유지하면서 세로를 target_h로 맞춤
    ratio1 = w1 / h1
    img1_resized = img1.resize((int(target_h * ratio1), target_h), Image.Resampling.LANCZOS)
    
    # img2도 같은 세로로 리사이즈 (비율 유지)
    ratio2 = w2 / h2
    img2_resized = img2.resize((int(target_h * ratio2), target_h), Image.Resampling.LANCZOS)
    
    # 가로는 원본의 가로 크기를 기준으로 양쪽 crop
    target_w = img1_resized.size[0]  # 원본의 리사이즈된 가로 크기
    
    # img2가 target_w보다 크면 양쪽 crop
    if img2_resized.size[0] > target_w:
        left = (img2_resized.size[0] - target_w) // 2
        img2_resized = img2_resized.crop((left, 0, left + target_w, target_h))
    # img2가 target_w보다 작으면 다시 확대
    elif img2_resized.size[0] < target_w:
        img2_resized = img2_resized.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # numpy 배열 변환
    arr1 = np.array(img1_resized)
    arr2 = np.array(img2_resized)

    # SSIM 계산 (컬러 지원: channel_axis=-1)
    score, _ = ssim(arr1, arr2, channel_axis=-1, full=True)

    return round(score * 100, 2)  # 0~100 점수

open = Image.open