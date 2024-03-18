# IV Phase Transition Indicator

This repository contains an indicator for detecting phase transitions in implied volatility (IV) premiums using the VIX index. The indicator is based on fitting the VIX data to a Student's t-distribution with 1 degree of freedom using a 30-day rolling window.

## Indicator Description

The indicator is calculated using the cumulative distribution function (CDF) of the Student's t-distribution with 1 degree of freedom:

```
Indicator = F_t(x; ν=1, μ, σ) = ∫_{-∞}^x \frac{\Gamma(\frac{\nu+1}{2})}{\sqrt{\nu\pi}\,\Gamma(\frac{\nu}{2})} \left(1+\frac{t^2}{\nu}\right)^{-\frac{\nu+1}{2}} \,dt
```

Where:
- `F_t` is the cumulative distribution function (CDF) of the Student's t-distribution, using the latest VIX Daily Close value
- `x` is the input value (30-day rolling average of VIX Daily Close value)
- `ν` is the degrees of freedom (set to 1)
- `μ` is the location parameter (estimated using `scipy.stats.t.fit`)
- `σ` is the scale parameter (estimated using `scipy.stats.t.fit`)
- `Γ` is the gamma function

## Data

The repository provides links to download the raw and smoothed indicator data in CSV format. The data is updated hourly via Github Actions.

## Code

The Python code for calculating and plotting the IV Phase Transition Indicator is included in the repository. The code uses the following libraries:
- pandas
- numpy
- matplotlib
- scipy
- yfinance

The main functionality is implemented in the `Data` class, which retrieves the historical VIX data, calculates the indicator, and generates the plots.

## Usage

To use the IV Phase Transition Indicator code:

1. Install the required dependencies: `pandas`, `numpy`, `matplotlib`, `scipy`, and `yfinance`.
2. Run the Python script to retrieve the VIX data, calculate the indicator, and generate the plots.
3. The generated plots will be saved in the `images` folder.

## References

- Taleb, N. N. (2020). *Statistical Consequences of Fat Tails*. STEM Academic Press.

## Author

- [Daniel Scott](https://github.com/nightvision04), March 2024
- [Buy me a coffee](https://www.buymeacoffee.com/danscottlearns)

Feel free to explore the website, download the data, and use the code to further analyze the IV Phase Transition Indicator.