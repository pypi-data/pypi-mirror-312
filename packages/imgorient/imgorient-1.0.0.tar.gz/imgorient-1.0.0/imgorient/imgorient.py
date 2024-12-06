import sys
import math
import click
import cv2
import numpy as np
from loguru import logger
# logの設定
logger.remove()
logger.add(sys.stderr, level="INFO", format="{level}: {message}")

from .version import __version__

######################################

@click.command()
@click.argument("img_path", type=click.Path(exists=True), required=False)
@click.option("--radian", "-r", is_flag=True, help="Output angle in radian.")
@click.option("--version", "-v", is_flag=True, help="Show version.")
# TODO: 長方形の場合にも対応させる
# TODO: 配向の矢印がついた画像を出力する機能を追加する
def main(img_path, version, radian):
    if version:
        logger.info(f"v{__version__}")
        exit(0)
    if img_path is None:
        logger.error("Input image path is required")
        exit(1)
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    if h != w:
        logger.error("Input image must be square")
        exit(1)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) #グレースケール変換
    if len(np.unique(img)) == 1:
        logger.error("Input image must be composed of multiple colors")
        exit(1)
    #0~255で規格化
    max, min = np.max(img), np.min(img)
    img = (img - min)/(max - min)*255
    img = img.astype(np.uint8)

    #FFTの実行
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    spectrum = np.abs(fshift)
    spectrum = spectrum[1:, 1:] #余分な端を削除する
    spectrum = np.rot90(spectrum) #視覚的にわかりやすいように、90度回転させる

    n = len(spectrum)//2
    thetas = np.arange(1,360,2)
    thetas_rad = np.deg2rad(thetas).reshape(len(thetas),1)
    r = np.tile(np.arange(1,n+1,1),(len(thetas),1))
    x = r * np.cos(thetas_rad)
    y = r * np.sin(thetas_rad)

    #近傍の2点を計算する関数
    vfunc = np.vectorize(lambda x: (math.ceil(x)-1, math.ceil(x)) if x >= 0 else (math.floor(x), math.floor(x)+1))
    xa, xb = vfunc(x)
    ya, yb = vfunc(y)
    Xa, Xb = xa + n, xb + n
    Ya, Yb = n - ya, n - yb
    dx = x - xa
    dy = y - ya
    p = (1-dx)*(1-dy)*spectrum[Ya,Xa] + dx*(1-dy)*spectrum[Ya,Xb] + (1-dx)*dy*spectrum[Yb,Xa] + dx*dy*spectrum[Yb,Xb]
    p_avgs = np.mean(p, axis=1)
    #(r,P)極座標から(x,y)座標のリストを作成
    x = p_avgs*np.cos(np.deg2rad(thetas))
    y = p_avgs*np.sin(np.deg2rad(thetas))

    #最小二乗法で近似楕円を計算
    A = np.array([x**2,x*y,y**2]).T
    b = np.ones(len(x))
    w = np.linalg.lstsq(A,b,rcond=None)[0]

    #楕円方程式の係数行列から固有値と単位固有ベクトルを計算
    O = np.array([[w[0], w[1]/2],
                  [w[1]/2, w[2]]])
    vals, vecs = np.linalg.eig(O)

    #固有ベクトルは軸長の逆数の2乗, 固有値が小さい方の固有ベクトルが長軸ベクトル,
    if vals[0]>vals[1]:
        minor_axis = 1/np.sqrt(vals[0])
        major_axis = 1/np.sqrt(vals[1])
        minor_vec = vecs[:,0]
        major_vec = vecs[:,1]
    else:
        minor_axis = 1/np.sqrt(vals[1])
        major_axis = 1/np.sqrt(vals[0])
        minor_vec = vecs[:,1]
        major_vec = vecs[:,0]

    intensity = (major_axis - minor_axis)/(major_axis + minor_axis)
    angle = np.arctan(major_vec[1]/major_vec[0])
    if not radian:
        angle = np.rad2deg(np.arctan(major_vec[1]/major_vec[0]))
    print(f"angle: {angle}\nintensity: {intensity}")

if __name__ == "__main__":   
    main()
    