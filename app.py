import streamlit as st
import base64

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


# --- Background CSS using local image ---
def set_background_image():
    image_path = "images.jpeg"  # Image file in your repo

    # Encode image as base64
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
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

    # Match Sides Display
    if team_a and team_b:
        st.subheader("Match Sides ⚔️")

        st.markdown("**First Half:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"<div style='background-color:#FD4556; color:white; padding:10px; border-radius:8px; text-align:center;'>⚔️ Attacking<br>{team_a}</div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"<div style='background-color:#3355C3; color:white; padding:10px; border-radius:8px; text-align:center;'>🛡️ Defending<br>{team_b}</div>",
                unsafe_allow_html=True
            )

        st.markdown("**Second Half:**")
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(
                f"<div style='background-color:#FD4556; color:white; padding:10px; border-radius:8px; text-align:center;'>⚔️ Attacking<br>{team_b}</div>",
                unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                f"<div style='background-color:#3355C3; color:white; padding:10px; border-radius:8px; text-align:center;'>🛡️ Defending<br>{team_a}</div>",
                unsafe_allow_html=True
            )

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
        bans_needed = len(ALL_MAPS) - st.session_state.final_map_count
        if len(st.session_state.banned_maps) < bans_needed:
            st.subheader(f"Available Maps (Ban Phase) - {len(st.session_state.available_maps)} left")
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
