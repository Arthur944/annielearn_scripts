import sys

file = open(sys.argv[1], "r").readlines()
cur_index = 1
cur_file = open(sys.argv[1] + "_{}".format(cur_index), "w+")
to_write = ""
for i in range(len(file)):
    if i > (len(file)/int(sys.argv[2])) * cur_index:
        cur_file.write(to_write.strip())
        to_write = ""
        cur_index += 1
        cur_file.close()
        cur_file = open(sys.argv[1] + "_{}".format(cur_index), "w+")
    to_write += file[i].strip() + "\n"
cur_file.write(to_write.strip())