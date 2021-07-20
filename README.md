# 200-SMA-Blog

All of our analysis and results can be found in the blog on our [website](https://extremistanresearch.com). In this README, we will broadly explain our code, as   well as our thought process in our methodology. 
  
We used 1 python program titles 200_sma_blog.py to gather the data for this blog. This program has been fully commented and uploaded to the repository.


## The Process

This program was not a super complicated one, but I will still explain our process. We started off by importing the necessary libraries and declaring some variables and a dataframe to be used throughout the program. We then downloaded our data using the Yahoo Finance API.
`data = yf.download("SPY", start="1900-01-01", end="2021-05-01", interval = "1mo")`
  
After that we looped through our data. We started off by calculating the 200 day SMA (code below). In order to do this we added the close price to a list, and when that list reached 200 values we took the average. This average was updated each loop through by removing the first value from the list, appending the most recent value, and taking the average again.
```
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

```
Then we checked to see if the Close price was above the current value of the SMA. If it was, and the length of time it had been above was 0 (meaning it just went above this loop), we stored the starting date and starting price. Otherwise, we simply added 1 to our variable "above_len," which kept track of how many days the Close was above the SMA for.
```
# If the Low is above the sma
        if float(data["Close"][i]) > float(sma) and str(data.index[i]) != "2021-07-15 00:00:00":

            # Store the starting price if this is the first time it has gone above
            if above_len == 0:
                start_price = data["Close"][i]
                start_date = str(data.index[i].date())

            # Add to the length of time it has spent above the sma
            above_len += 1
```
Following this, we checked to see if the Close had dipped below the SMA when the above_len still had a value. This indiciated that the price had gone from above to below in the most recent loop. If this occurred, we calculated the percent change during the time period that the Close was above the SMA. Note, the date in the else if statement is there to make sure that the program detects our current period of being above the SMA, as it has not yet dipped back below. 
```
# If it dips below the sma and it was just above
        elif (data["Close"][i] < sma and above_len > 0) or str(data.index[i]) == "2021-07-15 00:00:00":
            # Calculate the % change
            pct_change = ((data["Close"][i] - start_price) / start_price) * 100
            # If this is the first time this duration has occurred
```
After finding the percent change, we needed to add our values to the dataframe. We checked to see if the duration had occurred before. If it hadn't we added it to the dataframe as a new row. If it had, we found the index where it occurred before, then added 1 to the occurrences tab, recalculated the average, and added another date to our date column.
```
if above_len not in df["Duration"]:
                # Add all attributes to the dataframe
                df = df.append({"Duration" : above_len, "% Change" : pct_change, "Occurrences" : 1, "Date Range": (start_date + " to " +                 str(data.index[i].date()))}, ignore_index = True)

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
```
Finally, we saved the dataframe to an excel file so we could export it.
  



