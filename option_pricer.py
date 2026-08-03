"""
European Option Pricing Model


Pricing European Call Options using:

1. Black-Scholes Analytical Model
2. Monte Carlo Simulation
3. Geometric Brownian Motion
4. Delta and Vega Greeks
5. Monte Carlo Convergence Plot
6. Simulated Stock Price Paths

Libraries Used:
NumPy
SciPy
Matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
import time

from scipy.stats import norm

S0 = 100          # Initial stock price
K = 105           # Strike price
T = 1             # Time to maturity (years)
r = 0.05          # Risk-free rate
sigma = 0.20      # Volatility

NUM_SIMULATIONS = 100000
NUM_STEPS = 252

np.random.seed(42)

#Black-Scholes
def d1(S, K, T, r, sigma):
    return (
        np.log(S / K)
        + (r + 0.5 * sigma ** 2) * T
    ) / (sigma * np.sqrt(T))


def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)


def black_scholes_call(S, K, T, r, sigma):

    D1 = d1(S, K, T, r, sigma)
    D2 = d2(S, K, T, r, sigma)

    price = (
        S * norm.cdf(D1)
        - K * np.exp(-r * T) * norm.cdf(D2)
    )

    return price

# Greeks
def delta(S, K, T, r, sigma):
    return norm.cdf(d1(S, K, T, r, sigma))


def vega(S, K, T, r, sigma):
    return (
        S
        * norm.pdf(d1(S, K, T, r, sigma))
        * np.sqrt(T)
    )
#GBM
def simulate_stock_paths():

    dt = T / NUM_STEPS

    paths = np.zeros((NUM_STEPS + 1, 100))

    paths[0] = S0

    for i in range(1, NUM_STEPS + 1):

        z = np.random.standard_normal(100)

        paths[i] = (
            paths[i - 1]
            * np.exp(
                (r - 0.5 * sigma ** 2) * dt
                + sigma * np.sqrt(dt) * z
            )
        )

    return paths
#GBM Plots
def plot_paths(paths):

    plt.figure(figsize=(10,6))

    plt.plot(paths)

    plt.title("Geometric Brownian Motion Stock Price Paths")

    plt.xlabel("Trading Days")

    plt.ylabel("Stock Price")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig("stock_paths.png")

    plt.close()
    
#monte-carlo simulation
def monte_carlo_call(
    S,
    K,
    T,
    r,
    sigma,
    simulations=NUM_SIMULATIONS
):

    # random standard normal variables
    Z = np.random.standard_normal(simulations)

    # Simulate terminal stock prices
    ST = S * np.exp(
        (r - 0.5 * sigma**2) * T
        + sigma * np.sqrt(T) * Z
    )

    # Option payoff
    payoffs = np.maximum(ST - K, 0)

    # Discount back to present value
    discounted_payoffs = np.exp(-r * T) * payoffs

    # Monte Carlo estimate
    option_price = np.mean(discounted_payoffs)

    # 95% Confidence Interval
    std_error = np.std(discounted_payoffs, ddof=1) / np.sqrt(simulations)

    lower = option_price - 1.96 * std_error
    upper = option_price + 1.96 * std_error

    return option_price, (lower, upper), discounted_payoffs

#convergence study
def convergence_study():

    simulation_sizes = [
        100,
        500,
        1000,
        2500,
        5000,
        10000,
        25000,
        50000,
        100000
    ]

    prices = []

    for sims in simulation_sizes:

        price, _, _ = monte_carlo_call(
            S0,
            K,
            T,
            r,
            sigma,
            simulations=sims
        )

        prices.append(price)

    return simulation_sizes, prices

def plot_convergence(sizes, prices, bs_price):

    plt.figure(figsize=(10, 6))

    plt.plot(
        sizes,
        prices,
        marker="o",
        linewidth=2,
        label="Monte Carlo"
    )

    plt.axhline(
        y=bs_price,
        linestyle="--",
        label="Black-Scholes"
    )

    plt.xscale("log")

    plt.xlabel("Number of Simulations")

    plt.ylabel("Option Price")

    plt.title("Monte Carlo Convergence")

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.savefig("convergence.png")

    plt.close()

#histogram
def plot_payoff_distribution(payoffs):

    plt.figure(figsize=(10,6))

    plt.hist(
        payoffs,
        bins=50
    )

    plt.title("Distribution of Discounted Option Payoffs")

    plt.xlabel("Discounted Payoff")

    plt.ylabel("Frequency")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig("payoff_distribution.png")

    plt.close()

start_time = time.perf_counter()

def main():

    print("=" * 55)
    print("EUROPEAN CALL OPTION PRICER")
    print("=" * 55)

    print()

    print(f"Stock Price (S0):       {S0}")
    print(f"Strike Price (K):       {K}")
    print(f"Volatility:             {sigma * 100:.2f}%")
    print(f"Risk Free Rate:         {r * 100:.2f}%")
    print(f"Maturity:               {T} years")

    print("-" * 55)

    bs_price = black_scholes_call(
        S0,
        K,
        T,
        r,
        sigma
    )

    mc_price, confidence, payoffs = monte_carlo_call(
        S0,
        K,
        T,
        r,
        sigma,
        NUM_SIMULATIONS
    )


    error = abs(mc_price - bs_price)

    option_delta = delta(
        S0,
        K,
        T,
        r,
        sigma
    )

    option_vega = vega(
        S0,
        K,
        T,
        r,
        sigma
    )

    sizes, prices = convergence_study()

    plot_convergence(
        sizes,
        prices,
        bs_price
    )

    paths = simulate_stock_paths()

    plot_paths(paths)

    plot_payoff_distribution(payoffs)


    execution_time = time.perf_counter() - start_time

    print()

    print("RESULTS")

    print("-" * 55)

    print(
        f"Black-Scholes Price:    {bs_price:.4f}"
    )

    print(
        f"Monte Carlo Price:      {mc_price:.4f}"
    )

    print(
        f"Pricing Error:          {error:.4f}"
    )

    print()

    print(
        f"95% Confidence Interval:"
    )

    print(
        f"[{confidence[0]:.4f}, {confidence[1]:.4f}]"
    )

    print()

    print("GREEKS")

    print("-" * 55)

    print(
        f"Delta:                  {option_delta:.4f}"
    )

    print(
        f"Vega:                   {option_vega:.4f}"
    )

    print()

    print(
        f"Simulations:            {NUM_SIMULATIONS:,}"
    )

    print(
        f"Execution Time:         {execution_time:.4f} seconds"
    )

    print("=" * 55)

    print()

    print(
        "Graphs generated:"
    )

    print(
        "- stock_paths.png"
    )

    print(
        "- convergence.png"
    )

    print(
        "- payoff_distribution.png"
    )

if __name__ == "__main__":

    main()