# Flying to Mars: Guessing Elon Musk Crypto Portfolio 
> Excel with all data to check

So, after Elon Musk & Dogecoin episode lately I wanted to build a crypto portfolio. Ok, ok, I know that according to academia fundamentals current crypto currencies cannot be defined under the standards of a proper currency due mainly to it risk and that it is not attached to the activity of any economy. But, I just want to build it and play the game, so that's why I made this. And also Benjamin Graham suggest that if you want to gamble, do it but limit your bet to the 10% value of your budget.

# Therefore, lets build a crypto portfolio, or as Musk desires, let fly to Mars.

First of all, we start by gathering the data, do proper backtest, statistics, and with that results apply different methods to optimize (sharpe ratio, sortino ratio, minimum variance, component value-at-risk...). Our goal basicly is to obtain a combination that enables us to have a lower volatility that if we just select any of the assets and put all eggs in one basket.

# Screenshoot of portfolio to start with.

Now lets simulate what was the time series and how our portfolio did.
& how diversification helps us to eliminate market risk.

# Let see our Portfolio performance over the last year.

# Data Describe data + data['Portfolio']

Trick question. What this graphic tell us? Under this approach we replicate what would had happened if we buy at the first day of the sample and hold it no matter what. This style of porfolio management is called Buy & Hold, mainly carried out by investors like Warren Buffet (although he looks for value and might hold a position for a period longer than just a year).

However, we are in crypto market, and even we got an optimized portfolio it is not desirable to just buy an asset and forget we own it, hoping to see we make a lot or lost it all. 
So we have to rebalance. But how can we do that? there two ways, the classic that will suggest that we have to update our portfolio weights in order to match initial weights, if you have a winner you have to cut the difference and if it is a looser you compensate the loss, reinvesting the difference. We will have our weights reset to our starting point, but I don't like that. 
Because, when we obtain an optimization the combination is a static recommendation, thats it, it is a photo of what will be the best with the old information. But the market is dynamic and needs to gather new events, we have to update our photo to end up with a sum of frames in motion, a movie (lets hope not directed by Tarantino).
As a result, we end up rebalancing our weights by each month. By using the method Component Value-At-Risk, we update the risk attribution of every crypto as a whole, and see how to minimize risk.
We will end up with a column ['liquidityToReinvest'] that relates to the amount of money we couldn't allocate by following the weights specified by the optimizer. This comes in handy when we have to rebalance, because will give us the flexibility to connect previous portfolio composition from the succesive month and so on to iterate, it helps to rebalance and reinvest our performance.


# WARNING WARNING WARNING
## HUGE DISCLAIMER

This analysis can be improved. I did not want to write a book, but we can add warnings to monitor our investment. Such as a relational simple-moving-average to
check if we are in a bullish trend or not. Try to add something and remake this by doing it your own, just copy-paste you will not have an idea of the process.
