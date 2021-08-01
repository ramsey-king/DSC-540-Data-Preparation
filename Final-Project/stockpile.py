import yfinance as yf
# import seaborn as sns
import matplotlib.pyplot as plt

'''
Currently VOO profit loss is calculated.  Need to add AMZN, DIS, MAT for Milana. Also
need to combine all the P/L's together to make a final P/L to plot.

Also -- have repeated code so I need to make functions to take the information in to make
the code more concise.
'''

milana_2 = yf.download('AMZN DIS MAT', start="2019-02-25")
milana_dict_2 = {'AMZN': 0.00959, 'DIS': 0.13786, 'MAT': 1.11937}

voo = yf.download('VOO', start="2019-05-20")
voo_num_shares_at_purchase = 0.66717
voo['current_daily_val'] = voo_num_shares_at_purchase * voo['Close']


milana_2_df = milana_2[[('Close', 'AMZN'),('Close', 'DIS'),('Close', 'MAT')]]
milana_2_df['AMZN_daily_val'] = milana_dict_2['AMZN'] * milana_2[('Close', 'AMZN')]
milana_2_df['DIS_daily_val'] = milana_dict_2['DIS'] * milana_2[('Close', 'DIS')]
milana_2_df['MAT_daily_val'] = milana_dict_2['MAT'] * milana_2[('Close', 'MAT')]

milana_2_df['VOO_daily_val'] = voo['current_daily_val']


milana_2_df.loc['2019-02-25':'2019-05-19','VOO_initial_val'] = 0
milana_2_df.loc['2019-05-20':,'VOO_initial_val'] = voo_num_shares_at_purchase*260.82

milana_2_df['voo_p_l'] = milana_2_df['VOO_daily_val'].dropna()-milana_2_df['VOO_initial_val']


print(milana_2_df.head())
print(milana_2_df.tail())

sum_column_list = [milana_2_df['AMZN_daily_val'] + milana_2_df['DIS_daily_val'] +
                    milana_2_df['MAT_daily_val'], milana_2_df['VOO_daily_val']]
milana_2_df['total_daily_val'] = sum(sum_column_list)
# milana_2_df.loc['2019-05-20':,'total_daily_val'] = sum(sum_column_list)

# print(milana_2_df.loc['2020-12-18':,'total_daily_val'])

# sns.lineplot(data=milana_2_df, x=milana_2_df.index, y='voo_p_l')
# plt.show()




