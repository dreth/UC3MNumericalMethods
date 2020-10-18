test_params = {
    'init_store': range(450, 550, 10),
    'target_store': range(450, 550, 10),
    'veg_cap': range(150, 250, 10),
    'oil_cap': range(200, 300, 10),
    'min_hardness': range(1, 11),
    'max_hardness': range(3, 13)
}


def loop_RHS(**params):
    default_params = {
        'init_store_b': (True, 500),
        'target_store_b': (True, 500),
        'veg_cap_b': (True, 200),
        'oil_cap_b': (True, 250),
        'min_hardness_b': (True, 3),
        'max_hardness_b': (True, 6)
    }

    # dict for obj values per RHS change
    obj_changes = {param: [] for param in params.keys()}

    for param, options in params.items():

        dp = {k: v for k, v in default_params.items() if k != f'{param}_b'}
        dp[f'{param}_b'] = (False, 0)

        for option in options:
            # Model deployment
            food = gp.Model('Food Manufacture I')
            # Quantity of food produced in each period
            produce = food.addVars(months, name="Produce")
            # Quantity bought of each product in each period
            buy = food.addVars(months, oils, name="Buy")
            # Quantity used of each product  in each period
            consume = food.addVars(months, oils, name="Use")
            # Quantity stored of each product  in each period
            store = food.addVars(months, oils, name="Store")

            if param == 'init_store':
                # 1. Initial Balance
                Balance0 = food.addConstrs((option + buy[months[0], oil]
                                            == consume[months[0], oil] + store[months[0], oil]
                                            for oil in oils), "Initial_Balance")
            elif param == 'target_store':
                # 3. Inventory Target
                TargetInv = food.addConstrs(
                    (store[months[-1], oil] == option for oil in oils), "End_Balance")
            elif param == 'veg_cap':
                # 4.1 Vegetable Oil Capacity
                VegCapacity = food.addConstrs((gp.quicksum(
                    consume[month, oil] for oil in oils if "VEG" in oil) <= option for month in months), "Capacity_Veg")
            elif param == 'oil_cap':
                # 4.2 Non-vegetable Oil Capacity
                NonVegCapacity = food.addConstrs((gp.quicksum(
                    consume[month, oil] for oil in oils if "OIL" in oil) <= option for month in months), "Capacity_Oil")
            elif param == 'min_hardness':
                # 5.1 Min Hardness
                HardnessMin = food.addConstrs((gp.quicksum(
                    hardness[oil]*consume[month, oil] for oil in oils) >= option*produce[month] for month in months), "Hardness_lower")
            else:
                # 5.2 Max Hardness
                HardnessMax = food.addConstrs((gp.quicksum(
                    hardness[oil]*consume[month, oil] for oil in oils) <= option*produce[month] for month in months), "Hardness_upper")

            if dp['init_store_b'][0] == True:
                Balance0 = food.addConstrs((dp['init_store_b'][1] + buy[months[0], oil]
                                            == consume[months[0], oil] + store[months[0], oil]
                                            for oil in oils), "Initial_Balance")
            Balance = food.addConstrs((store[months[months.index(month)-1], oil] + buy[month, oil]
                                       == consume[month, oil] + store[month, oil]
                                       for oil in oils for month in months if month != month[0]), "Balance")
            if dp['target_store_b'][0] == True:
                TargetInv = food.addConstrs(
                    (store[months[-1], oil] == dp['target_store_b'][1] for oil in oils), "End_Balance")
            if dp['veg_cap_b'][0] == True:
                VegCapacity = food.addConstrs((gp.quicksum(consume[month, oil] for oil in oils if "VEG" in oil)
                                               <= dp['veg_cap_b'][1] for month in months), "Capacity_Veg")
            if dp['oil_cap_b'][0] == True:
                NonVegCapacity = food.addConstrs((gp.quicksum(consume[month, oil] for oil in oils if "OIL" in oil)
                                                  <= dp['oil_cap_b'][1] for month in months), "Capacity_Oil")
            if dp['min_hardness_b'][0] == True:
                HardnessMin = food.addConstrs((gp.quicksum(hardness[oil]*consume[month, oil] for oil in oils)
                                               >= dp['min_hardness_b'][1]*produce[month] for month in months), "Hardness_lower")
            if dp['max_hardness_b'][0] == True:
                HardnessMax = food.addConstrs((gp.quicksum(hardness[oil]*consume[month, oil] for oil in oils)
                                               <= dp['max_hardness_b'][1]*produce[month] for month in months), "Hardness_upper")
            MassConservation = food.addConstrs(
                (consume.sum(month) == produce[month] for month in months), "Mass_conservation")
            obj = price*produce.sum() - buy.prod(cost) - holding_cost*store.sum()
            food.setObjective(obj, GRB.MAXIMIZE)  # maximize profit
            food.optimize()
            try:
                obj_changes[param].append(food.ObjVal)
            except:
                obj_changes[param].append(0)

    return obj_changes


loop_RHS(**test_params)
