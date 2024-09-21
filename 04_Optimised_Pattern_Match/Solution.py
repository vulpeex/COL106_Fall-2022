import random
import math

# To generate random prime less than N


def randPrime(N):
    primes = []
    for q in range(2, N+1):
        if (isPrime(q)):
            primes.append(q)
    return primes[random.randint(0, len(primes)-1)]

# To check(if a number is prime


def isPrime(q):
    if (q > 1):
        for i in range(2, int(math.sqrt(q)) + 1):
            if (q % i == 0):
                return False
        return True
    else:
        return False

# pattern matching


def randPatternMatch(eps, p, x):
    '''
    max(q)=N so maximum logN bits in q. N=aloga, a=c*m/eps.
    So O(logm/eps) space needed to store q.
    '''
    N = findN(eps, len(p))
    q = randPrime(N)
    return modPatternMatch(q, p, x)

# pattern matching with wildcard


def randPatternMatchWildcard(eps, p, x):
    '''
    max(q)=N so maximum logN bits in q. N=aloga, a=c*m/eps.
    So O(logm/eps) space needed to store q.
    '''
    N = findN(eps, len(p))
    q = randPrime(N)
    return modPatternMatchWildcard(q, p, x)

# return appropriate N that satisfies the error bounds


def findN(eps, m):
    '''
    x= hash of the pattern
    y=has of the substring
    (x%q=y%q means (x-y)%q=0 or q divides (x-y))
    If N is the chosen upper limit, then:
    Probability of reporting false positives is = (number of primes less than N, which divide (x-y))/(number of primes less than N)<=eps

    ((x-y) is max 26^m-1. Sum of GP)
    A number w, has atmost log w divisors.
    Mumber of primes less than N, which divide (x-y)<= log (x-y) <= log(26^m-1) approx mlog26.

    number of primes less than N> N/2logN

    mlog26*2*logN/N <= eps
    or

    (2mlog26)/eps<=N/logN

    Let 2mlog26/eps=t

    To solve this, we assume solution of form aloga as we have a log in denominator and we want to cancel it.

    t<= aloga/(loga+logloga)
    logloga<loga
    So,
    t<=aloga/(2loga)
    or 
    2t<=a
    thus, N=aloga=2tlog2t
    '''
    # log 26 is approx 5.
    a = 20*m/eps
    # Using factor of 2 for safety
    N = (2*a*math.log2(a))
    return int(N)+1

# Return sorted list of starting indices where p matches x


def check(a):
    '''Return the correct integer value of character'''
    return ord(a)-ord('A')


def modPatternMatch(q, p, x):
    # O((m+n)*logq) time
    # O(k+logq+logn) space
    i = 0  # Storing i takes O(logn) space. index of the text.
    t = 0  # Storing t takes O(logq) space. Hash of pattern.
    l = []  # list to store the answer. O(k) space.
    s = 0  # Storing s takes O(logq) space. Hash of substring
    mo = 1  # O(logq) space
    for j in range(len(p)-1, -1, -1):  # O(m*logq) Time Complexity
        # O(logq) Time Complexity since arithmetic operations take logq time.
        t += (mo*(check(p[j]) % q)) % q
        # O(logq) Time Complexity since arithmetic operations take logq time.
        s += (mo*(check(x[j]) % q)) % q
        mo *= 26  # O(logq) Time Complexity
        mo = mo % q
    t = t % q
    s = s % q
    if s == t:
        l.append(0)
    while i < len(x)-len(p):  # O(nlogq) time
        s = (s*(26 % q)) % q  # O(logq) time
        # O(logq) time
        s += (check(x[i+len(p)])+q -
              (mo*(check(x[i]) % q))) % q
        s = s % q
        if s == t:
            l.append(i+1)
        i += 1
    return l


# Return sorted list of starting indices where p matches x


def modPatternMatchWildcard(q, p, x):
    # O((m+n)*logq) time
    # O(k+logq+logn) space
    i = 0  # Storing i takes O(logn) space. index of the text.
    t = 0  # Storing t takes O(logq) space. Hash of pattern.
    l = []  # list to store the answer. O(k) space.
    s = 0  # Storing s takes O(logq) space. Hash of substring
    # Storing k takes O(logm) space. Since log(m)<logn as m<n, space is O(logn)
    k = 0
    mo = 1  # O(logq) space
    for j in range(len(p)-1, -1, -1):  # O(m*logq) Time Complexity
        if p[j] != '?':
            # O(logq) Time Complexity since arithmetic operations take logq time.
            t += (mo*(check(p[j]) % q)) % q
            # O(logq) Time Complexity since arithmetic operations take logq time.
            s += (mo*(check(x[j]) % q)) % q
        else:
            mi = mo
            k = j
        if p[j-1] == '?':
            mii = mo
        mo *= 26  # O(logq) Time Complexity
        mo = mo % q
    t = t % q
    s = s % q
    if s == t:
        l.append(0)
    while i < len(x)-len(p):  # O(nlogq) time
        if len(p)-k-2 >= 0:
            s += (mi*(check(x[i+k]))+q-(mii) *
                  ((check(x[i+k+1])))) % q  # O(logq) time
            s = (s*(26 % q)) % q  # O(logq) time
            s += (check(x[i+len(p)])+q -
                  (mo*(check(x[i]) % q))) % q  # O(logq) time
            s = s % q
        else:
            s += (check(x[i+k])) % q  # O(logq) time
            s = (s*(26 % q)) % q  # O(logq) time
            s += (q - (mo*(check(x[i]) % q))) % q  # O(logq) time
            s = s % q
        if s == t:
            l.append(i+1)
        i += 1
    return l


# print(modPatternMatch(1000000007, 'CD', 'ABCDE'))
# # [2]
# print(modPatternMatch(1000000007, 'AA', 'AAAAA'))
# # [0, 1, 2, 3]
# print(modPatternMatchWildcard(1000000007, 'D?', 'ABCDE'))
# # [3]
# print(modPatternMatch(2, 'AA', 'ACEGI'))
# # [0, 1, 2, 3]
# print(modPatternMatchWildcard(1000000007, '?A', 'ABCDE'))
# # []
# print(modPatternMatchWildcard(
#     19, 'JA?S', 'AMADBOXERSHOTQUICKGLOVEDJABSTOTHEJAWSOFHISDIZZYOPPONENTATTHEJAMSROCKSHUFFLE'))
# # [7, 23, 24, 33, 36, 60]
# print(modPatternMatchWildcard(
#     79, 'JA?S', 'AMADBOXERSHOTQUICKGLOVEDJABSTOTHEJAWSOFHISDIZZYOPPONENTATTHEJAMSROCKSHUFFLE'))
# # [24, 33, 60]
