from polypy.base import x


def test_call():
    f = 2*x
    assert f(2) == 4

def test_str():
    f = 2 * x
    assert str(f) == "2x"

    f = x * 2
    assert str(f) == "2x"

def test_square():
    f = x
    assert f*x == x**2

def test_square_with_coefficient():
    f = 2*x
    assert f*x == (2*x)**2
