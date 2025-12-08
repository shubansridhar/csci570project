import os
import glob
import matplotlib.pyplot as plt
from src.basic import read_input

basic_dir = "outputs_basic"
eff_dir = "outputs_efficient"
input_dir = "inputs"

input_files = sorted(glob.glob(f"{input_dir}/*.txt"))

problem_sizes = []
basic_times = []
basic_mems = []
eff_times = []
eff_mems =[]

for input_path in input_files:

    s,t = read_input(input_path)
    size = len(s) + len(t)
    problem_sizes.append(size)

    base = os.path.splitext(os.path.basename(input_path))[0]

    basic_out = f"{basic_dir}/{base}_basic.out"
    eff_out = f"{eff_dir}/{base}_efficient.out"

    with open(basic_out) as f:
        lines = f.read().strip().splitlines()
        basic_times.append(float(lines[3]))
        basic_mems.append(float(lines[4]))

    with open(eff_out) as f:
        lines = f.read().strip().splitlines()
        eff_times.append(float(lines[3]))
        eff_mems.append(float(lines[4]))

data = sorted(zip(problem_sizes, basic_mems, eff_mems))
sizes_sorted, basic_mems_sorted, eff_mems_sorted = zip(*data)

plt.figure()  # start a fresh figure

plt.plot(
    sizes_sorted,
    basic_mems_sorted,
    marker="o",
    linestyle="-",
    label="Basic"
)
plt.plot(
    sizes_sorted,
    eff_mems_sorted,
    marker="o",
    linestyle="-",
    label="Efficient"
)

plt.xlabel("Problem Size (m+n)")
plt.ylabel("Memory Usage (KB)")
plt.title("Memory Usage for Different Algorithms")
plt.legend()
plt.grid(True) 
plt.tight_layout()
plt.savefig("memory_vs_size.png", dpi=300)
plt.close()

data_t = sorted(zip(problem_sizes, basic_times, eff_times))
sizes_t, basic_times_sorted, eff_times_sorted = zip(*data_t)

plt.figure()

plt.plot(
    sizes_t,
    basic_times_sorted,
    marker="o",
    linestyle="-",
    label="Basic"
)
plt.plot(
    sizes_t,
    eff_times_sorted,
    marker="o",
    linestyle="-",
    label="Efficient"
)

plt.xlabel("Problem Size (m+n)")
plt.ylabel("Execution Time (ms)")
plt.title("Time for Different Algorithms")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("time_vs_size.png", dpi=300)
plt.close()