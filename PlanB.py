import random

allStr = []
maxCap = []


def genLists(amount, capacity):
    for a in range(0, amount):
        allStr.append([])
        maxCap.append(random.randint(1, capacity))


def simulate_system(cars):
    iterations = 0

    while cars > 0:
        iterations += 1

        # Move cars
        for i in range(len(allStr) - 1):
            current_list = allStr[i]
            next_list = allStr[i + 1]

            if len(current_list) > 0:
                car = current_list.pop(0)

                if len(next_list) < maxCap[i + 1]:
                    next_list.append(car)
                else:
                    current_list.insert(0, car)

        # Handle the last list
        last_list = allStr[-1]
        if len(last_list) > 0:
            last_car = last_list.pop(0)
            cars -= 1

        # Add 1 to a random list
        random_list_index = random.randint(0, len(allStr) - 1)
        random_list = allStr[random_list_index]

        if len(random_list) < maxCap[random_list_index]:
            random_list.append(1)
        # Decrease capacity after waiting
        for i in range(len(allStr)):
            for j in range(len(allStr[i])):
                allStr[i][j] -= 1
                if allStr[i][j] == 0:
                    allStr[i].pop(j)

        # Increase capacity
        for i in range(len(allStr)):
            maxCap[i] += 1

    return iterations


def simulate_systemGenAlg(initcars, amount, capacity, maxCap2):
    iterations = 0
    population = 100
    mut_rate = 0.2
    best = True

    first = True
    maxiter = 0

    bestOfAll = 1000000
    same = 0

    # Generate initial population
    while best:

        popList = []

        for a in range(0, population - 1):
            maxCap1 = random.choices(range(1,capacity), k = amount)
            # for i in range(0, amount):
            #     maxCap1.append(random.randint(1, capacity))
            popList.append(maxCap1)

        if first:
            popList.append(maxCap2)
            first = False

        else:
            while len(popList) - 5 <= population:
                kid = []
                for i in range(0, amount):
                    if random.random() < 0.2:
                        kid.append(top5[0][i])
                    elif 0.2 < random.random() < 0.4:
                        kid.append(top5[1][i])
                    elif 0.4 < random.random() < 0.6:
                        kid.append(top5[2][i])
                    elif 0.6 < random.random() < 0.8:
                        kid.append(top5[3][i])
                    else:
                        kid.append(top5[4][i])
                # Mutate
                for a in range(0, len(kid)):
                    if random.random() < mut_rate:
                        kid[a] = random.randint(1, capacity)
                popList.append(kid)

            popList.append(top5)

        totalIt = []

        for a in range(0, len(popList)):
            cars = initcars
            iterations = 0

            while cars > 0:
                iterations += 1

                # Move cars
                for i in range(len(allStr) - 1):
                    current_list = allStr[i]
                    next_list = allStr[i + 1]

                    if len(current_list) > 0:
                        car = current_list.pop(0)

                        if len(next_list) < maxCap[i + 1]:
                            next_list.append(car)
                        else:
                            current_list.insert(0, car)

                # Handle the last list
                last_list = allStr[-1]
                if len(last_list) > 0:
                    last_car = last_list.pop(0)
                    cars -= 1

                # Add 1 to a random list
                random_list_index = random.randint(0, len(allStr) - 1)
                random_list = allStr[random_list_index]

                if len(random_list) < maxCap[random_list_index]:
                    random_list.append(1)

                # Decrease capacity after waiting
                for i in range(len(allStr)):
                    for j in range(len(allStr[i])):
                        allStr[i][j] -= 1
                        if allStr[i][j] == 0:
                            allStr[i].pop(j)

                # Increase capacity
                for i in range(len(allStr)):
                    maxCap[i] += 1

            totalIt.append(iterations)

        # Fitness
        min_values = sorted(set(totalIt))[:5]  # Get the 5 unique lowest values
        if len(min_values) != 0:
            bestIndex = [index for index, value in enumerate(totalIt) if value in min_values]
            top5 = []
            # Check the length of bestIndex before trying to access elements
            for a in range(min(5, len(bestIndex))):
                top5.append(popList[bestIndex[a]])

        if len(min_values) == 0:
            maxiter += 1

        elif min_values[0] < bestOfAll:
            bestOfAll = min_values[0]

        else:
            same += 1

        if same == 50 or maxiter == 500:
            best = False


    return top5, bestOfAll



amnt = 20
cap = 25
cars1 = 100

genLists(amnt, cap)
iterations_taken = simulate_system(cars1)
print(f"Cars took {iterations_taken} iterations to leave the system.")
genetic, iterGen = simulate_systemGenAlg(cars1, amnt, cap, maxCap)
print(f"Cars took {iterGen} iterations to leave the system.")
print(genetic)
