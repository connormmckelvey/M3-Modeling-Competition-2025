# Open the file and read all lines
with open("electdata.csv", "r") as file:
    temps = []
    for line in file:
        # Split the line by comma
        parts = line.strip().split(',')
        if len(parts) == 2:
            # Convert the second part (temperature) to float and add to the list
            try:
                temp = float(parts[1])
                temps.append(temp)
            except ValueError:
                print(f"Warning: Could not convert '{parts[1]}' to float.")
                
# Process every 12 temperatures and find the max value
max_temps = [max(temps[i:i+12]) for i in range(0, len(temps), 12)]
max_temps.reverse()

for temp in max_temps:
    print(temp)

for i in range(21):
    year = i + 2025
    usage = ((((1.787 * (year)) - 3286) * 0.0331) * 0.2874)
    print(str(usage))