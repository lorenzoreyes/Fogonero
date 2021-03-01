# Flying to Mars: Guessing Elon Musk Crypto Portfolio 
> Excel with all data to check

So, after Elon Musk & Dogecoin episode lately I wanted to build a crypto portfolio. Ok, ok, I know that according to academia fundamentals current crypto currencies cannot be defined under the standards of a proper currency due mainly to it risk and that it is not attached to the activity of any economy. But, I just want to build it and play the game, so that's why I made this. And also Benjamin Graham suggest that if you want to gamble, do it but limit your bet to the 10% value of your budget.

### Therefore, lets build a crypto portfolio, or as Musk desires, lets fly to Mars.

<img src="Flying.png?raw=true" width="70%" height="70%" alt="portfolio" title="portfolio">


First of all, we start by gathering the data, do proper backtest, statistics, and with that results apply different methods to optimize (sharpe ratio, sortino ratio, minimum variance, component value-at-risk...). Our goal basicly is to obtain a combination that enables us to have a lower volatility that if we just select any of the assets and put all eggs in one basket.

![Setting](Setting.png?raw=true "Initial Setting")

#  Performance && Statistics. Getting the safest portfolio

![BuynHold](BuynHold.png?raw=true "BuyAndHold")
![stats](Statistics.png?raw=true "Stats")


Trick question. What this graphic tell us? Under this approach we replicate what would had happened if we buy at the first day of the sample and hold it no matter what. This style of porfolio management is called Buy & Hold, mainly carried out by investors like Warren Buffet (although he looks for value and might hold a position for a period longer than just a year).

However, we are in crypto market, and even we got an optimized portfolio it is not desirable to just buy an asset and forget we own it, hoping to see we make a lot or lost it all. 
So we have to rebalance. But how can we do that? there two ways, the classic that will suggest that we have to update our portfolio weights in order to match initial weights, if you have a winner you have to cut the difference and if it is a looser you compensate the loss, reinvesting the difference. We will have our weights reset to our starting point, but I don't like that. 
Because, when we obtain an optimization the combination is a static recommendation, thats it, it is a photo of what will be the best with the old information. But the market is dynamic and needs to gather new events, we have to update our photo to end up with a sum of frames in motion, a movie (lets hope not directed by Tarantino).
As a result, we end up rebalancing our weights by each month. By using the method Component Value-At-Risk, we update the risk attribution of every crypto as a whole, and see how to minimize risk.

![January](January21.png?raw=true "January")


We will end up with a column ['liquidityToReinvest'] that relates to the amount of money we couldn't allocate by following the weights specified by the optimizer. This comes in handy when we have to rebalance, because will give us the flexibility to connect previous portfolio composition from the succesive month and so on to iterate, it helps to rebalance, reinvest our performance and pass from one composition to another. And also we want our weights to fluctuate, not to concentrate positions, to get ups and downs will
tell us the optimizer rebuilds the weights properly.

![Weights](CryptoWeigths.png?raw=true "Weights")

# Final.

This investment wall planned with 100 million dollars (or $$99.999.681,37 invested), or a penny in Elon Musk terms. It ended with $ $1.624.833.726,88 
column notionalToday of Febraury. The return was 16,24 times initial capital, hope it convinces you over Buy-and-Hold Strategy.


# WARNING WARNING WARNING
## HUGE DISCLAIMER

This analysis can be improved. I did not want to write a book, but we can add warnings to monitor our investment. Such as a relational simple-moving-average to
check if we are in a bullish trend or not. Try to add something and remake this by doing it your own, just copy-paste you will not have an idea of the process.
