import pandas as pd
import streamlit as st

def get_demo_data():
    data = {
        'Time created': [1, 1, 2, 3, 1],
        'Dev bought own token (SOL)': [0.5, 1.2, 0.8, 1.5, 0.2],
        'Dev sold %': [100, 50, 100, 90, 100],
        'ATH market cap': [50000000, 200000000, 300000000, 100000000, 45000000],
        'ROI': [10, 8, 5, 15, 20],
        'X\'s': [2, 5, 3, 7, 10],
    }
    return pd.DataFrame(data)

def add_trend_analysis(data):
    data['Short-Term Change'] = data['ATH market cap'].astype(float).pct_change()
    data['Trend Alignment'] = data['Short-Term Change'].apply(
        lambda x: "+" if x > 0.02 else "-" if x < -0.02 else "<" if x < 0 else ">"
    )
    return data

def apply_dynamic_filters(data):
    filters = []
    available_columns = list(data.columns)

    with st.form("filter_form"):
        st.write("Create Your Filters:")
        num_filters = st.number_input("Number of filters to add", min_value=1, max_value=10, step=1, value=1)
        for i in range(num_filters):
            col = st.selectbox(f"Select column for filter {i+1}", available_columns, key=f"col_{i}")
            condition = st.selectbox(
                f"Condition for filter {i+1}",
                ["==", "!=", "<", "<=", ">", ">="],
                key=f"cond_{i}"
            )
            value = st.text_input(f"Value for filter {i+1}", key=f"value_{i}")
            filters.append((col, condition, value))
        
        submit = st.form_submit_button("Apply Filters")

    if submit:
        filtered_data = data.copy()
        for col, condition, value in filters:
            try:
                if condition == "==":
                    filtered_data = filtered_data[filtered_data[col] == float(value)]
                elif condition == "!=":
                    filtered_data = filtered_data[filtered_data[col] != float(value)]
                elif condition == "<":
                    filtered_data = filtered_data[filtered_data[col] < float(value)]
                elif condition == "<=":
                    filtered_data = filtered_data[filtered_data[col] <= float(value)]
                elif condition == ">":
                    filtered_data = filtered_data[filtered_data[col] > float(value)]
                elif condition == ">=":
                    filtered_data = filtered_data[filtered_data[col] >= float(value)]
            except ValueError:
                st.error(f"Invalid value or condition for filter on column: {col}")
        
        return filtered_data
    return data

def ensure_blacklist_size(blacklist, data, min_size=100):
    if len(blacklist) < min_size:
        additional_data = data[(data['X\'s'].astype(float) < 10) | (data['ROI'].isnull())]
        additional_needed = min_size - len(blacklist)
        blacklist = pd.concat([blacklist, additional_data.head(additional_needed)])
    return blacklist

def filter_ui():
    st.title('Crypto Signal Pattern Recognition - Demo')
    data = get_demo_data()
    data = add_trend_analysis(data)
    st.write(f"Data loaded successfully with {len(data)} records.")

    st.subheader('Raw Data for Testing:')
    st.write(data)
    
    st.subheader('Dynamic Filtering:')
    filtered_data = apply_dynamic_filters(data)
    
    st.subheader("Blacklist Signals:")
    blacklist = filtered_data[(filtered_data['X\'s'].astype(float) < 10) | (filtered_data['ROI'].astype(float) < 10)]
    blacklist = ensure_blacklist_size(blacklist, data)
    st.write(f"Blacklist contains {len(blacklist)} signals:")
    st.write(blacklist)

    st.subheader("Trend Insights:")
    st.bar_chart(data['Short-Term Change'].astype(float))

    st.download_button(
        label="Download Filtered Data (CSV)",
        data=filtered_data.to_csv(index=False),
        file_name=f"filtered_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    st.download_button(
        label="Download Blacklist Data (CSV)",
        data=blacklist.to_csv(index=False),
        file_name=f"blacklist_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    filter_ui()
