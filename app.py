import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go

from src.anomaly_detection import detect_anomalies
from src.recommendations import generate_recommendation
from src.forecasting import forecast_metric
from src.sustainability_score import calculate_sustainability_score


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SustainAI | Facility Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.html(
    """
    <style>

    /* Main application background */
    .stApp {
        background-color: #f5f7fa;
    }

    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #0f766e, #16a085);
        padding: 28px 35px;
        border-radius: 18px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.10);
    }

    .main-header h1 {
        margin: 0;
        font-size: 38px;
        font-weight: 700;
    }

    .main-header p {
        margin-top: 8px;
        font-size: 17px;
        opacity: 0.92;
    }

    /* Section title */
    .section-title {
        font-size: 25px;
        font-weight: 700;
        color: #17324d;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        min-height: 125px;
    }

    .kpi-title {
        color: #64748b;
        font-size: 14px;
        font-weight: 600;
    }

    .kpi-value {
        color: #17324d;
        font-size: 28px;
        font-weight: 700;
        margin-top: 8px;
    }

    .kpi-description {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 5px;
    }

    /* Sustainability score card */
    .score-card {
        background: white;
        border-radius: 18px;
        padding: 25px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }

    .score-value {
        font-size: 48px;
        font-weight: 800;
        color: #0f766e;
        margin: 10px 0;
    }

    .score-label {
        color: #64748b;
        font-size: 14px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        padding: 30px 0 15px 0;
    }

    </style>
    """
)


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="main-header">

        <h1>🌱 SustainAI</h1>

        <p>
            Sustainable Facility & Estate Intelligence Dashboard
            | AI-Powered Monitoring • Risk Detection • Forecasting
        </p>

    </div>
    """
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_data
def load_data():
    try:
        connection = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            port=int(st.secrets["mysql"]["port"]),
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )

        query = "SELECT * FROM facility_data"

        data = pd.read_sql(query, connection)

        connection.close()

        return data

    except Exception as e:
        st.error(f"Unable to connect to the SustainAI MySQL database: {e}")
        return pd.DataFrame()


# ============================================================
# LOAD DATA
# ============================================================

try:

    df = load_data()

except Exception as e:

    st.error(
        "Unable to connect to the SustainAI MySQL database."
    )

    st.code(
        str(e)
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🌱 SustainAI")

st.sidebar.markdown(
    """
    **Facility Intelligence Platform**

    Monitor sustainability, detect abnormal
    facility behavior, identify risks and
    forecast future resource consumption.
    """
)

st.sidebar.divider()


facility_options = [
    "All Facilities"
] + sorted(
    df["facility_name"]
    .dropna()
    .unique()
    .tolist()
)


selected_facility = st.sidebar.selectbox(
    "🏥 Select Facility",
    facility_options
)


min_date = df["date"].min().date()
max_date = df["date"].max().date()


selected_dates = st.sidebar.date_input(
    "📅 Analysis Period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


st.sidebar.divider()


st.sidebar.info(
    "Prototype dashboard developed for the "
    "SustainAI sustainable facility intelligence "
    "hackathon project."
)


# ============================================================
# DATE FILTER
# ============================================================

if (
    isinstance(selected_dates, tuple)
    and len(selected_dates) == 2
):

    start_date = pd.to_datetime(
        selected_dates[0]
    )

    end_date = pd.to_datetime(
        selected_dates[1]
    )

else:

    start_date = pd.to_datetime(
        min_date
    )

    end_date = pd.to_datetime(
        max_date
    )


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    (df["date"] >= start_date)
    &
    (df["date"] <= end_date)
].copy()


if selected_facility != "All Facilities":

    filtered_df = filtered_df[
        filtered_df["facility_name"]
        == selected_facility
    ]


if filtered_df.empty:

    st.warning(
        "No data available for the selected filters."
    )

    st.stop()


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

st.html(
    """
    <div class="section-title">
        📊 Executive Overview
    </div>

    <div class="section-subtitle">
        Real-time sustainability and operational intelligence
        for the selected facility and analysis period.
    </div>
    """
)


# ============================================================
# SUSTAINABILITY SCORE
# ============================================================

sustainability_scores = (
    calculate_sustainability_score(
        filtered_df
    )
)

overall_score = (
    sustainability_scores["overall_score"]
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_electricity = (
    filtered_df["electricity_kwh"].sum()
)

total_water = (
    filtered_df["water_liters"].sum()
)

total_waste = (
    filtered_df["waste_kg"].sum()
)

average_aqi = (
    filtered_df["aqi"].mean()
)

average_occupancy = (
    filtered_df["occupancy_percent"].mean()
)

total_incidents = (
    filtered_df["maintenance_incidents"].sum()
    +
    filtered_df["safety_incidents"].sum()
)


# ============================================================
# EXECUTIVE KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = (
    st.columns(6)
)


with kpi1:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                🌱 Sustainability
            </div>

            <div class="kpi-value">
                {overall_score:.1f}/100
            </div>

            <div class="kpi-description">
                Overall facility score
            </div>

        </div>
        """
    )


with kpi2:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                ⚡ Electricity
            </div>

            <div class="kpi-value">
                {total_electricity:,.0f}
            </div>

            <div class="kpi-description">
                Total kWh
            </div>

        </div>
        """
    )


with kpi3:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                💧 Water
            </div>

            <div class="kpi-value">
                {total_water:,.0f}
            </div>

            <div class="kpi-description">
                Total liters
            </div>

        </div>
        """
    )


with kpi4:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                ♻️ Waste
            </div>

            <div class="kpi-value">
                {total_waste:,.0f}
            </div>

            <div class="kpi-description">
                Total kg
            </div>

        </div>
        """
    )


with kpi5:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                🌫️ AQI
            </div>

            <div class="kpi-value">
                {average_aqi:.1f}
            </div>

            <div class="kpi-description">
                Average air quality
            </div>

        </div>
        """
    )


with kpi6:

    st.html(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                🚨 Incidents
            </div>

            <div class="kpi-value">
                {int(total_incidents)}
            </div>

            <div class="kpi-description">
                Maintenance + safety
            </div>

        </div>
        """
    )


# ============================================================
# SUSTAINABILITY INTELLIGENCE
# ============================================================

st.html(
    """
    <div class="section-title">
        🌱 Sustainability Intelligence
    </div>
    """
)


score_col, component_col = st.columns(
    [1, 2]
)


# ============================================================
# OVERALL SCORE
# ============================================================

with score_col:

    st.html(
        f"""
        <div class="score-card">

            <div class="score-label">
                Overall Sustainability Score
            </div>

            <div class="score-value">
                {overall_score:.1f}
            </div>

            <div class="score-label">
                Out of 100
            </div>

        </div>
        """
    )


# ============================================================
# COMPONENT SCORE CHART
# ============================================================

with component_col:

    component_data = pd.DataFrame(
        {
            "Component": [
                "Energy",
                "Water",
                "Waste",
                "Air Quality",
                "Occupancy",
                "Incidents"
            ],

            "Score": [
                sustainability_scores[
                    "energy_score"
                ],

                sustainability_scores[
                    "water_score"
                ],

                sustainability_scores[
                    "waste_score"
                ],

                sustainability_scores[
                    "air_quality_score"
                ],

                sustainability_scores[
                    "occupancy_score"
                ],

                sustainability_scores[
                    "incident_score"
                ]
            ]
        }
    )


    fig_components = px.bar(
        component_data,
        x="Component",
        y="Score",
        range_y=[0, 100],
        title="Sustainability Component Performance",
        text_auto=".1f"
    )


    fig_components.update_layout(
        height=330,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )


    st.plotly_chart(
        fig_components,
        use_container_width=True
    )


# ============================================================
# AI RISK ENGINE
# ============================================================

st.html(
    """
    <div class="section-title">
        🤖 AI Risk & Priority Engine
    </div>

    <div class="section-subtitle">
        AI-assisted facility risk scoring using sustainability
        performance, environmental conditions, operational
        incidents and anomaly detection.
    </div>
    """
)


risk_results = []


for facility in sorted(
    df["facility_name"].unique()
):

    facility_df = df[
        df["facility_name"] == facility
    ].copy()


    scores = (
        calculate_sustainability_score(
            facility_df
        )
    )


    facility_score = (
        scores["overall_score"]
    )


    avg_aqi = (
        facility_df["aqi"].mean()
    )


    incidents = (
        facility_df[
            "maintenance_incidents"
        ].sum()
        +
        facility_df[
            "safety_incidents"
        ].sum()
    )


    anomaly_count = 0


    for metric in [
        "electricity_kwh",
        "water_liters",
        "waste_kg",
        "aqi"
    ]:

        try:

            anomaly_data = detect_anomalies(
                facility_df,
                metric
            )

            anomaly_count += (
                anomaly_data[
                    f"{metric}_anomaly"
                ] == -1
            ).sum()

        except Exception:

            pass


    # --------------------------------------------------------
    # RISK SCORE
    # --------------------------------------------------------

    risk_score = 0


    if facility_score < 50:

        risk_score += 40

    elif facility_score < 65:

        risk_score += 25

    elif facility_score < 80:

        risk_score += 10


    if avg_aqi > 300:

        risk_score += 30

    elif avg_aqi > 200:

        risk_score += 25

    elif avg_aqi > 150:

        risk_score += 20

    elif avg_aqi > 100:

        risk_score += 10


    if incidents >= 20:

        risk_score += 25

    elif incidents >= 10:

        risk_score += 20

    elif incidents >= 5:

        risk_score += 10


    if anomaly_count >= 20:

        risk_score += 25

    elif anomaly_count >= 10:

        risk_score += 20

    elif anomaly_count >= 5:

        risk_score += 10

    elif anomaly_count > 0:

        risk_score += 5


    risk_score = min(
        risk_score,
        100
    )


    # --------------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------------

    if risk_score >= 70:

        risk_level = "Critical"
        priority = "Immediate"

    elif risk_score >= 50:

        risk_level = "High"
        priority = "High"

    elif risk_score >= 30:

        risk_level = "Medium"
        priority = "Monitor"

    else:

        risk_level = "Low"
        priority = "Routine"


    # --------------------------------------------------------
    # PRIMARY ISSUE
    # --------------------------------------------------------

    if avg_aqi > 150:

        primary_issue = "Air Quality"

        recommendation = (
            generate_recommendation(
                "Air Quality",
                avg_aqi
            )
        )

    elif anomaly_count > 0:

        primary_issue = "Resource Anomaly"

        recommendation = (
            "Investigate abnormal electricity, "
            "water or waste consumption."
        )

    elif incidents >= 5:

        primary_issue = "Operational Incidents"

        recommendation = (
            "Review maintenance and safety incidents "
            "and implement preventive actions."
        )

    elif facility_score < 65:

        primary_issue = (
            "Sustainability Performance"
        )

        recommendation = (
            "Review energy, water and waste efficiency "
            "to improve overall sustainability."
        )

    else:

        primary_issue = "No Major Issue"

        recommendation = (
            "Continue monitoring facility performance."
        )


    risk_results.append(
        {
            "Facility": facility,
            "Sustainability Score": facility_score,
            "Risk Score": risk_score,
            "Risk Level": risk_level,
            "Priority": priority,
            "AQI": round(avg_aqi, 1),
            "Incidents": int(incidents),
            "Anomalies": int(anomaly_count),
            "Primary Issue": primary_issue,
            "Recommended Action": recommendation
        }
    )


risk_df = pd.DataFrame(
    risk_results
)


# ============================================================
# RISK KPI CARDS
# ============================================================

critical_count = (
    risk_df["Risk Level"]
    == "Critical"
).sum()


high_count = (
    risk_df["Risk Level"]
    == "High"
).sum()


medium_count = (
    risk_df["Risk Level"]
    == "Medium"
).sum()


low_count = (
    risk_df["Risk Level"]
    == "Low"
).sum()


r1, r2, r3, r4 = st.columns(4)


with r1:

    st.metric(
        "🔴 Critical Facilities",
        critical_count
    )


with r2:

    st.metric(
        "🟠 High Risk Facilities",
        high_count
    )


with r3:

    st.metric(
        "🟡 Medium Risk Facilities",
        medium_count
    )


with r4:

    st.metric(
        "🟢 Low Risk Facilities",
        low_count
    )


# ============================================================
# RISK ASSESSMENT TABLE
# ============================================================

st.subheader(
    "Facility Risk Assessment"
)


display_risk_df = risk_df[
    [
        "Facility",
        "Sustainability Score",
        "Risk Score",
        "Risk Level",
        "Priority",
        "AQI",
        "Incidents",
        "Anomalies",
        "Primary Issue"
    ]
].copy()


st.dataframe(
    display_risk_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# RISK SCORE CHART
# ============================================================

fig_risk = px.bar(
    risk_df.sort_values(
        "Risk Score",
        ascending=False
    ),
    x="Facility",
    y="Risk Score",
    color="Risk Level",
    range_y=[0, 100],
    title="AI Facility Risk Score"
)


fig_risk.update_layout(
    height=400
)


st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# ============================================================
# PRIORITY ACTION CENTER
# ============================================================

st.html(
    """
    <div class="section-title">
        🚨 Priority Action Center
    </div>
    """
)


priority_df = risk_df[
    risk_df["Priority"].isin(
        [
            "Immediate",
            "High",
            "Monitor"
        ]
    )
].sort_values(
    "Risk Score",
    ascending=False
)


if priority_df.empty:

    st.success(
        "No high-priority facility actions detected."
    )

else:

    for _, row in priority_df.iterrows():

        if row["Priority"] == "Immediate":

            st.error(
                f"🔴 {row['Facility']} — "
                f"Risk Score: {row['Risk Score']} | "
                f"{row['Recommended Action']}"
            )

        elif row["Priority"] == "High":

            st.warning(
                f"🟠 {row['Facility']} — "
                f"Risk Score: {row['Risk Score']} | "
                f"{row['Recommended Action']}"
            )

        else:

            st.info(
                f"🟡 {row['Facility']} — "
                f"Risk Score: {row['Risk Score']} | "
                f"{row['Recommended Action']}"
            )


# ============================================================
# FACILITY COMPARISON
# ============================================================

st.html(
    """
    <div class="section-title">
        🏥 Facility Sustainability Comparison
    </div>
    """
)


comparison_results = []


for facility in sorted(
    df["facility_name"].unique()
):

    facility_df = df[
        df["facility_name"] == facility
    ]


    scores = (
        calculate_sustainability_score(
            facility_df
        )
    )


    comparison_results.append(
        {
            "Facility": facility,
            "Overall Score": scores[
                "overall_score"
            ],
            "Energy": scores[
                "energy_score"
            ],
            "Water": scores[
                "water_score"
            ],
            "Waste": scores[
                "waste_score"
            ],
            "Air Quality": scores[
                "air_quality_score"
            ],
            "Occupancy": scores[
                "occupancy_score"
            ],
            "Incidents": scores[
                "incident_score"
            ]
        }
    )


comparison_df = pd.DataFrame(
    comparison_results
)


st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)


fig_comparison = px.bar(
    comparison_df.sort_values(
        "Overall Score",
        ascending=False
    ),
    x="Facility",
    y="Overall Score",
    title="Overall Sustainability Score by Facility",
    range_y=[0, 100],
    text_auto=".1f"
)


st.plotly_chart(
    fig_comparison,
    use_container_width=True
)


# ============================================================
# INDIA FACILITY MAP
# ============================================================

st.html(
    """
    <div class="section-title">
        🇮🇳 India Facility Intelligence Map
    </div>
    """
)


city_coordinates = {

    "Bhubaneswar": (
        20.2961,
        85.8245
    ),

    "Bengaluru": (
        12.9716,
        77.5946
    ),

    "Mumbai": (
        19.0760,
        72.8777
    ),

    "Delhi": (
        28.6139,
        77.2090
    ),

    "Hyderabad": (
        17.3850,
        78.4867
    ),

    "Chennai": (
        13.0827,
        80.2707
    ),

    "Kolkata": (
        22.5726,
        88.3639
    ),

    "Pune": (
        18.5204,
        73.8567
    ),

    "Ahmedabad": (
        23.0225,
        72.5714
    ),

    "Jaipur": (
        26.9124,
        75.7873
    )
}


map_data = comparison_df.copy()


map_data["Latitude"] = map_data[
    "Facility"
].map(
    lambda x: None
)


map_data["Longitude"] = None


for city, coordinates in city_coordinates.items():

    mask = map_data[
        "Facility"
    ].str.contains(
        city,
        case=False,
        na=False
    )

    map_data.loc[
        mask,
        "Latitude"
    ] = coordinates[0]

    map_data.loc[
        mask,
        "Longitude"
    ] = coordinates[1]


map_data = map_data.dropna(
    subset=[
        "Latitude",
        "Longitude"
    ]
)


if not map_data.empty:

    fig_map = px.scatter_geo(
        map_data,
        lat="Latitude",
        lon="Longitude",
        size="Overall Score",
        color="Overall Score",
        hover_name="Facility",
        hover_data={
            "Overall Score": True,
            "Latitude": False,
            "Longitude": False
        },
        scope="asia",
        projection="natural earth",
        title=(
            "Facility Sustainability Performance "
            "Across India"
        )
    )


    fig_map.update_geos(
        showcountries=True,
        countrycolor="lightgray"
    )


    fig_map.update_layout(
        height=550
    )


    st.plotly_chart(
        fig_map,
        use_container_width=True
    )

else:

    st.info(
        "Facility city coordinates are not available "
        "for the current facility names."
    )


# ============================================================
# RESOURCE CONSUMPTION ANALYSIS
# ============================================================

st.html(
    """
    <div class="section-title">
        📈 Resource Consumption Analysis
    </div>
    """
)


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "⚡ Electricity",
        "💧 Water",
        "♻️ Waste",
        "🌫️ Air Quality"
    ]
)


# ============================================================
# ELECTRICITY
# ============================================================

with tab1:

    fig_electricity = px.line(
        filtered_df,
        x="date",
        y="electricity_kwh",
        color=(
            "facility_name"
            if selected_facility
            == "All Facilities"
            else None
        ),
        title="Electricity Consumption"
    )


    st.plotly_chart(
        fig_electricity,
        use_container_width=True
    )


# ============================================================
# WATER
# ============================================================

with tab2:

    fig_water = px.line(
        filtered_df,
        x="date",
        y="water_liters",
        color=(
            "facility_name"
            if selected_facility
            == "All Facilities"
            else None
        ),
        title="Water Consumption"
    )


    st.plotly_chart(
        fig_water,
        use_container_width=True
    )


# ============================================================
# WASTE
# ============================================================

with tab3:

    fig_waste = px.line(
        filtered_df,
        x="date",
        y="waste_kg",
        color=(
            "facility_name"
            if selected_facility
            == "All Facilities"
            else None
        ),
        title="Waste Generation"
    )


    st.plotly_chart(
        fig_waste,
        use_container_width=True
    )


# ============================================================
# AIR QUALITY
# ============================================================

with tab4:

    fig_aqi = px.line(
        filtered_df,
        x="date",
        y="aqi",
        color=(
            "facility_name"
            if selected_facility
            == "All Facilities"
            else None
        ),
        title="Air Quality Index"
    )


    fig_aqi.add_hline(
        y=100,
        line_dash="dash",
        annotation_text="AQI 100"
    )


    st.plotly_chart(
        fig_aqi,
        use_container_width=True
    )


# ============================================================
# AI ANOMALY DETECTION
# ============================================================

st.html(
    """
    <div class="section-title">
        🔎 AI Anomaly Detection
    </div>
    """
)


anomaly_metric = st.selectbox(
    "Select metric for anomaly detection",
    [
        "electricity_kwh",
        "water_liters",
        "waste_kg",
        "aqi"
    ]
)


try:

    anomaly_result = detect_anomalies(
        filtered_df,
        anomaly_metric
    )


    anomaly_rows = anomaly_result[
        anomaly_result[
            f"{anomaly_metric}_anomaly"
        ] == -1
    ].copy()


    if anomaly_rows.empty:

        st.success(
            "No significant anomalies detected."
        )

    else:

        st.warning(
            f"{len(anomaly_rows)} "
            "potential anomalies detected."
        )


        anomaly_display = anomaly_rows[
            [
                "date",
                "facility_name",
                anomaly_metric,
                f"{anomaly_metric}_status"
            ]
        ]


        st.dataframe(
            anomaly_display,
            use_container_width=True,
            hide_index=True
        )


        recommendation_category = (
            "Electricity"
            if anomaly_metric
            == "electricity_kwh"
            else
            "Water"
            if anomaly_metric
            == "water_liters"
            else
            "Waste"
            if anomaly_metric
            == "waste_kg"
            else
            "Air Quality"
        )


        st.info(
            generate_recommendation(
                recommendation_category,
                0
            )
        )


except Exception as e:

    st.error(
        f"Unable to perform anomaly detection: {e}"
    )


# ============================================================
# FORECASTING
# ============================================================

st.html(
    """
    <div class="section-title">
        🔮 Predictive Resource Forecast
    </div>

    <div class="section-subtitle">
        Prophet-based forecasting helps facility managers
        anticipate future resource consumption.
    </div>
    """
)


forecast_metric_name = st.selectbox(
    "Select metric for 30-day forecast",
    [
        "Electricity",
        "Water",
        "Waste"
    ]
)


forecast_column_map = {

    "Electricity": "electricity_kwh",

    "Water": "water_liters",

    "Waste": "waste_kg"
}


if st.button(
    "🔮 Generate 30-Day Forecast",
    type="primary"
):

    selected_column = (
        forecast_column_map[
            forecast_metric_name
        ]
    )


    try:

        model, forecast = forecast_metric(
            filtered_df,
            "date",
            selected_column,
            periods=30
        )


        fig_forecast = go.Figure()


        # Historical values
        fig_forecast.add_trace(
            go.Scatter(
                x=filtered_df["date"],
                y=filtered_df[
                    selected_column
                ],
                mode="lines",
                name="Historical"
            )
        )


        # Future forecast
        future_forecast = forecast[
            forecast["ds"]
            > filtered_df["date"].max()
        ]


        fig_forecast.add_trace(
            go.Scatter(
                x=future_forecast["ds"],
                y=future_forecast["yhat"],
                mode="lines",
                name="Forecast"
            )
        )


        # Upper bound
        fig_forecast.add_trace(
            go.Scatter(
                x=future_forecast["ds"],
                y=future_forecast[
                    "yhat_upper"
                ],
                mode="lines",
                name="Upper Bound",
                line=dict(
                    dash="dot"
                )
            )
        )


        # Lower bound
        fig_forecast.add_trace(
            go.Scatter(
                x=future_forecast["ds"],
                y=future_forecast[
                    "yhat_lower"
                ],
                mode="lines",
                name="Lower Bound",
                line=dict(
                    dash="dot"
                )
            )
        )


        fig_forecast.update_layout(
            title=(
                f"{forecast_metric_name} "
                "— 30-Day Forecast"
            ),
            height=500
        )


        st.plotly_chart(
            fig_forecast,
            use_container_width=True
        )


        # ----------------------------------------------------
        # FORECAST KPIs
        # ----------------------------------------------------

        if not future_forecast.empty:

            forecast_avg = (
                future_forecast[
                    "yhat"
                ].mean()
            )


            forecast_max = (
                future_forecast[
                    "yhat"
                ].max()
            )


            forecast_min = (
                future_forecast[
                    "yhat"
                ].min()
            )


            f1, f2, f3 = st.columns(3)


            with f1:

                st.metric(
                    "Average Forecast",
                    f"{forecast_avg:,.1f}"
                )


            with f2:

                st.metric(
                    "Maximum Forecast",
                    f"{forecast_max:,.1f}"
                )


            with f3:

                st.metric(
                    "Minimum Forecast",
                    f"{forecast_min:,.1f}"
                )


            st.subheader(
                "Future Forecast Values"
            )


            future_table = (
                future_forecast[
                    [
                        "ds",
                        "yhat",
                        "yhat_lower",
                        "yhat_upper"
                    ]
                ]
                .rename(
                    columns={
                        "ds": "Date",
                        "yhat": "Forecast",
                        "yhat_lower": "Lower Bound",
                        "yhat_upper": "Upper Bound"
                    }
                )
            )


            st.dataframe(
                future_table,
                use_container_width=True,
                hide_index=True
            )


    except Exception as e:

        st.error(
            f"Forecast generation failed: {e}"
        )


# ============================================================
# RAW DATA
# ============================================================

with st.expander(
    "📋 View Raw Facility Data"
):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">

        🌱 <b>SustainAI</b> —
        AI-Powered Sustainable Facility Intelligence

        <br><br>

        Built for sustainable infrastructure,
        operational intelligence and data-driven
        decision making.

        <br><br>

        Prototype • Hackathon Edition

    </div>
    """
)
