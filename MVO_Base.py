"""
This script is adapted from:
Quantified Strategies. "Mean-Variance Portfolio in Python" (2022).
URL: https://www.quantifiedstrategies.com/mean-variance-portfolio-in-python/

Modifications made by Max H. for an academic project:
- Added computation and highlighting of the Minimum Variance Portfolio (MVP)
- Added interactive Plotly-based visualization of the Efficient Frontier
- Included additional outputs: allocations, expected return, volatility

Note: Some code adjustments and text formulations were created using ChatGPT (OpenAI, 2025) and revised by the author.
"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import scipy.optimize as sco
import plotly.express as px

"""
The code to download the data and get the closing prices from the previous securities
"""

# === Data Acquisition and Preprocessing ===

def run_analysis():

############################
    # Download data
    #=== Enter your stocks here ===
    symbol_list = ["AAPL", "PLTR", "KO", "TSLA", "V"]


    # Add start and end date
    start_date = "2024-02-01"
    end_date = "2025-02-01"

############################



    data = yf.download(symbol_list, start = start_date, end = end_date)
    data_close = data.loc[:, "Close"]
    names_stocks = data_close.columns.tolist()

    # Plot the historical prices
    nhprice = data_close / data_close.iloc[0, :] * 100
    nhprice.plot()
    data_close.plot()
    plt.title("Normalized Stock Prices 2024")
    plt.legend()
    plt.show()


    """
    Estimate the return and covariance.
    """
    data_ret = np.log(data_close).diff().dropna()
    data_return = data_ret * 252
    mean_returns = data_return.mean().values
    data_covariance = data_ret.cov() * 252

    """
    Generate 10,000 random portfolios
    """

    returns_list = []
    volatility_list = []

    for i in range(10000):
        # Generate random weights
        rweights = np.random.random(len(names_stocks))

        # normailzed weights to sum 1
        normalized_weights = rweights / np.sum(rweights)

        # Random Portfolio: Expected Return
        rpreturn = mean_returns.dot(normalized_weights)

        # Append results to returns_list
        returns_list.append(rpreturn)

        # Random Portfolio: Variance
        rpvariance = np.dot(np.dot(normalized_weights.T, data_covariance), normalized_weights)

        # Random Portfolio: Standard Deviation
        rpstd = np.sqrt(rpvariance)

        # Append results to volatility_list
        volatility_list.append(rpstd)

    """
    Portfolio Random weights: pandas data frame with Returns and Volatility
    """
    ptrw = pd.DataFrame({'Return': returns_list, 'Volatility': volatility_list}) * 100



    """
    Mean-Variance Optimization
    """

    # Returns
    def mean_portfolios(weights):
        mean_returns = args[0]
        portfolio_return = mean_returns.dot(weights)
        return portfolio_return

    # Volatilty
    def std_portfolio(weights, *args):
        cov_returns = args[1]
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_returns, weights)))
        return portfolio_volatility

    # Bounds
    lower_bound = 0
    upper_bound = 1
    bounds = tuple((lower_bound, upper_bound) for i in range(len(names_stocks)))

    # Initial weights
    initial_weights = np.ones(len(names_stocks))/len(names_stocks) # Equal weighted Portfolio

    # Args (mean vector, covariance vector)
    args = (data_return.mean(), data_return.cov())

    ############################ 
    # s=== Enter you target return here ===

    target_return_p = 0.13 # This is our target return per year.

    ############################

    constraints = ({'type': 'eq', 'fun': lambda x: mean_portfolios(x) - target_return_p},
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # Optimization results
    result_p = sco.minimize(std_portfolio, initial_weights, args=args, method= 'SLSQP', bounds=bounds,
                            constraints=constraints)
    weights_p = result_p.x
    # print(weights_p)


    # Give error if Optimization os not successfull/possible
    if result_p.success:
        print("Optimization succeeded.")
    else:
        print("Optimization failed:", result_p.message)

    optimal_portfolio = nhprice.dot(weights_p)

    equal_weighted = np.ones(len(names_stocks))/len(names_stocks)
    equal_weighted_portfolio = nhprice.dot(equal_weighted)

    # Calculate and print expected return and risk for equal-weighted portfolio
    equal_expected_return = mean_returns.dot(equal_weighted)
    equal_variance = np.dot(np.dot(equal_weighted.T, data_covariance), equal_weighted)
    equal_volatility = np.sqrt(equal_variance)

    print("\nEqual Weighted Portfolio:")
    print(f"  Expected Return: {equal_expected_return:.2%}")
    print(f"  Volatility (Risk): {equal_volatility:.2%}")

    # Calculate and print expected return and risk for optimized (target-return) portfolio
    optimized_expected_return = mean_returns.dot(weights_p)
    optimized_variance = np.dot(np.dot(weights_p.T, data_covariance), weights_p)
    optimized_volatility = np.sqrt(optimized_variance)

    print("\nOptimized Portfolio (Target Return):")
    print(f"  Expected Return: {optimized_expected_return:.2%}")
    print(f"  Volatility (Risk): {optimized_volatility:.2%}")

    plt.plot(equal_weighted_portfolio, label = "Equal Weighted Portfolio")
    plt.plot(optimal_portfolio, label = f"Mean Variance Portfolio. Target = {target_return_p * 100.}%")
    plt.xlabel('Time period')
    plt.ylabel('Portfolio return')
    plt.legend()
    plt.show()

    # Print the Target Return Portfolio
    if result_p.success:
        print("\nOptimized Portfolio Allocation (Target Return):")
    for stock, weight in zip(names_stocks, weights_p):
        print(f"{stock}: {weight * 100:.2f}%")

    '''
    Minimum Variance Portfolio
    '''
    mvp_constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    mvp_result = sco.minimize(std_portfolio, initial_weights, args=args,
                            method='SLSQP', bounds=bounds, constraints=mvp_constraints)

    mvp_weights = mvp_result.x

    print("Minimum Variance Portfolio Allocation: ")
    for stock, weight in zip(names_stocks, mvp_weights):
        print(f"{stock}: {weight * 100:.2f}%")

    mvp_return = mean_returns.dot(mvp_weights)
    mvp_variance = np.dot(np.dot(mvp_weights.T, data_covariance), mvp_weights)
    mvp_volatility = np.sqrt(mvp_variance)

    print(f"\nMinimum Variance Portfolio:")
    print(f"  Expected Return: {mvp_return:.2%}")
    print(f"  Volatility (Risk): {mvp_volatility:.2%}")



    '''
    Efficient Frontier Construction
    '''

    # List to get the Efficient Frontier returns and volatilities
    frontier_returns = []
    frontier_volatility = []

    frontier_weights = []

    # Make a loop to get the Efficient Frontier return and Volatility
    for ii in range(1, 150):
        # Target returns
        target_return = ii/50.
        # Constraints
        constraints = ({'type': 'eq', 'fun': lambda x, target=target_return: mean_portfolios(x) - target},
                        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        # Optimization results
        result = sco.minimize(std_portfolio, initial_weights, args=args, method='SLSQP', 
                            bounds=bounds, constraints=constraints)
        # Optimal weights
        optimal_weights = result.x
        frontier_weights.append(optimal_weights)
        # Efficient Frontier Portfolio: Expected Return
        efpreturn = mean_returns.dot(optimal_weights)
        # Append result to returns_frontier
        frontier_returns.append(efpreturn)
        # Efficient FrontierPortfolio: Variance
        efpvariance = np.dot(np.dot(optimal_weights.T, data_covariance), optimal_weights)
        # Efficient Frontie Portfolio: Standard Deviation
        efpstd = np.sqrt(efpvariance)
        # Append result to frontier_volatility
        frontier_volatility.append(efpstd)


    # Pandas Efficient Frontier: return and volatility
    ef_portfolio = pd.DataFrame({'Return': frontier_returns, 'Volatility': frontier_volatility})


    # Plot Efficient Frontier
    plt.plot(ef_portfolio.Volatility * 100., ef_portfolio.Return * 100, color = "red", 
            label = "Efficient Frontier")

    plt.scatter(mvp_volatility * 100, mvp_return * 100, color='blue', marker='*',
                s=200, label ='Minimum Variance Portfolio')
    plt.scatter(ptrw.Volatility, ptrw.Return, s = 8, alpha = 0.3)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.title("Efficient Frontier")
    plt.legend()
    plt.show()

    '''
    Interactive Plotting
    '''

    allocation_strings = [
    "<br>".join([f"{name}: {w*100:.1f}%" for name, w in zip(names_stocks, weights)])
    for weights in frontier_weights
    ]

    ef_df = pd.DataFrame({
    "Return": np.array(frontier_returns) * 100,
    "Volatility": np.array(frontier_volatility) * 100,
    "Allocation": allocation_strings
    })

    fig = px.scatter(
        ef_df,
        x="Volatility",
        y="Return",
        hover_data=["Allocation"],
        title="Efficient Frontier with Hover Info"
    )

    fig.show()

    return frontier_returns, frontier_volatility, frontier_weights, names_stocks

if __name__ == "__main__":
    frontier_returns, frontier_volatility, frontier_weights, names_stocks = run_analysis()