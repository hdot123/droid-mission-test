"""angle.py 的验收测试（第四十二轮 · 并发 D 单）。"""

import angle


def test_deg2rad_180():
    assert abs(angle.deg2rad(180) - 3.141592653589793) < 1e-12


def test_deg2rad_90():
    assert abs(angle.deg2rad(90) - 1.5707963267948966) < 1e-12


def test_deg2rad_45():
    assert abs(angle.deg2rad(45) - 0.7853981633974483) < 1e-12


def test_rad2deg_pi():
    assert abs(angle.rad2deg(3.141592653589793) - 180.0) < 1e-12


def test_normalize_deg_370():
    assert angle.normalize_deg(370) == 10.0


def test_normalize_deg_neg10():
    assert angle.normalize_deg(-10) == 350.0


def test_normalize_deg_720():
    assert angle.normalize_deg(720) == 0.0


def test_normalize_deg_360():
    assert angle.normalize_deg(360) == 0.0


def test_normalize_deg_0():
    assert angle.normalize_deg(0) == 0.0
