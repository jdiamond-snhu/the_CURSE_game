import streamlit as st

# Configure canvas framework for an immersive visual experience
st.set_page_config(page_title="Tomb of the Unspoken", layout="wide")

# 1. Initialize Game State Metrics
if "scene" not in st.session_state:
    st.session_state.scene = "entrance"
    st.session_state.curse = 0          # Ranges from 0 to 100
    st.session_state.knowledge = []     # Tracks discovered lore items
    st.session_state.powers = []        # Tracks unlocked supernatural traits

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

# 4. Generate Centered Perimeter Grid Data
HIEROGLYPH_BANK = ["𓁹", "𓃠", "𓆗", "𓅃", "𓀾", "𓋹", "𓎬", "𓆣", "𓇳", "𓆙", "𓁶", "𓃓", "𓅓", "𓎛", "𓏢", "𓆏"]
TOTAL_BORDER_SLOTS = 16

# Determine how many total slots should reveal symbols based on current curse percentage
active_slots_count = int((st.session_state.curse / 100) * TOTAL_BORDER_SLOTS)

# Ensure at least 1 glyph illuminates if knowledge has been acquired
if st.session_state.knowledge and active_slots_count == 0:
    active_slots_count = 1

# Define priority layout maps for each side growing outwards from the exact centers
# Map layout numbers to specific slots: Top (T), Bottom (B), Left (L), Right (R)
activation_priority = [
    "T3", "B3", "L2", "R2",  # Generation 1: True centers of each of the four walls
    "T2", "T4", "B2", "B4",  # Generation 2: Spreading outward on top and bottom
    "L1", "L3", "R1", "R3",  # Generation 3: Spreading outward on left and right walls
    "T1", "T5", "B1", "B5"   # Generation 4: Corner-adjacent slots completing the frame
]

# Track which slots are currently active
active_slots_set = set(activation_priority[:active_slots_count])

def render_slot(slot_id, glyph_index):
    """Helper to return active or empty slot html structures"""
    if slot_id in active_slots_set:
        glyph = HIEROGLYPH_BANK[glyph_index % len(HIEROGLYPH_BANK)]
        return f'<div class="glyph-slot active-glyph">{glyph}</div>'
    else:
        return '<div class="glyph-slot empty-slot"></div>'

# Build mapping dictionary for every position in our 7x5 matrix framework
slots = {
    # Top wall slots (1 to 5)
    "t1": render_slot("T1", 0), "t2": render_slot("T2", 1), "t3": render_slot("T3", 2), "t4": render_slot("T4", 3), "t5": render_slot("T5", 4),
    # Left wall slots (1 to 3)
    "l1": render_slot("L1", 5), "l2": render_slot("L2", 6), "l3": render_slot("L3", 7),
    # Right wall slots (1 to 3)
    "r1": render_slot("R1", 8), "r2": render_slot("R2", 9), "r3": render_slot("R3", 10),
    # Bottom wall slots (1 to 5)
    "b1": render_slot("B1", 11), "b2": render_slot("B2", 12), "b3": render_slot("B3", 13), "b4": render_slot("B4", 14), "b5": render_slot("B5", 15)
}

# 5. Inject Clean Structural Grid Layout CSS
custom_css = """
<style>
    .game-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        max-width: 1000px;
        padding-top: 10px;
    }
    .game-grid-container {
        display: grid;
        grid-template-columns: repeat(7, 60px); /* Strict element widths */
        grid-template-rows: repeat(5, 90px);   /* Strict element heights */
        grid-gap: 12px;
        background-color: #060708;
        padding: 24px;
        border-radius: 14px;
        border: 1px solid #1a1f26;
        justify-content: center;
    }
    .glyph-slot {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 90px;
        font-size: 2.2rem;
        border-radius: 6px;
    }
    .empty-slot {
        border: 2px dashed #1e222b;
        background-color: #0b0d12;
    }
    .active-glyph {
        border: 2px solid #6b1111;
        background-color: #1f0707;
        color: #ff453a;
        text-shadow: 0px 0px 10px #ff453a;
    }
    .viewport-screen {
        grid-column: 2 / 7;
        grid-row: 2 / 5;
        background-color: #0f1115;
        border: 2px solid #232731;
        border-radius: 8px;
        padding: 20px;
        color: #f1f5f9;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 100%;
        height: 100%;
        box-sizing: border-box;
    }
    .viewport-screen img {
        width: 100%; 
        border-radius: 6px; 
        height: 160px; 
        object-fit: cover; 
        border-bottom: 2px solid #232731;
        filter: grayscale(100%) contrast(140%) brightness(80%);
    }
    .vn-text {
        font-size: 1rem;
        line-height: 1.4;
        margin-top: 8px;
        overflow-y: auto;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 6. Render Structural Frame Structure 
current_node = STORY.get(st.session_state.scene, STORY["entrance"])

# Every grid cell is now explicitly wrapped in valid HTML elements to prevent layout collapses
grid_html = f"""
<div class="game-wrapper">
    <div class="game-grid-container">
        <!-- Row 1 -->
        <div class="corner-space"></div>
        {slots['t1']} {slots['t2']} {slots['t3']} {slots['t4']} {slots['t5']}
        <div class="corner-space"></div>
        
        <!-- Row 2 -->
        {slots['l1']}
        <div class="viewport-screen">
            <img src="{current_node['image']}">
            <p class="vn-text">{current_node['text']}</p>
        </div>
        {slots['r1']}
        
        <!-- Row 3 -->
        {slots['l2']}
        <!-- Hidden underlying spacer to let the viewport take control of middle tracks -->
        <div style="grid-column: 2 / 7; grid-row: 3 / 4; pointer-events: none;"></div>
        {slots['r2']}
        
        <!-- Row 4 -->
        {slots['l3']}
        <div style="grid-column: 2 / 7; grid-row: 4 / 5; pointer-events: none;"></div>
        {slots['r3']}
        
        <!-- Row 5 -->
        <div class="corner-space"></div>
        {slots['b1']} {slots['b2']} {slots['b3']} {slots['b4']} {slots['b5']}
        <div class="corner-space"></div>
    </div>
</div>
"""
st.markdown(grid_html, unsafe_allow_html=True)
st.write(" ") 
