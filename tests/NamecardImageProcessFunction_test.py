import os
import io
import base64
import tempfile
import pytest
from PIL import Image
from logic.NamecardImageProcessFunction import ImageProcessorNamecard

def create_test_image(color=(255, 0, 0), size=(200, 200)):
    """
    指定された色とサイズでシンプルなRGB画像を生成します。
    """
    return Image.new("RGB", size, color)

def test_load_image(tmp_path):
    # テスト用画像を一時ファイルとして保存し、load_image で読み込むテスト
    processor = ImageProcessorNamecard()
    image = create_test_image(size=(100, 100))
    
    file_path = tmp_path / "test_image.jpg"
    image.save(file_path, format="JPEG")
    
    loaded_image = processor.load_image(str(file_path))
    assert isinstance(loaded_image, Image.Image)
    assert loaded_image.size == (100, 100)

def test_resize_image_with_resize_factor():
    processor = ImageProcessorNamecard()
    image = create_test_image(size=(200, 200))
    
    resized = processor.resize_image(image, resize_factor=0.5)
    # 200x200 の画像を 50% に縮小 → 100x100 になるはず
    assert resized.size == (100, 100)

def test_resize_image_with_target_size():
    processor = ImageProcessorNamecard()
    image = create_test_image(size=(200, 200))
    
    target_size = (150, 150)
    resized = processor.resize_image(image, target_size=target_size)
    assert resized.size == target_size

def test_image_to_base64():
    processor = ImageProcessorNamecard()
    image = create_test_image(size=(100, 100))
    
    encoded_str = processor.image_to_base64(image, format="JPEG")
    assert isinstance(encoded_str, str)
    assert len(encoded_str) > 0
    
    # デコードしてJPEGのシグネチャがあるか確認
    decoded = base64.b64decode(encoded_str)
    # JPEGファイルは先頭に 0xFF 0xD8 のシグネチャがある
    assert decoded.startswith(b'\xff\xd8')

def test_process_image(tmp_path):
    processor = ImageProcessorNamecard()
    image = create_test_image(size=(200, 200))
    
    file_path = tmp_path / "test_image.jpg"
    image.save(file_path, format="JPEG")
    
    # process_image で画像を50%に縮小し、Base64文字列を取得
    encoded_str = processor.process_image(str(file_path), resize_factor=0.5)
    assert isinstance(encoded_str, str)
    assert len(encoded_str) > 0
    
    # Base64文字列から画像を再生成し、サイズが 100x100 になっているか確認
    decoded = base64.b64decode(encoded_str)
    processed_image = Image.open(io.BytesIO(decoded))
    assert processed_image.size == (100, 100)
