import streamlit as st

# --- Safe rerun for compatibility ---
def safe_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


# --- All 12 Valorant maps ---
ALL_MAPS = [
    "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus",
    "Pearl", "Split", "Sunset", "Abyss", "Corrode"
]


# --- Background CSS ---
def set_background_image():
    background_image_url = "https://images.alphacoders.com/131/1319702.jpeg"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{background_image_url}") no-repeat center center fixed !important;
            background-size: cover !important;
        }}
        .block-container {{
            background-color: rgba(0, 0, 0, 0.55) !important;
            border-radius: 12px;
            padding: 20px;
        }}
        .stButton > button {{
            background-color: #FD4556;
            color: white;
            border-radius: 10px;
            border: 2px solid white;
            font-weight: bold;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 4px #992b35;
            padding: 8px 16px;
        }}
        .stButton > button:hover {{
            background-color: #C33543;
            transform: translateY(-2px);
            box-shadow: 0 6px #7c222c;
        }}
        .map-card {{
            background-color: rgba(255,255,255,0.15);
            color: #fff;
            padding: 12px;
            border-radius: 12px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .final-map {{
            background-color: rgba(253, 69, 86, 0.85);
            color: white;
            padding: 14px;
            border-radius: 12px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            margin: 6px 0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# --- Session State ---
def initialize_session_state():
    if 'available_maps' not in st.session_state:
        st.session_state.available_maps = list(ALL_MAPS)
    if 'banned_maps' not in st.session_state:
        st.session_state.banned_maps = []
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'final_map_count' not in st.session_state:
        st.session_state.final_map_count = 0


# --- Ban a map ---
def ban_map(map_name):
    if map_name in st.session_state.available_maps:
        st.session_state.available_maps.remove(map_name)
        st.session_state.banned_maps.append(map_name)
        st.session_state.history.append(f"Banned: {map_name}")
        safe_rerun()


# --- Reset ---
def reset_state():
    st.session_state.available_maps = list(ALL_MAPS)
    st.session_state.banned_maps = []
    st.session_state.history = []
    st.session_state.final_map_count = 0
    safe_rerun()


# --- Main ---
def main():
    set_background_image()
    initialize_session_state()

    st.title("🎮 Valorant Map Veto Tool")

    # Team Names
    st.header("Enter Team Names")
    col1, col2 = st.columns(2)
    with col1:
        team_a = st.text_input("Team A Name", value=st.session_state.get("team_a", ""))
        st.session_state["team_a"] = team_a
    with col2:
        team_b = st.text_input("Team B Name", value=st.session_state.get("team_b", ""))
        st.session_state["team_b"] = team_b

    if team_a and team_b:
        st.subheader("Match Sides")
        st.markdown(f"**First Half:** Attacking → {team_a} | Defending → {team_b}")
        st.markdown(f"**Second Half:** Attacking → {team_b} | Defending → {team_a}")

    # Map veto setup
    st.header("🗺️ Map Veto & Selection")

    if st.session_state.final_map_count == 0:
        maps_to_keep = st.selectbox(
            "How many maps should remain?",
            [1, 3, 5, 7, 9, 11]
        )
        if st.button("Start Ban Phase"):
            st.session_state.final_map_count = maps_to_keep
            safe_rerun()
    else:
        # If still more bans allowed
        bans_needed = len(ALL_MAPS) - st.session_state.final_map_count
        if len(st.session_state.banned_maps) < bans_needed:
            st.subheader("Available Maps (Ban Phase):")
            cols = st.columns(3)
            for i, map_name in enumerate(st.session_state.available_maps):
                with cols[i % 3]:
                    st.markdown(f"<div class='map-card'>{map_name}</div>", unsafe_allow_html=True)
                    if st.button(f"Ban {map_name}", key=f"ban_{map_name}"):
                        ban_map(map_name)
        else:
            st.success("✅ Veto complete! The final maps have been chosen.")
            st.subheader("🏆 Final Maps")
            for map_name in st.session_state.available_maps:
                st.markdown(f"<div class='final-map'>{map_name}</div>", unsafe_allow_html=True)

    # History
    st.subheader("📜 Map Ban History")
    for item in st.session_state.history:
        st.text(item)

    # Reset
    if st.button("🔄 Reset All"):
        reset_state()


if __name__ == "__main__":
    main()
