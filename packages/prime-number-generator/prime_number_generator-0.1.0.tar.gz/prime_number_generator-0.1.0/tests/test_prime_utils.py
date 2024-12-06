import pytest
from prime_generator import is_prime, generate_primes, nth_prime, prime_factors, count_primes_in_range

def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(10) is False
    assert is_prime(13) is True

def test_generate_primes():
    assert generate_primes(2, 10) == [2, 3, 5, 7]

def test_nth_prime():
    assert nth_prime(1) == 2
    assert nth_prime(5) == 11

def test_prime_factors():
    assert prime_factors(28) == [2, 2, 7]

def test_count_primes_in_range():
    assert count_primes_in_range(10, 20) == 4
