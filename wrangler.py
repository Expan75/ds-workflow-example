# Useful imports
import csv
import pandas as pd

''' Function that wrangles the total number of logins for any given company
    given a engagement_report.log file in the current directory.
    The function returns a dictonary with the wrangled total usage time (key:value where company_id:total_times_logged)
'''
def engagement_report_wrangler(filename):

    # Use rstrip to only get each line by itself (no whitespace at the end)
    lines = [line.rstrip('\n') for line in open(filename)]

    # Checking that we got all
    # print(lines[1])
    # print(lines[-1])
    # print("These many lines were collected: " + str(len(lines)))

    # Define useful var (main thing is dict with key:value pairs of company_id:total_usage)
    company_total_service_usage = {}
    companies = []
    total_usages = []

    # Loop over lines var and extract 1) company_id and total_usage 2) store them in above directory
    for line in lines:
        # Define temporary list containing any given line as words (with no whitespace)
        temp = line.split()
        # Check if we acheived desired structure
        # rint("Company: " + temp[1] + " logged in " + temp[-5])

        any_given_company_id    = temp[1]
        times_logged_anyday     = temp[-5]

        # start adding to the dict but on conditons
        if any_given_company_id in companies:
            total_usages[-1] += int(times_logged_anyday)
        else:
            companies.append(any_given_company_id)
            total_usages.append(int(times_logged_anyday))

    # make sure to add made lists to dictonary
    company_total_service_usage["company"] = companies
    company_total_service_usage["total_times_logged"] = total_usages

    return company_total_service_usage

''' Function that creates a dataframe from both the attributes_report.csv and the wrangled dict of total_times_logged.
    Takes a wrangled dict as input and returns a pandas dataframe containing the wrangled dataself.
    NOTE: the returned dataframe is also preproccessed (turning dummy vars into digits etc.).
'''
def get_wrangled_df(company_total_serv_dict):
    engagement_report_dict = engagement_report_wrangler(company_total_serv_dict)
    # Now that we have a dict, we turn it into a df
    engagement_report_df = pd.DataFrame.from_dict(engagement_report_dict)
    # print(engagement_report_df) # => to spot bugs: print and compare with server log

    # Wrangle attributes into df
    attributes_report_df = pd.read_csv('attributes_report.csv')
    # print(attributes_report_df)

    # Join them into one (map onto right ID) NOTE: need to use assign w/ astype to ensure similar data type
    merged_report_df = pd.merge(attributes_report_df, engagement_report_df.assign(company=engagement_report_df.company.astype('int64')), on='company')
    # print(merged_report_df.to_string())

    '''
    Now that we have a completed the data wrangling we need to apply some numerical transformation to get the Data
    ready for our model. This includes making binary variables and dummy variables (company_type etc.) into numbers.
    This will all be done below:
    '''
    # Replaces company type with int in range (1:3) where:
    # 1 = uk_limited_company
    # 2 = uk_sole_trader
    # 3 = universal_company
    merged_report_df.loc[merged_report_df['company_type'] == "uk_limited_company", 'company_type'] = 1
    merged_report_df.loc[merged_report_df['company_type'] == "uk_sole_trader", 'company_type'] = 2
    merged_report_df.loc[merged_report_df['company_type'] == "universal_company", 'company_type'] = 3
    merged_report_df.company_type = merged_report_df.company_type.astype(int)

    # print(merged_report_df.to_string())

    # Replaces subscribed_after_free_trial with int in range (0:1) where:
    # 0 = false
    # 1 = true
    # Technically not neccessary as python views booleans as numbers, but just to be thorough...
    merged_report_df.subscribed_after_free_trial = merged_report_df.subscribed_after_free_trial.astype(int)
    merged_report_df.subscribed_after_free_trial = merged_report_df.subscribed_after_free_trial.astype(int)

    return merged_report_df

# print(get_wrangled_df("engagement_report.log"))
'''
We are now done with the preproccessing and can start answering descriptive questions and predict behaviour.
These tasked will be split into to seperate files (within the same directory). For descriptive statistics and visualsations,
please view "descriptive.py". For the predictve model (and evaluation of the model), please see "model.py".
'''
