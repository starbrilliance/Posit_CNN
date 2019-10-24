from MobileNet_V2 import param2posit

root_path = "./parameters/"
ifile = "mobilenet_v2-b0353104.pth"
posit_type = ["p4_0", "p8_0", "p8_1", "p8_2"]
wfile = "_weight.txt"
bfile = "_bias.txt"

for i in range(len(posit_type)):
    param2posit.posit_param_file(root_path + ifile, root_path + posit_type[i] + wfile,
                                 root_path + posit_type[i] + bfile,
                                 posit_type[i])
