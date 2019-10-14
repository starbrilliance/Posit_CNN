from Posit import posit, unum


class QuireN8E1C14(object):
    def __init__(self, arg=0):
        self.__q8_1_14 = unum.Quire_8_1_14_t(arg)

    def set_from_bits(self, bits, radix=2):
        bin_bits = bin(int(bits, radix))[2:]
        pad_bits = "{:0>64}".format(bin_bits)

        if pad_bits[0] == '0':
            sign = "+:"
        else:
            sign = "-:"

        res = sign + pad_bits[1:15] + "_" + pad_bits[15:40] \
              + "." + pad_bits[40:]

        self.__q8_1_14.load_bits(res)
        return self

    def to_posit8_1(self):
        p8 = unum.Posit_8_1_t()
        q2v = unum.quire_to_value_8_1_14(self.__q8_1_14)
        unum.convert_q8_to_p8(q2v, p8)
        return posit.PositN8E1(p8)

    def to_float(self):
        value = unum.quire_to_value_8_1_14(self.__q8_1_14)
        display = unum.value_62_show(value)
        component = display.split(',')

        if len(component) == 1:
            return 0
        else:
            frac = component[-1][:24]  # float has 23bit fraction
            dec = 0.0
            scale = 1 << int(component[1])

            for i in range(0, 24):
                if frac[i] == '1':
                    dec += 2 ** (-i - 1)

            tmp = scale * (1 + dec)

            if component[0] == "(-":
                return -tmp
            else:
                return tmp

    def value_string(self):
        value = unum.quire_to_value_8_1_14(self.__q8_1_14)
        display = unum.value_62_show(value)
        component = display.split(',')

        if len(component) == 1:
            return "(zero, 0)"
        else:
            frac = str(component[-1][::-1])
            whereone = frac.find('1')

            if whereone == -1:
                norm = "1.0)"
            else:
                norm = "1." + component[-1][:63 - whereone] + ")"

            return component[0] + "," + component[1] + "," + norm

    def assign(self, arg):
        return self.__q8_1_14.assign(arg)

    def abs(self):
        res = QuireN8E1C14()
        res.__q8_1_14 = unum.quire_abs_8_1_14(self.__q8_1_14)
        return res

    def reset(self):
        self.__q8_1_14.reset()
        return self

    def set_sign(self, v):
        self.__q8_1_14.set_sign(v)
        return self

    def sign(self):
        return self.__q8_1_14.sign()

    def isneg(self):
        return self.__q8_1_14.isneg()

    def ispos(self):
        return self.__q8_1_14.ispos()

    def iszero(self):
        return self.__q8_1_14.iszero()

    def __add__(self, rhs):
        res = QuireN8E1C14()
        res.__q8_1_14 = unum.__add__(self.__q8_1_14, rhs.__q8_1_14)
        return res

    def __iadd__(self, rhs):
        if isinstance(rhs, QuireN8E1C14):
            self.__q8_1_14 += rhs.__q8_1_14
        else:
            self.__q8_1_14 += rhs._PositN8E1__p8_1

        return self

    def __isub__(self, rhs):
        if isinstance(rhs, QuireN8E1C14):
            self.__q8_1_14 -= rhs.__q8_1_14
        else:
            self.__q8_1_14 -= rhs._PositN8E1__p8_1

        return self

    def __eq__(self, rhs):
        if isinstance(rhs, QuireN8E1C14):
            value = rhs.__q8_1_14
        else:
            value = unum.posit_to_value_8_1(rhs._PositN8E1__p8_1)

        return unum.__eq__(self.__q8_1_14, value)

    def __lt__(self, rhs):
        if isinstance(rhs, QuireN8E1C14):
            value = rhs.__q8_1_14
        else:
            value = unum.posit_to_value_8_1(rhs._PositN8E1__p8_1)

        return unum.__lt__(self.__q8_1_14, value)

    def __gt__(self, rhs):
        if isinstance(rhs, QuireN8E1C14):
            value = rhs.__q8_1_14
        else:
            value = unum.posit_to_value_8_1(rhs._PositN8E1__p8_1)

        return unum.__gt__(self.__q8_1_14, value)

    def __ne__(self, rhs):
        return not self == rhs

    def __le__(self, rhs):
        return (self < rhs) | (self == rhs)

    def __ge__(self, rhs):
        return (self > rhs) | (self == rhs)
