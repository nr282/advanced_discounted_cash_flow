"""
Module handles the Discounted Cash Flow on the basis of the Variational Framework.

This creates the Advanced Discounted Cash Flow.

"""

import pandas as pd
from pandas_add_on import solve_pandas_series, IntegralConstraint, IntegralConstraintElement
from variational_framework import VariationalFramework, correct_function
import scipy.integrate as integrate



def calculate_daily_cash_flow(data: pd.DataFrame):
    """
    Calculates the discounted cash flow (DCF) for the given dates and values.


    """

    data.set_index("Date", inplace=True)
    data.index = data.index.sort_values()
    freq = pd.infer_freq(data.index)
    assert(freq == "QS-OCT")
    data["start_time"] = data["Quarters"].apply(lambda x: x.start_time)
    begin_time = data["start_time"].min()
    data["end_time"] = data["Quarters"].apply(lambda x: x.end_time)
    end_time = data["end_time"].max()
    data["start_time_days"] = data["start_time"].apply(lambda x: (x - begin_time).days)
    data["end_time_days"] = data["end_time"].apply(lambda x: (x - begin_time).days + 1)
    global_begin_time = data["start_time_days"].min()
    global_end_time = data["end_time_days"].max()
    data.to_csv("data.csv")

    constraint_id = 1
    integral_constraints = []
    for index, row in data.iterrows():

        start_dt = row["start_time_days"]
        end_dt = row["end_time_days"]
        value = row["Value"]

        elem = IntegralConstraintElement(1, start_dt, end_dt, constraint_id)
        constraint = IntegralConstraint([elem], value, constraint_id)

        constraint_id += 1

        integral_constraints.append(constraint)


    framework = VariationalFramework(integral_constraints,
                                     number_of_functions=1,
                                     start_time = global_begin_time,
                                     end_time = global_end_time)


    res1, res2 = framework.solve()
    func = correct_function(res1.get(1))
    daily_values = pd.date_range(start=begin_time, end=end_time, freq="D")
    data = pd.DataFrame.from_dict({"Date": daily_values})
    data["Start_Date"] = data["Date"].apply(lambda x: (x - begin_time).days)
    data["End_Date"] = data["Start_Date"].apply(lambda x: x + 1)
    data["Value"] = data.apply(lambda  row: integrate.quad(func, row["Start_Date"], row["End_Date"])[0], axis=1)
    return data

