import cv2
import numpy as np

def aplicar_clahe(img_gray):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(img_gray)

def corrigir_inclinacao(img_bin):
    coords = np.column_stack(np.where(img_bin > 0))
    if len(coords) == 0:
        return img_bin
        
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        
    (h, w) = img_bin.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img_bin, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return rotated

def preprocessar_para_ocr(imagem_placa_rgb):
    gray = cv2.cvtColor(imagem_placa_rgb, cv2.COLOR_BGR2GRAY)
    
    gray_contrast = aplicar_clahe(gray)
    
    blur = cv2.bilateralFilter(gray_contrast, d=11, sigmaColor=17, sigmaSpace=17)
    
    binarizada = cv2.adaptiveThreshold(
        blur, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 
        19, 9
    )
    
    binarizada_alinhada = corrigir_inclinacao(binarizada)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morfologia = cv2.morphologyEx(binarizada_alinhada, cv2.MORPH_CLOSE, kernel)
    
    imagem_final_ocr = cv2.bitwise_not(morfologia)
    
    return imagem_final_ocr