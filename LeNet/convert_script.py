from LeNet import weight2posit

ifile = r"./mnist_cnn.pt"
wfile = "p8_1_weight.txt"
bfile = "p8_1_bias.txt"
weight2posit.posit_weight_file(ifile, wfile, bfile)