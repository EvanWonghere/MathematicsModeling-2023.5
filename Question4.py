import numpy as np
import math
import matplotlib.pyplot as plt

historicalData = [92.9, 100.8, 102.3, 108.7, 115.2, 121.6, 128.1, 134.5, 132.65, 137.6]
years = len(historicalData)
Data0 = np.array(historicalData)

e = math.e


# 级比检验
def comparison_test():
    left_border = math.exp(float(-2) / (years + 1))
    right_border = math.exp(float(2) / (years + 2))
    for k in range(2, years):
        test_value = float(Data0[k - 1]) / Data0[k]
        if test_value < left_border or test_value > right_border:
            return False
    return True


def get_prefix_sum_sequence():
    history_data_prefix_sum = [sum(historicalData[0: i + 1]) for i in range(years)]
    return np.array(history_data_prefix_sum)


def get_y_and_b(data1):
    y = np.zeros([years - 1, 1])
    b = np.zeros([years - 1, 2])
    for i in range(0, years - 1):
        y[i][0] = historicalData[i + 1]
        b[i][0] = -0.5 * (data1[i] + data1[i + 1])
        b[i][1] = 1
    return y, b


def calc_a_and_u(y, b):
    _u = np.linalg.inv(b.T.dot(b)).dot(b.T).dot(y)
    return _u[0][0], _u[1][0]


def get_fitted_data1(_a, _u):
    fitted_data1 = np.zeros(years + 1)
    fitted_data1[0] = Data0[0]
    for i in range(1, years + 1):
        fitted_data1[i] = (Data0[0] - _u / _a) * math.exp(-_a * i) + _u / _a
    return fitted_data1


def get_diff_ave(fitted_data1):
    diff_ave = 0.0
    for i in range(0, years):
        diff_ave += (Data0[i] - fitted_data1[i])
    return diff_ave / years


def get_diff_variance(fitted_data1):
    diff_ave = get_diff_ave(fitted_data1)
    _diff_var = 0.0
    for i in range(0, years):
        _diff_var += (Data0[i] - fitted_data1[i] - diff_ave) ** 2
    return _diff_var / years


def get_histo_ave():
    return sum(Data0) / years


def get_histo_variance():
    histo_ave = get_histo_ave()
    _histo_var = 0.0
    for i in range(0, years):
        _histo_var += (Data0[i] - histo_ave) ** 2
    return _histo_var / years


def get_fitted_data0(fitted_data1):
    fitted_data0 = np.zeros(years + 1)
    fitted_data0[0] = fitted_data1[0]
    for i in range(1, years + 1):
        fitted_data0[i] = fitted_data1[i] - fitted_data1[i - 1]
    return fitted_data0


def test_model_accuracy(_histo_var, _diff_var):
    _c = _histo_var / _diff_var
    if _c < 0.35:
        print("High model accuracy!")
    elif _c < 0.5:
        print("Qualified model accuracy!")
    elif _c < 0.65:
        print("Basically qualified model accuracy!")
    else:
        print("Unqualified model accuracy!")
        return False
    return True


if __name__ == '__main__':
    if not comparison_test():
        print("Failed to pass comparison test!")
        exit(0)

    print("Passed comparison test!")

    Data1 = get_prefix_sum_sequence()
    Y, B = get_y_and_b(Data1)
    a, u = calc_a_and_u(Y, B)
    fittedData1 = get_fitted_data1(a, u)
    histo_var = get_histo_variance()
    diff_var = get_diff_variance(fittedData1)
    fittedData0 = get_fitted_data0(fittedData1)

    if not test_model_accuracy(histo_var, diff_var):
        print("Using Grey Prediction model is not suitable!")
        exit(0)

    print("Predict: " + str(fittedData0[-1]))

    plt.figure(figsize=(20, 12))
    x0_label = range(2013, 2024)
    x1_label = range(2013, 2023)
    plt.plot(x0_label, fittedData0, 's-', color='r', label="Fitted carbon emissions")
    plt.plot(x1_label, Data0, 's-', color='g', label="Historical carbon emissions")

    plt.title("Comparison of the data given by fitted model and historical data")
    plt.xticks(x0_label)
    plt.xlabel("Year")
    plt.ylabel("Carbon emissions")
    plt.legend(loc="best")

    plt.show()
