import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import sqlite3
from scipy import stats  

connection = sqlite3.connect('data_db.db')
c = connection.cursor()

plt.xkcd()

def animate(i):
    query = ('SELECT * FROM two_values')
    data = pd.read_sql_query(query, connection)
    x = data.Trial
    y = data.output  

    plt.clf()  

    # Chart 1: Histogram of means
    ax1 = plt.subplot2grid((2, 3), (0, 0))
    means = data.groupby('Trial')['output'].mean()
    plt.hist(means, bins=20, color='blue', alpha=0.7)
    plt.xlabel('Mean')
    plt.ylabel('Frequency')
    plt.title("Distribution of means")
    

    # Chart 2: QQ Plot
    ax2 = plt.subplot2grid((2, 3), (0, 1))
    stats.probplot(y, dist="norm", plot=plt)
    plt.title("QQ Plot")
    plt.tight_layout()
    

    # Chart 3: Shapiro-Wilk Test Results
    ax3 = plt.subplot2grid((2, 3), (1, 0))
    shapiro_results = stats.shapiro(y)
    textstr = '\n'.join((
        r'Shapiro-Wilk Test:',
        r'W-statistic: %.4f' % shapiro_results.statistic,
        r'Skewness: %.4f' % y.skew(),
        r'Kurtosis: %.4f' % y.kurtosis()))
    plt.text(0.5, 0.5, textstr, fontsize=10, ha='center')
    plt.axis('off')  # Turn off axis

    # Chart 4: P-values from Shapiro-Wilk Test
    ax4 = plt.subplot2grid((2, 3), (1, 1))
    shapiro_results = stats.shapiro(y)
    textstr = '\n'.join((
        r'Shapiro-Wilk Test:',
        r'p-value: %.4f' % shapiro_results.pvalue))
    plt.text(0.5, 0.5, textstr, fontsize=10, ha='center')
    plt.axis('off')

    # Chart 5: Original Distribution
    ax5 = plt.subplot2grid((2, 3), (0, 2), rowspan=2)
    plt.hist(y, bins=20, color='purple', alpha=0.7)
    plt.xlabel('Value')
    plt.title("Distribution of outputs")
    

ani = FuncAnimation(plt.gcf(), animate)


plt.show()
