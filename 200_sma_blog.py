# Import libraries
from datetime import date
import calendar
import calendar
import yfinance as yf
import pandas as pd

# Create our list of symbols we want to run through the program
list_of_symbols = ["^GSPC"]

# Initialize variables
sma_list = []
sma = 0
above_len = 0
start_price = 0
df = pd.DataFrame(columns = ["Duration", "% Change", "Occurrences", "Date Range"])

# Download data from Yahoo Finance
data = yf.download('^GSPC', start="1993-01-01", end="2021-07-17", interval = "1d")

# Loop through all the data
for i in range(len(data["Close"]) - 1):

    # Start adding values to the sma
    if len(sma_list) < 200:
        sma_list.append(data["Close"][i])

    # Once there are enough values in the sma list, we can start computing the sma
    else:
        # Update sma list and calculate current sma
        sma_list.pop(0)
        sma_list.append(data["Close"][i])
        sma = sum(sma_list) / len(sma_list)

        # If the Low is above the sma
        if float(data["Close"][i]) > float(sma) and str(data.index[i]) != "2021-07-15 00:00:00":

            # Store the starting price if this is the first time it has gone above
            if above_len == 0:
                start_price = data["Close"][i]
                start_date = str(data.index[i].date())

            # Add to the length of time it has spent above the sma
            above_len += 1

        # If it dips below the sma and it was just above
        elif (data["Close"][i] < sma and above_len > 0) or str(data.index[i]) == "2021-07-15 00:00:00":

            # Calculate the % change
            pct_change = ((data["Close"][i] - start_price) / start_price) * 100

            # If this is the first time this duration has occurred
            if above_len not in df["Duration"]:

                # Add all attributes to the dataframe
                df = df.append({"Duration" : above_len, "% Change" : pct_change, "Occurrences" : 1, "Date Range": (start_date + " to " + str(data.index[i].date()))}, ignore_index = True)

            # If it has occurred before
            else:

                # Find the index value of the duration
                index = df.index[df["Duration"] == above_len]

                # Find the total percent change so that we can add the new value to it
                cur_pct_change = df["% Change"][index]
                total_change = df["% Change"][index] * df["Occurrences"][index]

                # Update the number of occurrences
                df["Occurrences"][index] = df["Occurrences"][index] + 1

                # Update the % change
                df["% Change"][index] = (total_change + pct_change) / df["Occurrences"][index]

                # Add our date range(s)
                df["Date Range"][index] = df["Date Range"][index] + ", " + start_date + " to " + str(data.index[i].date())

            # Reset our variables
            above_len = 0

# Save the dataframe to an excel file
df.to_excel(r'200_sma_data_year2.xlsx', index = False)
