import streamlit as st
import math

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Electronic Flight Computer", layout="centered")

# ---------------------------------------------------------
# GARMIN-STYLE THEME (CSS)
# ---------------------------------------------------------
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
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR MENU
# ---------------------------------------------------------
st.sidebar.title("🛩️ Flight Computer Menu")

menu = st.sidebar.radio(
    "Select a module:",
    [
        "Density Altitude",
        "TAS / CAS / IAS",
        "Wind Triangle",
        "Glide Calculator",
        "Crosswind Component",
        "Weight & Balance",
        "E6B Speed / Time / Distance / Fuel",
    ]
)

# ---------------------------------------------------------
# MODULE 1 — DENSITY ALTITUDE
# ---------------------------------------------------------
if menu == "Density Altitude":
    st.title("✈️ Density Altitude Calculator")

    qnh = st.number_input("QNH (hPa)", value=1013)
    elevation = st.number_input("Field Elevation (ft)", value=0)
    oat = st.number_input("Outside Air Temperature (°C)", value=15.0)

    pressure_altitude = elevation + 30 * (1013 - qnh)
    isa_temp = 15 - 2 * (pressure_altitude / 1000)
    density_altitude = pressure_altitude + 120 * (oat - isa_temp)

    st.markdown('<div class="instrument-box">', unsafe_allow_html=True)
    st.markdown('<div class="instrument-title">Pressure Altitude</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{pressure_altitude:.0f} ft</div>', unsafe_allow_html=True)

    st.markdown('<div class="instrument-title">ISA Temperature</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{isa_temp:.1f} °C</div>', unsafe_allow_html=True)

    st.markdown('<div class="instrument-title">Density Altitude</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{density_altitude:.0f} ft</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 2 — TAS / CAS / IAS
# ---------------------------------------------------------
if menu == "TAS / CAS / IAS":
    st.title("🌡️ Airspeed Conversions (Rule of Thumb)")

    st.write(
        "Simple VFR rule of thumb for light aircraft:\n\n"
        "- CAS ≈ IAS (assuming small position/instrument error)\n"
        "- TAS ≈ IAS × [1 + 0.02 × (Altitude(ft) / 1000)]"
    )

    ias = st.number_input("Indicated Airspeed (IAS, kt)", value=90.0)
    altitude_ft = st.number_input("Pressure Altitude (ft)", value=0)

    cas = ias
    tas = ias * (1 + 0.02 * (altitude_ft / 1000.0))

    st.markdown('<div class="instrument-box">', unsafe_allow_html=True)
    st.markdown('<div class="instrument-title">Calibrated Airspeed (CAS)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{cas:.0f} kt</div>', unsafe_allow_html=True)

    st.markdown('<div class="instrument-title">True Airspeed (TAS)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{tas:.0f} kt</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 3 — WIND TRIANGLE
# ---------------------------------------------------------
if menu == "Wind Triangle":
    st.title("🧭 Wind Triangle Calculator")

    tas = st.number_input("True Airspeed (kt)", value=90.0)
    wind_speed = st.number_input("Wind Speed (kt)", value=10.0)
    wind_dir = st.number_input("Wind Direction (° FROM)", value=270)
    course = st.number_input("Desired Track (° TO)", value=0)

    rel_angle = math.radians(wind_dir - course)
    crosswind = wind_speed * math.sin(rel_angle)
    headwind = wind_speed * math.cos(rel_angle)

    wca = math.degrees(math.atan2(crosswind, tas))
    heading = course + wca
    groundspeed = tas - headwind

    st.markdown('<div class="instrument-box">', unsafe_allow_html=True)
    st.markdown('<div class="instrument-title">Heading to Fly</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{heading:.0f}°</div>', unsafe_allow_html=True)

    st.markdown('<div class="instrument-title">Wind Correction Angle</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{wca:.1f}°</div>', unsafe_allow_html=True)

    st.markdown('<div class="instrument-title">Groundspeed</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{groundspeed:.0f} kt</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 4 — GLIDE CALCULATOR
# ---------------------------------------------------------
if menu == "Glide Calculator":
    st.title("🪂 Glide Calculator")

    glide_ratio = st.number_input("Glide Ratio (e.g., 30 = 30:1)", value=30)
    altitude_ft = st.number_input("Altitude AGL (ft)", value=3000)
    headwind = st.number_input("Headwind/Tailwind (kt, + = headwind)", value=0)

    still_air_distance = altitude_ft * glide_ratio
    wind_adjusted = still_air_distance * (1 - headwind / 100)

    st.markdown('<div class="instrument-box">', unsafe_allow_html=True)
    st.markdown('<div class="instrument-title">Still-Air Glide Distance</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{still_air_distance/6076:.1f} NM</div>', unsafe_allow_html=True)

    st.markdown('<div class="instrument-title">Wind-Adjusted Distance</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{wind_adjusted/6076:.1f} NM</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 5 — CROSSWIND COMPONENT
# ---------------------------------------------------------
if menu == "Crosswind Component":
    st.title("🌬️ Crosswind Calculator")

    wind_speed = st.number_input("Wind Speed (kt)", value=12)
    wind_dir = st.number_input("Wind Direction (° FROM)", value=270)
    runway = st.number_input("Runway Heading (°)", value=270)

    angle = math.radians(wind_dir - runway)
    crosswind = wind_speed * math.sin(angle)
    headwind = wind_speed * math.cos(angle)

    st.markdown('<div class="instrument-box">', unsafe_allow_html=True)
    st.markdown('<div class="instrument-title">Crosswind</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{abs(crosswind):.0f} kt</div>', unsafe_allow_html=True)

    st.markdown('<div class="instrument-title">Headwind / Tailwind</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{headwind:.0f} kt</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 6 — WEIGHT & BALANCE
# ---------------------------------------------------------
if menu == "Weight & Balance":
    st.title("⚖️ Weight & Balance")

    st.write("Simple CG calculator")

    weight1 = st.number_input("Pilot + Passenger Weight (kg)", value=150)
    arm1 = st.number_input("Pilot Arm (mm)", value=300)

    weight2 = st.number_input("Fuel Weight (kg)", value=40)
    arm2 = st.number_input("Fuel Arm (mm)", value=400)

    total_weight = weight1 + weight2
    total_moment = weight1 * arm1 + weight2 * arm2
    cg = total_moment / total_weight if total_weight > 0 else 0

    st.markdown('<div class="instrument-box">', unsafe_allow_html=True)
    st.markdown('<div class="instrument-title">Total Weight</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="instrument-value">{total_weight:.0f} kg</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# MODULE 7 — E6B SPEED / TIME / DISTANCE / FUEL
# ---------------------------------------------------------
if menu == "E6B Speed / Time / Distance / Fuel":
    st.title("⏱️ E6B Speed / Time / Distance / Fuel")

    st.write("Solve any one of the four: Speed, Time, Distance, Fuel")

    solve_for = st.selectbox(
        "What do you want to solve for?",
        ["Time", "Distance", "Speed", "Fuel"]
    )

    st.subheader("Inputs")

    speed = st.number_input("Speed", value=90.0)
    speed_units = st.selectbox("Speed Units", ["kt", "km/h"])

    distance = st.number_input("Distance", value=50.0)
    distance_units = st.selectbox("Distance Units", ["NM", "km"])

    time_hours = st.number_input("Time (decimal hours)", value=0.5)

    fuel_burn = st.number_input("Fuel Burn (L/hr)", value=20.0)

    reserve_minutes = st.number_input("Reserve (minutes)", value=30)
    reserve_percent = st.number_input("Reserve (%)", value=10)

    # Convert speed to knots
    if speed_units == "km/h":
        speed_knots = speed * 0.539957
    else:
        speed_knots = speed

    # Convert distance to NM
    if distance_units == "km":
        distance_nm = distance * 0.539957
    else:
        distance_nm = distance

    # Calculations
    time_result = None
    distance_result_nm = None
    speed_result_knots = None
    fuel_required = None

    if solve_for == "Time":
        time_result = distance_nm / speed_knots if speed_knots > 0 else 0

    if solve_for == "Distance":
        distance_result_nm = speed_knots * time_hours

    if solve_for == "Speed":
        speed_result_knots = distance_nm / time_hours if time_hours > 0 else 0

    if solve_for == "Fuel":
        fuel_required = fuel_burn * time_hours
        reserve_fuel_minutes = fuel_burn * (reserve_minutes / 60)
        reserve_fuel_percent = fuel_required * (reserve_percent / 100)
        total_fuel = fuel_required + reserve_fuel_minutes + reserve_fuel_percent

    # Output
    st.markdown('<div class="instrument-box">', unsafe_allow_html=True)

    if solve_for == "Time":
        st.markdown('<div class="instrument-title">Time Required</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{time_result:.2f} hr</div>', unsafe_allow_html=True)

    if solve_for == "Distance":
        st.markdown('<div class="instrument-title">Distance Covered</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{distance_result_nm:.1f} NM</div>', unsafe_allow_html=True)

    if solve_for == "Speed":
        st.markdown('<div class="instrument-title">Required Speed</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{speed_result_knots:.0f} kt</div>', unsafe_allow_html=True)

    if solve_for == "Fuel":
        st.markdown('<div class="instrument-title">Trip Fuel</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{fuel_required:.1f} L</div>', unsafe_allow_html=True)

        st.markdown('<div class="instrument-title">Reserve (Minutes)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{reserve_fuel_minutes:.1f} L</div>', unsafe_allow_html=True)

        st.markdown('<div class="instrument-title">Reserve (%)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{reserve_fuel_percent:.1f} L</div>', unsafe_allow_html=True)

        st.markdown('<div class="instrument-title">Total Fuel Required</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{total_fuel:.1f} L</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
