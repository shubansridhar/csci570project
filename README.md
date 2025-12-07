# CSCI 570 Final Project — Sequence Alignment

This repository contains two implementations of the Sequence Alignment problem:

1. **Basic Dynamic Programming Algorithm**  
2. **Efficient Memory-Optimized Algorithm (Hirschberg’s Divide & Conquer)**

Both implementations follow the official specification for CSCI 570 (Fall 2025).

---

## Project Structure

- `basic.py` — O(mn) DP with full memory table  
- `efficient.py` — Hirschberg divide-and-conquer version  
- `basic.sh` — Shell script for running basic implementation  
- `efficient.sh` — Shell script for running efficient implementation  
- `README.md` — Documentation (this file)

---

## Problem Description

Given two DNA sequences over the alphabet {A, C, G, T}, the goal is to compute an optimal alignment that minimizes the alignment cost.

### **Cost Model**

- Gap penalty δ = 30  
- Mismatch cost table:

|     | A  | C  | G  | T  |
|-----|----|----|----|----|
| A   | 0  |110 | 48 | 94 |
| C   |110 | 0  |118 | 48 |
| G   |48  |118 | 0  |110 |
| T   |94  |48  |110 | 0  |

Total cost = mismatch costs + gap penalties.

---

## Input Format

Each input file contains:

1. Base string `s0`  
2. A list of indices to generate `s1, s2, …, sj`  
3. Base string `t0`  
4. A list of indices to generate `t1, t2, …, tk`

### **String Expansion Rule**

For each index `n`:

`s_new = s[:n+1] + s + s[n+1:]`

Both `s` and `t` are expanded using this rule.

The programs automatically parse the input and generate the final sequences.

---

## Output Format

Each implementation writes **exactly five lines**:

1. Total alignment cost  
2. Aligned string 1  
3. Aligned string 2  
4. Runtime in milliseconds  
5. Memory usage in KB  

The output format must match exactly for grading.

---

## Algorithms

### 1.Basic Algorithm — Full Dynamic Programming

- Builds a full `(m+1) × (n+1)` DP table  
- Applies the classic alignment recurrence  
- Backtracks to reconstruct the final alignment  
- **Time complexity:** O(mn)  
- **Space complexity:** O(mn)

---

### 2.Efficient Algorithm — Hirschberg Divide & Conquer

- Splits the first string into two halves  
- Computes forward DP (1-row) and backward DP (1-row)  
- Finds optimal split point in the second string  
- Recursively aligns each half  
- **Time complexity:** O(mn)  
- **Space complexity:** O(m+n)  

This version dramatically reduces memory usage.

---

## How to Run

### **Basic Version**

`./basic.sh input.txt output_basic.txt`  
or  
`python3 basic.py input.txt output_basic.txt`

### **Efficient Version**

`./efficient.sh input.txt output_efficient.txt`  
or  
`python3 efficient.py input.txt output_efficient.txt`

Make scripts executable if needed:

`chmod +x basic.sh efficient.sh`

---

## Dependencies

- Python 3.x  
- `psutil` (for memory measurement)

Install:

`pip install psutil`  
or  
`conda install psutil`

---

## Experiments

Steps for performance evaluation:

1. Prepare input files with increasing sequence lengths  
2. Run both programs  
3. Record:
   - `m + n`  
   - Runtime (milliseconds)  
   - Memory usage (KB)  
4. Plot:
   - Memory vs problem size  
   - Runtime vs problem size  

Include plots in your Summary report.

---

## Validating Correctness

- Compare total alignment cost from both programs  
- Ensure aligned strings have equal length  
- Test small and random DNA cases  
- The efficient version must produce the same optimal cost as basic version

---

## Example Workflow

1. Run both implementations on the same input  
2. Compare outputs  
3. Use time & memory values to create tables  
4. Plot results  
5. Insert findings into Summary  

---

## Notes

- Output must be exactly 5 lines  
- No debug prints allowed  
- Memory usage may vary across machines  
- Efficient version uses far less memory  
- Basic version may run faster on small inputs  

---

## End of README

This README provides all instructions needed to run, test, and evaluate the Sequence Alignment project for CSCI 570.
