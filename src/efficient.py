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

def compute_alignment_cost_forward(x, y):
    """
    Computes alignment costs using space-efficient DP (forward direction)
    Returns array of costs for last row
    """
    m, n = len(x), len(y)
    
    # only keep two rows
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
    Returns array of costs for first row
    """
    m, n = len(x), len(y)
    
    # initialize for going backwards
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
    Hirschberg's divide-and-conquer algorithm 
    Returns aligned x and y strings
    """
    m, n = len(x), len(y)
    
    # base cases
    if m == 0:
        return '_' * n, y
    if n == 0:
        return x, '_' * m
    if m == 1:
        # for single character in x, find best alignment with y
        min_cost = float('inf')
        best_j = 0
        
        for j in range(n + 1):
            # cost = gaps before + match/mismatch + gaps after
            if j < n:
                cost = j * DELTA + ALPHA[(x[0], y[j])] + (n - j - 1) * DELTA
            else:
                cost = n * DELTA + DELTA  # x[0] as gap at end
            
            if cost < min_cost:
                min_cost = cost
                best_j = j
        
        if best_j < n:
            aligned_x = '_' * best_j + x[0] + '_' * (n - best_j - 1)
            aligned_y = y
        else:
            aligned_x = '_' * n + x[0]
            aligned_y = y + '_'
        
        return aligned_x, aligned_y
    
    if n == 1:
        # for single character in y, find best alignment with x 
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
            aligned_x = x
            aligned_y = '_' * best_i + y[0] + '_' * (m - best_i - 1)
        else:
            aligned_x = x + '_'
            aligned_y = '_' * m + y[0]
        
        return aligned_x, aligned_y
    
    # divide step - split x in the middle
    mid = m // 2
    
    # compute costs for left and right halves
    left_costs = compute_alignment_cost_forward(x[:mid], y)
    right_costs = compute_alignment_cost_backward(x[mid:], y)
    
    # find optimal split point in y
    min_cost = float('inf')
    split_j = 0
    for j in range(n + 1):
        cost = left_costs[j] + right_costs[j]
        if cost < min_cost:
            min_cost = cost
            split_j = j
    
    # conquer step - recursively align left and right parts
    align_x_left, align_y_left = hirschberg(x[:mid], y[:split_j])
    align_x_right, align_y_right = hirschberg(x[mid:], y[split_j:])
    
    return align_x_left + align_x_right, align_y_left + align_y_right

def compute_cost(aligned_x, aligned_y):
    """Computes the total cost of an alignment"""
    cost = 0
    for i in range(len(aligned_x)):
        if aligned_x[i] == '_' or aligned_y[i] == '_':
            cost += DELTA
        else:
            cost += ALPHA[(aligned_x[i], aligned_y[i])]
    return cost

def process_memory():
    """Get current memory usage"""
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed

def sequence_alignment_efficient(x, y):
    """Main efficient alignment function"""
    aligned_x, aligned_y = hirschberg(x, y)
    cost = compute_cost(aligned_x, aligned_y)
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
    cost, aligned_x, aligned_y = sequence_alignment_efficient(str1, str2)
    # calculate metrics
    final_memory = process_memory()
    end_time = time.time()
    total_time = (end_time - start_time) * 1000
    total_memory = final_memory - initial_memory_
    # write output
    write_output(output_file, cost, aligned_x, aligned_y, total_time, total_memory)

if __name__ == "__main__":
    main()
