'''
Zipcode class to hold all data related to a specific zipcode
Methods:
    __init__(): takes in all data associated to a specific zipcode given in the data
        self.neighborhood: String
        self.ZIP_code: String
        self.factors: dict{dict{value,relationship,weight}}
            all factors taken into consideration when calculating risk, each factor will have a normalized value,
            relationship (direct/inverse), weight (significance to risk)
        self.risk: float
            risk value for this zipcode calculated using self.get_risk()
    get_risk(): computes factors and returns a risk value, higher value means a zipcode is at more risk
        iterates through self.factors and adds them to a risk value after multipying by value weighting
'''
class Zipcode():

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

            "median_household_income": {"value": Median_household_income, "relationship": "inverse", "weight": 1},
            "developed_open_space": {"value": Proportion_of_developed_open_space, "relationship": "inverse", "weight": 0.2},
            "public_transit_usage": {"value": Primary_mode_of_transportation_walking_or_public_transit, "relationship": "direct", "weight": 0.6},
            "homes_built_2010_or_later": {"value": Homes_built_2010_or_later, "relationship": "inverse", "weight": 0.7},
            "homes_built_1990_to_2009": {"value": Homes_built_1990_to_2009, "relationship": "inverse", "weight": 0.4},
            "homes_built_1970_to_1989": {"value": Homes_built_1970_to_1989, "relationship": "direct", "weight": 0.3},
            "homes_built_1950_to_1969": {"value": Homes_built_1950_to_1969, "relationship": "direct", "weight": 0.4},
            "homes_built_1950_or_earlier": {"value": Homes_built_1950_or_earlier, "relationship": "direct", "weight": 0.7},
            "percentage_old_and_young": {"value": Percentage_of_Old_and_Young_people, "relationship": "direct", "weight": 0.5},

        }
        
        self.risk = self.get_risk()

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

#defines lists used
zipcodes = get_info()
risks = []
scaled_risks = []
#iterates through the Zipcodes and gets the risk for each zip code
for zip in zipcodes:
    risks.append(zip.risk)
#finds min and max risk to use in normalization
min_risk = max(risks)
max_risk = min(risks)
#converts risks to normalized/scaled risks (0-100)
for risk in risks:
    scaled_risks.append(1 + ((risk - min_risk) / (max_risk - min_risk)) * 99)
#print normalized/scaled risks (1-100)
for srisk in scaled_risks:
    print(str(srisk))