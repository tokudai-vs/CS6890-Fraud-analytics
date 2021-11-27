# import libraries
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


# Benford's Law percentages for leading digits 1-9
BENFORD = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]


# we create a function which output is the final counts, and the frequency of each count as a
# percentage, are returned as lists to use in subsequent functions.
def count_first_digit(df, data_str):  # TAKE AS AN ARGUMENT A STR-COLUMN NAME
    mask = df[data_str] > 1.0
    data = list(df[mask][data_str])
    for i in range(len(data)):
        while data[i] > 10:
            data[i] = data[i] / 10
    first_digits = [int(x) for x in sorted(data)]
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
    data_col = "Population"
    # print(data)

    total_count, data_count, data_percentage = count_first_digit(df, data_col)
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
