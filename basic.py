import sys

def generate_string(str, indices):
    s = str
    for i in indices:
        s = s[:i+1] + s + s[i+1:]
    return s
    

def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    """
    1. Read i/p and generate s and t
    2. start timer
    3. find similarity
    4. stop timer
    5. output to file
    """

if __name__ == "__main__":
    main()