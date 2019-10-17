from Posit import posit, unum


class QuireN4E0C6(object):
    def __init__(self, arg=0):
        self.__q4_0_6 = unum.Quire_4_0_6_t(arg)

    def set_from_bits(self, bits, radix=2):
        bin_bits = bin(int(bits, radix))[2:]
        pad_bits = "{:0>16}".format(bin_bits)

        if pad_bits[0] == '0':
            sign = "+:"
        else:
            sign = "-:"

        res = sign + pad_bits[1:7] + "_" + pad_bits[7:12] \
              + "." + pad_bits[12:]

        self.__q4_0_6.load_bits(res)
        return self

    def to_posit4_0(self):
        p4 = unum.Posit_4_0_t()
        q2v = unum.quire_to_value_4_0_6(self.__q4_0_6)
        unum.convert_q40_to_p40(q2v, p4)
        return posit.PositN4E0(p4)

    def to_float(self):
        value = unum.quire_to_value_4_0_6(self.__q4_0_6)
        display = unum.value_14_show(value)
        component = display.split(',')

        if len(component) == 1:
            return 0
        else:
            frac = component[-1]  # float has 23bit fraction
            dec = 0.0
            scale = 1 << int(component[1])

            for i in range(0, 14):
                if frac[i] == '1':
                    dec += 2 ** (-i - 1)

            tmp = scale * (1 + dec)

            if component[0] == "(-":
                return -tmp
            else:
                return tmp

    def value_string(self):
        value = unum.quire_to_value_4_0_6(self.__q4_0_6)
        display = unum.value_14_show(value)
        component = display.split(',')

        if len(component) == 1:
            return "(zero, 0)"
        else:
            frac = str(component[-1][::-1])
            whereone = frac.find('1')

            if whereone == -1:
                norm = "1.0)"
            else:
                norm = "1." + component[-1][:15 - whereone] + ")"

            return component[0] + "," + component[1] + "," + norm

    def assign(self, arg):
        return self.__q4_0_6.assign(arg)

    def abs(self):
        res = QuireN4E0C6()
        res.__q4_0_6 = unum.quire_abs_4_0_6(self.__q4_0_6)
        return res

    def reset(self):
        self.__q4_0_6.reset()
        return self

    def set_sign(self, v):
        self.__q4_0_6.set_sign(v)
        return self

    def sign(self):
        return self.__q4_0_6.sign()

    def isneg(self):
        return self.__q4_0_6.isneg()

    def ispos(self):
        return self.__q4_0_6.ispos()

    def iszero(self):
        return self.__q4_0_6.iszero()

    def __add__(self, rhs):
        res = QuireN4E0C6()
        res.__q4_0_6 = unum.__add__(self.__q4_0_6, rhs.__q4_0_6)
        return res

    def __iadd__(self, rhs):
        if isinstance(rhs, QuireN4E0C6):
            self.__q4_0_6 += rhs.__q4_0_6
        else:
            self.__q4_0_6 += rhs._PositN4E0__p4_0

        return self

    def __isub__(self, rhs):
        if isinstance(rhs, QuireN4E0C6):
            self.__q4_0_6 -= rhs.__q4_0_6
        else:
            self.__q4_0_6 -= rhs._PositN4E0__p4_0

        return self

    def __eq__(self, rhs):
        if isinstance(rhs, QuireN4E0C6):
            value = rhs.__q4_0_6
        else:
            value = unum.posit_to_value_4_0(rhs._PositN4E0__p4_0)

        return unum.__eq__(self.__q4_0_6, value)

    def __lt__(self, rhs):
        if isinstance(rhs, QuireN4E0C6):
            value = rhs.__q4_0_6
        else:
            value = unum.posit_to_value_4_0(rhs._PositN4E0__p4_0)

        return unum.__lt__(self.__q4_0_6, value)

    def __gt__(self, rhs):
        if isinstance(rhs, QuireN4E0C6):
            value = rhs.__q4_0_6
        else:
            value = unum.posit_to_value_4_0(rhs._PositN4E0__p4_0)

        return unum.__gt__(self.__q4_0_6, value)

    def __ne__(self, rhs):
        return not self == rhs

    def __le__(self, rhs):
        return (self < rhs) | (self == rhs)

    def __ge__(self, rhs):
        return (self > rhs) | (self == rhs)


class QuireN8E0C6(object):
    def __init__(self, arg=0):
        self.__q8_0_6 = unum.Quire_8_0_6_t(arg)

    def set_from_bits(self, bits, radix=2):
        bin_bits = bin(int(bits, radix))[2:]
        pad_bits = "{:0>32}".format(bin_bits)

        if pad_bits[0] == '0':
            sign = "+:"
        else:
            sign = "-:"

        res = sign + pad_bits[1:7] + "_" + pad_bits[7:20] \
              + "." + pad_bits[20:]

        self.__q8_0_6.load_bits(res)
        return self

    def to_posit8_0(self):
        p8 = unum.Posit_8_0_t()
        q2v = unum.quire_to_value_8_0_6(self.__q8_0_6)
        unum.convert_q80_to_p80(q2v, p8)
        return posit.PositN8E0(p8)

    def to_float(self):
        value = unum.quire_to_value_8_0_6(self.__q8_0_6)
        display = unum.value_30_show(value)
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
        value = unum.quire_to_value_8_0_6(self.__q8_0_6)
        display = unum.value_30_show(value)
        component = display.split(',')

        if len(component) == 1:
            return "(zero, 0)"
        else:
            frac = str(component[-1][::-1])
            whereone = frac.find('1')

            if whereone == -1:
                norm = "1.0)"
            else:
                norm = "1." + component[-1][:31 - whereone] + ")"

            return component[0] + "," + component[1] + "," + norm

    def assign(self, arg):
        return self.__q8_0_6.assign(arg)

    def abs(self):
        res = QuireN8E0C6()
        res.__q8_0_6 = unum.quire_abs_8_0_6(self.__q8_0_6)
        return res

    def reset(self):
        self.__q8_0_6.reset()
        return self

    def set_sign(self, v):
        self.__q8_0_6.set_sign(v)
        return self

    def sign(self):
        return self.__q8_0_6.sign()

    def isneg(self):
        return self.__q8_0_6.isneg()

    def ispos(self):
        return self.__q8_0_6.ispos()

    def iszero(self):
        return self.__q8_0_6.iszero()

    def __add__(self, rhs):
        res = QuireN8E0C6()
        res.__q8_0_6 = unum.__add__(self.__q8_0_6, rhs.__q8_0_6)
        return res

    def __iadd__(self, rhs):
        if isinstance(rhs, QuireN8E0C6):
            self.__q8_0_6 += rhs.__q8_0_6
        else:
            self.__q8_0_6 += rhs._PositN8E0__p8_0

        return self

    def __isub__(self, rhs):
        if isinstance(rhs, QuireN8E0C6):
            self.__q8_0_6 -= rhs.__q8_0_6
        else:
            self.__q8_0_6 -= rhs._PositN8E0__p8_0

        return self

    def __eq__(self, rhs):
        if isinstance(rhs, QuireN8E0C6):
            value = rhs.__q8_0_6
        else:
            value = unum.posit_to_value_8_0(rhs._PositN8E0__p8_0)

        return unum.__eq__(self.__q8_0_6, value)

    def __lt__(self, rhs):
        if isinstance(rhs, QuireN8E0C6):
            value = rhs.__q8_0_6
        else:
            value = unum.posit_to_value_8_0(rhs._PositN8E0__p8_0)

        return unum.__lt__(self.__q8_0_6, value)

    def __gt__(self, rhs):
        if isinstance(rhs, QuireN8E0C6):
            value = rhs.__q8_0_6
        else:
            value = unum.posit_to_value_8_0(rhs._PositN8E0__p8_0)

        return unum.__gt__(self.__q8_0_6, value)

    def __ne__(self, rhs):
        return not self == rhs

    def __le__(self, rhs):
        return (self < rhs) | (self == rhs)

    def __ge__(self, rhs):
        return (self > rhs) | (self == rhs)


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
        unum.convert_q81_to_p81(q2v, p8)
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


class QuireN8E2C30(object):
    def __init__(self, arg=0):
        self.__q8_2_30 = unum.Quire_8_2_30_t(arg)

    def set_from_bits(self, bits, radix=2):
        bin_bits = bin(int(bits, radix))[2:]
        pad_bits = "{:0>128}".format(bin_bits)

        if pad_bits[0] == '0':
            sign = "+:"
        else:
            sign = "-:"

        res = sign + pad_bits[1:31] + "_" + pad_bits[31:80] \
              + "." + pad_bits[80:]

        self.__q8_2_30.load_bits(res)
        return self

    def to_posit8_2(self):
        p8 = unum.Posit_8_2_t()
        q2v = unum.quire_to_value_8_2_30(self.__q8_2_30)
        unum.convert_q82_to_p82(q2v, p8)
        return posit.PositN8E2(p8)

    def to_float(self):
        value = unum.quire_to_value_8_2_30(self.__q8_2_30)
        display = unum.value_126_show(value)
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
        value = unum.quire_to_value_8_2_30(self.__q8_2_30)
        display = unum.value_126_show(value)
        component = display.split(',')

        if len(component) == 1:
            return "(zero, 0)"
        else:
            frac = str(component[-1][::-1])
            whereone = frac.find('1')

            if whereone == -1:
                norm = "1.0)"
            else:
                norm = "1." + component[-1][:127 - whereone] + ")"

            return component[0] + "," + component[1] + "," + norm

    def assign(self, arg):
        return self.__q8_2_30.assign(arg)

    def abs(self):
        res = QuireN8E2C30()
        res.__q8_2_30 = unum.quire_abs_8_2_30(self.__q8_2_30)
        return res

    def reset(self):
        self.__q8_2_30.reset()
        return self

    def set_sign(self, v):
        self.__q8_2_30.set_sign(v)
        return self

    def sign(self):
        return self.__q8_2_30.sign()

    def isneg(self):
        return self.__q8_2_30.isneg()

    def ispos(self):
        return self.__q8_2_30.ispos()

    def iszero(self):
        return self.__q8_2_30.iszero()

    def __add__(self, rhs):
        res = QuireN8E2C30()
        res.__q8_2_30 = unum.__add__(self.__q8_2_30, rhs.__q8_2_30)
        return res

    def __iadd__(self, rhs):
        if isinstance(rhs, QuireN8E2C30):
            self.__q8_2_30 += rhs.__q8_2_30
        else:
            self.__q8_2_30 += rhs._PositN8E2__p8_2

        return self

    def __isub__(self, rhs):
        if isinstance(rhs, QuireN8E2C30):
            self.__q8_2_30 -= rhs.__q8_2_30
        else:
            self.__q8_2_30 -= rhs._PositN8E2__p8_2

        return self

    def __eq__(self, rhs):
        if isinstance(rhs, QuireN8E2C30):
            value = rhs.__q8_2_30
        else:
            value = unum.posit_to_value_8_2(rhs._PositN8E2__p8_2)

        return unum.__eq__(self.__q8_2_30, value)

    def __lt__(self, rhs):
        if isinstance(rhs, QuireN8E2C30):
            value = rhs.__q8_2_30
        else:
            value = unum.posit_to_value_8_2(rhs._PositN8E2__p8_2)

        return unum.__lt__(self.__q8_2_30, value)

    def __gt__(self, rhs):
        if isinstance(rhs, QuireN8E2C30):
            value = rhs.__q8_2_30
        else:
            value = unum.posit_to_value_8_2(rhs._PositN8E2__p8_2)

        return unum.__gt__(self.__q8_2_30, value)

    def __ne__(self, rhs):
        return not self == rhs

    def __le__(self, rhs):
        return (self < rhs) | (self == rhs)

    def __ge__(self, rhs):
        return (self > rhs) | (self == rhs)
