# make sure we can retrieve our wrangled data
from wrangler import get_wrangled_df

# various useful imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="ticks", color_codes=True)

'''
This file contains visualisations and descriptive analytics of the wrangled dataset. It is split into 2 parts,
the first containing visualsations of the dataset, the second containing summary descriptive statistics of the dataset,
as well as its segments.
'''

'''
PART 1: Visualisation
'''
# Get our data in a var
wrangled_df = get_wrangled_df("engagement_report.log")

# Revert the numerical values so we can make use of value_counts for discrete strings (for pretty graphs etc.)
wrangled_df.loc[wrangled_df['company_type'] == 1, 'company_type'] = "uk_limited_company"
wrangled_df.loc[wrangled_df['company_type'] == 2, 'company_type'] = "uk_sole_trader"
wrangled_df.loc[wrangled_df['company_type'] == 3, 'company_type'] = "universal_company"

# Reminder of the schema (excluding index):
# 1. company                        : company id as an integer
# 2. company_type                   : company type expressed as integer (1=uk_limited_company, 2 = uk_sole_trader, 3 = universal_company)
# 3. subscribed_after_free_trial    : binary (1=yes,0=no)
# 4. total_times_logged             : integer for total log-ons during trial

# UNCOMMENT TO GENERATE/SHOW GRAPHS
#sns.catplot(x="company_type", y="total_times_logged", hue="subscribed_after_free_trial", kind="box", data=wrangled_df);
#plt.show()

#sns.catplot(x="company_type", y="total_times_logged", hue="subscribed_after_free_trial", kind="swarm", data=wrangled_df);
#plt.show() # <-- UNCOMMENT TO SEE PLOT!
'''
Just by these plots, we already gain a lot of information. At a quick glance, we can summarise these foundings as:

1. Demographics/Customer Segments: It is clear that few universal companies used the service at all (although there are execptions).
   One could therefore theorise that universal companies seem to be an unfavourable segment to target ceteris paribus.

2. Trends: there seems to be a clear trend for companies login on to the service for around >=5 times will subscribe with high certainity.
   around 5 logins seem to be the breaking point wether a subcribtion is made or not.

3. General segments & audience: assuming the data set is a fair representation of the actual customers of the company,
   the main customer segements appears to be 1) uk_limited_company 2) uk_sole_trader (in that order!).
'''

'''
PART 2: Summary descriptive statistics
We will return 5-point summary for reach segment (company_type) as well as a summary for the entire dataset.
'''

# Outputs summary stastistics for total_times_logged
print(wrangled_df.total_times_logged.describe())
# Summarises and counts company types
print(wrangled_df.company_type.value_counts())

# Generate subset containing each type
uk_limited_companies    = wrangled_df.loc[wrangled_df['company_type'] == "uk_limited_company"]
uk_sole_traders         = wrangled_df.loc[wrangled_df['company_type'] == "uk_sole_trader"]
universal_companies     = wrangled_df.loc[wrangled_df['company_type'] == "universal_company"]

# Use above subsets to generate five point again for eacht type
print(uk_limited_companies.total_times_logged.describe())
print(uk_sole_traders.total_times_logged.describe())
print(universal_companies.total_times_logged.describe())

'''
The summary statistics help us to reaffirm the points made in the visualisations. It is clear that
the dataset is comprised of mostly uk_limited_company and that the uk_limited_company also have the
the highest mean and median usage of the service.

We can also see that the standard deviation is relatively lower for universal_companies, which
basically translates to that type of company being relatively unresponsive (from login on to the service)
when granted with a trial.

As for the general dataset in its entirety, while the summary statistics don't really give that much
additional information compared to looking at each segment sepereately, one could use it to design simple
metrics/KPIs that can be used to guide product development or marketing efforts. E.g., as we have already
concluded that the cut-off point (wehter one will subscribe or not) seems to fall around 5 logins during
the trial, the higher our median usage time is, the better we are.

More ideas can be found in the attached presentation (also in this directory).

Please view "model.py" for the final piece of the analysis.
'''

print("end of script...")
