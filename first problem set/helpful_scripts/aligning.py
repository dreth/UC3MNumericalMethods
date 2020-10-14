# 1. Initial Balance
Balance0 = food.addConstrs((init_store + buy[months[0], oil]
                            == consume[months[0], oil] + store[months[0], oil]
                            for oil in oils), "Initial_Balance")

# 2. Balance
Balance = food.addConstrs((store[months[months.index(month)-1], oil] + buy[month, oil]
                           == consume[month, oil] + store[month, oil]
                           for oil in oils for month in months if month != month[0]), "Balance")

# 3. Inventory Target
TargetInv = food.addConstrs(
    (store[months[-1], oil] == target_store for oil in oils), "End_Balance")

# 4.1 Vegetable Oil Capacity
VegCapacity = food.addConstrs((gp.quicksum(consume[month, oil] for oil in oils if "VEG" in oil)
                               <= veg_cap for month in months), "Capacity_Veg")

# 4.2 Non-vegetable Oil Capacity
NonVegCapacity = food.addConstrs((gp.quicksum(consume[month, oil] for oil in oils if "OIL" in oil)
                                  <= oil_cap for month in months), "Capacity_Oil")

# 5. Hardness
HardnessMin = food.addConstrs((gp.quicksum(hardness[oil]*consume[month, oil] for oil in oils)
                               >= min_hardness*produce[month] for month in months), "Hardness_lower")
HardnessMax = food.addConstrs((gp.quicksum(hardness[oil]*consume[month, oil] for oil in oils)
                               <= max_hardness*produce[month] for month in months), "Hardness_upper")


# 6. Mass Conservation
MassConservation = food.addConstrs(
    (consume.sum(month) == produce[month] for month in months), "Mass_conservation")
