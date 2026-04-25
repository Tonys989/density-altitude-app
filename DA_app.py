import streamlit as st

import streamlit as st

st.set_page_config(page_title="EFC", layout="centered")

# --- MENU SYSTEM ---
st.sidebar.title("🛩️ Tonys Wizz Wheel")

menu = st.sidebar.radio(
    "Select a module:",
    [
        "Density Altitude",
        "Wind Triangle (coming soon)",
        "Glide Calculator (coming soon)",
        "TAS / CAS / IAS (coming soon)",
        "Crosswind Component (coming soon)",
        "Weight & Balance (coming soon)"
    ]
)

if menu == "Density Altitude":
    st.title("✈️ Density Altitude Calculator")

    qnh = st.number_input("QNH (hPa)", value=1013)
    elevation = st.number_input("Field Elevation (ft)", value=0)
    oat = st.number_input("Outside Air Temperature (°C)", value=15.0)

    pressure_altitude = elevation + 30 * (1013 - qnh)
    isa_temp = 15 - 2 * (pressure_altitude / 1000)
    density_altitude = pressure_altitude + 120 * (oat - isa_temp)

    st.subheader("Results")
    st.write(f"**Pressure Altitude:** {pressure_altitude:.0f} ft")
    st.write(f"**ISA Temperature:** {isa_temp:.1f} °C")
    st.write(f"**Density Altitude:** {density_altitude:.0f} ft")

if menu == "Wind Triangle (coming soon)":
    st.title("🧭 Wind Triangle")
    st.info("This module will calculate heading, groundspeed, and wind correction angle.")

if menu == "Glide Calculator (coming soon)":
    st.title("🪂 Glide Calculator")
    st.info("This module will compute glide ratio, arrival height, and final glide.")

if menu == "TAS / CAS / IAS (coming soon)":
    st.title("🌡️ Airspeed Conversions")
    st.info("This module will convert IAS ↔ CAS ↔ TAS.")

if menu == "Crosswind Component (coming soon)":
    st.title("🌬️ Crosswind Calculator")
    st.info("This module will compute crosswind and headwind components.")

if menu == "Weight & Balance (coming soon)":
    st.title("⚖️ Weight & Balance")
    st.info("This module will compute CG and loading envelopes.")


# --- Garmin-style UI theme ---
st.set_page_config(page_title="Density Altitude", layout="centered")

st.markdown("""
<style>
body {
    background-color: #0a0a0a;
    color: #e6e6e6;
    font-family: 'Segoe UI', sans-serif;
}
.instrument-box {
    background-color: #111;
    padding: 25px;
    border-radius: 12px;
    border: 2px solid #333;
    margin-top: 20px;
}
.instrument-title {
    font-size: 26px;
    font-weight: bold;
    color: #00b4ff;
    text-align: center;
    margin-bottom: 10px;
}
.instrument-value {
    font-size: 40px;
    font-weight: bold;
    color: #00ff90;
    text-align: center;
}
.label {
    font-size: 16px;
    color: #cccccc;
}
</style>
""", unsafe_allow_html=True)

st.title("✈️ Density Altitude Calculator ")

# Inputs
qnh = st.number_input("QNH (hPa)", value=1013)
elevation = st.number_input("Field Elevation (ft)", value=0)
oat = st.number_input("Outside Air Temperature (°C)", value=15.0)

# Calculations
pressure_altitude = elevation + 30 * (1013 - qnh)
isa_temp = 15 - 2 * (pressure_altitude / 1000)
density_altitude = pressure_altitude + 120 * (oat - isa_temp)

# Output panel
st.markdown('<div class="instrument-box">', unsafe_allow_html=True)
st.markdown('<div class="instrument-title">Pressure Altitude</div>', unsafe_allow_html=True)
st.markdown(f'<div class="instrument-value">{pressure_altitude:.0f} ft</div>', unsafe_allow_html=True)

st.markdown('<div class="instrument-title">ISA Temperature</div>', unsafe_allow_html=True)
st.markdown(f'<div class="instrument-value">{isa_temp:.1f} °C</div>', unsafe_allow_html=True)

st.markdown('<div class="instrument-title">Density Altitude</div>', unsafe_allow_html=True)
st.markdown(f'<div class="instrument-value">{density_altitude:.0f} ft</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
