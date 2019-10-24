from Matrix import func


def ConvBNReLU(input_data, kernel, bias, dsize, ksize, stride=1, ichannel=1, ochannel=1, posit_type="p8_1",
               use_fma=False, use_quire=False, one_group=True):