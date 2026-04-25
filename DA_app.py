import streamlit as st

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

st.title("✈️ Density Altitude Calculator (Garmin‑Style)")

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
