# app.py  ────────────────────────────────────────────────────────────────
# Interactive dashboard: Avg salary by state & major category
# Run with:  streamlit run app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page‑wide settings MUST be first Streamlit call ────────────────────
st.set_page_config(page_title="State Salary Dashboard", layout="wide")

# ────────────────────────────────────────────────────────────────────────
# 1. DATA LOADER  (cached)
# ────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    grads = pd.read_csv("data/recent-grads.csv")

    oews = pd.read_excel("data/state_M2024_dl.xlsx", sheet_name=0)
    oews = oews.rename(columns={
        "AREA_TITLE": "StateName",
        "OCC_CODE":   "SOC",
        "A_MEAN":     "Annual_Mean_Wage"
    })

    # full‑name → USPS mapping
    state_abbrev = {
        "Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA",
        "Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC",
        "Florida":"FL","Georgia":"GA","Hawaii":"HI","Idaho":"ID","Illinois":"IL",
        "Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA",
        "Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN",
        "Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV",
        "New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY",
        "North Carolina":"NC","North Dakota":"ND","Ohio":"OH","Oklahoma":"OK","Oregon":"OR",
        "Pennsylvania":"PA","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD",
        "Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virginia":"VA",
        "Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"
    }
    oews["State"] = oews["StateName"].map(state_abbrev)

    major_to_soc = {
        "Engineering":"17-0000","Business":"13-0000","Health":"29-0000",
        "Social Science":"19-0000","Psychology":"19-3000","Biology":"19-0000"
    }
    grads["SOC"] = grads["Major_category"].map(major_to_soc)

    merged = grads.merge(oews[["SOC","State","Annual_Mean_Wage"]], on="SOC", how="left")
    tbl = (merged
           .groupby(["State","Major_category"])["Annual_Mean_Wage"]
           .mean()
           .reset_index()
           .dropna())
    return tbl

state_major_salary = load_data()

# ────────────────────────────────────────────────────────────────────────
# 2. STREAMLIT UI
# ────────────────────────────────────────────────────────────────────────
st.title("💼 Avg Salary by State & Major Category")

major = st.selectbox(
    "Major Category",
    state_major_salary["Major_category"].unique(),
    index=0
)

df = state_major_salary[state_major_salary["Major_category"] == major].copy()
df["Annual_Mean_Wage"] = pd.to_numeric(df["Annual_Mean_Wage"], errors="coerce")  # ensure numeric

fig = px.choropleth(
    df,
    locations="State",
    locationmode="USA-states",
    color="Annual_Mean_Wage",
    scope="usa",
    color_continuous_scale="YlGnBu",
    range_color=(df["Annual_Mean_Wage"].min(), df["Annual_Mean_Wage"].max()),
    labels={"Annual_Mean_Wage":"Avg Salary ($)"}
)
fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
st.plotly_chart(fig, use_container_width=True)

# ────────────────────────────────────────────────────────────────────────
# 3. METRICS & DETAIL TABLE
# ────────────────────────────────────────────────────────────────────────
st.subheader(f"Key numbers for “{major}” majors")

avg_salary = df["Annual_Mean_Wage"].mean()
hi_state   = df.loc[df["Annual_Mean_Wage"].idxmax()]
lo_state   = df.loc[df["Annual_Mean_Wage"].idxmin()]

c1, c2, c3, c4 = st.columns(4)
c1.metric("National avg", f"${avg_salary:,.0f}")
c2.metric("Highest state", f"{hi_state.State}  •  ${hi_state.Annual_Mean_Wage:,.0f}")
c3.metric("Lowest state",  f"{lo_state.State}  •  ${lo_state.Annual_Mean_Wage:,.0f}")
c4.metric("# States w/ data", f"{df.shape[0]}")

st.markdown("### State‑level detail")
st.dataframe(
    df.sort_values("Annual_Mean_Wage", ascending=False)
      .reset_index(drop=True)
      .style.format({"Annual_Mean_Wage": "${:,.0f}"})
)
