
def power_set(initial_set):
    sets = {frozenset(initial_set)} if len(initial_set) > 0 else set()

    if len(initial_set) > 1:     
        for item in initial_set:
            subset = initial_set ^ {item}
            sets = sets | power_set(subset)
        
    return sets

def belief_interval(event_set, set_values, initial_set):
    event_power_set = power_set(event_set)
    complement_power_set = power_set(initial_set ^ event_set)

    bel = 0.0
    for subset in event_power_set:
        bel += set_values[subset]

    p_asterisk = 1.0
    for subset in complement_power_set:
        p_asterisk -= set_values[subset]

    return [bel, p_asterisk]

initial_set = {"Baixo", "Médio", "Alto"}
sets = power_set(initial_set)

print("Number of iterations: ", end="")
n_iter = int(input())

old_values = {}
for i in range(n_iter):
    print(f"ITERATION {i+1}:")

    new_values = {}
    for item in sets:
        print(f"Value for {set(item)}: ", end="")
        new_values[item] = float(input())

    if i == 0:
        old_values = new_values
    else:
        temp_values = {old_set: 0.0 for old_set in old_values}
        temp_values[frozenset()] = 0.0

        for old_set in old_values:
            for new_set in new_values:
                key = old_set & new_set
                temp_values[key] += old_values[old_set] * new_values[new_set]

        print("Empty set: ", temp_values[frozenset()])

        for old_set in old_values:
            old_values[old_set] = temp_values[old_set]/(1.0 - temp_values[frozenset()])

for old_set in old_values:
    print()
    print(f"{set(old_set)}: {old_values[old_set]}")
    print(f"BI: {belief_interval(old_set, old_values, initial_set)}")
