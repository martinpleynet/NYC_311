"""
This script preprocesses the 2020 NYC 311 data to allow for increased dashboard refresh speed
"""
import pandas as pd

# read in cleaned 2020 data
nyc_2020=pd.read_csv("../nyc_2020_final.csv")

#create list of all zipcode
unique_zips=list(nyc_2020['zipcode'].unique())
#remove nan from menu list
del unique_zips[3]
#convert all zipcodes into strings ans sort
unique_zips = sorted([ str(int(x)) for x in unique_zips ])

#calculate averages of all zipcodes and store in a dictionary
zip_avgs_dict ={}
for z in unique_zips:
    df=nyc_2020.groupby('zipcode').get_group(float(z))
    cur_zip=[]
    for i in range(1,10):
        try:
            cur_zip.append(df.groupby('month').get_group(i)['response_time'].mean())
        except KeyError:
            cur_zip.append(0)

    zip_avgs_dict[z]=cur_zip

# save df of monthly averages by zipcode
pre_df=pd.DataFrame.from_dict(zip_avgs_dict)
pre_df.to_csv('preprocessed.csv', index=False)

# calculate overall response time averages by month
avg_2020={}
monthly_avgs=[]
for i in range(1,10):
    monthly_avgs.append(nyc_2020.groupby('month').get_group(i)['response_time'].mean())

avg_2020['2020']=monthly_avgs
df_2020=pd.DataFrame.from_dict(avg_2020)
# save df of overall monthly averages
df_2020.to_csv('all_avgs.csv', index=False)
