
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# PAGE CONFIGURATION

st.set_page_config(
    page_title="SmartTransit",
    page_icon="🚌",
    layout="wide"
)

# LOAD DATA

DATA_PATH = "."

@st.cache_data
def load_data():

    routes = pd.read_csv(
        os.path.join(DATA_PATH, "routes.csv")
    )

    stops = pd.read_csv(
        os.path.join(DATA_PATH, "stops.csv")
    )

    trips = pd.read_csv(
        os.path.join(DATA_PATH, "trips.csv")
    )

    return routes, stops, trips


routes, stops, trips = load_data()


# APPLICATION HEADER

st.title("🚌 SmartTransit")

st.subheader(
    "Chennai Public Transport Analysis Using Data Science"
)

st.markdown(
    "An interactive platform for analysing "
    "Chennai's public transportation network."
)

st.divider()


# SIDEBAR

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Route Analytics",
        "Stop Analytics",
        "Trip Analytics",
        "Transport Map",
        "Smart Insights",
        "About Project"
    ]
)


# DASHBOARD

if page == "Dashboard":

    st.header("Transport Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Routes",
        f"{len(routes):,}"
    )

    col2.metric(
        "Total Stops",
        f"{len(stops):,}"
    )

    col3.metric(
        "Total Scheduled Trips",
        f"{len(trips):,}"
    )

    st.divider()

    st.subheader("Transport Route Distribution")

    if "route_type" in routes.columns:

        route_counts = (
            routes["route_type"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        route_counts.columns = [
            "Transport Type",
            "Route Count"
        ]

        fig = px.bar(
            route_counts,
            x="Transport Type",
            y="Route Count",
            title="Routes by GTFS Route Type",
            text="Route Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.info(
        "Statistics describe the records in the "
        "selected dataset, not necessarily current "
        "operational service counts."
    )


# ROUTE ANALYTICS

elif page == "Route Analytics":

    st.header("Route Analytics")

    if "route_type" in routes.columns:

        st.subheader("Route Type Distribution")

        route_counts = (
            routes["route_type"]
            .value_counts()
            .reset_index()
        )

        route_counts.columns = [
            "Route Type",
            "Count"
        ]

        fig = px.pie(
            route_counts,
            names="Route Type",
            values="Count",
            hole=0.4
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Route Dataset")

    st.dataframe(
        routes,
        use_container_width=True
    )


# STOP ANALYTICS

elif page == "Stop Analytics":

    st.header("Transport Stop Analytics")

    st.metric(
        "Total Stop Records",
        len(stops)
    )

    if "stop_name" in stops.columns:

        st.subheader("Most Repeated Stop Names")

        top_stops = (
            stops["stop_name"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_stops.columns = [
            "Stop Name",
            "Records"
        ]

        fig = px.bar(
            top_stops,
            x="Records",
            y="Stop Name",
            orientation="h"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.dataframe(
        stops.head(100),
        use_container_width=True
    )


# TRIP ANALYTICS

elif page == "Trip Analytics":

    st.header("Scheduled Trip Analytics")

    if "route_id" in trips.columns:

        trip_counts = (
            trips["route_id"]
            .value_counts()
            .head(15)
            .reset_index()
        )

        trip_counts.columns = [
            "Route ID",
            "Trip Records"
        ]

        fig = px.bar(
            trip_counts,
            x="Route ID",
            y="Trip Records",
            title="Top 15 Routes by Scheduled Trip Records"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            trip_counts,
            use_container_width=True
        )


# TRANSPORT MAP

elif page == "Transport Map":

    st.header("Chennai Transport Network Map")

    map_data = stops.copy()

    map_data["stop_lat"] = pd.to_numeric(
        map_data["stop_lat"], errors="coerce"
    )

    map_data["stop_lon"] = pd.to_numeric(
        map_data["stop_lon"], errors="coerce"
    )

    map_data = map_data.dropna(
        subset=["stop_lat", "stop_lon"]
    )

    map_data = map_data[
        map_data["stop_lat"].between(12.5, 13.5)
        & map_data["stop_lon"].between(79.5, 80.5)
    ]

    st.write("Valid Chennai stops:", len(map_data))

    if not map_data.empty:

        st.map(
            map_data,
            latitude="stop_lat",
            longitude="stop_lon",
            zoom=9
        )

    else:
        st.warning("No valid stop coordinates found.")

            )

    else:

        st.warning(
            "Geographical information unavailable."
        )


# SMART INSIGHTS

elif page == "Smart Insights":

    st.header("Automated Data Insights")

    st.write(
        "The following observations are generated "
        "automatically from the available dataset."
    )

    st.success(
        f"The dataset contains {len(routes):,} route records."
    )

    st.success(
        f"The dataset contains {len(stops):,} stop records."
    )

    st.success(
        f"The dataset contains {len(trips):,} scheduled trip records."
    )

    if "route_type" in routes.columns:

        most_common = routes["route_type"].value_counts()

        if not most_common.empty:

            st.info(
                f"Route type {most_common.idxmax()} "
                f"has the highest number of route records."
            )


# ABOUT PROJECT

elif page == "About Project":

    st.header("About SmartTransit")

    st.write("""
    SmartTransit is a Data Science project designed
    to analyse Chennai's public transportation network.

    The project uses Python, Pandas, Plotly and Streamlit
    to process and visualize transport information.

    Main objectives:

    - Analyse public transport routes.
    - Examine transport stop locations.
    - Analyse scheduled trips.
    - Visualize geographical information.
    - Generate automated data observations.

    Data sources and dataset limitations are documented
    separately in the project report.
    """)

    st.subheader("Technologies Used")

    st.write(
        "Python | Pandas | Plotly | Streamlit | GTFS"
    )

st.divider()

st.caption(
    "SmartTransit | Academic Data Science Project"
)
