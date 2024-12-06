def is_prime(n: int) -> bool:
    """
    Check if a number is prime.
    
    Args:
        n (int): Number to check for primality
    
    Returns:
        bool: True if the number is prime, False otherwise
    
    Raises:
        ValueError: If input is less than 2
    """
    if n < 2:
        raise ValueError("Prime numbers are defined for integers >= 2")
    
    # Optimization: Check only up to square root
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(start: int = 2, end: int = 100) -> list[int]:
    """
    Generate a list of prime numbers within a given range.
    
    Args:
        start (int, optional): Starting number. Defaults to 2.
        end (int, optional): Ending number. Defaults to 100.
    
    Returns:
        list[int]: List of prime numbers in the range
    
    Raises:
        ValueError: If start is less than 2 or end is less than start
    """
    if start < 2:
        raise ValueError("Start must be at least 2")
    if end < start:
        raise ValueError("End must be greater than or equal to start")
    
    return [num for num in range(start, end + 1) if is_prime(num)]

def nth_prime(n: int) -> int:
    """
    Find the nth prime number.
    
    Args:
        n (int): The position of the prime number to find
    
    Returns:
        int: The nth prime number
    
    Raises:
        ValueError: If n is less than 1
    """
    if n < 1:
        raise ValueError("n must be a positive integer")
    
    count = 0
    candidate = 2
    
    while True:
        if is_prime(candidate):
            count += 1
            if count == n:
                return candidate
        candidate += 1

def prime_factors(n: int) -> list[int]:
    """
    Compute the prime factors of a given number.
    
    Args:
        n (int): Number to factorize
    
    Returns:
        list[int]: List of prime factors
    
    Raises:
        ValueError: If input is less than 2
    """
    if n < 2:
        raise ValueError("Prime factorization is defined for integers >= 2")
    
    factors = []
    divisor = 2
    
    while divisor * divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        else:
            divisor += 1
    
    if n > 1:
        factors.append(n)
    
    return factors

def count_primes_in_range(start: int, end: int) -> int:
    """
    Count the number of prime numbers in a given range.
    
    Args:
        start (int): Starting number of the range
        end (int): Ending number of the range
    
    Returns:
        int: Number of prime numbers in the range
    
    Raises:
        ValueError: If start is less than 2 or end is less than start
    """
    return len(generate_primes(start, end))