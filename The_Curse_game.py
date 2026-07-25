import streamlit as st

# Configure canvas framework 
st.set_page_config(page_title="Tomb of the Unspoken", layout="wide")

# 1. Initialize Game State Metrics
if "scene" not in st.session_state:
    st.session_state.scene = "entrance"
    st.session_state.curse = 0          # Ranges from 0 to 100
    st.session_state.knowledge = []     
    st.session_state.powers = []        

# 2. Sidebar Settings & Diagnostics Panel
with st.sidebar:
    st.title("𓋹 Archeologist Toolkit")
    st.subheader("System Configuration")
    text_speed = st.slider("Text Rendering Cadence", 1, 10, 5)
    audio_toggle = st.checkbox("Enable Ambient Sub-Bass", value=True)
    
    st.divider()
    st.subheader("Manifested Abilities")
    if not st.session_state.powers:
        st.info("You possess no anomalies. Your body is entirely human.")
    else:
        for power in st.session_state.powers:
            st.error(f"𓏢 {power}")

    st.divider()
    if st.button("Abandon Descent (Reset Expedition)", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# 3. Comprehensive Story Database with Public Domain Images
STORY = {
    "entrance": {
        "text": "The sandstone slab seals behind you with a crushing echo. Total dark. Your flashlight cuts through ancient air heavy with dust and the scent of copper. Before you rests an altar carved with rhythmic, pulsing inscriptions.",
        "image": "https://wikimedia.org",
        "choices": [
            {"text": "Ignore the altar and step blindly into the main corridor.", "next": "main_hall", "curse": 0, "get_knowledge": None, "get_power": None},
            {"text": "Translate the forbidden glyphs to understand where you are.", "next": "altar_read", "curse": 20, "get_knowledge": "Deity Lore", "get_power": "Third-Eye Vision"}
        ]
    },
    "altar_read": {
        "text": "The symbols burn into your retinas. You learn of Anubis-Set, a fused entity of cosmic decay. A sharp snap echoes inside your skull. Your vision shifts—you can now perceive a faint, heat-signature warmth emanating from organic objects in the dark.",
        "image": "https://wikimedia.org",
        "choices": [
            {"text": "Clutch your throbbing head and stumble forward into the main corridor.", "next": "main_hall", "curse": 0, "get_knowledge": None, "get_power": None}
        ]
    },
    "main_hall": {
        "text": "You enter a vast, vaulted chamber. Suddenly, a clicking sound echoes overhead. A heavy stone trap door triggers, dropping down from the ceiling to seal your forward path completely. A standard human cannot lift this sandstone block.",
        "image": "https://wikimedia.org",
        "choices": [
            {"text": "Throw your human shoulder against the stone block to force it open.", "next": "trap_fail", "curse": 5, "get_knowledge": None, "get_power": None}
        ],
        "power_choices": [
            {
                "requires_power": "Third-Eye Vision",
                "text": "Use your Third-Eye Vision to look through the solid stone for an alternate mechanisms layout.",
                "next": "bypass_trap",
                "curse": 25,
                "get_knowledge": "Tomb Structural Flow",
                "get_power": "Chitinous Muscle Reshaping"
            }
        ]
    },
    "bypass_trap": {
        "text": "Your anomalies pierce the density of the rock, showing you a hidden pressure plate behind the masonry. You bypass the obstacle safely, but your muscle fibers tear and stitch back together as dense, fibrous black chitin. You are evolving.",
        "image": "https://wikimedia.org",
        "choices": [] 
    },
    "trap_fail": {
        "text": "Your human bones fracture against the block. You are trapped in the dark as cold, wet breathing echoes from the shadows behind you.",
        "image": "https://wikimedia.org",
        "choices": []
    }
}

# 4. Generate Symmetrical Hieroglyph Placements
HIEROGLYPH_BANK = ["𓁹", "𓃠", "𓆗", "𓅃", "𓀾", "𓋹", "𓎬", "𓆣", "𓇳", "𓆙", "𓁶", "𓃓", "𓅓", "𓎛", "𓏢", "𓆏"]
TOTAL_BORDER_SLOTS = 16

# Determine how many slots to activate based on curse percent
active_slots_count = int((st.session_state.curse / 100) * TOTAL_BORDER_SLOTS)
if st.session_state.knowledge and active_slots_count == 0:
    active_slots_count = 1

# Symmetrical growth sequence beginning exactly at the center offsets
activation_priority = [
    "t3", "b3", "l2", "r2",  # Generation 1: True Center of all 4 borders
    "t2", "t4", "b2", "b4",  # Generation 2: Spreading horizontally outwards
    "l1", "l3", "r1", "r3",  # Generation 3: Spreading vertically outwards
    "t1", "t5", "b1", "b5"   # Generation 4: Completing the outer bounds
]
active_slots_set = set(activation_priority[:active_slots_count])

def make_glyph_html(slot_id, inline_css_coords, bank_idx):
    """Generates individual layered glyph element absolute markup strings"""
    if slot_id in active_slots_set:
        glyph = HIEROGLYPH_BANK[bank_idx % len(HIEROGLYPH_BANK)]
        return f'<div class="glyph-slot active-glyph" style="{inline_css_coords}">{glyph}</div>'
    else:
        return f'<div class="glyph-slot empty-slot" style="{inline_css_coords}"></div>'

# 5. Build Layered Content Layout & Inject Absolute Position Styles
custom_css = """
<style>
    /* Absolute Positioning Core Engine Sandbox Wrapper */
    .canvas-container {
        position: relative;
        width: 80%;               /* Takes up exactly 80% width layout screen */
        float: left;              /* Flush Left alignment structural constraint */
        background-color: #c2b280; /* Desert Sand Tan solid frame color */
        padding: 200px;           /* Pushes interior contents in from frame bounds */
        box-sizing: border-box;
        border-radius: 12px;
        min-height: 850px;
    }

    /* Central Core Screen Framework Container */
    .viewport-screen {
        background-color: #0f1115;
        border: 4px solid #232731;
        border-radius: 8px;
        padding: 20px;
        color: #f1f5f9;
        width: 100%;
        height: 450px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
    }
    .viewport-screen img {
        width: 100%; 
        border-radius: 6px; 
        height: 270px; 
        object-fit: cover; 
        border-bottom: 2px solid #232731;
        filter: grayscale(100%) contrast(140%) brightness(75%);
    }
    .vn-text {
        font-size: 1.1rem;
        line-height: 1.5;
        margin-top: 12px;
    }

    /* Layered Foreground Custom Elements (2" wide by 3" tall visual aspect equivalent) */
    .glyph-slot {
        position: absolute;
        z-index: 10;              /* Forces elements on top of sand background */
        display: flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 90px;
        font-size: 2.2rem;
        border-radius: 6px;
        transition: all 0.5s ease-in-out;
    }
    .empty-slot {
        border: 2px dashed rgba(30, 34, 43, 0.4);
        background-color: rgba(11, 13, 18, 0.2);
    }
    .active-glyph {
        border: 2px solid #6b1111;
        background-color: #1f0707;
        color: #ff453a;
        text-shadow: 0px 0px 10px #ff453a;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.5);
    }
    
    /* Clean layout formatting fix to isolate choices area properly */
    .actions-block {
        clear: both;
        width: 80%;
        padding-top: 24px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 6. Render Stacking Layer Map Interface
current_node = STORY.get(st.session_state.scene, STORY["entrance"])

# Absolute Coordinate Computations for 5 across top/bottom, 3 vertically on sides
# Offsets map to center nicely within the 200px padding perimeter around the center block
layer_markup = f"""
<div class="canvas-container">
    <!-- Centered Game Content Screen Viewport -->
    <div class="viewport-screen">
        <img src="{current_node['image']}">
        <p class="vn-text">{current_node['text']}</p>
    </div>

    <!-- Top Border Horizontal Chain (5 Items distributed across) -->
    {make_glyph_html('t1', 'top: 55px; left: calc(20% + 0px);', 0)}
    {make_glyph_html('t2', 'top: 55px; left: calc(20% + 110px);', 1)}
    {make_glyph_html('t3', 'top: 55px; left: calc(50% - 30px);', 2)}   <!-- TRUE TOP CENTER -->
    {make_glyph_html('t4', 'top: 55px; right: calc(20% + 110px);', 3)}
    {make_glyph_html('t5', 'top: 55px; right: calc(20% + 0px);', 4)}

    <!-- Bottom Border Horizontal Chain (5 Items distributed across) -->
    {make_glyph_html('b1', 'bottom: 55px; left: calc(20% + 0px);', 5)}
    {make_glyph_html('b2', 'bottom: 55px; left: calc(20% + 110px);', 6)}
    {make_glyph_html('b3', 'bottom: 55px; bottom: 55px; left: calc(50% - 30px);', 7)} <!-- TRUE BOTTOM CENTER -->
    {make_glyph_html('b4', 'bottom: 55px; right: calc(20% + 110px);', 8)}
    {make_glyph_html('b5', 'bottom: 55px; right: calc(20% + 0px);', 9)}

    <!-- Left Border Vertical Chain (3 Items stacked) -->
    {make_glyph_html('l1', 'top: calc(20% + 40px); left: 70px;', 10)}
    {make_glyph_html('l2', 'top: calc(50% - 45px); left: 70px;', 11)}  <!-- TRUE LEFT CENTER -->
    {make_glyph_html('l3', 'bottom: calc(20% + 40px); left: 70px;', 12)}

    <!-- Right Border Vertical Chain (3 Items stacked) -->
    {make_glyph_html('r1', 'top: calc(20% + 40px); right: 70px;', 13)}
    {make_glyph_html('r2', 'top: calc(50% - 45px); right: 70px;', 14)} <!-- TRUE RIGHT CENTER -->
    {make_glyph_html('r3', 'bottom: calc(20% + 40px); right: 70px;', 15)}"""
st.markdown(layer_markup, unsafe_allow_html=True)
