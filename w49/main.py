
import os
import time
import uuid
import streamlit as st
from mock_car import Car
import plotly.graph_objects as go

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Car Simulator", layout="wide")

# -----------------------------
# Theme-aware, high-contrast CSS (works in dark & light)
# -----------------------------
st.markdown("""
<style>
  :root {
    --bg: var(--background-color, #0e1117);
    --bg-secondary: var(--secondary-background-color, #1d232f);
    --text: var(--text-color, #e5e7eb);
    --primary: var(--primary-color, #2563eb);
    --border: rgba(127,127,127,0.25);
  }

  .block-container { padding-top: 0.8rem; padding-bottom: 1.2rem; max-width: 1180px; }

  .card {
    background: var(--bg-secondary);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 12px 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,.12);
    margin-bottom: 12px;
  }

  h1, h2, h3, h4, p { color: var(--text); margin: 0.25rem 0; }

  /* Buttons: white text always for contrast */
  .stButton>button {
    background: var(--primary);
    color: #ffffff !important;
    border: 0;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
    letter-spacing: .2px;
    transition: transform .12s ease, box-shadow .12s ease, filter .12s ease;
    box-shadow: 0 3px 10px rgba(37,99,235,.35);
  }
  .stButton>button:hover { transform: translateY(-1px); filter: brightness(1.06); }

  /* Tabs */
  .stTabs [role="tablist"] { gap: 8px; border-bottom: 1px solid var(--border); margin-bottom: 8px; }
  .stTabs [role="tab"] { border-radius: 8px 8px 0 0; padding: 6px 12px; }

  /* Status grid (no outlines) */
  .status-title { font-weight: 700; font-size: 14px; margin-bottom: 6px; color: var(--text); }
  .status-item { margin-bottom: 8px; }
  /* Keep images centered and inside their cell */
  .status-img { display: block; margin: 0 auto; }

  /* Toast (high-contrast info) */
  .toast {
    background: rgba(37, 99, 235, 0.15);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 10px;
    padding: 10px 12px;
    margin: 6px 0 10px 0;
    font-weight: 500;
  }

  /* Plotly margin fix */
  .js-plotly-plot, .plotly { margin: 0 !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Helpers
# -----------------------------


def safe_image_path(path: str, fallback: str) -> str:
    return path if os.path.exists(path) else fallback


def toast(placeholder, msg: str):
    """High-contrast info message that works in dark & light mode."""
    placeholder.markdown(
        f'<div class="toast">{msg}</div>', unsafe_allow_html=True)


def scroll_to_car():
    st.markdown("""
    <script>
      const el = document.getElementById('car-top');
      if (el) { el.scrollIntoView({behavior: 'smooth', block: 'start'}); }
    </script>
    """, unsafe_allow_html=True)


# -----------------------------
# Session & Model
# -----------------------------
if "car" not in st.session_state:
    st.session_state.car = Car("Renault", "Clio", 2025)
car = st.session_state.car

# -----------------------------
# Header (card)
# -----------------------------
st.markdown("""
<div class="card" style="padding: 16px;">
  <div style="display:flex; align-items:center; gap:12px;">
    <span style="font-size:28px;">🚗</span>
    <div>
      <h1 style="margin:0;">Car Simulator</h1>
      <p style="margin:2px 0 0 0;">Simulate car controls and visualize the internal state before real integration.</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

header_placeholder = st.empty()  # "Current Speed ... | Lights ..."

# -----------------------------
# Image assets (paths)
# -----------------------------
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
wipers_off_img = "w49/images/no_whipers.jpg"

radio_off = "w49/images/radio_off.jpg"
radio_on = "w49/images/radio_on.jpg"

reverse_light_on = "w49/images/reverse_light_on.jpg"
reverse_light_off = "w49/images/reverse_light_off.jpg"

clutch_off_img = "w49/images/not_clutch.jpg"
clutch_on_img = "w49/images/clutch.jpg"

# -----------------------------
# Main layout: Image | Status | Gauge
# -----------------------------
col_img, col_status, col_speed = st.columns([2.0, 1.2, 1.5])

# Left: car image (with anchor)
with col_img:
    st.markdown('<a id="car-top"></a>', unsafe_allow_html=True)
car_image_placeholder = col_img.empty()

# ------------- STATUS GRID (2×2, NO BOX OUTLINES) -------------
# We DO NOT wrap placeholders with HTML. We render the image inside the placeholder,
# so when the placeholder updates, the layout doesn't shift.
with col_status:
    st.markdown('<div class="card"><div class="status-title">Status</div></div>',
                unsafe_allow_html=True)

    row1 = st.columns(2)
    row2 = st.columns(2)

    # Reverse
    with row1[0]:
        st.markdown('<div class="status-title">Reverse</div>',
                    unsafe_allow_html=True)
        reverse_placeholder = st.empty()
        # initial OFF image (keeps layout fixed)
        reverse_placeholder.image(reverse_light_off, width=100, clamp=True)

    # Radio
    with row1[1]:
        st.markdown('<div class="status-title">Radio</div>',
                    unsafe_allow_html=True)
        radio_placeholder = st.empty()
        radio_placeholder.image(radio_off, width=100, clamp=True)

    # Wipers
    with row2[0]:
        st.markdown('<div class="status-title">Wipers</div>',
                    unsafe_allow_html=True)
        wipers_placeholder = st.empty()
        wipers_placeholder.image(safe_image_path(
            wipers_off_img, car_default), width=100, clamp=True)

    # Clutch
    with row2[1]:
        st.markdown('<div class="status-title">Clutch</div>',
                    unsafe_allow_html=True)
        clutch_placeholder = st.empty()
        clutch_placeholder.image(safe_image_path(
            clutch_off_img, car_default), width=100, clamp=True)

# Right: speedometer
speedometer_placeholder = col_speed.empty()

# -----------------------------
# UI update helpers
# -----------------------------


def update_header():
    header_placeholder.markdown(
        f"### Current Speed: **{car.speed} km/h** | Lights: **{'ON' if car.lights else 'OFF'}**"
    )


def update_speedometer():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=car.speed,
        title={'text': "Speed (km/h)", 'font': {'size': 16}},
        gauge={
            'axis': {'range': [0, 200]},
            'bar': {'color': "#2563eb"},
            'bgcolor': "rgba(0,0,0,0)",   # transparent to adapt to theme
            'bordercolor': "#8b8b8b",
            'steps': [
                {'range': [0, 60], 'color': '#8ab4f8'},
                {'range': [60, 120], 'color': '#7aa2f7'},
                {'range': [120, 200], 'color': '#5f8cf5'}
            ]
        }
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",  # transparent
    )
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
    car_image_placeholder.image(get_current_image(), width=480)


def blink_animation(image_path, cycles=6, delay=0.45):
    for _ in range(cycles):
        car_image_placeholder.image(image_path, width=480)
        time.sleep(delay)
        car_image_placeholder.empty()
        time.sleep(delay)
    update_car_image()


# Initialize visuals
update_header()
update_speedometer()
update_car_image()

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["Controls", "Other Controls", "Current State", "Logs"])

# -----------------------------
# Tab 1: Main Controls (carded)
# -----------------------------
with tab1:
    st.markdown('<div class="card"><h3 style="margin:0;">Main Controls</h3></div>',
                unsafe_allow_html=True)
    tab1_feedback = st.empty()  # high-contrast feedback near controls

    # ---- Row 1 ----
    st.markdown('<div class="card">', unsafe_allow_html=True)
    row1 = st.columns(4)
    with row1[0]:
        if st.button("🚀 Accelerate", key="btn_accel"):
            toast(tab1_feedback, car.accelerate())
            update_header()
            update_speedometer()
            scroll_to_car()
    with row1[1]:
        if st.button("🛑 Brake", key="btn_brake"):
            toast(tab1_feedback, car.brake())
            update_header()
            update_speedometer()
            scroll_to_car()
    with row1[2]:
        if st.button("🧰 Clutch Press", key="btn_clutch_press"):
            toast(tab1_feedback, car.clutch_press())
            clutch_placeholder.image(safe_image_path(
                clutch_on_img, car_default), width=100, clamp=True)
            scroll_to_car()
    with row1[3]:
        if st.button("🧰 Clutch Release", key="btn_clutch_release"):
            toast(tab1_feedback, car.clutch_release())
            clutch_placeholder.image(safe_image_path(
                clutch_off_img, car_default), width=100, clamp=True)
            scroll_to_car()
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Row 2 ----
    st.markdown('<div class="card">', unsafe_allow_html=True)
    row2 = st.columns(4)
    with row2[0]:
        if st.button("💡 Lights ON", key="btn_lights_on"):
            toast(tab1_feedback, car.lights_on())
            update_header()
            update_car_image()
            scroll_to_car()
    with row2[1]:
        if st.button("💡 Lights OFF", key="btn_lights_off"):
            toast(tab1_feedback, car.lights_off())
            car.blinkers = None
            car.hazard_lights = False
            update_header()
            update_car_image()
            scroll_to_car()
    with row2[2]:
        if st.button("📻 Radio ON", key="btn_radio_on"):
            toast(tab1_feedback, car.radio_on())
            radio_placeholder.image(radio_on, width=100, clamp=True)
    with row2[3]:
        if st.button("📻 Radio OFF", key="btn_radio_off"):
            toast(tab1_feedback, car.radio_off())
            radio_placeholder.image(radio_off, width=100, clamp=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Row 3 ----
    st.markdown('<div class="card">', unsafe_allow_html=True)
    row3 = st.columns(4)
    with row3[0]:
        if st.button("⬅️ Blinkers LEFT", key="btn_blink_left"):
            toast(tab1_feedback, car.blinkers_left())
            blink_animation(get_current_image())
            scroll_to_car()
    with row3[1]:
        if st.button("➡️ Blinkers RIGHT", key="btn_blink_right"):
            toast(tab1_feedback, car.blinkers_right())
            blink_animation(get_current_image())
            scroll_to_car()
    with row3[2]:
        if st.button("⚠️ Hazard ON", key="btn_hazard_on"):
            toast(tab1_feedback, car.hazard_lights_on())
            blink_animation(get_current_image())
            scroll_to_car()
    with row3[3]:
        if st.button("✅ Hazard OFF", key="btn_hazard_off"):
            toast(tab1_feedback, car.hazard_lights_off())
            car.blinkers = None
            update_car_image()
            scroll_to_car()
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Row 4 (Reset) centered ----
    st.markdown('<div class="card">', unsafe_allow_html=True)
    row4 = st.columns([4, 2, 4])
    with row4[1]:
        if st.button("🔄 Reset Car State", key="btn_reset"):
            st.session_state.car = Car("Renault", "Clio", 2025)
            car = st.session_state.car
            toast(tab1_feedback, "Car state reset successfully!")
            update_header()
            update_speedometer()
            update_car_image()
            reverse_placeholder.image(reverse_light_off, width=100, clamp=True)
            radio_placeholder.image(radio_off, width=100, clamp=True)
            wipers_placeholder.image(safe_image_path(
                wipers_off_img, car_default), width=100, clamp=True)
            clutch_placeholder.image(safe_image_path(
                clutch_off_img, car_default), width=100, clamp=True)
            scroll_to_car()
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Tab 2: Other Controls (carded)
# -----------------------------
with tab2:
    st.markdown('<div class="card"><h3 style="margin:0;">Other Controls</h3></div>',
                unsafe_allow_html=True)
    tab2_feedback = st.empty()

    # ---- Row 1: Reverse + Wipers Slow/Off ----
    st.markdown('<div class="card">', unsafe_allow_html=True)
    row1 = st.columns(4)
    with row1[0]:
        if st.button("🔙 Reverse Light ON", key="btn_rev_on"):
            toast(tab2_feedback, car.reverse_light_on())
            reverse_placeholder.image(reverse_light_on, width=100, clamp=True)
            scroll_to_car()
    with row1[1]:
        if st.button("🔙 Reverse Light OFF", key="btn_rev_off"):
            toast(tab2_feedback, car.reverse_light_off())
            reverse_placeholder.image(reverse_light_off, width=100, clamp=True)
            scroll_to_car()
    with row1[2]:
        if st.button("🌧️ Wipers Slow", key="btn_wipers_slow"):
            toast(tab2_feedback, car.wipers_light())
            wipers_placeholder.image(slow_whipers, width=100, clamp=True)
            scroll_to_car()
    with row1[3]:
        if st.button("🌤️ Wipers OFF", key="btn_wipers_off"):
            if hasattr(car, "wipers_off") and callable(getattr(car, "wipers_off")):
                toast(tab2_feedback, car.wipers_off())
            else:
                car.wipers = "Off"
                if hasattr(car, "log_action"):
                    car.log_action("Wipers Off")
                toast(tab2_feedback, "Wipers turned OFF.")
            wipers_placeholder.image(safe_image_path(
                wipers_off_img, car_default), width=100, clamp=True)
            scroll_to_car()
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Row 2: Wipers Medium & Fast ----
    st.markdown('<div class="card">', unsafe_allow_html=True)
    row2 = st.columns([2, 2, 2])
    with row2[1]:
        if st.button("🌧️ Wipers Medium", key="btn_wipers_med"):
            toast(tab2_feedback, car.wipers_medium())
            wipers_placeholder.image(medium_whipers, width=100, clamp=True)
            scroll_to_car()
    with row2[2]:
        if st.button("⛈️ Wipers Fast", key="btn_wipers_fast"):
            toast(tab2_feedback, car.wipers_fast())
            wipers_placeholder.image(fast_whipers, width=100, clamp=True)
            scroll_to_car()
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Tab 3: Current State (carded)
# -----------------------------
with tab3:
    st.markdown('<div class="card"><h3 style="margin:0;">Current State</h3></div>',
                unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Tab 4: Logs (carded)
# -----------------------------
with tab4:
    st.markdown('<div class="card"><h3 style="margin:0;">Recent Logs</h3></div>',
                unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    try:
        with open("car_events.log", "r") as log_file:
            logs = log_file.readlines()[-50:]
            st.text_area("Logs", value="".join(logs), height=300)
    except FileNotFoundError:
        st.warning("No logs found yet.")
    st.markdown('</div>', unsafe_allow_html=True)
