import argparse
from tabulate import tabulate

def next(bitstrings, constraints=[]):
    new_bitstrings = []
    for b in bitstrings:
        illegal0=False
        illegal1=False
        for c in constraints:
            cut = b[(-len(c)+1):]
            if cut+"0" == c:
                illegal0=True
            if cut+"1" == c:
                illegal1=True
        if not illegal0: new_bitstrings.append(b+"0")
        if not illegal1: new_bitstrings.append(b+"1")
    return new_bitstrings
        
def get_x(n, constraints=[]):
    bs = [""]
    for i in range(n):
        bs = next(bs, constraints=constraints)
    return bs  
   
def main(): 
    parser = argparse.ArgumentParser(description="A CLI app to count how many bitstrings of each length can be made with one or more constraints (e.g., no '000')")
    parser.add_argument("constraints", type=str, default="000,11 000", help="Constraints, comma-separated. Separate multiple constraints with commas. Separate multiple combinations of constraints with spaces.")
    parser.add_argument("max_length", type=int, default=20, help="Length of bitstring to go up to. WARNING: Going above ~20 will result in long computation time and possible crashes!")
    args = parser.parse_args()
    reps = args.max_length
    combos = args.constraints.split(" ")
    combos_bs = {}

    combos_bs["x"] = []
    for j in range(reps):
        combos_bs["x"].append(range(j+1))

    for c in combos:
        combos_bs[c] = []
        for j in range(reps):
            combos_bs[c].append(get_x(j+1, constraints=c.split(',')))

    table_bs = []
    for i in range(len(combos_bs[combos[0]])):
        table_bs.append([len(combos_bs[c][i]) for c in combos_bs])
    print(tabulate(table_bs, headers=combos))

if __name__ == "__main__":
    main()