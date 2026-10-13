import streamlit as st
import math

st.set_page_config(
    page_title="Textile Required Time Calculator",
    page_icon="🧵",
    layout="centered"
)

st.title("🧵 Textile Required Time Calculator")
st.caption("Textile Engineering | Roll No. 25TE051")
st.write(
    "Calculate estimated production time for common textile operations. "
    "Choose a calculation method, enter the production details, and view the formula and steps."
)

with st.sidebar:
    st.header("About")
    st.write("**Student Roll No.:** 25TE051")
    st.write("**Application:** Textile Required Time Calculator")
    st.info(
        "Results are estimates. Use consistent units and your mill's actual "
        "machine settings for practical production planning."
    )

method = st.selectbox(
    "Select calculation method",
    [
        "General production time",
        "Yarn winding / machine production",
        "Spinning: hank-based production",
        "Simple speed-distance calculation",
    ],
)

def show_result(hours, formula, steps, unit_note=""):
    if hours < 0 or not math.isfinite(hours):
        st.error("Please enter values that produce a valid, non-negative time.")
        return
    total_minutes = hours * 60
    whole_hours = int(total_minutes // 60)
    remaining_minutes = total_minutes - whole_hours * 60
    st.success(f"Estimated required time: **{whole_hours} h {remaining_minutes:.2f} min**")
    st.metric("Time in hours", f"{hours:.4f} h")
    st.markdown("**Formula**")
    st.latex(formula)
    st.markdown("**Calculation steps**")
    for i, step in enumerate(steps, start=1):
        st.write(f"{i}. {step}")
    if unit_note:
        st.caption(unit_note)

if method == "General production time":
    st.subheader("General production")
    c1, c2 = st.columns(2)
    with c1:
        quantity = st.number_input("Required quantity (units)", min_value=0.0, value=1000.0, step=100.0)
        rate = st.number_input("Actual production rate (units/hour)", min_value=0.0, value=250.0, step=10.0)
    with c2:
        machines = st.number_input("Number of identical machines", min_value=1, value=1, step=1)
        setup_minutes = st.number_input("Setup time (minutes)", min_value=0.0, value=0.0, step=5.0)
    if st.button("Calculate required time", type="primary"):
        if rate <= 0:
            st.error("Production rate must be greater than zero.")
        else:
            production_hours = quantity / (rate * machines)
            setup_hours = setup_minutes / 60
            total = production_hours + setup_hours
            show_result(
                total,
                r"T = \frac{Q}{R \\times N} + \frac{S}{60}",
                [
                    f"Production time = {quantity:g} ÷ ({rate:g} × {machines}) = {production_hours:.4f} hours.",
                    f"Setup time = {setup_minutes:g} ÷ 60 = {setup_hours:.4f} hours.",
                    f"Total time = {production_hours:.4f} + {setup_hours:.4f} = {total:.4f} hours.",
                ],
                "Q = required quantity, R = actual rate per machine per hour, N = machine count, S = setup minutes."
            )

elif method == "Yarn winding / machine production":
    st.subheader("Yarn winding / machine production")
    st.write("Use this method when the required yarn length and effective winding speed are known.")
    c1, c2 = st.columns(2)
    with c1:
        length_km = st.number_input("Required yarn length (km)", min_value=0.0, value=100.0, step=10.0)
        speed_m_min = st.number_input("Machine speed (m/min)", min_value=0.0, value=800.0, step=50.0)
    with c2:
        positions = st.number_input("Working positions", min_value=1, value=1, step=1)
        efficiency = st.slider("Efficiency (%)", min_value=1, max_value=100, value=85)
    if st.button("Calculate required time", type="primary"):
        if speed_m_min <= 0:
            st.error("Machine speed must be greater than zero.")
        else:
            length_m = length_km * 1000
            effective_rate = speed_m_min * positions * (efficiency / 100)
            minutes = length_m / effective_rate
            hours = minutes / 60
            show_result(
                hours,
                r"T = \frac{L \\times 1000}{V \\times P \\times (E/100) \\times 60}",
                [
                    f"Convert yarn length: {length_km:g} km × 1000 = {length_m:,.2f} m.",
                    f"Effective production rate = {speed_m_min:g} × {positions} × {efficiency}/100 = {effective_rate:,.2f} m/min.",
                    f"Time = {length_m:,.2f} ÷ {effective_rate:,.2f} = {minutes:,.2f} minutes.",
                    f"Convert to hours: {minutes:,.2f} ÷ 60 = {hours:.4f} hours.",
                ],
                "Assumes all working positions operate at the same stated speed and efficiency."
            )

elif method == "Spinning: hank-based production":
    st.subheader("Spinning: hank-based production")
    st.write("For production expressed in hanks, use the actual output per spindle per hour.")
    c1, c2 = st.columns(2)
    with c1:
        required_hanks = st.number_input("Required production (hanks)", min_value=0.0, value=2880.0, step=120.0)
        actual_hanks_per_spindle_hour = st.number_input(
            "Actual production (hanks/spindle/hour)", min_value=0.0, value=1.0, step=0.1,
            help="Enter the actual production rate for one spindle per hour, after efficiency."
        )
    with c2:
        spindles = st.number_input("Number of working spindles", min_value=1, value=8, step=1)
        extra_minutes = st.number_input("Additional allowance (minutes)", min_value=0.0, value=0.0, step=5.0)
    if st.button("Calculate required time", type="primary"):
        if actual_hanks_per_spindle_hour <= 0:
            st.error("Actual production per spindle per hour must be greater than zero.")
        else:
            production_hours = required_hanks / (actual_hanks_per_spindle_hour * spindles)
            total = production_hours + extra_minutes / 60
            show_result(
                total,
                r"T = \frac{H}{P_s \\times N} + \frac{A}{60}",
                [
                    f"Total production rate = {actual_hanks_per_spindle_hour:g} × {spindles} = {actual_hanks_per_spindle_hour * spindles:,.4f} hanks/hour.",
                    f"Production time = {required_hanks:g} ÷ {actual_hanks_per_spindle_hour * spindles:,.4f} = {production_hours:.4f} hours.",
                    f"Additional allowance = {extra_minutes:g} ÷ 60 = {extra_minutes / 60:.4f} hours.",
                    f"Total required time = {total:.4f} hours.",
                ],
                "Important: if your textbook gives production in lb/hour, convert the required quantity to lb and use lb/hour consistently. Do not mix hanks and pounds."
            )

else:
    st.subheader("Simple speed-distance calculation")
    c1, c2 = st.columns(2)
    with c1:
        distance = st.number_input("Required length / distance (metres)", min_value=0.0, value=1000.0, step=100.0)
        speed = st.number_input("Speed (metres/minute)", min_value=0.0, value=100.0, step=10.0)
    with c2:
        efficiency = st.slider("Operating efficiency (%)", min_value=1, max_value=100, value=100)
        allowance = st.number_input("Extra allowance (minutes)", min_value=0.0, value=0.0, step=5.0)
    if st.button("Calculate required time", type="primary"):
        if speed <= 0:
            st.error("Speed must be greater than zero.")
        else:
            effective_speed = speed * efficiency / 100
            minutes = distance / effective_speed + allowance
            hours = minutes / 60
            show_result(
                hours,
                r"T = \frac{D}{V \\times (E/100) \\times 60} + \frac{A}{60}",
                [
                    f"Effective speed = {speed:g} × {efficiency}/100 = {effective_speed:.4f} m/min.",
                    f"Running time = {distance:g} ÷ {effective_speed:.4f} = {distance / effective_speed:.4f} minutes.",
                    f"Add allowance: {distance / effective_speed:.4f} + {allowance:g} = {minutes:.4f} minutes.",
                    f"Time in hours = {minutes:.4f} ÷ 60 = {hours:.4f} hours.",
                ],
                "This simplified method assumes steady speed and does not include stoppages unless represented by the allowance."
            )

st.divider()
st.caption("Developed for Textile Engineering | Roll No. 25TE051")
