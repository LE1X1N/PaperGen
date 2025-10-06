from PIL import Image
import cv2
import numpy as np
import io
import base64

# from src.errors import  WhiteScreenshotError

# def post_processing_img(img_path, style):    
#     # 1. crop right scrollbar
#     _crop_scrollbar(img_path) 
    
#     # 2. crop by edge detection
#     if style == 1 or style == 2:
#         _crop_by_edge_detection(img_path)
    
#     # 3. solid color detection
#     if _isSolidColorImage(img_path):
#         raise WhiteScreenshotError
#     return img_path


def post_processing_img_b64(img_b64, style):    
    # 1. crop right scrollbar
    img_b64 = _crop_scrollbar_b64(img_b64) 
    
    # 2. crop by edge detection
    if style == 1 or style == 2:
        img_b64 = _crop_by_edge_detection_b64(img_b64)
    return img_b64


def _crop_scrollbar(img_path, output_path: str=None, crop_width: int=20):
    # crop right scrollbar
    img = Image.open(img_path).convert('RGB')
    width, height = img.size    
    img = img.crop((0, 0, width-crop_width, height))

    save_path = img_path if output_path is None else output_path
    img.save(save_path)
    return save_path

def _crop_scrollbar_b64(img_b64, crop_width: int=20):
    # crop right scrollbar based on base64 encoded images
    img = Image.open(io.BytesIO(base64.b64decode(img_b64))).convert('RGB')  # b64 to PIL
    width, height = img.size    
    img = img.crop((0, 0, width-crop_width, height))
    
    img_io = io.BytesIO()
    img.save(img_io, format="PNG")
    img_b64 = base64.b64encode(img_io.getvalue()).decode("utf-8")
    return img_b64
    

def _crop_by_edge_detection(img_path, output_path=None):
    
    img = Image.open(img_path).convert('RGB')
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    height, width = cv_img.shape[:2]
    
    blurred = cv2.GaussianBlur(cv_img, (5, 5), 0)
    
    v = np.median(blurred)
    lower = int(max(0, (1.0 - 0.33) * v))
    upper = int(min(255, (1.0 + 0.33) * v))
    edges = cv2.Canny(blurred, lower, upper)
    
    edge_coords = np.where(edges > 0)  
    
    if len(edge_coords[0]) == 0:
        return img
    
    min_y, max_y = np.min(edge_coords[0]), np.max(edge_coords[0])
    min_x, max_x = np.min(edge_coords[1]), np.max(edge_coords[1])
    
    padding = 5
    min_x = max(0, min_x - padding)
    max_x = min(width - 1, max_x + padding)
    min_y = max(0, min_y - padding)
    max_y = min(height - 1, max_y + padding)
    
    cropped_img = img.crop((min_x, min_y, max_x + 1, max_y + 1))
    
    save_path = output_path if output_path else img_path
    cropped_img.save(save_path)
    return cropped_img


def _crop_by_edge_detection_b64(img_b64):
    img = Image.open(io.BytesIO(base64.b64decode(img_b64))).convert('RGB')  # b64 to PIL
    
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    height, width = cv_img.shape[:2]
    
    blurred = cv2.GaussianBlur(cv_img, (5, 5), 0)
    
    v = np.median(blurred)
    lower = int(max(0, (1.0 - 0.33) * v))
    upper = int(min(255, (1.0 + 0.33) * v))
    edges = cv2.Canny(blurred, lower, upper)
    
    edge_coords = np.where(edges > 0)  
    
    if len(edge_coords[0]) == 0:
        return img
    
    min_y, max_y = np.min(edge_coords[0]), np.max(edge_coords[0])
    min_x, max_x = np.min(edge_coords[1]), np.max(edge_coords[1])
    
    padding = 5
    min_x = max(0, min_x - padding)
    max_x = min(width - 1, max_x + padding)
    min_y = max(0, min_y - padding)
    max_y = min(height - 1, max_y + padding)
    
    cropped_img = img.crop((min_x, min_y, max_x + 1, max_y + 1))
    
    # PIL to base64
    img_io = io.BytesIO()
    cropped_img.save(img_io, format="PNG")
    img_b64 = base64.b64encode(img_io.getvalue()).decode("utf-8")
    return img_b64


def _crop_by_black_border(img_path, output_path=None, threshold=230):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)
    
    cropped_img = img[y:y+h, x:x+w]
    save_path = output_path if output_path else img_path
    cv2.imwrite(save_path, cropped_img)
    return cropped_img


def _isSolidColorImage(img_path, max_size=400, tolerance=0.92):
        
    with Image.open(img_path) as img:
        
        width, height = img.size
        if max(width, height) > max_size:
        
            scale = max_size / max(width, height)
            new_width = int(width * scale)
            new_height = int(height * scale)
        
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        gray_img = img.convert('L')  
        
        pixels = list(gray_img.getdata())
        total_pixels = len(pixels)
        pixel_counts = {}
        for p in pixels:
            pixel_counts[p] = pixel_counts.get(p, 0) + 1
        
        if not pixel_counts:
            return True
        
        max_count = max(pixel_counts.values())
        peak_ratio = max_count / float(total_pixels)
        
        return peak_ratio >= tolerance
