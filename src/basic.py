import sys
import time
import psutil

# Constants
DELTA = 30
ALPHA = {
    ('A', 'A'): 0, ('A', 'C'): 110, ('A', 'G'): 48, ('A', 'T'): 94,
    ('C', 'A'): 110, ('C', 'C'): 0, ('C', 'G'): 118, ('C', 'T'): 48,
    ('G', 'A'): 48, ('G', 'C'): 118, ('G', 'G'): 0, ('G', 'T'): 110,
    ('T', 'A'): 94, ('T', 'C'): 48, ('T', 'G'): 110, ('T', 'T'): 0
}

def generate_string(base_str, indices):
    """Generate string by iteratively inserting at specified indices"""
    s = base_str
    for idx in indices:
        s = s[:idx+1] + s + s[idx+1:]
    return s

def read_input(file_path):
    """Parse input file and generate the two strings"""
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    # Parse first string
    idx = 0
    base_str1 = lines[idx]
    idx += 1
    
    indices1 = []
    while idx < len(lines) and lines[idx].isdigit():
        indices1.append(int(lines[idx]))
        idx += 1
    
    # Parse second string
    base_str2 = lines[idx]
    idx += 1
    
    indices2 = []
    while idx < len(lines) and lines[idx].isdigit():
        indices2.append(int(lines[idx]))
        idx += 1
    
    # Generate strings
    str1 = generate_string(base_str1, indices1)
    str2 = generate_string(base_str2, indices2)
    
    return str1, str2

def compute_dp_table(x, y):
    """
    Compute full DP table for sequence alignment
    Returns: DP table and cost
    """
    m, n = len(x), len(y)
    
    # Initialize DP table (m+1) x (n+1) 
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i * DELTA
    for j in range(n + 1):
        dp[0][j] = j * DELTA
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match_cost = dp[i-1][j-1] + ALPHA[(x[i-1], y[j-1])]
            gap_x = dp[i-1][j] + DELTA
            gap_y = dp[i][j-1] + DELTA
            dp[i][j] = min(match_cost, gap_x, gap_y)
    
    return dp, dp[m][n]

def traceback(dp, x, y):
    """
    Reconstruct alignment by tracing back through DP table
    Returns: aligned x, aligned y
    """
    m, n = len(x), len(y)
    align_x = []
    align_y = []
    
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            # Check which direction we came from
            match_cost = dp[i-1][j-1] + ALPHA[(x[i-1], y[j-1])]
            gap_x = dp[i-1][j] + DELTA
            gap_y = dp[i][j-1] + DELTA
            
            if dp[i][j] == match_cost:
                align_x.append(x[i-1])
                align_y.append(y[j-1])
                i -= 1
                j -= 1
            elif dp[i][j] == gap_x:
                align_x.append(x[i-1])
                align_y.append('_')
                i -= 1
            else:
                align_x.append('_')
                align_y.append(y[j-1])
                j -= 1
        elif i > 0:
            align_x.append(x[i-1])
            align_y.append('_')
            i -= 1
        else:
            align_x.append('_')
            align_y.append(y[j-1])
            j -= 1
    
    # Reverse since we built backwards
    return ''.join(reversed(align_x)), ''.join(reversed(align_y))

def process_memory():
    """Get current memory usage in KB"""
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed

def sequence_alignment(x, y):
    """Main alignment function"""
    dp, cost = compute_dp_table(x, y)
    align_x, align_y = traceback(dp, x, y)
    return cost, align_x, align_y

def write_output(output_path, cost, align_x, align_y, time_ms, memory_kb):
    """Write results to output file"""
    with open(output_path, 'w') as f:
        f.write(f"{cost}\n")
        f.write(f"{align_x}\n")
        f.write(f"{align_y}\n")
        f.write(f"{time_ms}\n")
        f.write(f"{memory_kb}\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python basic.py <input_file> <output_file>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Read and generate strings
    str1, str2 = read_input(input_path)
    
    # Measure performance
    start_time = time.time()
    memory_before = process_memory()
    
    # Run alignment
    cost, align_x, align_y = sequence_alignment(str1, str2)
    
    memory_after = process_memory()
    end_time = time.time()
    
    # Calculate metrics
    time_ms = (end_time - start_time) * 1000
    memory_kb = memory_after - memory_before
    
    # Write output
    write_output(output_path, cost, align_x, align_y, time_ms, memory_kb)

if __name__ == "__main__":
    main()
