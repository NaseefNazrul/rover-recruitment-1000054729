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
        row.append(False)   # found_status
        target.append(row)

    
mission_files = sys.argv[1:-1]        # Mission logs


# Parsing
for file in range(len(mission_files)):
    for i in range(len(target)):
        target[i][3] = False  # Resets the target 

    with open(mission_files[file], "r", encoding="utf-8") as f:
        time = 0
        csv_reader = csv.DictReader(f)
        prev = None
        green_status = 0

        for row in csv_reader:
            if time == 0:      # Starting coords
                prev = row
                time += 1
                continue

            if green_status != 0:     # Green for 5 seconds

                print(str(row["time_s"]) + "," + " Green")
                if row["lat"] == "" or row["lon"] == "":
                    temp = row
                    temp["lat"] = prev["lat"]
                    temp["lon"] = prev["lon"]
                    prev = temp
                    green_status -= 1
                    time += 1
                    continue
                else:
                    prev = row
                    green_status -= 1
                    time += 1
                    continue

            if time != int(row["time_s"]):   # No time  
                temp_time = int(row["time_s"]) - time
                for i in range(temp_time):
                    print(str(time) + ",")
                    time+=1
                

            if row["mode"] == "MANUAL":     # Blue 
                if row["lat"] == "" or row["lon"] == "":
                    temp = row
                    temp["lat"] = prev["lat"]
                    temp["lon"] = prev["lon"]
                    prev = temp
                    print(str(time)+ "," + " Blue")
                else:
                    print(str(time)+ "," + " Blue")
                    prev = row

            elif row["mode"] == "AUTO": 
                if row["lat"] == "" or row["lon"] == "":
                    temp = row
                    temp["lat"] = prev["lat"]
                    temp["lon"] = prev["lon"]
                    prev = temp
                    print(str(time)+ "," + " Red")

                else:
                    for target_number in range(len(target)):
                        if target_number == (len(target)-1) and target[target_number][3] == True:   # All targets have beenn found
                            print(str(time)+ "," + " Red")
                            prev = row

                        if target[target_number][3] == True:  # Current target as been found
                            continue

                        if distance_calculator(prev["lat"], prev["lon"], target[target_number][1], target[target_number][2]) <= 3 \
                                and \
                                    distance_calculator(prev["lat"], prev["lon"], row["lat"], row["lon"]) / (int(row["time_s"]) - int(prev["time_s"])) < 0.5:
                            # This means Green
                            print(str(time)  + "," + " Green")
                            prev = row
                            green_status = 4
                            target[target_number][3] = True
                            break

                        else:
                            print(str(time) + "," + " Red")
                            prev = row
                            break

            time += 1