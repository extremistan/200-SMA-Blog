# 200-SMA-Blog

# May Effect Blog 

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
Following this, we checked to see if the date 
```
# For each row in the data sheet, get the necessary data and calculate the percent change
for i in range(len(data["Unnamed: 0"])):
    if str(data["Unnamed: 0"][i])[1].isnumeric():

        # Note, the years in the line below will be changed for each run through to keep the proper time frame
        if float(str(data["Unnamed: 0"][i])) > 2009 and float(str(data["Unnamed: 0"][i])) < 2022:

            # Store the current date
            if len(str(data["Unnamed: 0"][i])) == 7 and str(data["Unnamed: 0"][i])[1].isnumeric():
                cur_date = str(data["Unnamed: 0"][i])[5] + str(data["Unnamed: 0"][i])[6]

            # The number 10 was corrupted on the date sheet, so here is our accounting for that
            elif len(str(data["Unnamed: 0"][i])) == 6 and str(data["Unnamed: 0"][i])[1].isnumeric():
                cur_date = "10"
            else:
                cur_date = 0

            # Start on the first May of the data sheet so we have all complete time periods
            if cur_date == "05" and begin == False:
                begin = True

            # If it is May, begin time period
            if cur_date == "05" and data["Unnamed: 1"][1] is not None:
                start_price = data["Unnamed: 1"][i]

            # If it is October, finish time period at the end of the month
            if cur_date == "10" and data["Unnamed: 1"][1] is not None:
                may_october.append(((float(data["Unnamed: 1"][i]) - float(start_price)) / float(start_price)) * 100)

            # If it is the start of November, start next period
            if cur_date == "11" and data["Unnamed: 1"][1] is not None:
                start_price = data["Unnamed: 1"][i]

            # If it is the end of April, finish the time period
            if cur_date == "04" and data["Unnamed: 1"][1] is not None and begin == True:
                november_april.append(((float(data["Unnamed: 1"][i]) - float(start_price)) / float(start_price)) * 100)
```

After gathering all the percent changes for each period, the rest of the program is the same as the previous one. We removed any incomplete data, averaged the whole data set, and plotted it.

  



