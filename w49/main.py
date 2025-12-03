import streamlit as st
from mock_car import Car
import plotly.graph_objects as go
import time
import uuid

# Page Config
st.set_page_config(page_title="Car Simulator", layout="wide")

# Reduce top padding
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize car instance in session state
if "car" not in st.session_state:
    st.session_state.car = Car("Renault", "Clio", 2025)

car = st.session_state.car

# Title
st.title("🚗 Car Simulator")
st.write("Simulate car controls and view internal state before real integration.")

# Dynamic Header placeholder
header_placeholder = st.empty()

# Load images
car_default = "w49/images/default.jpg"
car_lights = "w49/images/lights_only.jpg"
car_right_blinker_on = "w49/images/right_blinker.jpg"
car_right_blinker_and_lightson = "w49/images/right_blinker_and_lightson.jpg"
car_left_blinker_on = "w49/images/left_blinker.jpg"
car_left_blinker_and_lightson = "w49/images/left_blinker_and_lightson.jpg"
car_4_blinkers = "w49/images/4_blinkers.jpg"
car_all_lightson = "w49/images/all_lightson.jpg"
slow_whipers = "w49/images/slow_whipers.jpg"
medium_whipers = "w49/images/medium_whipers.jpg"
fast_whipers = "w49/images/fast_whipers.jpg"
clutch_off = "w49/images/bot_clutch.jpg"
clutch_on = "w49/images/clutch.jpg"
radio_off = "w49/images/radio_off.jpg"
radio_on = "w49/images/radio_on.jpg"
reverse_light_on = "w49/images/reverse_light_on.jpg"
reverse_light_off = "w49/images/reverse_light_off.jpg"

# Layout: Car image and speedometer side by side
col_img, col_speed = st.columns([2, 1])
car_image_placeholder = col_img.empty()
speedometer_placeholder = col_speed.empty()


def update_header():
    header_placeholder.markdown(
        f"### Current Speed: **{car.speed} km/h** | Lights: **{'ON' if car.lights else 'OFF'}**"
    )


def update_speedometer():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=car.speed,
        title={'text': "Speed (km/h)"},
        gauge={'axis': {'range': [0, 200]}, 'bar': {'color': "blue"}}
    ))
    speedometer_placeholder.plotly_chart(
        fig, use_container_width=True, key=str(uuid.uuid4()))


def get_current_image():
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
    car_image_placeholder.image(get_current_image(), width=400)


def blink_animation(image_path, cycles=6, delay=0.5):
    for i in range(cycles):
        car_image_placeholder.image(image_path, width=400)
        time.sleep(delay)
        car_image_placeholder.empty()
        time.sleep(delay)
    update_car_image()  # restore final state


# Initial updates
update_header()
update_speedometer()
update_car_image()

# Feedback placeholder
feedback = st.empty()

# Tabs for better layout
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
    with row1[3]:
        if st.button("Clutch Release"):
            feedback.info(car.clutch_release())

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
    with row2[3]:
        if st.button("Radio OFF"):
            feedback.info(car.radio_off())

    st.markdown("---")  # Divider

    # Row 3: Blinkers and Hazard
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

    # Row 4: Reset button centered
    row4 = st.columns([4, 2, 4])
    with row4[1]:
        if st.button("🔄 Reset Car State"):
            st.session_state.car = Car("Renault", "Clio", 2025)
            car = st.session_state.car
            feedback.success("Car state reset successfully!")
            update_header()
            update_speedometer()
            update_car_image()

# Tab 2: Other Controls
with tab2:
    st.markdown("### Other Controls")

    # Row 1: Reverse Lights and Wipers Slow
    row1 = st.columns(3)
    with row1[0]:
        if st.button("Reverse Light ON"):
            feedback.info(car.reverse_light_on())
    with row1[1]:
        if st.button("Reverse Light OFF"):
            feedback.info(car.reverse_light_off())
    with row1[2]:
        if st.button("Wipers Slow"):
            feedback.info(car.wipers_light())

    st.markdown("---")

    # Row 2: Wipers Medium and Fast
    row2 = st.columns([2, 2, 2])
    with row2[1]:
        if st.button("Wipers Medium"):
            feedback.info(car.wipers_medium())
    with row2[2]:
        if st.button("Wipers Fast"):
            feedback.info(car.wipers_fast())

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

# Tab 4: Logs in Scrollable Box
with tab4:
    st.subheader("Recent Logs")
    try:
        with open("car_events.log", "r") as log_file:
            logs = log_file.readlines()[-50:]  # Last 50 entries
            st.text_area("Logs", value="".join(logs), height=300)
    except FileNotFoundError:
        st.warning("No logs found yet.")
