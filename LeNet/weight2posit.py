import torch
import os
import math
from Posit import posit


def param2posit(input_data, dsize, is_matrix=True):
    output_str = ""

    if is_matrix:
        for i in range(dsize):
            for j in range(dsize):
                p8 = posit.PositN8E1(input_data[i][j].item())
                p8_str = p8.raw_hex_string()
                output_str += p8_str
    else:
        for i in range(dsize):
            p8 = posit.PositN8E1(input_data[i].item())
            p8_str = p8.raw_hex_string()
            output_str += p8_str

    return output_str


def posit_weight_file(fileName="", weightFile="", biasFile=""):
    assert os.path.exists(fileName)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    collection = torch.load(fileName, map_location=device)

    wfile = open(weightFile, "w")
    bfile = open(biasFile, 'w')

    last_oc = 0
    last_ds = 0

    for param_tensor in collection:
        size = collection[param_tensor].size()

        if 'weight' in param_tensor:
            if 'conv' in param_tensor:
                last_oc = size[0]
                last_ds = size[2]

                for oc in range(size[0]):
                    for ic in range(size[1]):
                        param_str = param2posit(collection[param_tensor][oc][ic], size[2])
                        wfile.write(param_str)
                        wfile.write('\n')
            else:
                last_ds = size[1] // last_oc
                last_oc = size[0]

                for oc in range(size[0]):
                    for ic in range(0, size[1], last_ds):
                        param_str = param2posit(collection[param_tensor][oc][ic:ic+last_ds], last_ds, False)
                        wfile.write(param_str)
                        wfile.write('\n')
        else:
            param_str = param2posit(collection[param_tensor], size[0], False)
            bfile.write(param_str)
            bfile.write('\n')

    bfile.close()
    wfile.close()

