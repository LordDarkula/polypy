from polypy.base import x


def test_call():
    f = 2 * x
    assert f(2) == 4

    f = 3 * x ** 2
    assert f(3) == 27


def test_str():
    f = 2 * x
    assert str(f) == "2x"

    f = x * 2
    assert str(f) == "2x"


def test_square():
    f = x
    assert f * x == x ** 2

    f = 3 * x
    assert f ** 2 == 9 * x ** 2


def test_multiply_x_and_linear_term():
    f = 2 * x
    assert f * x == (2 * x ** 2)


def test_multiply_two_linear_terms():
    assert (3 * x) * (2 * x) == 6 * x ** 2


def test_multiply_two_linear_expressions():
    assert str((x + 1) * (x + 2)) == "x^2 + 2x + x + 2"
