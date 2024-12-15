import pandas as pd

def get_static_data():
    data = {
        'Time created': [1, 2, 1, 3, 1],
        'Dev bought own token (SOL)': [0.5, 1.2, 0.8, 1.5, 0.2],
        'Dev sold %': [100, 50, 100, 90, 100],
        'ATH market cap': [50000000, 200000000, 300000000, 100000000, 45000000],
        'ROI': [10, 8, 5, 15, 20],
        'X\'s': [2, 5, 3, 7, 10],
    }
    return pd.DataFrame(data)
def apply_filters(data, filters):
    print("Applying Filters...")
    filtered_data = data.copy()
    for col, condition, value in filters:
        if condition == "==":
            filtered_data = filtered_data[filtered_data[col] == value]
        elif condition == "<=":
            filtered_data = filtered_data[filtered_data[col] <= value]
        elif condition == ">=":
            filtered_data = filtered_data[filtered_data[col] >= value]
    return filtered_data

def get_bad_signals(data):
    bad_signals = data[data["X's"] < 10]
    print("\nBad Signals (X's < 10):")
    print(bad_signals)
    return bad_signals

def generate_output(filtered_data, columns_to_include):
    print("\nFinal Filtered Data:")
    output_data = filtered_data[columns_to_include]
    print(output_data)
    return output_data
def column_statistics(data):
    print("\nColumn-Wise Statistics:")
    stats = data.describe()
    print(stats)
    return stats
def highlight_top_performers(data):
    print("\nTop Performers:")
    top_roi = data.loc[data['ROI'].idxmax()]
    top_xs = data.loc[data["X's"].idxmax()]
    print("Highest ROI Row:")
    print(top_roi)
    print("\nHighest X's Row:")
    print(top_xs)
    return top_roi, top_xs
def sort_data(data, column, ascending=True):
    print(f"\nData Sorted by '{column}' (Ascending={ascending}):")
    sorted_data = data.sort_values(by=column, ascending=ascending)
    print(sorted_data)
    return sorted_data

def validate_data(data):
    print("\nValidating Data for Missing or Inconsistent Values...")
    if data.isnull().values.any():
        print("Warning: Missing values detected!")
    else:
        print("No missing values found.")
    print("\nData Types:")
    print(data.dtypes)
    return data
def generate_summary(data):
    print("\nSummary Report:")
    summary = {
        "Total Rows": len(data),
        "Max ROI": data["ROI"].max(),
        "Max X's": data["X's"].max(),
        "Average ROI": data["ROI"].mean(),
        "Average X's": data["X's"].mean(),
    }
    for key, value in summary.items():
        print(f"{key}: {value}")
    return summary
def main():
    print("Testing Script with Static Data:")
    data = get_static_data()
    print("\nOriginal Data:")
    print(data)
    validate_data(data)

    column_statistics(data)
    filters = [
        ("Time created", ">=", 2),
        ("Dev sold %", "==", 100),
    ]
    filtered_data = apply_filters(data, filters)
    filtered_data = filtered_data[filtered_data["X's"] >= 10]
    get_bad_signals(data)
    highlight_top_performers(data)
    sorted_data = sort_data(filtered_data, "ROI", ascending=False)
    columns_to_include = ['Time created', 'ROI', "X's"]
    generate_output(sorted_data, columns_to_include)
    generate_summary(filtered_data)
if __name__ == "__main__":
    main()
