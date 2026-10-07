"""Unit tests for Shannon entropy algorithms and information-theoretic calculations."""
import math
import pytest
from backend.app.engine.features import calculate_shannon_entropy


def test_entropy_empty_string():
    """Verify that empty string returns exactly 0.0 entropy."""
    assert calculate_shannon_entropy("") == 0.0


def test_entropy_single_character():
    """Verify that a string with identical repeating characters has 0.0 entropy."""
    assert calculate_shannon_entropy("a") == 0.0
    assert calculate_shannon_entropy("aaaaaaa") == 0.0
    assert calculate_shannon_entropy("ZZZZZZZZZZZZZZZZ") == 0.0


def test_entropy_binary_uniform():
    """Verify that two symbols with equal probability yield exactly 1.0 bit entropy."""
    # H = - (0.5*log2(0.5) + 0.5*log2(0.5)) = - (-0.5 - 0.5) = 1.0
    assert calculate_shannon_entropy("01") == 1.0
    assert calculate_shannon_entropy("01010101") == 1.0
    assert calculate_shannon_entropy("abababab") == 1.0


def test_entropy_four_uniform_symbols():
    """Verify that 4 equally probable symbols yield exactly 2.0 bits entropy."""
    # log2(4) = 2.0
    assert calculate_shannon_entropy("abcd") == 2.0
    assert calculate_shannon_entropy("aabbccdd") == 2.0


def test_entropy_eight_uniform_symbols():
    """Verify that 8 equally probable symbols yield exactly 3.0 bits entropy."""
    # log2(8) = 3.0
    assert calculate_shannon_entropy("abcdefgh") == 3.0


def test_entropy_sixteen_uniform_symbols():
    """Verify that 16 distinct symbols yield exactly 4.0 bits entropy."""
    # log2(16) = 4.0
    symbols = "0123456789abcdef"
    assert calculate_shannon_entropy(symbols) == 4.0


def test_entropy_dga_vs_natural_words():
    """Verify that algorithmic/random domain strings have significantly higher entropy than natural words."""
    dga_domain = "xkq7m9w2znb4"
    natural_domain = "google"
    service_domain = "services"

    dga_entropy = calculate_shannon_entropy(dga_domain)
    natural_entropy = calculate_shannon_entropy(natural_domain)
    service_entropy = calculate_shannon_entropy(service_domain)

    assert dga_entropy > 3.0
    assert dga_entropy > natural_entropy
    assert dga_entropy > service_entropy


def test_entropy_numerical_stability():
    """Verify numerical stability on long strings and mixed character sets."""
    long_string = "a" * 1000 + "b" * 1000
    entropy = calculate_shannon_entropy(long_string)
    assert entropy == 1.0

    diverse_string = "".join(chr(i) for i in range(32, 127))
    expected = round(math.log2(95), 4)
    assert calculate_shannon_entropy(diverse_string) == expected
