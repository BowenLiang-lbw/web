import ctypes

seed = 111111
base = 62
num_list = ['0','1','2','3','4','5','6','7','8','9',
            'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
            'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
def int_overflow(val):
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val

def unsigned_right_shitf(n, r=24):
    if n < 0:
        n = ctypes.c_uint32(n).value
    if r < 0:
        return -int_overflow(n << abs(r))
    return int_overflow(n >> r)

def int_overflow_multiplication(a, m=1540483477):
    result = a * m
    result = int_overflow(result)
    return result

def murmurhash(origin_string):
    origin_bytes = origin_string.encode()
    length = len(origin_bytes)
    h = seed ^ length
    i = 0
    r = 24
    const = 0xff

    while (length >= 4):
        k = (origin_bytes[i] & const) + ((origin_bytes[i + 1] & const) << 8) + (
                    (origin_bytes[i + 2] & const) << 16) + ((origin_bytes[i + 3] & const) << 24)
        k = int_overflow_multiplication(k)
        k ^= k >> r
        k = int_overflow_multiplication(k)
        h = int_overflow_multiplication(h)
        h ^= k
        length -= 4
        i += 4
    if (length == 3):
        h ^= (origin_bytes[i + 2] & const) << 16
        h ^= (origin_bytes[i + 1] & const) << 8
        h ^= (origin_bytes[i] & const)
        h = int_overflow_multiplication(h)

    if (length == 2):
        h ^= (origin_bytes[i + 1] & const) << 8
        h ^= (origin_bytes[i] & const)
        h = int_overflow_multiplication(h)

    if (length == 1):
        h ^= (origin_bytes[i] & const)
        h = int_overflow_multiplication(h)

    h ^= h >> 13
    h = int_overflow_multiplication(h)
    h ^= h >> 15

    return h

def transfer(orginal_num):
    quotient = orginal_num
    result = ""
    while(quotient>0):
        remainder = int(quotient%base)
        quotient = int(quotient/base)
        result = "".join([num_list[remainder],result])
    return result


if __name__ == "__main__":
    short = murmurhash("wscb")
    print(short)
    print(transfer(short))
