import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>

/* Main page spacing */
.block-container{
    padding-top:1.5rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#f8fafc;
    border-right:1px solid #e5e7eb;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label{
    color:#1f2937 !important;
}

/* -------- Navigation Buttons -------- */

div[role="radiogroup"]{
    gap:16px;          /* Space between buttons */
}

/* Individual navigation buttons */
div[role="radiogroup"] label{

    padding:18px 18px;     /* Button height */
    border-radius:12px;

    font-size:18px;        /* Text size */

    font-weight:600;

    border:1px solid #d1d5db;

    transition:0.2s;
}

/* Hover effect */
div[role="radiogroup"] label:hover{

    background:#eef4ff;

    border-color:#2563eb;

}

/* Selected button */
div[role="radiogroup"] label[data-selected="true"]{

    background:#dbeafe;

    border-color:#2563eb;

}

/* -------- Radio circle (arrow) -------- */

/* Increase radio circle size */
div[role="radiogroup"] input{

    transform:scale(1.6);

}

/* -------- Metric Cards -------- */

[data-testid="metric-container"]{

    border:1px solid #e5e7eb;

    border-radius:12px;

    padding:15px;

    box-shadow:0 2px 6px rgba(0,0,0,0.05);

}

/* -------- Captions -------- */

.stCaption{

    font-size:18px !important;

    color:#4b5563 !important;

}

/* -------- Subheaders -------- */

h3{

    font-size:28px;

}

/* -------- Titles -------- */

h1{

    font-size:42px;

}

</style>
""",unsafe_allow_html=True)


sales_df = pd.read_csv("train.csv")

sales_df["Order Date"] = pd.to_datetime(
    sales_df["Order Date"],
    dayfirst=True
)

weekly_sales = pd.read_csv(
    "weekly_sales.csv"
)

weekly_sales["Order Date"] = pd.to_datetime(
    weekly_sales["Order Date"],
    format="mixed",
    errors="coerce"
)

forecast_df = pd.read_csv("segment_forecast.csv")

comparison_df = pd.read_csv("model_comparison.csv")

anomaly_df = pd.read_csv("anomaly_report.csv")

def dashboard_header(title, subtitle):

    st.title(title)

    st.caption(subtitle)

    st.divider()


#st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "",
    [
        "Sales Overview",
        "Forecast Explorer",
        "Anomaly Report",
        "Product Demand Segments"
    ]
)

if page == "Sales Overview":

    dashboard_header(" Sales Overview Dashboard", "Comprehensive view of sales performance")

    # -------------------------
    # Total Sales by Year
    # -------------------------

    st.subheader("Total Sales by Year")

    yearly_sales = (
        sales_df
        .groupby(sales_df["Order Date"].dt.year)["Sales"]
        .sum()
        .reset_index()
    )

    yearly_sales.columns = [
        "Year",
        "Sales"
    ]


    fig1 = px.bar(
        yearly_sales,
        x="Year",
        y="Sales",
        title="Year-wise Sales"
    )

    fig1.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.02,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)

    st.plotly_chart(
        fig1,
        use_container_width=True
    )


    # -------------------------
    # Monthly Sales Trend
    # -------------------------

    st.subheader("Monthly Sales Trend")


    monthly_sales = (
        sales_df
        .groupby(
            sales_df["Order Date"]
            .dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )


    monthly_sales["Order Date"] = (
        monthly_sales["Order Date"]
        .astype(str)
    )


    fig2 = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    fig2.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.02,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


    # -------------------------
    # Region and Category Filter
    # -------------------------

    st.subheader("Sales by Region and Category")


    col1, col2 = st.columns(2)


    with col1:

        selected_region = st.multiselect(
            "Select Region",
            sales_df["Region"].unique(),
            default=sales_df["Region"].unique()
        )


    with col2:

        selected_category = st.multiselect(
            "Select Category",
            sales_df["Category"].unique(),
            default=sales_df["Category"].unique()
        )


    filtered_df = sales_df[
        (sales_df["Region"].isin(selected_region))
        &
        (sales_df["Category"].isin(selected_category))
    ]


    region_category_sales = (
        filtered_df
        .groupby(
            ["Region","Category"]
        )["Sales"]
        .sum()
        .reset_index()
    )


    fig3 = px.bar(
        region_category_sales,
        x="Region",
        y="Sales",
        color="Category",
        title="Sales by Region and Category"
    )

    fig3.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.02,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)
    st.plotly_chart(
        fig3,
        use_container_width=True
    )

elif page == "Forecast Explorer":

    dashboard_header(" Forecast Explorer", "Explore sales forecasts for different segments")

    # Convert date column
    forecast_df["ds"] = pd.to_datetime(
        forecast_df["ds"]
    )


    # Segment dropdown

    selected_segment = st.selectbox(
        "Select Category / Region",
        forecast_df["Segment"].unique()
    )


    # Forecast horizon slider

    months = st.slider(
        "Select Forecast Horizon (Months)",
        min_value=1,
        max_value=3,
        value=3
    )


    # Filter selected segment

    segment_data = forecast_df[
        forecast_df["Segment"] == selected_segment
    ].head(months)



    st.subheader(
        f"Forecast for {selected_segment}"
    )


    # Forecast chart

    fig = px.line(
        segment_data,
        x="ds",
        y="yhat",
        markers=True,
        title="3 Month Sales Forecast"
    )

    fig.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.02,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)
    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Forecast table

    st.subheader("Forecast Values")

    st.dataframe(
        segment_data
    )


    # Model metrics

    st.subheader("Model Performance")


    best_model = comparison_df.iloc[
        comparison_df["RMSE"].idxmin()
    ]


    col1, col2, col3 = st.columns(3)


    with col1:
        st.metric(
            "Best Model",
            best_model["Model"]
        )


    with col2:
        st.metric(
            "MAE",
            round(best_model["MAE"],2)
        )


    with col3:
        st.metric(
            "RMSE",
            round(best_model["RMSE"],2)
        )




    # -------------------------
    # Anomaly Count
    # -------------------------

elif page == "Anomaly Report":

    dashboard_header(" Sales Anomaly Report", "Identify and analyze sales anomalies")

    # Get anomalies
    anomaly_df = weekly_sales[
        weekly_sales["Isolation_Anomaly"] == "Anomaly"
    ].copy()


    # Summary
    st.subheader(" Anomaly Summary")

    st.metric(
        "Total anomalies detected",
        len(anomaly_df)
    )


    # Interactive chart
    st.subheader(" Detected Anomaly Chart")


    normal = weekly_sales[
        weekly_sales["Isolation_Anomaly"] == "Normal"
    ]

    anomaly = weekly_sales[
        weekly_sales["Isolation_Anomaly"] == "Anomaly"
    ]


    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            x=normal["Order Date"],
            y=normal["Sales"],
            mode="lines",
            name="Normal Sales"
        )
    )


    fig.add_trace(
        go.Scatter(
            x=anomaly["Order Date"],
            y=anomaly["Sales"],
            mode="markers",
            name="Anomaly",
            marker=dict(
                symbol="x",
                size=12
            )
        )
    )

    fig.update_layout(
    template="plotly_white",
    title="Weekly Sales Anomalies using Isolation Forest",
    title_x=0.02,
    xaxis_title="Date",
    yaxis_title="Sales",
    hovermode="x unified",
    height=500,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)
    

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # Details table
    st.subheader(" Anomaly Details")


    st.dataframe(
        anomaly_df[
            [
                "Order Date",
                "Sales",
                "Isolation_Anomaly"
            ]
        ],
        use_container_width=True
    )

elif page == "Product Demand Segments":

    dashboard_header(" Product Demand Segments", "Analyze product demand patterns and segments")

    cluster_df = pd.read_csv(
        "product_clusters.csv",
        index_col=0
    )


    st.subheader(" Cluster Summary")


    col1, col2, col3, col4 = st.columns(4)


    with col1:
        st.metric(
            "Total Products",
            len(cluster_df)
        )


    with col2:
        st.metric(
            "Total Clusters",
            cluster_df["Cluster"].nunique()
        )


    with col3:
        st.metric(
            "Highest Sales Product",
            cluster_df["Total_Sales"].idxmax()
        )


    with col4:
        st.metric(
            "Average Sales",
            round(cluster_df["Total_Sales"].mean(),2)
        )


    st.subheader(" Product Demand Clusters")


    fig = px.scatter(
        cluster_df,
        x="PCA1",
        y="PCA2",
        color="Cluster",
        hover_name=cluster_df.index,
        title="Product Demand Segmentation using K-Means"
    )

    fig.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.02,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.subheader(" Product Cluster Details")


    st.dataframe(
        cluster_df,
        use_container_width=True
    )