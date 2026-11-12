import numpy as np 
import csv 
import sys 


def distance_calculator(lat1, lon1, lat2, lon2): # Uses Haversine formula
#   Convert to radians 
    lat1 = np.radians(float(lat1))
    lon1 = np.radians(float(lon1))
    lat2 = np.radians(float(lat2))
    lon2 = np.radians(float(lon2))

#   Haversine value
    a = (np.sin((lat2-lat1)/2))**2 + np.cos(lat1)*np.cos(lat2)*(np.sin((lon2-lon1)/2))**2

#   Central angle
    c = 2 * np.arctan2(np.sqrt(a),np.sqrt(1-a))

#   Return Distance
    return (6371000) * c




# There could be multiple csv files as inputs so we use sys
if len(sys.argv) < 3: 
    print("Please enter the targets.csv or at least 1 mission.csv file")
    sys.exit(1)

target_file = sys.argv[-1]            # Target file
target = []
with open(target_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        target.append(row)


print(target)
    
mission_files = sys.argv[1:-1]        # Mission logs


# Parsing
for file in range(len(mission_files)):
    with open(mission_files[file], "r", encoding="utf-8") as f:
        time = 0
        csv_reader = csv.DictReader(f)
        prev = None
        print(target)
        for row in csv_reader:
            if time == 0:      # Starting coords
                prev = row
                time += 1
                continue

            if time != int(row["time_s"]):       # GREEN
                print(str(row["time_s"]) + "," + " Green")
                
                continue

            if row["lat"] == "" or row["lon"] == "": # no lat or lon meaning no data
                print(str(time)+",")
                time += 1
                continue

            if row["mode"] == "MANUAL":     # BLUE 
                print(str(time)  + "," + "Blue")
                prev = row
                time += 1
                continue

            if row["mode"] == "AUTO":
                if distance_calculator(prev["lat"], prev["lon"], target[file][1], target[file][2]) <= 3: 
                    if distance_calculator(prev["lat"], prev["lon"], row["lat"], row["lon"]) / (int(row["time_s"]) - int(prev["time_s"])) < 0.5:
                        # This means Green
                        print(str(time)  + "," + "Green")
                        time += 4
                        continue
                    else:
                        print(str(time)  + "," + "Red")
                        prev = row
                        time += 1
                        continue
                else: 
                    print(str(time)  + "," + "Red")
                    prev = row
                    time += 1
                    continue