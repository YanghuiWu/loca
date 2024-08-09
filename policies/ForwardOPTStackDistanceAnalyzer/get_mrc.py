import os
import sys

ITEM_PER_MB = 128  # every item is 8kb
MEM_UNIT = int(sys.argv[3]) * 16  # set 256MB as one memory unit

MAX_TRACE_LEN = 8000000

trace_name = sys.argv[1]
mrc = []


def get_mrc():
    global mrc
    opt_dis = []
    trace_path = f"{trace_name}"
    opt_dis_file = open(trace_path, "r")
    for line in opt_dis_file.readlines():
        dis = line.split()[2]
        if "INF" in dis:
            opt_dis += [MAX_TRACE_LEN]
        else:
            opt_dis += [int(dis)]
    opt_dis_file.close()

    for i in range(1, int(sys.argv[2])):
        mem = i * MEM_UNIT * ITEM_PER_MB
        miss = 0
        for dis in opt_dis:
            if dis > mem:
                miss += 1
        mrc += [float(miss) / float(len(opt_dis))]

    write_mrc()


def write_mrc():
    if not os.path.exists("mrcs"):
        os.makedirs("mrcs")
    mrc_file = open("mrcs/" + "opt_" + trace_name.split("/")[0] + "_" + trace_name.split("/")[1] + "_mrc", "w")
    mrc_file.write("memory miss_ratio\n")
    for i in range(0, len(mrc)):
        mrc_file.write(str((i + 1) * MEM_UNIT) + " " + str(mrc[i]) + "\n")
    mrc_file.close()


if __name__ == "__main__":
    get_mrc()

# Constants
ITEM_PER_MB = 128  # Each item is 8KB
MAX_TRACE_LEN = 8000000  # Maximum trace length

# Get arguments
trace_name = sys.argv[1]
max_mem_units = int(sys.argv[2])
mem_unit_size_mb = int(sys.argv[3]) * 16  # Set 256MB as one memory unit

# Initialize miss ratio curve list
mrc = []


def get_opt_dis(trace_name):
    """
    Reads the optimal distances from the trace file.
    """
    opt_dis = []
    trace_path = f"../../traces/{trace_name}/trace.tr_forward-OPT-dis.txt"
    trace_path = f"{trace_name}"

    with open(trace_path, 'r') as opt_dis_file:
        for line in opt_dis_file:
            dis = line.split()[2]
            opt_dis.append(MAX_TRACE_LEN if "INF" in dis else int(dis))

    return opt_dis


def calculate_mrc(opt_dis, max_mem_units, mem_unit_size_mb):
    """
    Calculates the miss ratio curve.
    """
    for i in range(1, max_mem_units + 1):
        mem_capacity = i * mem_unit_size_mb * ITEM_PER_MB
        miss_count = sum(1 for dis in opt_dis if dis > mem_capacity)
        mrc.append(float(miss_count) / len(opt_dis))


def write_mrc(trace_name, mrc, mem_unit_size_mb):
    """
    Writes the miss ratio curve to a file.
    """
    if not os.path.exists("mrcs"):
        os.makedirs("mrcs")

    trace_parts = trace_name.split("/")
    mrc_file_name = f"mrcs/opt_{trace_parts[0]}_{trace_parts[1]}_mrc"

    with open(mrc_file_name, 'w') as mrc_file:
        mrc_file.write("memory miss_ratio\n")
        for i, miss_ratio in enumerate(mrc):
            memory = (i + 1) * mem_unit_size_mb
            mrc_file.write(f"{memory} {miss_ratio}\n")


def main():
    opt_dis = get_opt_dis(trace_name)
    calculate_mrc(opt_dis, max_mem_units, mem_unit_size_mb)
    write_mrc(trace_name, mrc, mem_unit_size_mb)


# if __name__ == "__main__":
#     main()
