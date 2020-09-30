# AlgoTrading
Just a fun little stock market prediction side project.

**Basic Premise**

There is a lot of noise in the day to day price of a stock, and this tends to obscure notworthy movements that could be capitalized upon. This project is to create an algortihm that tries to spot real changes in "signals" in the market, buy stocks, and then sell them a short bit later. I'm willing to have a high number of False Negatives if it means a fewer number of False Positives, as False Positives are actively detrimental to the total portfolio.

**Goals**
 - Identify stocks that are about to make a large jump
 - Buy said stock as a fixed initial percent of the portfolio, then sell two business days later
 - Outperform VOOG ETF
 
 **Exploration**
 - How does a model trained over a large period of time compare to one regularly retrained on recent data
 - What features help identify signal from noise (assuming such classifications can be assigned to the trends)
 
 **Results**
 
 ![](/Images/TestPredictorPlot.png)
 
 Trained on data from Jan 2019- Jan 2020, then tested on data from Jan 2020 - Sept 2020
