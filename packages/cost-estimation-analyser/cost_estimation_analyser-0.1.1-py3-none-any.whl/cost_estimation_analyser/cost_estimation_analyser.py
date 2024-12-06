class CostAnalyzer:
    def __init__(self, base_costs, cost_multipliers):
        #It initialize the CostAnalyzer with dictionary base_costs and cost_multipliers.
        self.base_costs = base_costs
        self.cost_multipliers = cost_multipliers

    def calculate_cost(self, category, incident_type, level):
        # The method calculate_cost calculates total estimated cost with combination of values.
        #Error handling, if any of the input value is invalid.
        if category not in self.base_costs:
            raise ValueError(f"Invalid category: {category}. Supported categories: {list(self.base_costs.keys())}")
        
        if incident_type not in self.cost_multipliers:
            raise ValueError(f"Invalid incident type: {incident_type}. Supported types: {list(self.cost_multipliers.keys())}")
        
        if level not in self.cost_multipliers[incident_type]:
            raise ValueError(f"Invalid level: {level}. Supported levels: {list(self.cost_multipliers[incident_type].keys())}")

        # Total cost calculation.
        base_cost = self.base_costs[category]
        multiplier = self.cost_multipliers[incident_type][level]
        estimated_cost = base_cost * multiplier

        return estimated_cost
