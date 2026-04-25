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
# MODULE 7 — E6B SPEED / TIME / DISTANCE / FUEL
# ---------------------------------------------------------
if menu == "E6B Speed / Time / Distance / Fuel":
    st.title("⏱️ E6B Speed / Time / Distance / Fuel")

    # -----------------------------
    # CLEAR ALL BUTTON
    # -----------------------------
    if st.button("🧹 Clear All Inputs"):
        st.session_state["e6b_speed"] = 0.0
        st.session_state["e6b_distance"] = 0.0
        st.session_state["e6b_time"] = 0.0
        st.session_state["e6b_fuel_burn"] = 0.0
        st.session_state["e6b_reserve"] = 0
        st.rerun()

    # -----------------------------
    # MODE SELECTOR
    # -----------------------------
    solve_for = st.selectbox(
        "What do you want to solve for?",
        ["Time", "Distance", "Speed", "Fuel"]
    )

    st.subheader("Inputs")

    # -----------------------------
    # INPUT ENABLE/DISABLE LOGIC
    # -----------------------------
    disable_speed = solve_for == "Speed"
    disable_distance = solve_for == "Distance"
    disable_time = solve_for in ["Time", "Fuel"]  # Fuel auto-calculates time
    disable_fuel_burn = solve_for != "Fuel"
    disable_reserve = solve_for != "Fuel"

    # -----------------------------
    # INPUT FIELDS (with session state)
    # -----------------------------
    speed = st.number_input(
        "Speed",
        value=st.session_state.get("e6b_speed", 0.0),
        disabled=disable_speed
    )
    st.session_state["e6b_speed"] = speed

    speed_units = st.selectbox("Speed Units", ["kt", "km/h"])

    distance = st.number_input(
        "Distance",
        value=st.session_state.get("e6b_distance", 0.0),
        disabled=disable_distance
    )
    st.session_state["e6b_distance"] = distance

    distance_units = st.selectbox("Distance Units", ["NM", "km"])

    # TIME FIELD — may be auto-filled later
    time_hours = st.number_input(
        "Time (decimal hours)",
        value=st.session_state.get("e6b_time", 0.0),
        disabled=disable_time
    )
    st.session_state["e6b_time"] = time_hours

    fuel_burn = st.number_input(
        "Fuel Burn (L/hr)",
        value=st.session_state.get("e6b_fuel_burn", 0.0),
        disabled=disable_fuel_burn
    )
    st.session_state["e6b_fuel_burn"] = fuel_burn

    reserve_minutes = st.number_input(
        "Reserve (minutes)",
        value=st.session_state.get("e6b_reserve", 0),
        disabled=disable_reserve
    )
    st.session_state["e6b_reserve"] = reserve_minutes

        # -----------------------------
    # REQUIRED FIELD HIGHLIGHTING
    # -----------------------------
    missing_required = {"flag": False}

    def warn_if_missing(condition, label):
        if condition:
            st.markdown(
                f"<span style='color:red;'>⚠ {label} is required</span>",
                unsafe_allow_html=True
            )
            missing_required["flag"] = True



    if solve_for == "Time":
        warn_if_missing(speed == 0, "Speed")
        warn_if_missing(distance == 0, "Distance")

    if solve_for == "Distance":
        warn_if_missing(speed == 0, "Speed")
        warn_if_missing(time_hours == 0, "Time")

    if solve_for == "Speed":
        warn_if_missing(distance == 0, "Distance")
        warn_if_missing(time_hours == 0, "Time")

    if solve_for == "Fuel":
        warn_if_missing(speed == 0, "Speed")
        warn_if_missing(distance == 0, "Distance")
        warn_if_missing(fuel_burn == 0, "Fuel burn")

    # If missing required fields → stop before calculations
    if missing_required["flag"]:
        st.info("Enter all required fields to calculate.")
        st.stop()

    # -----------------------------
    # UNIT CONVERSIONS
    # -----------------------------

    speed_knots = speed * 0.539957 if speed_units == "km/h" else speed
    distance_nm = distance * 0.539957 if distance_units == "km" else distance
    # -----------------------------
    # CALCULATIONS
    # -----------------------------
    result_time = None
    result_distance = None
    result_speed = None
    result_fuel = None
    result_reserve = None
    result_total_fuel = None

    # Solve for TIME
    if solve_for == "Time":
        result_time = distance_nm / speed_knots

    # Solve for DISTANCE
    if solve_for == "Distance":
        result_distance = speed_knots * time_hours

    # Solve for SPEED
    if solve_for == "Speed":
        result_speed = distance_nm / time_hours

    # Solve for FUEL
    if solve_for == "Fuel":
        # Auto-calc time
        result_time = distance_nm / speed_knots

        # Auto-fill time into disabled input
        st.session_state["e6b_time"] = result_time

        # Fuel calculations
        result_fuel = fuel_burn * result_time
        result_reserve = fuel_burn * (reserve_minutes / 60)
        result_total_fuel = result_fuel + result_reserve

    # -----------------------------
    # OUTPUT PANEL
    # -----------------------------
    st.markdown('<div class="instrument-box">', unsafe_allow_html=True)

    if solve_for == "Time":
        st.markdown('<div class="instrument-title">Time Required</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{result_time:.2f} hr</div>', unsafe_allow_html=True)

    if solve_for == "Distance":
        st.markdown('<div class="instrument-title">Distance Covered</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{result_distance:.1f} NM</div>', unsafe_allow_html=True)

    if solve_for == "Speed":
        st.markdown('<div class="instrument-title">Required Speed</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{result_speed:.0f} kt</div>', unsafe_allow_html=True)

    if solve_for == "Fuel":
        st.markdown('<div class="instrument-title">Time Enroute</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{result_time:.2f} hr</div>', unsafe_allow_html=True)

        st.markdown('<div class="instrument-title">Trip Fuel</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{result_fuel:.1f} L</div>', unsafe_allow_html=True)

        st.markdown('<div class="instrument-title">Reserve Fuel</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{result_reserve:.1f} L</div>', unsafe_allow_html=True)

        st.markdown('<div class="instrument-title">Total Fuel Required</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="instrument-value">{result_total_fuel:.1f} L</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # SHOW WORKING (COLLAPSIBLE)
    # -----------------------------
    with st.expander("▼ Show Working"):
        if solve_for == "Time":
            st.write(f"""
**Distance:** {distance_nm:.2f} NM  
**Speed:** {speed_knots:.2f} kt  

**Formula:**  
Time = Distance / Speed  

**Working:**  
Time = {distance_nm:.2f} / {speed_knots:.2f}  
Time = **{result_time:.2f} hr**
""")

        if solve_for == "Distance":
            st.write(f"""
**Speed:** {speed_knots:.2f} kt  
**Time:** {time_hours:.2f} hr  

**Formula:**  
Distance = Speed × Time  

**Working:**  
Distance = {speed_knots:.2f} × {time_hours:.2f}  
Distance = **{result_distance:.2f} NM**
""")

        if solve_for == "Speed":
            st.write(f"""
**Distance:** {distance_nm:.2f} NM  
**Time:** {time_hours:.2f} hr  

**Formula:**  
Speed = Distance / Time  

**Working:**  
Speed = {distance_nm:.2f} / {time_hours:.2f}  
Speed = **{result_speed:.2f} kt**
""")

        if solve_for == "Fuel":
            st.write(f"""
**Distance:** {distance_nm:.2f} NM  
**Speed:** {speed_knots:.2f} kt  

**Time Calculation:**  
Time = Distance / Speed  
Time = {distance_nm:.2f} / {speed_knots:.2f}  
Time = **{result_time:.2f} hr**

**Fuel Burn:** {fuel_burn:.2f} L/hr  
**Reserve:** {reserve_minutes} min = {reserve_minutes/60:.2f} hr  

**Trip Fuel:**  
{fuel_burn:.2f} × {result_time:.2f} = **{result_fuel:.2f} L**

**Reserve Fuel:**  
{fuel_burn:.2f} × {reserve_minutes/60:.2f} = **{result_reserve:.2f} L**

**Total Fuel:**  
{result_fuel:.2f} + {result_reserve:.2f} = **{result_total_fuel:.2f} L**
""")

# ---------------------------------------------------------
# CUSTOM CSS FOR DISABLED + COMPUTED FIELDS
# ---------------------------------------------------------
st.markdown("""
<style>

    /* Grey-out disabled fields */
    input[disabled] {
        background-color: #444 !important;
        color: #999 !important;
        border: 1px solid #666 !important;
    }

    /* Garmin yellow computed fields */
    .computed-field input[disabled] {
        background-color: #ffe066 !important;  /* Garmin yellow */
        color: #000 !important;
        font-weight: bold !important;
        border: 2px solid #ffcc33 !important;
    }

    </style>
""", unsafe_allow_html=True)

st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            setTimeout(() => { this.select(); }, 50);
        });
    });
});
</script>
""", unsafe_allow_html=True)



