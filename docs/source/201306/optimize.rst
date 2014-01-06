=======================
优化算法
======================

计算两条线段是否相交， 两条线段的坐标分别是A: (x1, y1), (x2, y2)， B: (x3, y3), (x4, y4)

.. code-block:: python

    den = (y4-y3) * (x2-x1) - (x4-x3) * (y2-y1)
    if den == 0: #平行
        return 0

    ua = ( (x4-x3)*(y1-y3) - (y4-y3) * (x1-x3) )/den
    ub = ( (x2-x1)*(y1-y3) - (y2-y1) * (x1-x3) )/den
    if ua > 0 and ua < 1 and ub >0 and ub < 1:
        return 1
    return 0
