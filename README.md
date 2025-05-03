# Mean-Variance Portfolio Optimization in Python

This Python project implements **Mean-Variance Portfolio Optimization**, a foundational concept from Modern Portfolio Theory (MPT). The script estimates optimal asset allocations based on historical price data, targeting a specified return or minimizing risk. It includes visualization of the **Efficient Frontier**, **Minimum Variance Portfolio (MVP)**, and an **interactive Graph** for better insight.

The project is adapted from [Quantified Strategies](https://www.quantifiedstrategies.com/mean-variance-portfolio-in-python/) and modified with additional functionality.

---

## How to Run the Script

### 1. Install Required Libraries

```bash
pip install pandas numpy matplotlib yfinance scipy plotly
```

#### Step 2: Set Your Ticker Symbols

Modify the list of stock symbols under symbol_list

```python
symbol_list = ["Stock 1", "Stock 2", ...]
```

### Step 3: Set Your Date Range

Edit the start_date and end_date as needed. The default is a 1-year interval:

```python
start_date = "2024-02-01"
end_date = "2025-02-01"
```

### Step 4: Set Target Expected Return

Scroll down to this line and adjust the return (annualized, between 0 and 1):

```python
target_return_p = 0.13  # Example: 13% annual return target
```


# Output

The script will:

- Download adjusted closing price data using Yahoo Finance.
- Generate and simulate 10,000 random portfolios.
- Find the optimal allocation for a target return.
- Compute the Minimum Variance Portfolio.

Display:
- Portfolio allocations
- Risk and return statistics
- Plots of the Efficient Frontier (static and interactive)

Graphs:
- Stock prizes
- Normalized Stock Prizes
- Portfolio Return Equal weighted Portfolio vs. Mean Variance Portfolio with target return
- Efficient Frontier
- Interactive Garph/Efficient Frontier