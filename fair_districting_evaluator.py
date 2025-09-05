
"""
    This program opens a data file containing election information and uses that data to calculate 
    wasted votes, efficiency gap percentage, and the favored political party of the year according
    to the state chosen by the user. 
    
    Filename: fair_districting_evaluator.py
    Author: foster miller
    Date: 03/03/2024
    Collaborators: None
    Internet Source: NA
"""

def data_compiler() -> list:
    """
    pull data from text file and store in 2D list
    parameters: None
    return: list
    """
    with open("1976-2020votes.txt") as infile:
        data_list = []
        # breaks apart each line // strip and split allow for multiple elems in list
        for line in infile:
            inner_lists = line.strip().split(',')
            data_list.append(inner_lists)
            # typecasts all items except state name from str to int
            # make state name lower case
            for i in range (len(inner_lists)):
                if i != 1:
                    inner_lists[i] = int(inner_lists[i])
                else:
                    inner_lists[i] = inner_lists[i].lower()

        return data_list
    
def process_voter_information(data_list, selected_index):
    """
    takes list and specific index to calculate districts, create districts list and output wasted votes,
    efficiency gap percentage, and favored party
    parameters: (list, int)
    return: None
    """
    # use print statement for troubleshooting
    # print(data_list[selected_index])
    districts = (len(data_list[selected_index]) - 2) // 3   # takes away index 0 and 1 (year and state), and divides by 3
    if districts <= 1:
        print('Efficiency gap cannot be computed for states with only one district.')
        return
    else:
        district_list = []
        new_district = []
        count = 0 
        for i in range(2, len(data_list[selected_index])): 
            if count == 1:      # democratic votes
                district_dem_votes = data_list[selected_index][i]
                new_district.append(district_dem_votes)
            elif count == 2:    # republican votes
                district_rep_votes = data_list[selected_index][i]
                new_district.append(district_rep_votes)

            count += 1
            
            if count == 3:  # appends and resets new_district and resets count
                district_list.append(new_district)
                new_district = []
                count = 0
                
        total_votes, wasted_dem_votes, wasted_rep_votes = evaluate_districts(district_list)

        if total_votes == 0 and wasted_dem_votes == 0 and wasted_rep_votes == 0:
            print('Efficiency gap cannot be computed because at least one district was uncontested.')
            return 
        else:
            gap_percentage, favored_party = gap_efficiency_calculator(total_votes, wasted_dem_votes, wasted_rep_votes)

            print(f'{districts} districts.')
            print(f'Wasted Democratic votes: {wasted_dem_votes}')
            print(f'Wasted Republican votes: {wasted_rep_votes}')
            print(f'Efficiency gap: {gap_percentage}%, in favor of {favored_party}.')

def gap_efficiency_calculator(total, wasted_dem, wasted_rep):
    """
    takes information and calculates and returns gap efficiency percentage and favored party
    parameters: (int, int, int)
    return: float, str
    """ 
    percentage = 0
    favored = ''
    if wasted_dem > wasted_rep:
        favored = 'Republicans'
        percentage = round(((wasted_dem - wasted_rep) / total) * 100, 2)    # round() takes number and rounds to the nearest hundreth of a percent
    elif wasted_dem < wasted_rep:
        favored = 'Democrats'
        percentage = round(((wasted_rep - wasted_dem) / total) * 100, 2)
        
    return percentage, favored

def evaluate_districts(district_list):
    """
    takes a 2D list and calculates and returns total votes and wasted votes
    parameters: (int, int, int)
    return: int, int, int
    """ 
    total_votes = 0
    wasted_dem_votes = 0
    wasted_rep_votes = 0

    for district in district_list:
        if district[0] == 0 or district[1] == 0:    # all 0's signifies uncontested district
            return 0, 0, 0 
        
        total_district_votes = district[0] + district[1]

        if district[0] > district[1]:
            wasted_dem_votes += district[0] - (total_district_votes // 2)   # calculates wasted votes for winning party
            wasted_rep_votes += district[1]     # calculates wasted votes for losing party
        elif district[0] < district[1]:
            wasted_rep_votes += district[1] - (total_district_votes // 2)
            wasted_dem_votes += district[0]

        total_votes += total_district_votes

    return total_votes, wasted_dem_votes, wasted_rep_votes

def main():
    """
    creates 2D list of voter information, creates year_list and state_list
    requests year and state inputs from user and outputs data with those in mind
    create loop until user no longer wants to recieve information
    parameters: None
    return: None
    """ 
    voter_information_list = data_compiler()
    year_list = [int(i) for i in range(1976, 2021, 2)]
    state_list = [voter_information_list[i][1].lower() for i in range(50)]

    is_finished = False

    print('This program evaluates districting fairness for US House elections from 1976-2020.')
    # keep prompting user until user no longer wants information
    while not is_finished:
        try:
            year = int(input('What election year would you like to evaluate? '))
        except ValueError:
            print(f"{year} is not a valid year.")
            year = None
        while year not in year_list:    # loop to catch invalid years
            print('Sorry, valid election years are even years from 1976-2020.')
            try:
                year = int(input('What election year would you like to evaluate? '))
            except ValueError:
                year = None

        state = input('What state would you like to evaluate? ').lower()
        while state not in state_list:  # loop to catch invalid state names
            print(f'{state.capitalize()} is not a valid state')
            state = input('What state would you like to evaluate? ').lower()

        selected_index = 0  # initialize selected_index
        for i in range(len(voter_information_list)):    # cycles through until correct election list is found
            if voter_information_list[i][0] == year and voter_information_list[i][1] == state:
                selected_index = i
                break   # stops iterating once correct nested list is found

        process_voter_information(voter_information_list, selected_index)

        user_answer = input('Would you like to continue, Y or N? ').lower()
        while user_answer != 'n' and user_answer != 'y':
            user_answer = input('Would you like to continue, Y or N? ').lower()

        if user_answer == 'n':
            is_finished = True

if __name__ == '__main__':
    main()