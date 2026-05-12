import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    return pd.read_csv("routes_play.csv")

routes_play = load_data()







st.title("Sustainable Travel in Europe")

# SIDE BAR SLIDERS

st.sidebar.header("Adjust assumptions for generalised cost")

value_of_time = st.sidebar.slider(
    "Value of time (€/hour)", 0, 50, 10, help="Might for example be higher for business travellers.")
airport_overhead = st.sidebar.slider(
    "Airport overhead (hours)", 0.0, 5.0, 4.0)
station_overhead = st.sidebar.slider(
    "Train station overhead (hours)", 0.0, 2.0, 0.5)
baggage_fee = st.sidebar.slider(
    "Baggage fee (€)", 0, 50, 23, help="Only concerns budget airlines")
include_carbon = st.sidebar.checkbox(
    "Include social cost of carbon", True)
carbon_price = st.sidebar.slider(
    "Social cost of carbon (€/tonne)", 0, 200, 166, help="Reflects the negative externality of carbon emissions. Estimated to be approx. 166€ per ton.")
emission_value = st.sidebar.selectbox("Rail emission intensity (g/km)", [4, 35], help="Depends on efficiency of the railway system. Values from Our World in Data.")



# GENERALISED COST FUNCTION

def calculate_generalised_cost(
    routes_play,
    value_of_time=10,
    carbon_price=150, #in € per ton, to get to kg divide by 1000
    airport_overhead=4.0,
    station_overhead=0.35,
    baggage_fee=23,
    emission_value=35, # in grams per kilometer, to get to kg divide by 1000
    include_carbon=True
):
    df = routes_play.copy()

    # Door-to-door times
    df['rail_total_time'] = df['rail_time_hrs'] + station_overhead
    df['air_total_time'] = df['air_time_hrs'] + airport_overhead

    # Carbon cost
    carbon_factor = carbon_price / 1000 if include_carbon else 0

    # Generalised cost
    df['rail_gc'] = (
        df['rail_fare_eur']
        + df['rail_total_time'] * value_of_time
        + df['distance_km'] * emission_value/1000 * carbon_factor #emission_value in kg, carbon factor in kg  
    )

    df['rail_co2_kg'] = df['distance_km'] * emission_value/1000 * carbon_factor
    # attention: by including this, I overwrite the original rail_co2_kg column!!

    df['air_gc'] = (
        df['air_fare_eur']
        + df['cheap_flight'] * baggage_fee
        + df['air_total_time'] * value_of_time
        + df['air_co2_kg'] * carbon_factor
    )

    # Margin
    df['gc_margin'] = df['air_gc'] - df['rail_gc']

    # Winner
    df['winner'] = None
    df.loc[df['gc_margin'] > 0, 'winner'] = 'rail'
    df.loc[df['gc_margin'] <= 0, 'winner'] = 'air'

    return df




# CALCULATE THE GENERALISED COST FUNCTION

df = calculate_generalised_cost(
    routes_play,
    value_of_time=value_of_time,
    carbon_price=carbon_price,
    airport_overhead=airport_overhead,
    station_overhead=station_overhead,
    baggage_fee=baggage_fee,
    emission_value=emission_value,
    include_carbon=include_carbon
)










# FIRST VISUAL (TIME GAP)

price_gap_adjusted = routes_play['rail_fare_eur'] - routes_play['air_fare_eur'] - baggage_fee * routes_play['cheap_flight'] # attention: this will overwrite time_gap
time_gap_adjusted = routes_play['rail_time_hrs'] - routes_play['air_time_hrs'] - airport_overhead + station_overhead


# def calculate_time_gap_adjusted(air_overhead=airport_overhead, station_overhead=station_overhead):
#     time_gap_adjusted = routes_play['rail_time_hrs'] - routes_play['air_time_hrs'] - air_overhead + station_overhead
#     return time_gap_adjusted


fig1 = px.scatter(
    routes_play, x=time_gap_adjusted, y=price_gap_adjusted,
    # routes_play, x=calculate_time_gap_adjusted(air_overhead=airport_overhead, station_overhead=station_overhead), y=price_gap_adjusted,
    hover_data=['route'],
    title='Slower does not always mean cheaper. Actually, rail is often faster',
    labels={'x': 'Time Gap: Rail Time - Air Time (hrs)', 'y': 'Price Gap: Rail Fare - Air Fare (€)'}
)

fig1.update_traces(marker=dict(size=10, opacity=0.6, color="green"))
fig1.add_vline(x=0, line_dash="dash", line_color="black")
fig1.add_hline(y=0, line_dash="dash", line_color="black")


# Annotations for each quadrant
x_vals = time_gap_adjusted
y_vals = price_gap_adjusted

x_min, x_max = x_vals.min(), x_vals.max()
y_min, y_max = y_vals.min(), y_vals.max()

x_pos_right = (0 + x_max) / 2
x_pos_left  = (0 + x_min-2) / 2
y_pos_top   = (0 + y_max+1) / 2
y_pos_bottom= (0 + y_min-1) / 2

# Add annotations in correct quadrants
fig1.add_annotation(x=x_pos_right, y=y_pos_top,
                            text="Slower & <br>More Expensive", showarrow=False)
fig1.add_annotation(x=x_pos_left, y=y_pos_top,
                            text="Faster & <br>More Expensive", showarrow=False)
fig1.add_annotation(x=x_pos_left, y=y_pos_bottom,
                            text="Faster & <br>Cheaper", showarrow=False)
fig1.add_annotation(x=x_pos_right, y=y_pos_bottom,
                            text="Slower & <br>Cheaper", showarrow=False)


fig1.update_layout(
    title_subtitle_text="Time difference vs. price difference. Taking the train is...",
    title_subtitle_font_size=12,
    title_subtitle_font_color="gray")

st.plotly_chart(fig1)








# FIGURE 2 (By DISTANCE CATEGORY)

distance_map = {1: "Short", 2: "Medium", 3: "Long", 4: "Ultra Long"}

fig2 = go.Figure()

gc_means = (
    df
    .groupby("distance_label")[["air_gc", "rail_gc"]]
    .mean()
    .reset_index()
)

gc_means["distance_label"] = gc_means["distance_label"].map(distance_map)

fig2.add_trace(go.Bar(
    x=gc_means["distance_label"],
    y=gc_means["air_gc"],
    name="Air GC",
    marker_color="#9467bd"
))

fig2.add_trace(go.Bar(
    x=gc_means["distance_label"],
    y=gc_means["rail_gc"],
    name="Rail GC",
    marker_color="#1f77b4"
))

fig2.update_layout(
    title="Rail is mostly competitive except for ultra long distances",
    xaxis_title="Distance Category",
    yaxis_title="Average Generalised Cost (€)",
    barmode="group"
)

fig2.update_layout(
    title_subtitle_text="Generalised cost by distance category under slider-based assumptions <br>(short = 0-250 km, medium = 250-500 km, long = 500-750 km, ultra long = 750+ km)",
    title_subtitle_font_size=12,
    title_subtitle_font_color="gray")

st.plotly_chart(fig2, use_container_width=True)





## INCLUDING THE CUTOFF

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
import streamlit as st

X = df[["distance_km"]]
y = (df["gc_margin"] > 0).astype(int)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression()
model.fit(X_scaled, y)

distance_range = np.linspace(df["distance_km"].min(), df["distance_km"].max(), 300).reshape(-1, 1)
distance_scaled = scaler.transform(distance_range)
prob_rail = model.predict_proba(distance_scaled)[:, 1]

threshold_idx = np.argmin(np.abs(prob_rail - 0.5))
threshold_distance = distance_range[threshold_idx][0]

st.metric(
    "**Rail threshold:** Based on your current settings, rail is competitive on distances up to ",
    f"{threshold_distance:.0f} km"
)

# st.write(f"Based on your current settings, rail is competitive on distances up to **{threshold_distance:.0f} km**.")
st.write("")
st.write("")









# FIGURE 3 (SHOWING THE THRESHOLD)

df['winner_co2_kg'] = df['air_co2_kg']
df.loc[df['gc_margin'] > 0, 'winner_co2_kg'] = df['rail_co2_kg']

fig3 = px.scatter(
    df,
    x='distance_km',
    y='gc_margin',
    color='winner',
    size='winner_co2_kg',
    size_max=30,
    hover_data=['route', 'winner_co2_kg'],
    title='Around the threshold of the generalised cost margin, a lot of emissions could be saved',
    labels={'distance_km': 'Distance (km)', 'gc_margin': 'GC Margin (€)', 'winner_co2_kg': 'Winner CO₂ (kg)'},
    color_discrete_map={'rail': '#1f77b4', 'air': '#9467bd'} 
)

fig3.update_layout(
    title_subtitle_text='Distance vs. Rail advantage (Generalised Cost Margin) under slider-based assumptions<br>Size represents carbon emissions for route and given means of transport',
    title_subtitle_font_size=12,
    title_subtitle_font_color="gray")
fig3.add_hline(y=0, line_width=2, line_color='black')  

st.plotly_chart(fig3, use_container_width=True)




# EXPLORE THE LOW-HANGING FRUITS


st.write("")
st.write("")
st.subheader("Let's find the low-hanging fruits for policy")
st.write("On some routes, air wins over rail only by a slim margin, say 50 euros. If these were targeted for example by policy, many carbon emissions could be saved")

theshold = st.slider("What is your threshold for 'low-hanging fruits'?", 0, 200, 50)

low_hanging_fruits = df[(df['gc_margin'] >= -theshold) & (df['gc_margin'] < 0)]

st.markdown(":gray[When travelling each of these routes once...]")
col1, col2, col3, col4 = st.columns(4)

n_routes = low_hanging_fruits["route"].nunique()
total_air_co2 = low_hanging_fruits["winner_co2_kg"].sum()
total_rail_co2 = low_hanging_fruits["rail_co2_kg"].sum()
train_savings = low_hanging_fruits["winner_co2_kg"].sum() - low_hanging_fruits["rail_co2_kg"].sum()

if total_air_co2 > 0:
    share_saved = round(train_savings / total_air_co2 * 100, 2)
else:
    share_saved = 0

col1.metric("Number of target routes", n_routes)
col2.metric("CO2 emitted by air", f"{total_air_co2:,.1f} kg")
col3.metric("CO2 emitted by rail", f"{total_rail_co2:,.1f} kg")
# col3.metric("CO2 saved by rail", f"{train_savings:,.1f} kg")
col4.metric("Share of CO2 saved", f"{share_saved}%")
col4.caption(f"by switching these {n_routes} routes to rail")

route_names = ", ".join(sorted(low_hanging_fruits["route"].unique()))
st.write(f"These are the routes where air wins by a slim margin of below {theshold} euros: {route_names}")


# FIGURE 4 (BY ROUTE BAR CHART)

routes_play_3_sorted = df.sort_values("gc_margin", ascending=True).copy()
routes_play_3_sorted["winner"] = routes_play_3_sorted["winner"].astype(str)

fig4 = px.bar(
    routes_play_3_sorted,
    x="gc_margin",
    y="route",
    orientation="h",
    color="winner",
    color_discrete_map={
        "rail": "#1f77b4",
        "air": "#9467bd"
    },
    category_orders={
        "winner": ["rail", "air"],
        "route": routes_play_3_sorted["route"].tolist()
    },
    title="What is the rail advantage of your next route, all things considered?",
    labels={"gc_margin": "Rail advantage (€)", "route": "", "winner": ""}
)

fig4.add_vline(x=0, line_width=2, line_color="black")
fig4.update_layout(
    legend_title_text="Winner",
    height=400 + 10 * len(routes_play_3_sorted)
)
fig4.update_yaxes(
    tickfont=dict(size=10),
    categoryorder="array",
    categoryarray=routes_play_3_sorted["route"].tolist()
)

fig4.update_layout(
    title_subtitle_text="Generalised cost margin under slider-based assumptions",
    title_subtitle_font_size=12,
    title_subtitle_font_color="gray")

st.plotly_chart(fig4, use_container_width=True)