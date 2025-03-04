class Zipcode():
    IMPORTANCE_SCORE = 1

    def __init__(self, Neighborhood, ZIP_code, Number_of_households, Population,
                 Households_with_one_or_more_people_65_years_and_over, Households_with_one_or_more_people_under_18_years,
                 Population_with_Bachelor_degree_or_higher, Median_household_income, Households_with_no_vehicles,
                 Households_with_1_plus_vehicles, Proportion_of_developed_open_space,
                 Primary_mode_of_transportation_walking_or_public_transit, Homes_built_2010_or_later,
                 Homes_built_1990_to_2009, Homes_built_1970_to_1989, Homes_built_1950_to_1969, Homes_built_1950_or_earlier,
                 Detached_whole_house, Townhouse, Apartments, Mobile_Homes_Other,
                 Percentage_of_Old_and_Young_people, Percentage_of_Educated_Population):
        
        self.neighborhood = Neighborhood
        self.ZIP_code = ZIP_code

        # Create a dictionary to store values, relationships, and weightings
        self.factors = {
            "number_of_households": {"value": Number_of_households, "relationship": "direct", "weight": 1},
            "population": {"value": Population, "relationship": "direct", "weight": 1},
            "households_with_elderly": {"value": Households_with_one_or_more_people_65_years_and_over, "relationship": "direct", "weight": 1},
            "households_with_children": {"value": Households_with_one_or_more_people_under_18_years, "relationship": "direct", "weight": 1},
            "educated_population": {"value": Population_with_Bachelor_degree_or_higher, "relationship": "direct", "weight": 1},
            "median_household_income": {"value": Median_household_income, "relationship": "inverse", "weight": 0.2},
            "households_with_no_vehicles": {"value": Households_with_no_vehicles, "relationship": "direct", "weight": 0.2},
            "households_with_vehicles": {"value": Households_with_1_plus_vehicles, "relationship": "inverse", "weight": 0.2},
            "developed_open_space": {"value": Proportion_of_developed_open_space, "relationship": "inverse", "weight": 0.1},
            "public_transit_usage": {"value": Primary_mode_of_transportation_walking_or_public_transit, "relationship": "direct", "weight": 0.1},
            "homes_built_2010_or_later": {"value": Homes_built_2010_or_later, "relationship": "inverse", "weight": 0.05},
            "homes_built_1990_to_2009": {"value": Homes_built_1990_to_2009, "relationship": "inverse", "weight": 0.05},
            "homes_built_1970_to_1989": {"value": Homes_built_1970_to_1989, "relationship": "inverse", "weight": 0.05},
            "homes_built_1950_to_1969": {"value": Homes_built_1950_to_1969, "relationship": "inverse", "weight": 0.05},
            "homes_built_1950_or_earlier": {"value": Homes_built_1950_or_earlier, "relationship": "inverse", "weight": 0.05},
            "detached_whole_house": {"value": Detached_whole_house, "relationship": "direct", "weight": 0.05},
            "townhouse": {"value": Townhouse, "relationship": "direct", "weight": 0.05},
            "apartments": {"value": Apartments, "relationship": "inverse", "weight": 0.05},
            "mobile_homes_other": {"value": Mobile_Homes_Other, "relationship": "direct", "weight": 0.05},
            "percentage_old_and_young": {"value": Percentage_of_Old_and_Young_people, "relationship": "direct", "weight": 0.1},
            "percentage_educated_population": {"value": Percentage_of_Educated_Population, "relationship": "direct", "weight": 0.1}
        }

    def __str__(self):
        return f"Zipcode: {self.zip_code}"

    def get_risk(self):
        risk = 0
        for key, factor in self.factors.items():
            if factor["relationship"] == "direct":
                risk += factor["value"] * factor["weight"]
            elif factor["relationship"] == "inverse":
                risk += (1 - factor["value"]) * factor["weight"]
        return risk

    def __str__(self):
        return str(self.zip_code)


 #list of Zipcodes in file
def get_info():
    zipcodes = []
    firstline = True
    with open("normdata.csv","r") as file:
        lines = file.readlines()
        for line in lines: #for each line in the file
            if firstline:
                firstline = False
            else:
                line = line.rstrip() #strip \n
                line = line.split(",") #split based on ,
                for i in range(len(line)):
                    if i != 0:
                        line[i] = float(line[i])
                zipcodes.append(Zipcode(*line))
    return zipcodes

def calculate_risk(zipcode:Zipcode):
    k = 1#some val to scale risk score
    sum_of_direct_vars = normalize_value(zipcode,"percentage_old_and_young") + normalize_value(zipcode,"public_transit_usage")
    sum_of_indirect_vars = normalize_value(zipcode,"median_household_income") + normalize_value(zipcode,"educated_population")
    risk = sum_of_direct_vars/sum_of_indirect_vars * k
    return risk

def normalize_value(zipcode: Zipcode, attribute_name):

    # Extract the attribute values
    values = [getattr(z, attribute_name) for z in zipcodes]

    # Min-Max Scaling
    min_val = min(values)
    max_val = max(values)
    normalized_value = (getattr(zipcode,attribute_name) - min_val)/(max_val-min_val)
    return normalized_value

zipcodes = get_info()
for zip in zipcodes:
    print(str(zip.get_risk()))