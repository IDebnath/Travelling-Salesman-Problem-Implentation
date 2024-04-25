import time
from itertools import combinations as it_combinations

def tsp(cost):
    n = len(cost)
    dp = {}
    parent = {}

    # Initialize starting point
    for i in range(n):
        dp[(1 << i, i)] = (0 if i == 0 else float('inf'))
    
    # Consider subsets of increasing sizes starting from 2
    for size in range(2, n+1):
        for S in it_combinations(range(n), size):
            if 0 not in S:
                continue  # Ensure the start city '0' is always included in the subset

            S_bitmask = 0
            for x in S:
                S_bitmask |= (1 << x)
            
            for i in S:
                if i == 0:
                    continue  # There's no need to try ending at the start city in subsets

                # Set the minimum to infinity before attempting to find a lesser value
                dp[(S_bitmask, i)] = float('inf')
                
                # Check previous cities that could lead to i
                for j in S:
                    if j == i:
                        continue  # Skip the same city
                    prev_mask = S_bitmask & ~(1 << i)

                    # Only try to update if j is in the previous mask
                    if (prev_mask, j) in dp:
                        candidate_cost = dp[(prev_mask, j)] + cost[j][i]
                        if candidate_cost < dp[(S_bitmask, i)]:
                            dp[(S_bitmask, i)] = candidate_cost
                            parent[(S_bitmask, i)] = j

    # Final step: return to the start city (0)
    min_cost = float('inf')
    final_mask = (1 << n) - 1
    last_leg = None
    for i in range(1, n):
        if (final_mask, i) in dp:
            cost_to_return = dp[(final_mask, i)] + cost[i][0]
            if cost_to_return < min_cost:
                min_cost = cost_to_return
                last_leg = i
    
    # Reconstruct the tour path
    tour = [0]
    mask = final_mask
    if last_leg is not None:
        tour.append(0)  # start at the beginning
    while last_leg:
        tour.append(last_leg)
        next_mask = mask & ~(1 << last_leg)
        next_leg = parent.get((mask, last_leg))
        mask = next_mask
        last_leg = next_leg if next_leg is not None else 0
    
    tour.append(0)

    return min_cost, tour

def main():
    examples = [
        [
            [0, 10, 15, 20],
            [5, 0, 9, 10],
            [6, 13, 0, 12],
            [8, 8, 9, 0]
        ],
        [
            [0, 20, 30, 10],
            [20, 0, 15, 25],
            [30, 15, 0, 35],
            [10, 25, 35, 0]
        ]
    ]

    for i, cost_matrix in enumerate(examples, start=1):
        print(f"Running TSP for example {i}:")
        start_time = time.time()
        min_cost, tour = tsp(cost_matrix)
        end_time = time.time()
        
        print("Number of cities:", len(cost_matrix))
        print("Cost matrix:", cost_matrix)
        print("Minimum cost:", min_cost)
        print("Optimal tour:", tour)
        print("Execution time (seconds):", end_time - start_time)
        print("\n")

if __name__ == "__main__":
    main()