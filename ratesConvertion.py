r = float(input("what is the rate to work with? ")) / 100.0

def rateScope(r):
    AnnualER = ((1.0 + r) ** 12.0) - 1.0
    MonthlyER = (1.0 * (( 1 + AnnualER / 12.0 ))) - 1.0
    DailyER = ((( 1.0 + (MonthlyER ** 1.0/30.0)) - 1.0 ))
    return AnnualER, MonthlyER, DailyER