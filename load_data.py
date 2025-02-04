
from datetime import datetime
import pandas as pd
import json

def load_data_into_data_frame():
    # load reform data
    data_file = open("./data/core.json")
    data = json.load(data_file)

    ####################################################
    # Put data from json file into Pandas DataFrame
    ####################################################

    # I'm organizing the data as one row for each parking reform 
    # (removal of parking minimum, addition of parking maximum etc.)

    # create lists to hold intermediate data to be added into the dataframe
    coord_list = []
    country_list = []
    name_list = []
    pop_list = []
    repeal_list = []
    state_list = []
    type_list = []
    reform_type_list = []
    date_list = []
    year_list = []
    land_list = []
    scope_list = []
    status_list = []


    # loop through all entries and put data into a list for each column of eventual DataFrame
    for entry in data.values():
        place = entry["place"]

        # create row for each parking minimum removed
        try:
            rm_min = entry["rm_min"]

            for removed_minimum in rm_min:

                coord_list.append(place["coord"])
                country_list.append(place["country"])
                name_list.append(place["name"])
                pop_list.append(place["pop"])
                repeal_list.append(place["repeal"])
                state_list.append(place["state"])
                type_list.append(place["type"])
                reform_type_list.append("Removed Parking Minimum")
                date_list.append(removed_minimum["date"])
                try:
                    year_list.append(
                        datetime.strptime(removed_minimum["date"], "%y-%m-%d").year
                    )
                except:
                    year_list.append(None)
                land_list.append(str(removed_minimum["land"]))
                scope_list.append(removed_minimum["scope"])
                status_list.append(removed_minimum["status"])
        except:
            pass

        # create row for each parking maximum added
        try:
            add_max = entry["add_max"]

            for added_maximum in add_max:

                coord_list.append(place["coord"])
                country_list.append(place["country"])
                name_list.append(place["name"])
                pop_list.append(place["pop"])
                repeal_list.append(place["repeal"])
                state_list.append(place["state"])
                type_list.append(place["type"])
                reform_type_list.append("Added Parking Maximum")
                date_list.append(added_maximum["date"])
                try:
                    year_list.append(
                        datetime.strptime(added_maximum["date"], "%Y-%m-%d").year
                    )
                except:
                    year_list.append(None)
                land_list.append(str(added_maximum["land"]))
                scope_list.append(added_maximum["scope"])
                status_list.append(added_maximum["status"])
        except:
            pass

        # create row for each parking minimum reduced 
        try:
            reduce_min = entry["reduce_min"]

            for reduced_min in reduce_min:

                coord_list.append(place["coord"])
                country_list.append(place["country"])
                name_list.append(place["name"])
                pop_list.append(place["pop"])
                repeal_list.append(place["repeal"])
                state_list.append(place["state"])
                type_list.append(place["type"])
                reform_type_list.append("Reduced Parking Minimum")
                date_list.append(reduced_min["date"])
                try:
                    year_list.append(
                        datetime.strptime(reduced_min["date"], "%Y-%m-%d").year
                    )
                except:
                    year_list.append(None)
                land_list.append(str(reduced_min["land"]))
                scope_list.append(reduced_min["scope"])
                status_list.append(reduced_min["status"])
        except:
            pass

    # put lists into new dictionary to create DataFrame
    data_list_dict = {
        "Coordinates": coord_list,
        "Country": country_list,
        "Name": name_list,
        "Population": pop_list,
        "Repealed": repeal_list,
        "State": state_list,
        "Type": type_list,
        "Reform Type": reform_type_list,
        "Date": date_list,
        "Year": year_list,
        "Land": land_list,
        "Scope": scope_list,
        "Status": status_list,
    }

    df = pd.DataFrame(data_list_dict)

    return df