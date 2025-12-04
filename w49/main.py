
import os
import time
import uuid
import streamlit as st
from mock_car import Car
import plotly.graph_objects as go

# -----------------------------
# Page Config & CSS
# -----------------------------
st.set_page_config(page_title="Car Simulator", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 0.8rem; }
        /* Tighten spacing between columns */
        .stColumn > div { padding-top: 0.25rem; }
        /* Center images inside placeholders */
        .status-item { text-align: center; }
        /* Reduce top gap above gauge title (Plotly wrapper class may vary) */
        .css-1dp5vir { padding-top: 0 !important; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Session & Model
# -----------------------------
if "car" not in st.session_state:
    st.session_state.car = Car("Renault", "Clio", 2025)

car = st.session_state.car

# -----------------------------
# Title & Header
# -----------------------------
st.title("🚗 Car Simulator")
st.write("Simulate car controls and view internal state before real integration.")

header_placeholder = st.empty()

# -----------------------------
# Images (paths)
# -----------------------------
car_default = "w49/images/default.jpg"
car_lights = "w49/images/lights_only.jpg"
car_right_blinker_on = "w49/images/right_blinker.jpg"
car_right_blinker_and_lightson = "w49/images/right_blinker_and_lightson.jpg"
car_left_blinker_on = "w49/images/left_blinker.jpg"
car_left_blinker_and_lightson = "w49/images/left_blinker_and_lightson.jpg"
car_4_blinkers = "w49/images/4_blinkers.jpg"
car_all_lightson = "w49/images/all_lightson.jpg"

# (Note: filenames use "whipers")
slow_whipers = "w49/images/slow_whipers.jpg"
medium_whipers = "w49/images/medium_whipers.jpg"
fast_whipers = "w49/images/fast_whipers.jpg"
# OFF image for "No Wipers"
wipers_off_img = "w49/images/no_whipers.jpg"

# Other components
radio_off = "w49/images/radio_off.jpg"
radio_on = "w49/images/radio_on.jpg"
reverse_light_on = "w49/images/reverse_light_on.jpg"
reverse_light_off = "w49/images/reverse_light_off.jpg"
# Clutch icons (you mentioned you have them)
clutch_off_img = "w49/images/not_clutch.jpg"
clutch_on_img = "w49/images/clutch.jpg"


def safe_image_path(path: str, fallback: str) -> str:
    """Return path if exists, else fallback."""
    return path if os.path.exists(path) else fallback


# -----------------------------
# Hero layout: Car | Status | Gauge
# -----------------------------
# Wider car image, narrow middle status column, standard gauge
col_img, col_status, col_speed = st.columns([2.0, 0.9, 1.6])

# Left: car image
car_image_placeholder = col_img.empty()

# Middle: vertical status column (Reverse, Radio, Wipers, Clutch)
with col_status:
    st.markdown("#### Status",
                help="Symbols centered between car and speedometer")
    reverse_status_box = st.container()
    radio_status_box = st.container()
    wipers_status_box = st.container()
    clutch_status_box = st.container()

# Right: speedometer
speedometer_placeholder = col_speed.empty()

# -----------------------------
# Dynamic header & gauge
# -----------------------------


def update_header():
    header_placeholder.markdown(
        f"### Current Speed: **{car.speed} km/h** | Lights: **{'ON' if car.lights else 'OFF'}**"
    )


def update_speedometer():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=car.speed,
        title={'text': "Speed (km/h)"},
        gauge={
            'axis': {'range': [0, 200]},
            'bar': {'color': "blue"},
            'bgcolor': "rgba(0,0,0,0)"
        }
    ))
    # Pull the gauge up/tighter
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=0))
    speedometer_placeholder.plotly_chart(
        fig, use_container_width=True, key=str(uuid.uuid4())
    )


def get_current_image():
    # Primary car image priority: Hazard > Blinkers(+lights) > Blinkers > Lights > Default
    if car.hazard_lights:
        return car_4_blinkers
    elif car.blinkers == "left" and car.lights:
        return car_left_blinker_and_lightson
    elif car.blinkers == "left":
        return car_left_blinker_on
    elif car.blinkers == "right" and car.lights:
        return car_right_blinker_and_lightson
    elif car.blinkers == "right":
        return car_right_blinker_on
    elif car.lights:
        return car_lights
    else:
        return car_default


def update_car_image():
    car_image_placeholder.image(get_current_image(), width=430)


def blink_animation(image_path, cycles=6, delay=0.45):
    for _ in range(cycles):
        car_image_placeholder.image(image_path, width=430)
        time.sleep(delay)
        car_image_placeholder.empty()
        time.sleep(delay)
    update_car_image()


# -----------------------------
# Initialize hero visuals
# -----------------------------
update_header()
update_speedometer()
update_car_image()

# Initialize middle column defaults (OFF states)
with reverse_status_box:
    st.markdown("<div class='status-item'><b>Reverse</b></div>",
                unsafe_allow_html=True)
    reverse_placeholder = st.empty()
    reverse_placeholder.image(reverse_light_off, width=120)

with radio_status_box:
    st.markdown("<div class='status-item'><b>Radio</b></div>",
                unsafe_allow_html=True)
    radio_placeholder = st.empty()
    radio_placeholder.image(radio_off, width=120)

with wipers_status_box:
    st.markdown("<div class='status-item'><b>Wipers</b></div>",
                unsafe_allow_html=True)
    wipers_placeholder = st.empty()
    wipers_placeholder.image(safe_image_path(
        wipers_off_img, car_default), width=120)

with clutch_status_box:
    st.markdown("<div class='status-item'><b>Clutch</b></div>",
                unsafe_allow_html=True)
    clutch_placeholder = st.empty()
    clutch_placeholder.image(safe_image_path(
        clutch_off_img, car_default), width=120)

# -----------------------------
# Feedback
# -----------------------------
feedback = st.empty()

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["Controls", "Other Controls", "Current State", "Logs"])

# Tab 1: Main Controls
with tab1:
    st.markdown("### Main Controls")

    # Row 1: Driving controls
    row1 = st.columns(4)
    with row1[0]:
        if st.button("Accelerate"):
            feedback.info(car.accelerate())
            update_header()
            update_speedometer()
    with row1[1]:
        if st.button("Brake"):
            feedback.info(car.brake())
            update_header()
            update_speedometer()
    with row1[2]:
        if st.button("Clutch Press"):
            feedback.info(car.clutch_press())
            clutch_placeholder.image(safe_image_path(
                clutch_on_img, car_default), width=120)
    with row1[3]:
        if st.button("Clutch Release"):
            feedback.info(car.clutch_release())
            clutch_placeholder.image(safe_image_path(
                clutch_off_img, car_default), width=120)

    st.markdown("---")  # Divider

    # Row 2: Lights and Radio
    row2 = st.columns(4)
    with row2[0]:
        if st.button("Lights ON"):
            feedback.info(car.lights_on())
            update_header()
            update_car_image()
    with row2[1]:
        if st.button("Lights OFF"):
            feedback.info(car.lights_off())
            car.blinkers = None
            car.hazard_lights = False
            update_header()
            update_car_image()
    with row2[2]:
        if st.button("Radio ON"):
            feedback.info(car.radio_on())
            radio_placeholder.image(radio_on, width=120)
    with row2[3]:
        if st.button("Radio OFF"):
            feedback.info(car.radio_off())
            radio_placeholder.image(radio_off, width=120)

    st.markdown("---")  # Divider

    # Row 3: Blinkers & Hazard
    row3 = st.columns(4)
    with row3[0]:
        if st.button("Blinkers LEFT"):
            feedback.info(car.blinkers_left())
            blink_animation(get_current_image())
    with row3[1]:
        if st.button("Blinkers RIGHT"):
            feedback.info(car.blinkers_right())
            blink_animation(get_current_image())
    with row3[2]:
        if st.button("Hazard ON"):
            feedback.info(car.hazard_lights_on())
            blink_animation(get_current_image())
    with row3[3]:
        if st.button("Hazard OFF"):
            feedback.info(car.hazard_lights_off())
            car.blinkers = None
            update_car_image()

    st.markdown("---")  # Divider

    # Row 4: Reset centered
    row4 = st.columns([4, 2, 4])
    with row4[1]:
        if st.button("🔄 Reset Car State"):
            st.session_state.car = Car("Renault", "Clio", 2025)
            car = st.session_state.car
            feedback.success("Car state reset successfully!")
            update_header()
            update_speedometer()
            update_car_image()
            # Reset middle-column defaults
            reverse_placeholder.image(reverse_light_off, width=120)
            radio_placeholder.image(radio_off, width=120)
            wipers_placeholder.image(safe_image_path(
                wipers_off_img, car_default), width=120)
            clutch_placeholder.image(safe_image_path(
                clutch_off_img, car_default), width=120)

# Tab 2: Other Controls
with tab2:
    st.markdown("### Other Controls")

    # Row 1: Reverse & Wipers Slow
    row1 = st.columns(4)
    with row1[0]:
        if st.button("Reverse Light ON"):
            feedback.info(car.reverse_light_on())
            reverse_placeholder.image(reverse_light_on, width=120)
    with row1[1]:
        if st.button("Reverse Light OFF"):
            feedback.info(car.reverse_light_off())
            reverse_placeholder.image(reverse_light_off, width=120)
    with row1[2]:
        if st.button("Wipers Slow"):
            feedback.info(car.wipers_light())
            wipers_placeholder.image(slow_whipers, width=120)
    with row1[3]:
        if st.button("No Wipers"):
            # Robust handling: use method if present, else set state & log
            if hasattr(car, "wipers_off") and callable(getattr(car, "wipers_off")):
                feedback.info(car.wipers_off())
            else:
                car.wipers = "Off"
                if hasattr(car, "log_action"):
                    car.log_action("Wipers Off")
                feedback.info("Wipers turned OFF.")
            wipers_placeholder.image(safe_image_path(
                wipers_off_img, car_default), width=120)

    st.markdown("---")

    # Row 2: Wipers Medium & Fast
    row2 = st.columns([2, 2, 2])
    with row2[1]:
        if st.button("Wipers Medium"):
            feedback.info(car.wipers_medium())
            wipers_placeholder.image(medium_whipers, width=120)
    with row2[2]:
        if st.button("Wipers Fast"):
            feedback.info(car.wipers_fast())
            wipers_placeholder.image(fast_whipers, width=120)

# Tab 3: Current State
with tab3:
    st.json({
        "Speed": car.speed,
        "Lights": car.lights,
        "Clutch": car.clutch,
        "Radio": car.radio,
        "Blinkers": car.blinkers,
        "Reverse Light": car.reverse_light,
        "Hazard Lights": car.hazard_lights,
        "Wipers": car.wipers
    })

# Tab 4: Logs
with tab4:
    st.subheader("Recent Logs")
    try:
        with open("car_events.log", "r") as log_file:
            logs = log_file.readlines()[-50:]
            st.text_area("Logs", value="".join(logs), height=300)
    except FileNotFoundError:
        st.warning("No logs found yet.")
