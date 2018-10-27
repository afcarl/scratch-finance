# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# %%
aapl  = pd.read_csv('data/AAPL_CLOSE', index_col='Date',parse_dates=True)
cisco = pd.read_csv('data/CISCO_CLOSE', index_col='Date',parse_dates=True)
ibm   = pd.read_csv('data/IBM_CLOSE', index_col='Date',parse_dates=True)
amzn  = pd.read_csv('data/AMZN_CLOSE', index_col='Date',parse_dates=True)

# %%
stocks = pd.concat([aapl, cisco, ibm, amzn], axis=1)
stocks.columns = ['AAPL', 'CISCO', 'IBM', 'AMZN']

log_ret = np.log(stocks/stocks.shift(1))
business_days = 252

# %%
# seed the Random
np.random.seed(101)
num_portfolios = 5000
all_weights = np.zeros((num_portfolios, len(stocks.columns)))
ret_arr = np.zeros(num_portfolios)
vol_arr = np.zeros(num_portfolios)
sharpe_arr = np.zeros(num_portfolios)

for idx in range(num_portfolios):
    # weights
    weights = np.array(np.random.random(4))
    weights = weights / np.sum(weights)

    # save the all_weights
    all_weights[idx,:] = weights

    # expected return and volatility
    ret_arr[idx] = np.sum(log_ret.mean() * weights * business_days)
    vol_arr[idx] = np.sqrt(np.dot(weights.T,np.dot(log_ret.cov()*business_days,weights)))

    # Sharpe Ratio
    sharpe_arr[idx] = ret_arr[idx] / vol_arr[idx]

# %%
print(sharpe_arr.max())
print(sharpe_arr.argmax())
print(all_weights[sharpe_arr.argmax(),:])

# %%
plt.figure(figsize=(12,8))
plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='plasma')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')

max_sr_ret = ret_arr[sharpe_arr.argmax()]
max_sr_vol = vol_arr[sharpe_arr.argmax()]
plt.scatter(max_sr_vol, max_sr_ret, c='red', s=100, edgecolor='black')

plt.savefig('sharpe.png')
plt.show()

# %%
def get_ret_vol_sr(w):
    ws = np.array(w)
    ret = np.sum(log_ret.mean() * ws) * business_days
    vol = np.sqrt(np.dot(ws.T,np.dot(log_ret.cov()*business_days, ws)))
    sr = ret/vol
    return np.array([ret,vol,sr])

def neg_sharpe(w):
    return get_ret_vol_sr(w)[2] * -1

def check_sum(w):
    # return 0 if the sum of the weights is 1
    return np.sum(w) - 1


# %%
constraints = ({'type': 'eq', 'fun': check_sum})
bounds = ((0,1),(0,1),(0,1),(0,1))
initial_guess = [0.25,0.25,0.25,0.25]
optimal_results = minimize(neg_sharpe, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)

def minimize_volatility(w):
    return get_ret_vol_sr(w)[1]
# %%
optimal_results.x
get_ret_vol_sr(optimal_results.x)

# %%
frontier_y = np.linspace(0, 0.3, 100)
frontier_volatility = []

for possible_return in frontier_y:
    cons = ({'type': 'eq', 'fun': check_sum},
            {'type': 'eq', 'fun': lambda w: get_ret_vol_sr(w)[0] - possible_return})
    result = minimize(minimize_volatility, initial_guess, method='SLSQP', bounds=bounds, constraints=cons)

    frontier_volatility.append(result['fun'])

# %%
plt.figure(figsize=(12,8))
plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='plasma')
plt.colorbar(label='Sharpe Ratio')
plt.xlabel('Volatility')
plt.ylabel('Return')

plt.plot(frontier_volatility, frontier_y, 'g--', lw=3)
plt.savefig('efficient-frontier.png')
plt.show()
