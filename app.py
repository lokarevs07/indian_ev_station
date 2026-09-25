# ============================================================
# INDIAN EV CHARGING STATION DATA ANALYTICS DASHBOARD
# STREAMLIT PROJECT
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Indian EV Charging Station Dashboard",
    page_icon="🔋",
    layout="wide"
)


# ============================================================
# MAIN DATA FILE
# ============================================================

DATA_FILE = "EV_dashboard_data.csv"


if not os.path.exists(DATA_FILE):

    st.error(
        "EV_dashboard_data.csv was not found."
    )

    st.info(
        "Keep EV_dashboard_data.csv in the same folder as app.py."
    )

    st.stop()


# ============================================================
# LOAD DATA
# ============================================================

data = pd.read_csv(DATA_FILE)


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

data.columns = data.columns.str.strip()


# ============================================================
# CONVERT NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "Latitude",
    "Longitude",
    "Power (kW)"
]

for col in numeric_columns:

    if col in data.columns:

        data[col] = pd.to_numeric(
            data[col],
            errors="coerce"
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🔋 EV Dashboard")

st.sidebar.markdown(
    "### Navigation"
)


page = st.sidebar.radio(
    "Select Section",
    [
        "Dashboard",
        "EV Station Analysis",
        "Map",
        "ML Model",
        "Predictions",
        "Feature Importance",
        "Project Summary"
    ]
)


# ============================================================
# PAGE 1 — MAIN DASHBOARD
# ============================================================

if page == "Dashboard":

    st.title(
        "🔋 Indian EV Charging Station Dashboard"
    )

    st.markdown(
        """
        ### Electric Vehicle Charging Station Data Analytics

        This dashboard analyses EV charging stations in India
        using station location, operator, connector type,
        usage type and charging power data.
        """
    )

    st.divider()


    # ========================================================
    # KEY PERFORMANCE INDICATORS
    # ========================================================

    st.subheader(
        "📊 Key Performance Indicators"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "🚗 Total Stations",
            f"{len(data):,}"
        )


    with col2:

        st.metric(
            "📍 States",
            data["State"].nunique()
        )


    with col3:

        st.metric(
            "🏙️ Cities",
            data["City"].nunique()
        )


    with col4:

        st.metric(
            "🏢 Operators",
            data["Operator"].nunique()
        )


    st.divider()


    # ========================================================
    # SECOND KPI ROW
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        avg_power = data["Power (kW)"].mean()

        st.metric(
            "⚡ Average Power",
            f"{avg_power:.2f} kW"
        )


    with col2:

        min_power = data["Power (kW)"].min()

        st.metric(
            "⬇️ Minimum Power",
            f"{min_power:.2f} kW"
        )


    with col3:

        max_power = data["Power (kW)"].max()

        st.metric(
            "⬆️ Maximum Power",
            f"{max_power:.2f} kW"
        )


    with col4:

        connector_count = (
            data["Connector Type"].nunique()
        )

        st.metric(
            "🔌 Connector Types",
            connector_count
        )


    st.divider()


    # ========================================================
    # STATE + CONNECTOR CHARTS
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # STATE CHART
    # --------------------------------------------------------

    with col1:

        st.subheader(
            "📍 Stations by State"
        )


        state_counts = (
            data["State"]
            .value_counts()
            .head(10)
            .reset_index()
        )


        state_counts.columns = [
            "State",
            "Number of Stations"
        ]


        fig_state = px.bar(
            state_counts,
            x="State",
            y="Number of Stations",
            title="Top 10 States"
        )


        fig_state.update_layout(
            xaxis_tickangle=-45
        )


        st.plotly_chart(
            fig_state,
            use_container_width=True
        )


    # --------------------------------------------------------
    # CONNECTOR CHART
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "🔌 Connector Distribution"
        )


        connector_counts = (
            data["Connector Type"]
            .value_counts()
            .reset_index()
        )


        connector_counts.columns = [
            "Connector Type",
            "Number of Stations"
        ]


        fig_connector = px.pie(
            connector_counts,
            names="Connector Type",
            values="Number of Stations",
            hole=0.4,
            title="Connector Types"
        )


        st.plotly_chart(
            fig_connector,
            use_container_width=True
        )


    st.divider()


    # ========================================================
    # OPERATOR + POWER CHARTS
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # OPERATOR CHART
    # --------------------------------------------------------

    with col1:

        st.subheader(
            "🏢 Top Operators"
        )


        operator_counts = (
            data["Operator"]
            .value_counts()
            .head(10)
            .reset_index()
        )


        operator_counts.columns = [
            "Operator",
            "Number of Stations"
        ]


        fig_operator = px.bar(
            operator_counts,
            x="Operator",
            y="Number of Stations",
            title="Top 10 Operators"
        )


        fig_operator.update_layout(
            xaxis_tickangle=-45
        )


        st.plotly_chart(
            fig_operator,
            use_container_width=True
        )


    # --------------------------------------------------------
    # POWER CHART
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "⚡ Charging Power"
        )


        fig_power = px.histogram(
            data,
            x="Power (kW)",
            nbins=30,
            title="Charging Power Distribution"
        )


        st.plotly_chart(
            fig_power,
            use_container_width=True
        )


    st.divider()


    # ========================================================
    # DATA PREVIEW
    # ========================================================

    st.subheader(
        "📋 Dataset Preview"
    )


    st.dataframe(
        data.head(10),
        use_container_width=True
    )


# ============================================================
# PAGE 2 — EV STATION ANALYSIS
# ============================================================

elif page == "EV Station Analysis":

    st.title(
        "📊 EV Charging Station Analysis"
    )


    st.write(
        "Use the filters below to analyse specific "
        "states, connector types and operators."
    )


    st.divider()


    # ========================================================
    # FILTERS
    # ========================================================

    col1, col2, col3 = st.columns(3)


    # State filter

    with col1:

        states = sorted(
            data["State"]
            .dropna()
            .unique()
            .tolist()
        )


        selected_state = st.selectbox(
            "📍 Select State",
            ["All"] + states
        )


    # Connector filter

    with col2:

        connectors = sorted(
            data["Connector Type"]
            .dropna()
            .unique()
            .tolist()
        )


        selected_connector = st.selectbox(
            "🔌 Select Connector Type",
            ["All"] + connectors
        )


    # Operator filter

    with col3:

        operators = sorted(
            data["Operator"]
            .dropna()
            .unique()
            .tolist()
        )


        selected_operator = st.selectbox(
            "🏢 Select Operator",
            ["All"] + operators
        )


    # ========================================================
    # APPLY FILTERS
    # ========================================================

    filtered = data.copy()


    if selected_state != "All":

        filtered = filtered[
            filtered["State"] == selected_state
        ]


    if selected_connector != "All":

        filtered = filtered[
            filtered["Connector Type"]
            == selected_connector
        ]


    if selected_operator != "All":

        filtered = filtered[
            filtered["Operator"]
            == selected_operator
        ]


    st.divider()


    # ========================================================
    # FILTERED KPI
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Filtered Stations",
            len(filtered)
        )


    with col2:

        st.metric(
            "Cities",
            filtered["City"].nunique()
        )


    with col3:

        st.metric(
            "Operators",
            filtered["Operator"].nunique()
        )


    with col4:

        if len(filtered) > 0:

            st.metric(
                "Average Power",
                f"{filtered['Power (kW)'].mean():.2f} kW"
            )

        else:

            st.metric(
                "Average Power",
                "0 kW"
            )


    st.divider()


    # ========================================================
    # CITY ANALYSIS
    # ========================================================

    st.subheader(
        "🏙️ Top Cities"
    )


    if len(filtered) > 0:

        city_counts = (
            filtered["City"]
            .value_counts()
            .head(15)
            .reset_index()
        )


        city_counts.columns = [
            "City",
            "Number of Stations"
        ]


        fig_city = px.bar(
            city_counts,
            x="City",
            y="Number of Stations",
            title="Top 15 Cities"
        )


        fig_city.update_layout(
            xaxis_tickangle=-45
        )


        st.plotly_chart(
            fig_city,
            use_container_width=True
        )


    else:

        st.warning(
            "No data available for the selected filters."
        )


    # ========================================================
    # POWER DISTRIBUTION
    # ========================================================

    st.subheader(
        "⚡ Charging Power Distribution"
    )


    if len(filtered) > 0:

        fig_power_filtered = px.histogram(
            filtered,
            x="Power (kW)",
            nbins=30,
            title="Charging Power Distribution"
        )


        st.plotly_chart(
            fig_power_filtered,
            use_container_width=True
        )


    # ========================================================
    # FILTERED DATA TABLE
    # ========================================================

    st.subheader(
        "📋 Filtered Charging Station Data"
    )


    st.dataframe(
        filtered,
        use_container_width=True,
        height=400
    )


    # ========================================================
    # DOWNLOAD FILTERED DATA
    # ========================================================

    csv_data = filtered.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="⬇️ Download Filtered Dataset",
        data=csv_data,
        file_name="filtered_EV_stations.csv",
        mime="text/csv"
    )


# ============================================================
# PAGE 3 — MAP
# ============================================================

elif page == "Map":

    st.title(
        "🗺️ EV Charging Station Locations"
    )


    st.write(
        "Geographical distribution of EV charging "
        "stations in India."
    )


    map_data = data.dropna(
        subset=[
            "Latitude",
            "Longitude"
        ]
    )


    if len(map_data) > 0:

        fig_map = px.scatter_map(
            map_data,
            lat="Latitude",
            lon="Longitude",

            hover_name=(
                "Station Name"
                if "Station Name" in map_data.columns
                else None
            ),

            hover_data=[
                "City",
                "State",
                "Operator",
                "Connector Type",
                "Power (kW)"
            ],

            zoom=4,
            height=650
        )


        fig_map.update_layout(
            map_style="open-street-map"
        )


        st.plotly_chart(
            fig_map,
            use_container_width=True
        )


    else:

        st.warning(
            "Latitude and Longitude data are not available."
        )


    st.divider()


    # ========================================================
    # STATE AVERAGE POWER
    # ========================================================

    st.subheader(
        "⚡ Average Charging Power by State"
    )


    avg_power_state = (
        data.groupby("State")["Power (kW)"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )


    avg_power_state.columns = [
        "State",
        "Average Power (kW)"
    ]


    fig_avg = px.bar(
        avg_power_state,
        x="State",
        y="Average Power (kW)",
        title="Top 15 States by Average Charging Power"
    )


    fig_avg.update_layout(
        xaxis_tickangle=-45
    )


    st.plotly_chart(
        fig_avg,
        use_container_width=True
    )


# ============================================================
# PAGE 4 — MACHINE LEARNING MODEL
# ============================================================

elif page == "ML Model":

    st.title(
        "🤖 Machine Learning Model"
    )


    st.write(
        """
        A Random Forest Regression model was developed
        to predict EV charging station power (kW).
        """
    )


    st.divider()


    model_file = (
        "EV_charging_power_model.pkl"
    )


    prediction_file = (
        "EV_model_predictions.csv"
    )


    # ========================================================
    # MODEL STATUS
    # ========================================================

    if os.path.exists(model_file):

        st.success(
            "✅ Trained Random Forest model found."
        )

    else:

        st.warning(
            "⚠️ EV_charging_power_model.pkl not found."
        )


    # ========================================================
    # MODEL PERFORMANCE
    # ========================================================

    if os.path.exists(prediction_file):

        predictions = pd.read_csv(
            prediction_file
        )


        actual_col = (
            "Actual Power (kW)"
        )


        predicted_col = (
            "Predicted Power (kW)"
        )


        if (
            actual_col in predictions.columns
            and
            predicted_col in predictions.columns
        ):


            actual = predictions[
                actual_col
            ]


            predicted = predictions[
                predicted_col
            ]


            # MAE

            mae = np.mean(
                np.abs(
                    actual - predicted
                )
            )


            # RMSE

            rmse = np.sqrt(
                np.mean(
                    (actual - predicted) ** 2
                )
            )


            # R2

            ss_res = np.sum(
                (actual - predicted) ** 2
            )


            ss_tot = np.sum(
                (actual - actual.mean()) ** 2
            )


            if ss_tot != 0:

                r2 = (
                    1
                    -
                    (ss_res / ss_tot)
                )

            else:

                r2 = 0


            # =================================================
            # DISPLAY METRICS
            # =================================================

            st.subheader(
                "📊 Model Performance"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "MAE",
                    f"{mae:.2f}"
                )


            with col2:

                st.metric(
                    "RMSE",
                    f"{rmse:.2f}"
                )


            with col3:

                st.metric(
                    "R² Score",
                    f"{r2:.3f}"
                )


            st.divider()


            # =================================================
            # ACTUAL VS PREDICTED
            # =================================================

            st.subheader(
                "Actual vs Predicted Power"
            )


            fig_prediction = px.scatter(
                predictions,
                x=actual_col,
                y=predicted_col,
                title="Actual vs Predicted Charging Power"
            )


            st.plotly_chart(
                fig_prediction,
                use_container_width=True
            )


        else:

            st.warning(
                "Required prediction columns were not found."
            )


    else:

        st.warning(
            "EV_model_predictions.csv not found."
        )


# ============================================================
# PAGE 5 — PREDICTIONS
# ============================================================

elif page == "Predictions":

    st.title(
        "🔮 EV Charging Power Predictions"
    )


    prediction_file = (
        "EV_model_predictions.csv"
    )


    if os.path.exists(prediction_file):

        predictions = pd.read_csv(
            prediction_file
        )


        st.write(
            "Actual and predicted charging power:"
        )


        st.dataframe(
            predictions,
            use_container_width=True,
            height=500
        )


        st.divider()


        # ====================================================
        # DOWNLOAD PREDICTIONS
        # ====================================================

        csv = predictions.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            label="⬇️ Download Predictions",
            data=csv,
            file_name="EV_model_predictions.csv",
            mime="text/csv"
        )


    else:

        st.error(
            "EV_model_predictions.csv was not found."
        )


# ============================================================
# PAGE 6 — FEATURE IMPORTANCE
# ============================================================

elif page == "Feature Importance":

    st.title(
        "📈 Feature Importance"
    )


    st.write(
        """
        Feature importance shows which input features
        contributed to the Random Forest model.
        """
    )


    importance_file = (
        "EV_feature_importance.csv"
    )


    if os.path.exists(importance_file):

        importance = pd.read_csv(
            importance_file
        )


        importance = importance.sort_values(
            "Importance",
            ascending=False
        )


        st.subheader(
            "Top Important Features"
        )


        st.dataframe(
            importance.head(20),
            use_container_width=True
        )


        st.divider()


        # ====================================================
        # FEATURE IMPORTANCE CHART
        # ====================================================

        top_features = importance.head(15)


        fig_importance = px.bar(
            top_features,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Top 15 Important Features"
        )


        fig_importance.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            }
        )


        st.plotly_chart(
            fig_importance,
            use_container_width=True
        )


        # ====================================================
        # DOWNLOAD
        # ====================================================

        csv = importance.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            label="⬇️ Download Feature Importance",
            data=csv,
            file_name="EV_feature_importance.csv",
            mime="text/csv"
        )


    else:

        st.error(
            "EV_feature_importance.csv was not found."
        )


# ============================================================
# PAGE 7 — PROJECT SUMMARY
# ============================================================

elif page == "Project Summary":

    st.title(
        "📋 EV Project Summary"
    )


    st.write(
        """
        Summary of the Indian EV Charging Station
        Data Analytics Project.
        """
    )


    # ========================================================
    # SUMMARY FILE
    # ========================================================

    summary_file = (
        "EV_summary.csv"
    )


    if os.path.exists(summary_file):

        summary = pd.read_csv(
            summary_file
        )


        st.subheader(
            "📊 Project Summary"
        )


        st.dataframe(
            summary,
            use_container_width=True
        )


    else:

        st.warning(
            "EV_summary.csv was not found."
        )


    st.divider()


    # ========================================================
    # DATASET INFORMATION
    # ========================================================

    st.subheader(
        "📁 Dataset Information"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Rows",
            data.shape[0]
        )


    with col2:

        st.metric(
            "Columns",
            data.shape[1]
        )


    with col3:

        st.metric(
            "States",
            data["State"].nunique()
        )


    with col4:

        st.metric(
            "Cities",
            data["City"].nunique()
        )


    st.divider()


    # ========================================================
    # DATASET COLUMNS
    # ========================================================

    st.subheader(
        "📝 Dataset Columns"
    )


    column_info = pd.DataFrame({
        "Column Name": data.columns,
        "Data Type": [
            str(data[col].dtype)
            for col in data.columns
        ],
        "Unique Values": [
            data[col].nunique()
            for col in data.columns
        ]
    })


    st.dataframe(
        column_info,
        use_container_width=True
    )


    st.divider()


    # ========================================================
    # PROJECT OBJECTIVE
    # ========================================================

    st.subheader(
        "🎯 Project Objective"
    )


    st.write(
        """
        The objective of this project is to analyse
        Indian EV charging station data, understand
        charging infrastructure distribution, identify
        patterns in charging power and connector types,
        and apply machine learning for charging power
        prediction.
        """
    )


    # ========================================================
    # MAIN ANALYSIS AREAS
    # ========================================================

    st.subheader(
        "🔍 Main Analysis Areas"
    )


    analysis_points = [
        "EV charging station distribution by state",
        "EV charging station distribution by city",
        "Charging station operator analysis",
        "Connector type analysis",
        "Charging power analysis",
        "Geographical distribution of stations",
        "Machine learning based charging power prediction",
        "Feature importance analysis"
    ]


    for point in analysis_points:

        st.write(
            "• " + point
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "🔋 Indian EV Charging Station Data Analytics Project | "
    "Streamlit Dashboard"
)