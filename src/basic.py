import sys
import time
import psutil

# gap penalty 
DELTA = 30
# mismatch costs
ALPHA = {
    ('A', 'A'): 0, ('A', 'C'): 110, ('A', 'G'): 48, ('A', 'T'): 94,
    ('C', 'A'): 110, ('C', 'C'): 0, ('C', 'G'): 118, ('C', 'T'): 48,
    ('G', 'A'): 48, ('G', 'C'): 118, ('G', 'G'): 0, ('G', 'T'): 110,
    ('T', 'A'): 94, ('T', 'C'): 48, ('T', 'G'): 110, ('T', 'T'): 0
}

def generate_string(base_str, indices):
    """Generate string by iteratively inserting at specified indices"""
    s = base_str
    for index in indices:
        s = s[:index+1] + s + s[index+1:]
    return s

def read_input(file_path):
    """Parse input file and generate the two strings"""
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    # parse first string
    index = 0
    base_str1 = lines[index]
    index += 1
    
    indices1 = []
    while index < len(lines) and lines[index].isdigit():
        indices1.append(int(lines[index]))
        index += 1
    
    # parse second string
    base_str2 = lines[index]
    index += 1
    
    indices2 = []
    while index < len(lines) and lines[index].isdigit():
        indices2.append(int(lines[index]))
        index += 1
    
    # generate strings
    str1 = generate_string(base_str1, indices1)
    str2 = generate_string(base_str2, indices2)
    
    return str1, str2

def compute_dp_table(x, y):
    """
    Computes full DP table for sequence alignment
    Returns final table and cost
    """
    m, n = len(x), len(y)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    # base cases
    for i in range(m + 1):
        dp[i][0] = i * DELTA
    for j in range(n + 1):
        dp[0][j] = j * DELTA
    # fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match_cost = dp[i-1][j-1] + ALPHA[(x[i-1], y[j-1])]
            gap_x = dp[i-1][j] + DELTA
            gap_y = dp[i][j-1] + DELTA
            dp[i][j] = min(match_cost, gap_x, gap_y)
    
    return dp, dp[m][n]

def traceback(dp, x, y):
    """
    Reconstructs alignment by tracing back through DP table
    Returns aligned x and y strings
    """
    m, n = len(x), len(y)
    aligned_x = []
    aligned_y = []
    
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            # chck which direction we came from
            match_cost = dp[i-1][j-1] + ALPHA[(x[i-1], y[j-1])]
            gap_x = dp[i-1][j] + DELTA
            gap_y = dp[i][j-1] + DELTA
            
            if dp[i][j] == match_cost:
                aligned_x.append(x[i-1])
                aligned_y.append(y[j-1])
                i -= 1
                j -= 1
            elif dp[i][j] == gap_x:
                aligned_x.append(x[i-1])
                aligned_y.append('_')
                i -= 1
            else:
                aligned_x.append('_')
                aligned_y.append(y[j-1])
                j -= 1
        elif i > 0:
            aligned_x.append(x[i-1])
            aligned_y.append('_')
            i -= 1
        else:
            aligned_x.append('_')
            aligned_y.append(y[j-1])
            j -= 1
    
    # reverse since we built backwards
    return ''.join(reversed(aligned_x)), ''.join(reversed(aligned_y))

def process_memory():
    """Get current memory usage"""
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed

def sequence_alignment(x, y):
    """Main alignment function"""
    dp, cost = compute_dp_table(x, y)
    aligned_x, aligned_y = traceback(dp, x, y)
    return cost, aligned_x, aligned_y

def write_output(output_file, cost, aligned_x, aligned_y, total_time, total_memory):
    """Write results to output file"""
    with open(output_file, 'w') as f:
        f.write(f"{cost}\n")
        f.write(f"{aligned_x}\n")
        f.write(f"{aligned_y}\n")
        f.write(f"{total_time}\n")
        f.write(f"{total_memory}\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python basic.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    # eead and generate strings
    str1, str2 = read_input(input_file)
    # measure performance
    start_time = time.time()
    initial_memory_= process_memory()
    # run alignment function
    cost, aligned_x, aligned_y = sequence_alignment(str1, str2)
    # calculate metrics
    final_memory = process_memory()
    end_time = time.time()
    total_time = (end_time - start_time) * 1000
    total_memory = final_memory - initial_memory_
    # write output
    write_output(output_file, cost, aligned_x, aligned_y, total_time, total_memory)

if __name__ == "__main__":
    main()
