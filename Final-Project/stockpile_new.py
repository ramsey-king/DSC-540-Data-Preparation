import yfinance as yf
import matplotlib.pyplot as plt

'''

'''

def make_stock_df(stocks, initial_costs, date_of_purchase):
    data = [yf.download(stocks[stock],start=date_of_purchase[stock]) for stock in range(len(stocks))]
    print(data)


if __name__ == '__main__':
    make_stock_df(['AMZN', 'DIS', 'MAT','VOO'], [15.66, 15.66, 15.66, 74.01], ['2019-02-25', '2019-02-25', '2019-02-25', '2019-05-20'])