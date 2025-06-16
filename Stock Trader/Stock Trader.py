import requests
import json
import os

# run mean reversion strategy and output buys/sells, final profit, and final percentage returns
def meanReversionStrategy(prices):
  #print title
  print(ticker + " Mean Reversion Strategy Output:")
  total_profit = 0
  buy = 0
  first_time = True
  for i in range(5, len(prices)):
      avg = (prices[i - 1] + prices[i - 2] + prices[i - 3] + prices[i - 4] + prices[i - 5])/5 #rolling avg price of 5 days
      price = prices[i]
      if price < avg * .98 and buy == 0:
        #buy
        buy = price
        # print("buying at:\t", price)
        if first_time: #save first time buy price
          first_buy = price
          first_time = False
        if i == len(prices)-1:
          print("You should buy", ticker, "today according to Mean Reversion Strategy!")
      elif price > avg * 1.02 and buy != 0: #sell
        # print("selling at:\t", price)
        profit = round(price - buy, 2) #sell - buy
        buy = 0
        if i == len(prices)-1:
          print("You should sell", ticker, "today according to Mean Reversion Strategy!")
        # print("trade profit:\t", profit)
        #keep a running total of all profit
        total_profit += profit
      else: #do nothing if not buying or selling
        pass
  final_profit_percentage_return = str(round((total_profit/first_buy) * 100, 2))

  #Print out results
  print("-----------------------")
  print("Total profit:\t", round((total_profit), 2))
  print("First buy:\t", round(first_buy, 2))
  print("% return:\t", str(final_profit_percentage_return) + "%\n") 
  #    return profit and returns
  return total_profit, final_profit_percentage_return

# run SMA strategy and output buys/sells, final profit, and final percentage returns
def simpleMovingAverageStrategy(prices):
  #print title
  print(ticker + " Simple Moving Average Strategy Output:")
  total_profit = 0
  buy = 0
  first_time = True
  for i in range(5, len(prices)):
    avg = (prices[i - 1] + prices[i - 2] + prices[i - 3] + prices[i - 4] + prices[i - 5])/5 #rolling avg price of 5 days
    price = prices[i]
    if price > avg and buy == 0: #buy
      buy = price
      # print("buying at:\t", price)
      if first_time: #save first time buy price
        first_buy = price
        first_time = False
      if i == len(prices)-1:
        print("You should buy", ticker, "today according to Simple Moving Average Strategy!")
    elif price < avg and buy != 0: #sell
      # print("selling at:\t", price)
      profit = round(price - buy, 2) #sell - buy
      buy = 0
      if i == len(prices)-1:
        print("You should sell", ticker, "today according to Simple Moving Average Strategy!")
      # print("trade profit:\t", profit)
      #keep a running total of all profit
      total_profit += profit
    else: #do nothing if not buying or selling
      pass
  final_profit_percentage_return = str(round((total_profit/first_buy) * 100, 2))
  #Print out results
  print("-----------------------")
  print("Total profit:\t", round((total_profit), 2))
  print("First buy:\t", round(first_buy, 2))
  print("% return:\t", str(final_profit_percentage_return) + "%\n") 
  #return profit and returns
  return total_profit, final_profit_percentage_return

# run bollinger bands strategy and output buys/sells, final profit, and final percentage returns
def bollingerBands(prices):
  #print title
  print(ticker + " Bollinger Bands Strategy Output:")
  total_profit = 0
  buy = 0
  first_time = True
  for i in range(5, len(prices)):
    avg = (prices[i - 1] + prices[i - 2] + prices[i - 3] + prices[i - 4] + prices[i - 5])/5 #rolling avg price of 5 days
    price = prices[i]
    if price > avg * 1.05 and buy == 0:
      #buy
      buy = price
      # print("buying at:\t", price)
      if first_time: #save first time buy price
        first_buy = price
        first_time = False
      if i == len(prices)-1:
        print("You should buy", ticker, "today according to the Bollinger Bands Strategy!")
    elif price < avg * .95 and buy != 0: #sell
      # print("selling at:\t", price)
      profit = round(price - buy, 2) #sell - buy
      buy = 0
      if i == len(prices)-1:
        print("You should sell", ticker, "today according to the Bollinger Bands Strategy!")
      # print("trade profit:\t", profit)
      #keep a running total of all profit
      total_profit += profit
    else: #do nothing if not buying or selling
      pass
  final_profit_percentage_return = str(round((total_profit/first_buy) * 100, 2))
  #Print out results
  print("-----------------------")
  print("Total profit:\t", round((total_profit), 2))
  print("First buy:\t", round(first_buy, 2))
  print("% return:\t", str(final_profit_percentage_return) + "%\n") 
  #    return profit and returns
  return total_profit, final_profit_percentage_return

# define function saveResults
def saveResults(results):
  json.dump(results, open("Stock Trader/results.json", "w"))

#Initial API Pull
def initialDataPull(ticker):
  url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ticker+"&outputsize=full&apikey=NG9C9EPVYBMQT0C8"
  #making api call for stocks
  request = requests.get(url)
  request_dictionary = json.loads(request.text)
  #keys
  time_series_key = "Time Series (Daily)"
  close_key = "4. close"
  lines = []
  #date append
  for date in request_dictionary[time_series_key].keys():
    lines.append(date + "," + request_dictionary[time_series_key][date][close_key] + "\n")
  
  #reverse close prices so the strategies aren't backwards
  lines = lines[::-1]

  with open("Stock Trader/"+ticker+".csv", "w") as file:
    file.writelines(lines)

##open csv files and load in the new prices
def appendData(ticker):
  url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ticker+"&outputsize=full&apikey=NG9C9EPVYBMQT0C8"
  #api call for stocks
  request = requests.get(url)
  request_dictionary = json.loads(request.text)
  #keys
  time_series_key = "Time Series (Daily)"
  close_key = "4. close"

  #open csv file and convert it to a list and get the last date
  stock_csv = open("Stock Trader/"+ticker+".csv", "r")
  lines = stock_csv.readlines()
  last_date = lines[-1].split(",")[0]
  
  #empty list of lines to be appened
  new_lines = []
  for date in request_dictionary[time_series_key].keys():
    if date == last_date: #stop appending if up to date
      break
    else:
      new_lines.append(date + "," + request_dictionary[time_series_key][date][close_key] + "\n")

  #reverse new lines to oldest -> newest 
  new_lines = new_lines[::-1]
    
  #append to csv
  stock_csv = open("Stock Trader/"+ticker+".csv", "a")
  stock_csv.writelines(new_lines)
  stock_csv.close()

# dictionary called results to store prices, profits and return percentages
results = {}
#dictionary called analysis to store performance analysis
analysis = {}

#variables for stock analysis
highest_profit = 0
best_strategy = ""
best_ticker = ""

# list to store 10 tickers
tickers = ["AAPL", "ADBE", "GOOG", "AMZN", "BA", "CSCO", "CVX", "META", "MSFT", "TSLA"]

# loop through the list of tickers
for ticker in tickers:
  if os.path.exists("Stock Trader/"+ticker+".csv"):
    appendData(ticker)
  else:
    initialDataPull(ticker)
  #set prices
  prices = [float(line.strip().split(",")[1])for line in (open("Stock Trader/"+ticker+".csv").readlines())]
# load prices from a file <ticker>.txt, and store them in the results dictionary with the key “<ticker>_prices”
  results[ticker+"_prices"] = prices

# call simpleMovingAverageStrategy(prices) and store the profit and returns in the results dictionary with the keys “<ticker>_sma_profit” and “<ticker>_sma_profit”
  sma_profit, sma_returns = simpleMovingAverageStrategy(prices)
  results[(ticker+"_sma_profit")] = sma_profit
  results[(ticker+"_sma_returns")] = sma_returns
# call meanReversionStrategy(prices) and store the profit and returns in the results dictionary with the keys “<ticker>_mr_profit” and “<ticker>_mr_returns”
  mr_profit, mr_returns = meanReversionStrategy(prices)
  results[(ticker+"_mr_profit")] = mr_profit
  results[(ticker+"_mr_returns")] = mr_returns
# call bollingerBands(prices) and store the profit and returns in the results dictionary with the keys “<ticker>_bb_profit” and “<ticker>_bb_returns”
  bb_profit, bb_returns = bollingerBands(prices)
  results[(ticker+"_bb_profit")] = bb_profit
  results[(ticker+"_bb_returns")] = bb_returns

  #stock analysis
  if sma_profit > highest_profit:
    highest_profit = sma_profit
    best_strategy = "Simple Moving Average"
    best_ticker = ticker
  elif mr_profit > highest_profit:
    highest_profit = mr_profit
    best_strategy = "Mean Reversion"
    best_ticker = ticker
  elif bb_profit > highest_profit:
    highest_profit = bb_profit
    best_strategy = "Bollinger Bands"
    best_ticker = ticker

#store analyis in analysis dictionary
analysis["Highest Profit"] = highest_profit
analysis["Best Strategy"] = best_strategy
analysis["Best Stock Ticker"] = best_ticker
#print the dictionary
for key in analysis.keys():
  print(key + ": " + str(analysis[key]))

saveResults(results) # do this last and outside of for loop - save the results dictionary to a file called results.json