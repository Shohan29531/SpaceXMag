from asyncio import events
import os
import json
import csv

# img_order = [100, 1067, 272, 201, 340, 313, 2535, 2778, 169, 327, 2084, 1530, 766, 102, 201, 6335, 1530, 237, 8, 469, 3546, 5448, 3268, 3122, 3800, 835, 1517, 1002, 366, 100, 2853, 2849, 4913, 4873, 5177, 5648]
# ui_order = ["org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc", "org", "spc"]

if __name__ == "__main__":

    directory = "E:/Ph.D. Studies/Fall 2022/Study Data- Magnification/.Optimal Mag Study Data/Participant data/"

    current_participant = "11. Ishtiak/"

    extension = 'logs/'

    complete_path = directory + current_participant + extension

    all_files = os.listdir( complete_path )

    # print(len(all_files), all_files[0])

    with open('mag_data.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
    for fileName in all_files:

        parts = fileName.split('_')
        participant_name = parts[0]
        task = parts[1]
        mag_mode = parts[2]
        image_id = parts[3]
        ui_type = parts[4]


        current_file = open( complete_path + "/" + fileName )
        current_file_data = json.load( current_file )
        current_file_data = current_file_data['events']

        mag_total = 0
        mag_total_not_normalized = 0

        fisheye_dict = {"1.5": 1.5,
         "2": 1.6 , "2.5": 1.75, 
         "3.0": 1.75,
         "3": 1.75, "4": 2.5, 
         "5": 3.25, "6": 4}

        for item in current_file_data:

            if( mag_mode == "fisheye" ):
                mag_total += ( float(item['base_magnification']) * 
                fisheye_dict[ str(item['d']) ] )
                mag_total_not_normalized += fisheye_dict[ str(item['d']) ]
            else:
                mag_total += ( float(item['base_magnification']) *
                float(item['current_magnification']) )
                mag_total_not_normalized += float(item['current_magnification'])

        avg_mag = mag_total / len(current_file_data)  
        avg_not_normalized_mag = mag_total_not_normalized / len(current_file_data)

        # base_mag = item['base_magnification']

        # print(participant_name, task, mag_mode, image_id, ui_type)

        with open('mag_data.csv', 'a', newline='', 
        encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow([participant_name, mag_mode, image_id, ui_type, task, avg_mag])