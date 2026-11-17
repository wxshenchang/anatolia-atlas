"""江山时序 VLQ 编解码（Python 侧），用于生成 PROVINCE_OUTLINES / HYDRO_DATA。
格式（与 js/china_geo_data.js 的 dec() 完全一致）:
  alphabet 64 字符, 每字符 5 bit（bit5=32 为续位）, zigzag 有符号, 坐标 x100（两位小数）, 逐点差分。
"""
import json
import os
import math
import re

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-"
IDX = {c: i for i, c in enumerate(ALPHABET)}


def decode(s: str):
    """返回 [[lon, lat], ...]"""
    out = []
    i, n = 0, len(s)
    x = y = 0
    while i < n:
        # x
        sh = 0
        v = 0
        while True:
            b = IDX[s[i]]; i += 1
            v |= (b & 31) << sh
            sh += 5
            if b < 32:
                break
        x += ~(v >> 1) if (v & 1) else (v >> 1)
        # y
        sh = 0
        v = 0
        while True:
            b = IDX[s[i]]; i += 1
            v |= (b & 31) << sh
            sh += 5
            if b < 32:
                break
        y += ~(v >> 1) if (v & 1) else (v >> 1)
        out.append([x / 100.0, y / 100.0])
    return out


def _num(v: int) -> str:
    v = (v << 1) ^ (v >> 31) if v < 0 else (v << 1)   # zigzag（与 JS 的 ~(v>>>1) 对应）
    v &= 0xFFFFFFFF
    zz = ((v >> 1) ^ -(v & 1)) & 0xFFFFFFFF
    # 直接用标准 zigzag
    zz = ((-v) << 1) | 1 if v < 0 else (v << 1)
    out = []
    while True:
        b = zz & 31
        zz >>= 5
        if zz:
            out.append(ALPHABET[b | 32])
        else:
            out.append(ALPHABET[b])
            break
    return "".join(out)


def _zz(n: int) -> int:
    return (n << 1) if n >= 0 else ((-n << 1) - 1)


def encode(points, scale: int = 100) -> str:
    """points: [[lon, lat], ...] -> VLQ string（逐点差分）"""
    out = []
    px = py = 0
    for lon, lat in points:
        x = int(round(lon * scale))
        y = int(round(lat * scale))
        out.append(_varint(_zz(x - px)))
        out.append(_varint(_zz(y - py)))
        px, py = x, y
    return "".join(out)


def _varint(v: int) -> str:
    o = []
    while True:
        b = v & 31
        v >>= 5
        if v:
            o.append(ALPHABET[b | 32])
        else:
            o.append(ALPHABET[b])
            break
    return "".join(o)


if __name__ == "__main__":
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "china_geo_data.js")
    txt = open(src, encoding="utf-8").read()
    # 取 PROVINCE_OUTLINES 里第一个省的第一个环做往返测试
    m = re.search(r'\{"title":"北京市".*?"rings":\[\["([^"]+)"', txt)
    s = m.group(1)
    pts = decode(s)
    s2 = encode(pts)
    print("样本长度:", len(s), "→ 解码点数:", len(pts), "→ 重编码长度:", len(s2))
    print("往返一致:", s == s2)
    if s != s2:
        for i, (a, b) in enumerate(zip(s, s2)):
            if a != b:
                print("首个差异位置", i, repr(s[max(0,i-10):i+10]), "vs", repr(s2[max(0,i-10):i+10]))
                break
    print("首末点:", pts[0], pts[-1])
