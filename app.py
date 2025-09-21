import streamlit as st
import random

# --- Safe rerun function for compatibility ---
def safe_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


# --- All 12 standard Valorant maps ---
ALL_MAPS = [
    "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus",
    "Pearl", "Split", "Sunset", "Abyss", "Corrode"
]


# --- Function to set background image and CSS ---
def set_background_image():
    background_image_url = "https://images.alphacoders.com/131/1319702.jpeg"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{background_image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
        .stButton > button:active {{
            transform: translateY(2px);
            box-shadow: 0 2px #51141a;
        }}
        .map-card {{
            background-color: rgba(0, 0, 0, 0.6);
            color: #fff;
            padding: 12px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        .final-map {{
            background-color: rgba(253, 69, 86, 0.8);
            color: #fff;
            padding: 14px;
            border-radius: 12px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            margin: 8px 0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# --- Initialize session state ---
def initialize_session_state():
    if 'available_maps' not in st.session_state:
        st.session_state.available_maps = list(ALL_MAPS)
    if 'banned_maps' not in st.session_state:
        st.session_state.banned_maps = []
    if 'picked_maps' not in st.session_state:
        st.session_state.picked_maps = []
    if 'teams' not in st.session_state:
        st.session_state.teams = {'Team A': '', 'Team B': ''}
    if 'history' not in st.session_state:
        st.session_state.history = []


# --- Ban a map ---
def ban_map(map_name):
    if map_name in st.session_state.available_maps:
        st.session_state.available_maps.remove(map_name)
        st.session_state.banned_maps.append(map_name)
        st.session_state.history.append(f"Banned: {map_name}")
        safe_rerun()


# --- Pick a map ---
def pick_map(map_name):
    if map_name in st.session_state.available_maps:
        st.session_state.available_maps.remove(map_name)
        st.session_state.picked_maps.append(map_name)
        st.session_state.history.append(f"Picked: {map_name}")
        safe_rerun()


# --- Reset the whole state ---
def reset_state():
    st.session_state.available_maps = list(ALL_MAPS)
    st.session_state.banned_maps = []
    st.session_state.picked_maps = []
    st.session_state.history = []
    safe_rerun()


# --- Main App ---
def main():
    set_background_image()
    initialize_session_state()

    st.title("🎮 Valorant Map Veto Tool")

    # Team names
    st.header("Enter Team Names")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.teams['Team A'] = st.text_input("Team A Name", value=st.session_state.teams['Team A'])
    with col2:
        st.session_state.teams['Team B'] = st.text_input("Team B Name", value=st.session_state.teams['Team B'])

    if st.session_state.teams['Team A'] and st.session_state.teams['Team B']:
        st.subheader("Match Sides")
        st.markdown(f"**First Half:**")
        st.markdown(f"**Attacking:** {st.session_state.teams['Team A']}")
        st.markdown(f"**Defending:** {st.session_state.teams['Team B']}")
        st.markdown(f"**Second Half:**")
        st.markdown(f"**Attacking:** {st.session_state.teams['Team B']}")
        st.markdown(f"**Defending:** {st.session_state.teams['Team A']}")

    # Map veto section
    st.header("🗺️ Map Veto & Selection")
    maps_to_keep = st.selectbox(
        "How many maps should remain?",
        [1, 3, 5, 7, 9, 11]
    )

    if len(st.session_state.available_maps) > maps_to_keep:
        st.subheader("Available Maps (Ban Phase):")
        cols = st.columns(3)
        for i, map_name in enumerate(st.session_state.available_maps):
            with cols[i % 3]:
                st.markdown(f"<div class='map-card'>{map_name}</div>", unsafe_allow_html=True)
                if st.button(f"Ban {map_name}", key=f"ban_{map_name}"):
                    ban_map(map_name)

    elif len(st.session_state.picked_maps) < maps_to_keep:
        st.subheader("Pick Maps:")
        cols = st.columns(3)
        for i, map_name in enumerate(st.session_state.available_maps):
            with cols[i % 3]:
                st.markdown(f"<div class='map-card'>{map_name}</div>", unsafe_allow_html=True)
                if st.button(f"Pick {map_name}", key=f"pick_{map_name}"):
                    pick_map(map_name)
    else:
        st.success("✅ Veto complete! The final maps have been chosen.")

    # Show final maps
    st.subheader("🏆 Final Maps")
    if st.session_state.picked_maps:
        for map_name in st.session_state.picked_maps:
            st.markdown(f"<div class='final-map'>{map_name}</div>", unsafe_allow_html=True)
    else:
        st.info("No maps have been picked yet.")

    # History
    st.subheader("📜 Map Ban & Pick History")
    for item in st.session_state.history:
        st.text(item)

    # Reset button
    if st.button("🔄 Reset All"):
        reset_state()


if __name__ == "__main__":
    main()
