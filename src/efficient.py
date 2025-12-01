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

def compute_alignment_cost_forward(x, y):
    """
    Compute alignment costs using space-efficient DP (forward direction)
    Returns: array of costs for last row
    """
    m, n = len(x), len(y)
    
    # Only keep two rows
    prev = [j * DELTA for j in range(n + 1)]
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr[0] = i * DELTA
        for j in range(1, n + 1):
            match_cost = prev[j-1] + ALPHA[(x[i-1], y[j-1])]
            gap_x = prev[j] + DELTA
            gap_y = curr[j-1] + DELTA
            curr[j] = min(match_cost, gap_x, gap_y)
        prev, curr = curr, prev
    
    return prev

def compute_alignment_cost_backward(x, y):
    """
    Compute alignment costs using space-efficient DP (backward direction)
    Returns: array of costs for first row (when going backwards from end)
    """
    m, n = len(x), len(y)
    
    # Initialize for going backwards
    prev = [(n - j) * DELTA for j in range(n + 1)]
    curr = [0] * (n + 1)
    
    for i in range(m - 1, -1, -1):
        curr[n] = (m - i) * DELTA
        for j in range(n - 1, -1, -1):
            match_cost = prev[j+1] + ALPHA[(x[i], y[j])]
            gap_x = prev[j] + DELTA
            gap_y = curr[j+1] + DELTA
            curr[j] = min(match_cost, gap_x, gap_y)
        prev, curr = curr, prev
    
    return prev

def hirschberg(x, y):
    """
    Hirschberg's divide-and-conquer algorithm for memory-efficient alignment
    Returns: aligned x, aligned y
    """
    m, n = len(x), len(y)
    
    # Base cases
    if m == 0:
        return '_' * n, y
    if n == 0:
        return x, '_' * m
    if m == 1:
        # For single character in x, find best alignment with y
        # Option 1: align x[0] with some y[j]
        min_cost = float('inf')
        best_j = 0
        
        for j in range(n + 1):
            # Cost: gaps before + match/mismatch + gaps after
            if j < n:
                cost = j * DELTA + ALPHA[(x[0], y[j])] + (n - j - 1) * DELTA
            else:
                cost = n * DELTA + DELTA  # x[0] as gap at end
            
            if cost < min_cost:
                min_cost = cost
                best_j = j
        
        if best_j < n:
            align_x = '_' * best_j + x[0] + '_' * (n - best_j - 1)
            align_y = y
        else:
            align_x = '_' * n + x[0]
            align_y = y + '_'
        
        return align_x, align_y
    
    if n == 1:
        # For single character in y, find best alignment with x
        min_cost = float('inf')
        best_i = 0
        
        for i in range(m + 1):
            if i < m:
                cost = i * DELTA + ALPHA[(x[i], y[0])] + (m - i - 1) * DELTA
            else:
                cost = m * DELTA + DELTA
            
            if cost < min_cost:
                min_cost = cost
                best_i = i
        
        if best_i < m:
            align_x = x
            align_y = '_' * best_i + y[0] + '_' * (m - best_i - 1)
        else:
            align_x = x + '_'
            align_y = '_' * m + y[0]
        
        return align_x, align_y
    
    # Divide: split x in the middle
    mid = m // 2
    
    # Compute costs for left and right halves
    left_costs = compute_alignment_cost_forward(x[:mid], y)
    right_costs = compute_alignment_cost_backward(x[mid:], y)
    
    # Find optimal split point in y
    min_cost = float('inf')
    split_j = 0
    for j in range(n + 1):
        cost = left_costs[j] + right_costs[j]
        if cost < min_cost:
            min_cost = cost
            split_j = j
    
    # Conquer: recursively align left and right parts
    align_x_left, align_y_left = hirschberg(x[:mid], y[:split_j])
    align_x_right, align_y_right = hirschberg(x[mid:], y[split_j:])
    
    return align_x_left + align_x_right, align_y_left + align_y_right

def compute_cost(align_x, align_y):
    """Compute the total cost of an alignment"""
    cost = 0
    for i in range(len(align_x)):
        if align_x[i] == '_' or align_y[i] == '_':
            cost += DELTA
        else:
            cost += ALPHA[(align_x[i], align_y[i])]
    return cost

def process_memory():
    """Get current memory usage in KB"""
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed

def sequence_alignment_efficient(x, y):
    """Main efficient alignment function"""
    align_x, align_y = hirschberg(x, y)
    cost = compute_cost(align_x, align_y)
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
        print("Usage: python efficient.py <input_file> <output_file>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Read and generate strings
    str1, str2 = read_input(input_path)
    
    # Measure performance
    start_time = time.time()
    memory_before = process_memory()
    
    # Run alignment
    cost, align_x, align_y = sequence_alignment_efficient(str1, str2)
    
    memory_after = process_memory()
    end_time = time.time()
    
    # Calculate metrics
    time_ms = (end_time - start_time) * 1000
    memory_kb = memory_after - memory_before
    
    # Write output
    write_output(output_path, cost, align_x, align_y, time_ms, memory_kb)

if __name__ == "__main__":
    main()
