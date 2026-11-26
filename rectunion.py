"""rectunion: 轴对齐矩形并集面积（多矩形，重叠只计一次）。

矩形为 (x1, y1, x2, y2) 四元组（列表或元组形态均可），坐标为 int/float。
本题是多个矩形的并集面积，与单多边形的鞋带面积/重心（polygonarea／centroid）
不同：仅边接触的矩形不重叠、面积直接相加；包含关系下内层矩形不增加面积。

算法：坐标压缩 + 网格扫描——把所有 x/y 边界排序去重形成网格，逐格判断是否
被任一矩形覆盖并累加面积。
"""


def union_area(rects):
    """返回轴对齐矩形列表的并集面积；空列表返回 0。

    入参约定：
    - rects 必须是列表形态；每个矩形必须是长度 4 的序列（列表或元组），
      否则抛 TypeError；
    - 坐标必须是 int/float（bool 不算），否则抛 TypeError；
    - 必须满足 x1 < x2 且 y1 < y2，否则抛 ValueError。
    """
    if not isinstance(rects, list):
        raise TypeError("rects must be a list of rectangles: %r" % (rects,))
    boxes = []
    for rect in rects:
        if not isinstance(rect, (list, tuple)):
            raise TypeError("rectangle must be a sequence: %r" % (rect,))
        if len(rect) != 4:
            raise TypeError("rectangle must have exactly 4 coordinates: %r" % (rect,))
        coords = []
        for value in rect:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(
                    "rectangle coordinates must be int or float: %r" % (value,)
                )
            coords.append(value)
        x1, y1, x2, y2 = coords
        if not (x1 < x2 and y1 < y2):
            raise ValueError(
                "rectangle must satisfy x1 < x2 and y1 < y2: %r" % (rect,)
            )
        boxes.append((x1, y1, x2, y2))
    if not boxes:
        return 0
    xs = sorted({v for b in boxes for v in (b[0], b[2])})
    ys = sorted({v for b in boxes for v in (b[1], b[3])})
    total = 0
    for i in range(len(xs) - 1):
        left, right = xs[i], xs[i + 1]
        for j in range(len(ys) - 1):
            bottom, top = ys[j], ys[j + 1]
            for x1, y1, x2, y2 in boxes:
                if x1 <= left and right <= x2 and y1 <= bottom and top <= y2:
                    total += (right - left) * (top - bottom)
                    break
    return total
