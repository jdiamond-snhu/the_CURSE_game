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

# 5. Inject Scaled Custom Layout & CSS UI Engine (Scaled to 70%)
custom_css = """
<style>
    /* Absolute Positioning Sandbox Wrapper (Scaled to 70%) */
    .canvas-container {
        position: relative;
        width: 56%;                /* 70% of previous 80% screen width constraint */
        float: left;               /* Flush Left alignment */
        background-color: #c2b280;  /* Desert Sand Tan solid frame color */
        padding: 140px;            /* Scaled down from 200px padding perimeter */
        box-sizing: border-box;
        border-radius: 12px;
        min-height: 595px;         /* Scaled down from 850px height */
    }

    /* Central Core Screen Framework Container (Scaled to 70%) */
    .viewport-screen {
        background-color: #0f1115;
        border: 3px solid #232731;
        border-radius: 8px;
        padding: 14px;
        color: #f1f5f9;
        width: 100%;
        height: 315px;             /* Scaled down from 450px height */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
    }
    .viewport-screen img {
        width: 100%; 
        border-radius: 6px; 
        height: 189px;             /* Scaled down from 270px height */
        object-fit: cover; 
        border-bottom: 2px solid #232731;
        filter: grayscale(100%) contrast(140%) brightness(75%);
    }
    .vn-text {
        font-size: 0.95rem;        /* Marginally smaller text for compact layout */
        line-height: 1.4;
        margin-top: 8px;
    }

    /* Foreground Elements (Maintained 2"x3" structural box equivalency) */
    .glyph-slot {
        position: absolute;
        z-index: 10;               /* Layer directly on top of the sand background */
        display: flex;
        align-items: center;
        justify-content: center;
        width: 42px;               /* Width scaled to 70% of 60px */
        height: 63px;              /* Height scaled to 70% of 90px */
        font-size: 1.54rem;        /* Font size scaled to 70% of 2.2rem */
        border-radius: 4px;
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
        text-shadow: 0px 0px 8px #ff453a;
        box-shadow: 0px 3px 6px rgba(0,0,0,0.5);
    }
    
    /* Formatting barrier layout rule */
    .actions-block {
        clear: both;
        width: 56%;                /* Matches the scaled canvas wrapper width */
        padding-top: 18px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 6. Render Stacking Layer Map Interface (Coordinates scaled to 70%)
current_node = STORY.get(st.session_state.scene, STORY["entrance"])

# Every absolute positioning calculation has been adjusted down by 30% to fit the tighter perimeter 
layer_markup = f"""
<div class="canvas-container">
    <div class="viewport-screen">
        <img src="{current_node['image']}">
        <p class="vn-text">{current_node['text']}</p>
    </div>

    {make_glyph_html('t1', 'top: 38px; left: calc(20% + 0px);', 0)}
    {make_glyph_html('t2', 'top: 38px; left: calc(20% + 77px);', 1)}
    {make_glyph_html('t3', 'top: 38px; left: calc(50% - 21px);', 2)}
    {make_glyph_html('t4', 'top: 38px; right: calc(20% + 77px);', 3)}
    {make_glyph_html('t5', 'top: 38px; right: calc(20% + 0px);', 4)}

    {make_glyph_html('b1', 'bottom: 38px; left: calc(20% + 0px);', 5)}
    {make_glyph_html('b2', 'bottom: 38px; left: calc(20% + 77px);', 6)}
    {make_glyph_html('b3', 'bottom: 38px; left: calc(50% - 21px);', 7)}
    {make_glyph_html('b4', 'bottom: 38px; right: calc(20% + 77px);', 8)}
    {make_glyph_html('b5', 'bottom: 38px; right: calc(20% + 0px);', 9)}

    {make_glyph_html('l1', 'top: calc(20% + 28px); left: 49px;', 10)}
    {make_glyph_html('l2', 'top: calc(50% - 31px); left: 49px;', 11)}
    {make_glyph_html('l3', 'bottom: calc(20% + 28px); left: 49px;', 12)}

    {make_glyph_html('r1', 'top: calc(20% + 28px); right: 49px;', 13)}
    {make_glyph_html('r2', 'top: calc(50% - 31px); right: 49px;', 14)}
    {make_glyph_html('r3', 'bottom: calc(20% + 28px); right: 49px;', 15)}
</div>
"""
st.markdown(layer_markup, unsafe_allow_html=True)

# 7. Action Processing Layer Input (Perfect Edge-to-Edge Alignment)
available_choices = list(current_node["choices"])

if "power_choices" in current_node:
    for p_choice in current_node["power_choices"]:
        if p_choice["requires_power"] in st.session_state.powers:
            available_choices.append(p_choice)

# This wrapper forces the columns to stretch exactly to the edges of your 56% display footprint
st.markdown('<div class="actions-block">', unsafe_allow_html=True)

if available_choices:
    # Generates equal-width column segments across the display block width
    cols = st.columns(len(available_choices))
    
    for index, choice in enumerate(available_choices):
        with cols[index]:
            label = choice["text"]
            if "requires_power" in choice:
                label = f"👁️ {label}"
                
            # use_container_width=True forces each button to expand to the full width of its column
            if st.button(label, key=f"act_{index}", use_container_width=True):
                st.session_state.scene = choice["next"]
                st.session_state.curse = min(100, st.session_state.curse + choice["curse"])
                
                if choice["get_knowledge"]:
                    st.session_state.knowledge.append(choice["get_knowledge"])
                if choice["get_power"]:
                    st.session_state.powers.append(choice["get_power"])
                    
                st.rerun()
else:
    if st.session_state.curse >= 100:
        st.error("### Complete Apotheosis: You belong to the tomb now.")
    else:
        st.warning("### Fatal End: Lost eternally within the shifting walls.")
        
    if st.button("Awaken back at the threshold (Restart Game)", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
