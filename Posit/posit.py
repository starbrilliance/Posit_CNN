from Posit import unum


class PositN8E1(object):
    def __init__(self, arg=0):
        self.__p8_1 = unum.Posit_8_1_t(arg)

    def to_int(self):
        return self.__p8_1.to_int()

    def to_long(self):
        return self.__p8_1.to_long()

    def to_longlong(self):
        return self.__p8_1.long_long()

    def to_float(self):
        return self.__p8_1.to_float()

    def to_double(self):
        return self.__p8_1.to_double()

    def to_longdouble(self):
        return self.__p8_1.to_long_double()

    def value_string(self):
        return unum.posit_to_string_8_1(self.__p8_1)

    def format_bits_string(self):
        return unum.to_binary_8_1(self.__p8_1)

    def raw_bin_string(self, separate=False):
        bb = self.__p8_1.get()
        return unum.bitblock_8_tobitstring(bb, separate)

    def raw_hex_string(self):
        bb = self.__p8_1.get()
        return unum.bitblock_8_tohexstring(bb)

    def base2_sci_string(self):
        return unum.posit_to_base2_scientific_8_1(self.__p8_1)

    def assign(self, arg):
        return self.__p8_1.assign(arg)

    def set_minpos(self):
        self.__p8_1 = unum.minpos_8_1()
        return self

    def set_maxpos(self):
        self.__p8_1 = unum.maxpos_8_1()
        return self

    def set_zero(self):
        self.__p8_1 = unum.Posit_8_1_t(0)
        return self

    def set_one(self):
        self.__p8_1 = unum.Posit_8_1_t(1)
        return self

    def set_nar(self):
        return self.set_from_bits(1 << 7)

    def fma(self, mul, add):
        p = unum.Posit_8_1_t()
        res = unum.fma_8_1(self.__p8_1, mul.__p8_1, add.__p8_1)
        unum.convert_15_to_8(res, p)
        out = PositN8E1()
        out.__p8_1 = p
        return out

    def fam(self, add, mul):
        p = unum.Posit_8_1_t()
        res = unum.fam_8_1(self.__p8_1, add.__p8_1, mul.__p8_1)
        unum.convert_20_to_8(res, p)
        out = PositN8E1()
        out.__p8_1 = p
        return out

    def bits_plus_one(self):
        self.__p8_1.increment()
        return self

    def bits_minus_one(self):
        self.__p8_1.decrement()
        return self

    def reciprocate(self):
        res = self.__p8_1.reciprocate()
        return PositN8E1(res)

    def set_from_bits(self, value):
        self.__p8_1.set_raw_bits(value)
        return self

    def abs(self):
        res = self.__p8_1.abs()
        return PositN8E1(res)

    def isnar(self):
        return self.__p8_1.isnar()

    def iszero(self):
        return self.__p8_1.iszero()

    def isone(self):
        return self.__p8_1.isone()

    def isminusone(self):
        return self.__p8_1.isminusone()

    def isneg(self):
        return self.__p8_1.isneg()

    def ispos(self):
        return self.__p8_1.ispos()

    def ispowerof2(self):
        return self.__p8_1.ispowerof2()

    def cfg(self):
        return self.__p8_1.cfg()

    def __neg__(self):
        res = -self.__p8_1
        return PositN8E1(res)

    def __pos__(self):
        res = +self.__p8_1
        return PositN8E1(res)

    def __iadd__(self, rhs):
        self.__p8_1 += rhs.__p8_1
        return self

    def __isub__(self, rhs):
        self.__p8_1 -= rhs.__p8_1
        return self

    def __imul__(self, rhs):
        self.__p8_1 *= rhs.__p8_1
        return self

    def __itruediv__(self, rhs):
        self.__p8_1 /= rhs.__p8_1
        return self

    def __add__(self, rhs):
        res = unum.__add__(self.__p8_1, rhs.__p8_1)
        return PositN8E1(res)

    def __sub__(self, rhs):
        res = unum.__sub__(self.__p8_1, rhs.__p8_1)
        return PositN8E1(res)

    def __mul__(self, rhs):
        res = unum.__mul__(self.__p8_1, rhs.__p8_1)
        return PositN8E1(res)

    def __truediv__(self, rhs):
        res = unum.__truediv__(self.__p8_1, rhs.__p8_1)
        return PositN8E1(res)

    def __eq__(self, rhs):
        return unum.__eq__(self.__p8_1, rhs.__p8_1)

    def __ne__(self, rhs):
        return unum.__ne__(self.__p8_1, rhs.__p8_1)

    def __lt__(self, rhs):
        return unum.__lt__(self.__p8_1, rhs.__p8_1)

    def __gt__(self, rhs):
        return unum.__gt__(self.__p8_1, rhs.__p8_1)

    def __le__(self, rhs):
        return unum.__le__(self.__p8_1, rhs.__p8_1)

    def __ge__(self, rhs):
        return unum.__ge__(self.__p8_1, rhs.__p8_1)
