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

# 3. Comprehensive Story Database
STORY = {
    "entrance": {
        "text": "The sandstone slab seals behind you with a crushing echo. Total dark. Your flashlight cuts through ancient air heavy with dust and the scent of copper. Before you rests an altar carved with rhythmic, pulsing inscriptions.",
        "image": "https://unsplash.com",
        "choices": [
            {"text": "Ignore the altar and step blindly into the main corridor.", "next": "main_hall", "curse": 0, "get_knowledge": None, "get_power": None},
            {"text": "Translate the forbidden glyphs to understand where you are.", "next": "altar_read", "curse": 15, "get_knowledge": "Deity Lore", "get_power": "Third-Eye Vision"}
        ]
    },
    "altar_read": {
        "text": "The symbols burn into your retinas. You learn of Anubis-Set, a fused entity of cosmic decay. A sharp snap echoes inside your skull. Your vision shifts—you can now perceive a faint, heat-signature warmth emanating from organic objects in the dark.",
        "image": "https://unsplash.com",
        "choices": [
            {"text": "Clutch your throbbing head and stumble forward into the main corridor.", "next": "main_hall", "curse": 0, "get_knowledge": None, "get_power": None}
        ]
    },
    "main_hall": {
        "text": "You enter a vast, vaulted chamber. Suddenly, a clicking sound echoes overhead. A heavy stone trap door triggers, dropping down from the ceiling to seal your forward path completely. A standard human cannot lift this sandstone block.",
        "image": "https://unsplash.com",
        "choices": [
            # This choice is always available, but leads to a dead end without powers
            {"text": "Throw your human shoulder against the stone block to force it open.", "next": "trap_fail", "curse": 5, "get_knowledge": None, "get_power": None}
        ],
        # Conditional power choices will be appended dynamically below
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
        "image": "https://unsplash.com",
        "choices": [] # Next story branches go here
    },
    "trap_fail": {
        "text": "Your human bones fracture against the block. You are trapped in the dark as cold, wet breathing echoes from the shadows behind you.",
        "image": "https://unsplash.com",
        "choices": []
    }
}

# 4. Generate the Perimeter Matrix Data
HIEROGLYPH_BANK = ["𓁹", "𓃠", "𓆗", "𓅃", "𓀾", "𓋹", "𓎬", "𓆣", "𓇳", "𓆙", "𓁶", "𓃓"]
TOTAL_BORDER_SLOTS = 20  # 6 top, 6 bottom, 4 left, 4 right

# Calculate active cells dynamically based on curse progress
active_slots_count = int((st.session_state.curse / 100) * TOTAL_BORDER_SLOTS)

# Ensure that if they have gained knowledge but math rounds slots to 0, at least 1 shows up
if st.session_state.knowledge and active_slots_count == 0:
    active_slots_count = 1

# Compile HTML string array for building the border frame layout
border_cells = []
for i in range(TOTAL_BORDER_SLOTS):
    if i < active_slots_count:
        glyph = HIEROGLYPH_BANK[i % len(HIEROGLYPH_BANK)]
        border_cells.append(f'<div class="glyph-slot active-glyph">{glyph}</div>')
    else:
        border_cells.append('<div class="glyph-slot empty-slot"></div>')

# 5. Inject Custom Structural Layout Layout & CSS UI Engine
custom_css = f"""
<style>
    .game-grid-container {{
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        grid-gap: 10px;
        background-color: #060708;
        padding: 20px;
        border-radius: 14px;
        max-width: 950px;
        margin: 0 auto;
        border: 1px solid #1a1f26;
    }}
    .glyph-slot {{
        display: flex;
        align-items: center;
        justify-content: center;
        aspect-ratio: 1 / 1;
        font-size: 2rem;
        border-radius: 6px;
        transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .empty-slot {{
        border: 2px dashed #1e222b;
        background-color: #0b0d12;
    }}
    .active-glyph {{
        border: 2px solid #6b1111;
        background-color: #1f0707;
        color: #ff453a;
        text-shadow: 0px 0px 10px #ff453a;
        box-shadow: inset 0 0 12px rgba(255,69,58,0.15);
    }}
    .viewport-screen {{
        grid-column: 2 / 6;
        grid-row: 2 / 5;
        background-color: #0f1115;
        border: 2px solid #232731;
        border-radius: 8px;
        padding: 24px;
        color: #f1f5f9;
    }}
    .vn-text {{
        font-size: 1.2rem;
        line-height: 1.65;
        margin-top: 18px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 6. Render Layout Map Structure
current_node = STORY.get(st.session_state.scene, STORY["entrance"])

# Construct complete perimeter mapping manually for pixel-perfect slot positioning
grid_html = f"""
<div class="game-grid-container">
    <!-- Top Row Boundary Frame (Slots 0 - 5) -->
    {border_cells[0]}{border_cells[1]}{border_cells[2]}{border_cells[3]}{border_cells[4]}{border_cells[5]}
    
    <!-- Row 2 Frame Layout -->
    {border_cells[19]}
    <div class="viewport-screen">
        <img src="{current_node['image']}" style="width:100%; border-radius:6px; max-height:320px; object-fit:cover; border-bottom: 2px solid #232731;">
        <p class="vn-text">{current_node['text']}</p>
    </div>
    {border_cells[6]}
    
    <!-- Row 3 Frame Layout -->
    {border_cells[18]}
    {border_cells[7]}
    
    <!-- Row 4 Frame Layout -->
    {border_cells[17]}
    {border_cells[8]}
    
    <!-- Bottom Row Boundary Frame (Slots 11 - 16) -->
    {border_cells[16]}{border_cells[15]}{border_cells[14]}{border_cells[13]}{border_cells[12]}{border_cells[11]}
</div>
"""
st.markdown(grid_html, unsafe_allow_html=True)
st.write(" ") 

# 7. Dynamic Action Button Input Processing
# Extract active options configuration list
available_choices = list(current_node["choices"])

# Inject conditional hidden powers routes dynamically if requirements are met
if "power_choices" in current_node:
    for p_choice in current_node["power_choices"]:
        if p_choice["requires_power"] in st.session_state.powers:
            available_choices.append(p_choice)

# Render choice buttons
if available_choices:
    cols = st.columns(len(available_choices))
    for index, choice in enumerate(available_choices):
        with cols[index]:
            # Highlight special supernatural actions visually using button labels
            label = choice["text"]
            if "requires_power" in choice:
                label = f"👁️ [MUTATED CHOICE] {label}"
                
            if st.button(label, key=f"act_{index}", use_container_width=True):
                # Update core states on click
                st.session_state.scene = choice["next"]
                st.session_state.curse = min(100, st.session_state.curse + choice["curse"])
                
                if choice["get_knowledge"]:
                    st.session_state.knowledge.append(choice["get_knowledge"])
                if choice["get_power"]:
                    st.session_state.powers.append(choice["get_power"])
                    
                st.rerun()
else:
    # Terminal State Catch Block
    if st.session_state.curse >= 100:
        st.error("### Complete Apotheosis: You belong to the tomb now.")
    else:
        st.warning("### Fatal End: Lost eternally within the shifting walls.")
        
    if st.button("Awaken back at the threshold (Restart Game)", use_container_width=True):
        st.session_state.clear()
        st.rerun()