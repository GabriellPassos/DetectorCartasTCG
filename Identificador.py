import cv2
import numpy as np
def DetectarObjetos(imagem, minAltura, maxAltura, minLargura, maxLargura, maxPontosContorno = 60):
    areas = []
    g = 0
    imagemCp = imagem.copy()
    imagemCinza = cv2.cvtColor(imagemCp, cv2.COLOR_BGR2GRAY)
    desfoque = cv2.GaussianBlur(imagemCinza, (17,17), 0)
    threshold = cv2.adaptiveThreshold(desfoque, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 12)
    threshold = cv2.bitwise_not(threshold)
    contornos, hierarquia = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contornos:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx) >= 4 and len(cnt) > maxPontosContorno:
            g = g + 1
            x, y, largura, altura = cv2.boundingRect(cnt)
            if(minAltura <= altura and maxAltura >= altura and
                minLargura <= largura and maxLargura >= largura):
                areas.append({
                    'x': x,
                    'y': y,
                    'largura': largura,
                    'altura': altura
                })
                ratio = float(largura)/altura
                if ratio >= 0.9 and ratio <= 1.1:
                    imagemComContorno = cv2.drawContours(imagemCp, [cnt], -1, (0,255,255), 2)
                else:
                    imagemComContorno = cv2.drawContours(imagemCp, [cnt], -1, (0,255,0), 2)
                imagemComContorno = cv2.resize(imagemComContorno, (0,0), fx=.5,fy=.5)
    if(areas):
        return areas, imagemComContorno
    raise Exception("Nenhum objeto encontrado")
def Recortar(imagem, areas):
    imagemCp = imagem.copy()
    recortes = []
    for area in areas:
        recortes.append(imagemCp[area['y']: area['y'] + area['altura'], area['x']: area['x'] + area['largura']])
    return recortes
def Redimensionar(imagem, altura, largura):
    return cv2.resize(imagem, (0, 0), fx= largura / imagem.shape[1], fy=altura / imagem.shape[0])
'''def DetectarTexto(imagem):
    imagemCp = imagem.copy()
    imagemCp = cv2.resize(imagemCp, (0,0), fx=3,fy=3)
    imagemCinza = cv2.cvtColor(imagemCp, cv2.COLOR_BGR2GRAY)
    thresult = cv2.adaptiveThreshold(imagemCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 12)
    texto = pytesseract.image_to_string(thresult,lang='eng+por')
    return texto'''
def RecortarTitulo(imagem):
    largura, altura, canal = imagem.shape
    return imagem[: int(altura / 6)]

def Identificar(imagem, minAltura, maxAltura, minLargura, maxLargura,maxPontosContorno=80):
        if imagem:
            imageArray = np.array(imagem)
            areasDet, imgComContorno = DetectarObjetos(imageArray, minAltura, maxAltura, minLargura, maxLargura,maxPontosContorno)
            recortes = Recortar(imageArray, areasDet)
            return recortes


