from LeNet import lenet, dataloader
import time


def run(total=10000, posit_type="p8_1", use_logfile=False, log_file="", use_fma=False, use_quire=False):
    if posit_type != "p4_0" and posit_type != "p8_0" and \
       posit_type != "p8_1" and posit_type != "p8_2":
        print("Unresolved type! Using default type to calculate: Posit8_1.")
        posit_type = "p8_1"

    count = 0
    equal = 0
    root_path = "./LeNet/parameters/"
    wfile = "_weight.txt"
    bfile = "_bias.txt"

    (weight, bias) = lenet.read_param_from_txt(root_path+posit_type+wfile, root_path+posit_type+bfile, posit_type)
    (train_data, test_data) = dataloader.read_data("./LeNet/data")

    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for i, (images, labels) in enumerate(test_data):
        if count == min(total, 10000):
            break

        count += 1
        test_res = lenet.lenet_test_without_read_param(images[0][0], weight, bias, posit_type, use_fma, use_quire)

        if labels[0].item() == test_res:
            equal += 1

    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if use_logfile:
        f = open(log_file, "a")
        f.write("\n")
        f.write("start: " + start_time + "\t\t" + "end: " + end_time + "\n")
        f.write("Posit type is " + posit_type + "." + "\n")
        f.write("use_fma = " + str(use_fma) + "\t\t" + "use_quire = " + str(use_quire) + "\n")
        f.write("total = " + str(total) + "\t" + "equal = " + str(equal) + "\n")
        f.write("\n")
        f.close()
    else:
        print("\n")
        print("start: " + start_time + "\t\t" + "end: " + end_time)
        print("Posit type is " + posit_type + ".")
        print("use_fma = " + str(use_fma) + "\t\t" + "use_quire = " + str(use_quire))
        print("total = " + str(total) + "\t" + "equal = " + str(equal))
        print("\n")
