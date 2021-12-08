###############################################################################################

# Implementation of First Digit Benford's algorithm
# Contributors:
# Vishal Singh Yadav: CS20MTECH01001
# Anilava Kundu: CS20MTECH01002
# Kuldeep Gautam: CS20MTECH01004

###############################################################################################

# import libraries
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


# Benford's Law percentages for leading digits 1-9
BENFORD = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]


# we create a function which output is the final counts, and the frequency of each count as a
# percentage, are returned as lists to use in subsequent functions.
def count_first_digit(data):
    digits = []
    for i in data:
        digits.append(str(i)[0])
    
    first_digits = [int(x) for x in sorted(digits)]
    unique = set(first_digits)  # a list with unique values of first_digit list
    data_count = []
    for i in unique:
        count = first_digits.count(i)
        data_count.append(count)
    total_count = sum(data_count)
    data_percentage = [(i / total_count) * 100 for i in data_count]

    return total_count, data_count, data_percentage


# Return list of expected Benford's Law counts for total sample count.
def get_expected_counts(total_count):

    return [round(p * total_count / 100) for p in BENFORD]


def chi_p(data_count, expected_counts):
    data = [data_count, expected_counts]
    stat, p, dof, expected = chi2_contingency(data)

    return p


def mad(data_count, expected_counts):
    diff = []
    for i in range(len(data_count)):
        diff.append(abs(data_count[i] - expected_counts[i]))

    return np.mean(diff)


if __name__ == "__main__":
    df = pd.read_csv("benford.csv", encoding="latin-1")
    data = df["Population"]
    # print(data)

    total_count, data_count, data_percentage = count_first_digit(data)
    expected_counts = get_expected_counts(total_count)

    print("\nobserved counts = {}".format(data_count))
    print("expected counts = {}".format(expected_counts), "\n")
    print("First Digit Probabilities:")
    for i in range(1, 10):
        print(
            "{}: observed: {:.3f}  expected: {:.3f}".format(
                i, data_percentage[i - 1] / 100, BENFORD[i - 1] / 100
            )
        )

    mad_value = mad(data_count, expected_counts)
    print("\nMean absolute deviation = {:.3f}".format(mad_value))

    p_value = chi_p(data_count, expected_counts)
    print("Chi-squared p value = {:.3f}".format(p_value))
