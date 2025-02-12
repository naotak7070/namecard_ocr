# NamecardImageProcessFunction.py

from PIL import Image
import io
import base64

class ImageProcessorNamecard:
    """
    名刺写真の処理に関する機能を提供するクラス。
    画像の読み込み、縮小、base64 エンコードなどを行います。
    """

    def __init__(self):
        pass

    def load_image(self, file_path):
        """
        指定されたパスから画像を読み込み、PIL Image オブジェクトを返します。
        
        Parameters:
            file_path (str): 画像ファイルへのパス
        
        Returns:
            Image: 読み込んだ画像
        """
        try:
            image = Image.open(file_path)
            return image
        except Exception as e:
            raise Exception(f"Failed to load image from {file_path}: {e}")

    def resize_image(self, image, resize_factor=None, target_size=None):
        """
        画像を縮小（リサイズ）します。
        
        Parameters:
            image (Image): PIL Image オブジェクト
            resize_factor (float, optional): 縮小率（例: 0.5 なら半分の大きさに）
            target_size (tuple, optional): (幅, 高さ) を直接指定する場合。両方指定されている場合は target_size を優先
        
        Returns:
            Image: リサイズ後の画像
        """
        # Pillow 10以降では、ANTIALIASはImage.Resampling.LANCZOSに置き換えられました。
        resample_filter = Image.Resampling.LANCZOS

        if target_size:
            resized = image.resize(target_size, resample=resample_filter)
        elif resize_factor:
            width, height = image.size
            new_width = int(width * resize_factor)
            new_height = int(height * resize_factor)
            resized = image.resize((new_width, new_height), resample=resample_filter)
        else:
            # 指定がなければ元の画像をそのまま返す
            resized = image
        return resized
    
    

    def image_to_base64(self, image, format="JPEG"):
        """
        PIL Image オブジェクトを base64 エンコードされた文字列に変換します。
        
        Parameters:
            image (Image): PIL Image オブジェクト
            format (str): エンコードする画像形式（デフォルトは "JPEG"）
        
        Returns:
            str: base64 エンコードされた画像文字列
        """
        buffered = io.BytesIO()
        image.save(buffered, format=format)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str

    def process_image(self, file_path, resize_factor=None, target_size=None, format="JPEG"):
        """
        指定された画像ファイルを読み込み、必要に応じて縮小し、base64 エンコードして返します。
        readNamecard で使用するための画像データの前処理として利用できます。
        
        Parameters:
            file_path (str): 画像ファイルへのパス
            resize_factor (float, optional): 縮小率
            target_size (tuple, optional): 直接指定するサイズ (width, height)
            format (str): エンコードする画像形式（デフォルトは "JPEG"）
        
        Returns:
            str: base64 エンコードされた画像文字列
        """
        image = self.load_image(file_path)
        image = self.resize_image(image, resize_factor, target_size)
        base64_str = self.image_to_base64(image, format=format)
        return base64_str
