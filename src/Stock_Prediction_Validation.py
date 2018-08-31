# Finding Error in Stock Price prediction model
# author @anuj

import pandas as pd
import numpy as np

# Reading all the input files
obj1 = open("./input/actual.txt")
if not obj1.read():                    # if the actual file is empty
    out_file = open("./output/comparison.txt","w")    # result an error msg in output file
    out_file.write("error: actual.txt file is empty.")
    out_file.close()
    exit()
else:
    actual_df = data = pd.read_csv("./input/actual.txt", sep="|", header = None)

obj2 = open("./input/predicted.txt")
if not obj2.read():                    # if the prediction file is empty
    out_file = open("./output/comparison.txt","w")   # result an error msg in output file
    out_file.write("error: predicted.txt file is empty.")
    out_file.close()
    exit()
else:
    predicted_df = pd.read_csv("./input/predicted.txt", sep="|", header = None)

# reading the size of the window
windowFile = open("./input/window.txt")
window = int(windowFile.read())
windowFile.close()




length = len(actual_df)
temp = 1    # is used to keep check of the hour of which we are calculating the error.
dict1 = {}  # it contains the actual value of each stock(Key) for 1 hour at a time.

# Function to calculate error per stock in a particular hour and will return the list of errors in that hour.
# Input to this function are 1. dictionary for that hour and predicted stock values of that hour.
def calulate_error_per_hour(dict1, predicted_df):
    error = predicted_df.apply(lambda x: abs(dict1[x[1]]-x[2]), axis=1)
    return error

# df dataframe is used to store average error corresponding to every hour
df = pd.DataFrame({'hour': [] ,'error':[]})

# this for loop will form the "df" dataframe
for i in range(0, length):
    
    if actual_df.loc[i, 0] != temp:     # to check if the hour is changed
        if predicted_df[predicted_df[0] == temp].empty:
            error_df = pd.DataFrame({'hour':[temp],'error': [np.nan]})
        else:
            error = calulate_error_per_hour(dict1, predicted_df[predicted_df[0] == temp])   # calling calulate_error_per_hour function
            error_df = pd.DataFrame({'hour':[temp]*len(predicted_df[predicted_df[0] == temp]),'error':error})
        df = pd.concat([df,error_df])
        temp = actual_df.loc[i, 0]
        dict1 = {}      # resetting the dictionary to save the values for the next hour
    
    dict1[actual_df.loc[i,1]] = actual_df.loc[i,2]      # storing actual values of stock for 1 hour

if predicted_df[predicted_df[0] == temp].empty:   # same code of for loop just for the last hour
    error_df = pd.DataFrame({'hour':[temp],'error': [np.nan]})
else:
    error = calulate_error_per_hour(dict1, predicted_df[predicted_df[0] == temp])   # calling calulate_error_per_hour function
    error_df = pd.DataFrame({'hour':[temp]*len(predicted_df[predicted_df[0] == temp]),'error':error})
df = pd.concat([df,error_df])

# Calculating error in each window and saving it in comparison.txt file
max_hr = int(df.iloc[-1,1])
out_file = open("./output/comparison.txt","w")    # creating output file
for i in range(1,max_hr-window+2):
    temp=0     # temp is used as a flag for checking either the error is NA or has some value
    for b in df[(df['hour']>=i) & (df['hour'] <=(i+window-1))]['error'].isnull():
        if b == False:
            temp=1
            mean_error_per_window = round(df[(df['hour']>=i) & (df['hour'] <=(i+window-1))]['error'].mean(), 2)
            out_file.write("" + str(i) + "|" + str(i+window-1) + "|" + str(mean_error_per_window) + "\n")
            break
    if temp==0:
        mean_error_per_window="NA"
        out_file.write("" + str(i) + "|" + str(i+window-1) + "|" + str(mean_error_per_window) + "\n")

out_file.close()
exit()
