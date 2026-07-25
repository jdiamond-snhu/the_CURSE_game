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
            {"text": "Translate the forbidden glyphs to understand where you are.", "next": "altar_read", "curse": 15, "get_knowledge": "Deity Lore", "get_power": "Third-Eye Vision"}
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
                "curse": 20,
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

# 4. Generate Perimeter Matrix Data (16 Total Perimeter Slots)
HIEROGLYPH_BANK = ["𓁹", "𓃠", "𓆗", "𓅃", "𓀾", "𓋹", "𓎬", "𓆣", "𓇳", "𓆙", "𓁶", "𓃓", "𓅓", "𓎛", "𓏢", "𓆏"]
TOTAL_BORDER_SLOTS = 16

# Calculate active cells dynamically based on curse progress
active_slots_count = int((st.session_state.curse / 100) * TOTAL_BORDER_SLOTS)

# Ensure at least 1 glyph illuminates if knowledge has been acquired
if st.session_state.knowledge and active_slots_count == 0:
    active_slots_count = 1

# Pre-populate glyph items dictionary for precise grid generation mapping
slots = {}
for i in range(1, TOTAL_BORDER_SLOTS + 1):
    if i <= active_slots_count:
        glyph = HIEROGLYPH_BANK[(i - 1) % len(HIEROGLYPH_BANK)]
        slots[f"s{i}"] = f'<div class="glyph-slot active-glyph">{glyph}</div>'
    else:
        slots[f"s{i}"] = '<div class="glyph-slot empty-slot"></div>'

# 5. Inject Custom Structural Layout Layout & CSS UI Engine
custom_css = """
<style>
    /* Centers the overall visual novel container on screen */
    .game-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        max-width: 1000px;
        padding-top: 10px;
    }

    /* 7x5 Grid Matrix Layout targeting your requested side counts */
    .game-grid-container {
        display: grid;
        grid-template-columns: repeat(7, auto);
        grid-gap: 12px;
        background-color: #060708;
        padding: 24px;
        border-radius: 14px;
        border: 1px solid #1a1f26;
        align-items: center;
        justify-content: center;
    }

    /* Custom 2" width by 3" height visual ratio styling per block */
    .glyph-slot {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 90px;
        font-size: 2.2rem;
        border-radius: 6px;
        transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
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
        box-shadow: inset 0 0 12px rgba(255,69,58,0.15);
    }

    /* Central Viewport Screen encompassing the 5x3 internal zone */
    .viewport-screen {
        grid-column: 2 / 7;
        grid-row: 2 / 5;
        background-color: #0f1115;
        border: 2px solid #232731;
        border-radius: 8px;
        padding: 20px;
        color: #f1f5f9;
        width: 600px;
        height: 410px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .viewport-screen img {
        width: 100%; 
        border-radius: 6px; 
        height: 240px; 
        object-fit: cover; 
        border-bottom: 2px solid #232731;
        filter: grayscale(100%) contrast(140%) brightness(80%);
    }
    .vn-text {
        font-size: 1.1rem;
        line-height: 1.5;
        margin-top: 10px;
        overflow-y: auto;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 6. Render Structural Frame Structure 
current_node = STORY.get(st.session_state.scene, STORY["entrance"])

# Re-assembled layout map creating perfect side slot counts (5 top/bottom, 3 left/right)
grid_html = f"""
<div class="game-wrapper">
    <div class="game-grid-container">
        <!-- Top Perimeter Boundary Row (5 Slots spanning columns 2 through 6) -->
        <div></div> {slots['s1']} {slots['s2']} {slots['s3']} {slots['s4']} {slots['s5']} <div></div>
        
        <!-- Interior Row 1 Framework Layout -->
        {slots['s14']}
        <div class="viewport-screen">
            <img src="{current_node['image']}">
            <p class="vn-text">{current_node['text']}</p>
        </div>
        {slots['s6']}
        
        <!-- Interior Row 2 Framework Layout -->
        {slots['s13']} {slots['s7']}
        
        <!-- Interior Row 3 Framework Layout -->
        {slots['s12']} {slots['s8']}
        
        <!-- Bottom Perimeter Boundary Row (5 Slots spanning columns 2 through 6) -->
        <div></div> {slots['s11']} {slots['s10']} {slots['s9']} {slots['s15']} {slots['s16']} <div></div>
    </div>
</div>
"""
st.markdown(grid_html, unsafe_allow_html=True)
st.write(" ") 

# 7. Dynamic Action Button Input Processing
available_choices = list(current_node["choices"])

if "power_choices" in current_node:
    for p_choice in current_node["power_choices"]:
        if p_choice["requires_power"] in st.session_state.powers:
            available_choices.append(p_choice)

if available_choices:
    # Anchor the choice options directly beneath our centered canvas box wrapper
    col_spacer_left, col_content, col_spacer_right = st.columns([1, 2, 1])
    with col_content:
        for index, choice in enumerate(available_choices):
            label = choice["text"]
            if "requires_power" in choice:
                label = f"👁️ [MUTATED CHOICE] {label}"
                
            if st.button(label, key=f"act_{index}", use_container_width=True):
                st.session_state.scene = choice["next"]
                st.session_state.curse = min(100, st.session_state.curse + choice["curse"])
                
                if choice["get_knowledge"]:
                    st.session_state.knowledge.append(choice["get_knowledge"])
                if choice["get_power"]:
                    st.session_state.powers.append(choice["get_power"])
                    
                st.rerun()
else:
    col_spacer_left, col_content, col_spacer_right = st.columns([1, 2, 1])
