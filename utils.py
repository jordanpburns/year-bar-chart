import math
def round_down_to_nearest_ten(x):
    """takes x and returns an int rounded down to the nearest ten"""
    return int(math.floor(x / 10.0)) * 10

def set_attractive_y_dtick_size(masked_df_years):
    """returns an int to be used as the spacing between the ticks on the y axis that
    allows for 5 or less ticks"""
    
    #in case the user selects a range without any data
    #TODO put in message that there is no data in selected range
    try:
        highest_year_count = max(masked_df_years.value_counts())
    except:
        return 1

    dticks = int(round(highest_year_count / 5))
    if dticks == 0:
        return 1
    else:
        return dticks

def set_attractive_x_dtick_size(years):
    """returns an int to be used as the spacing between the ticks on the x axis that
    allows for 5 or less ticks"""
    
    #in case the user selects a range without any data
    #TODO put in message that there is no data in selected range

    dticks = int(round((years[1] - years[0]) / 5))
    if dticks == 0:
        return 1
    else:
        return dticks