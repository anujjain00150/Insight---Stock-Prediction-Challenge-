# Finding Error in Stock Price prediction model
# author@anuj

import pandas as pd

# Reading all the input files
obj1 = open("./input/actual.txt")
if not obj1.read():                    # if the actual file is empty
    out_file = open("./output/comparison.txt","w")
    exit()
else:
    actual_df = data = pd.read_csv('./input/actual.txt', sep="|", header = None)

obj2 = open("./input/predicted.txt")
if not obj2.read():                    # if the prediction file is empty
    out_file = open("./output/comparison.txt","w")
    exit()
else:
    predicted_df = pd.read_csv('./input/predicted.txt', sep="|", header = None)
windowFile = open("./input/window.txt")
window = int(windowFile.read())
windowFile.close()

# Calculating error per stock per hour and saving it in "df" dataframe
def calulate_error_per_hour(dict1, predicted_df):
    error = predicted_df.apply(lambda x: abs(dict1[x[1]]-x[2]), axis=1)
    return error

df = pd.DataFrame({'hour': [] ,'error':[]})

length = len(actual_df)
temp = 1
dict1 = {}

for i in range(0, length):

    if actual_df.loc[i, 0] != temp:
        error = calulate_error_per_hour(dict1, predicted_df[predicted_df[0] == temp])
        error_df = pd.DataFrame({'hour':[temp]*len(predicted_df[predicted_df[0] == temp]),'error':error})
        df = pd.concat([df,error_df])
        temp = actual_df.loc[i, 0]
        dict1 = {}

    dict1[actual_df.loc[i,1]] = actual_df.loc[i,2]

error = calulate_error_per_hour(dict1, predicted_df[predicted_df[0] == temp])
error_df = pd.DataFrame({'hour':[temp]*len(predicted_df[predicted_df[0] == temp]),'error':error})
df = pd.concat([df,error_df])

# Calculating error in each window and saving it in comparison.txt file
max_hr = int(df.iloc[-1,1])
out_file = open("./output/comparison.txt","w")
for i in range(1,max_hr-window+2):
    mean_error_per_window = round(df[(df['hour']>=i) & (df['hour'] <=(i+window-1))]['error'].mean(), 2)
    out_file.write("" + str(i) + "|" + str(i+window-1) + "|" + str(mean_error_per_window) + "\n")
out_file.close()
exit()
