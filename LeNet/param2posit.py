import torch
import os
from Posit import posit


def param2posit(input_data, dsize, posit_type="p8_1", is_matrix=True):
    output_str = ""

    if posit_type == "p4_0":
        tmp = posit.PositN4E0()
    elif posit_type == "p8_0":
        tmp = posit.PositN8E0()
    elif posit_type == "p8_2":
        tmp = posit.PositN8E2()
    else:
        tmp = posit.PositN8E1()

    if is_matrix:
        for i in range(dsize):
            for j in range(dsize):
                tmp.assign(input_data[i][j].item())
                tmp_str = tmp.raw_hex_string()
                output_str += tmp_str
    else:
        for i in range(dsize):
            tmp.assign(input_data[i].item())
            tmp_str = tmp.raw_hex_string()
            output_str += tmp_str

    return output_str


def posit_weight_file(fileName="", weightFile="", biasFile="", posit_type="p8_1"):
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
                        param_str = param2posit(collection[param_tensor][oc][ic], size[2], posit_type)
                        wfile.write(param_str)
                        wfile.write('\n')
            else:
                last_ds = size[1] // last_oc
                last_oc = size[0]

                for oc in range(size[0]):
                    for ic in range(0, size[1], last_ds):
                        param_str = param2posit(collection[param_tensor][oc][ic:ic+last_ds], last_ds, posit_type, False)
                        wfile.write(param_str)
                        wfile.write('\n')
        else:
            param_str = param2posit(collection[param_tensor], size[0], posit_type, False)
            bfile.write(param_str)
            bfile.write('\n')

    bfile.close()
    wfile.close()

