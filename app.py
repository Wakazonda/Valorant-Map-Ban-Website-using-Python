import streamlit as st
import random

# All 12 standard Valorant maps
ALL_MAPS = [
    "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus",
    "Pearl", "Split", "Sunset", "Abyss", "Corrode"
]


# --- Function to set background image ---
def set_background_image():
    """Sets a Valorant-themed background image using a URL and custom CSS."""
    # Using a Valorant-themed wallpaper from a public source.
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
        }}
        .stButton > button {{
            background-color: #FD4556;
            color: white;
            border-radius: 8px;
            border: 2px solid white;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 4px #992b35;
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
        .stSlider, .stNumberInput, .stTextInput {{
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# --- Session State Initialization ---
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


def ban_map(map_name):
    """Move a map from available to banned list."""
    if map_name in st.session_state.available_maps:
        st.session_state.available_maps.remove(map_name)
        st.session_state.banned_maps.append(map_name)
        st.session_state.history.append(f"Banned: {map_name}")
        st.rerun()


def pick_map(map_name):
    """Move a map from available to picked list."""
    if map_name in st.session_state.available_maps:
        st.session_state.available_maps.remove(map_name)
        st.session_state.picked_maps.append(map_name)
        st.session_state.history.append(f"Picked: {map_name}")
        st.rerun()


def reset_state():
    """Reset the app to its initial state."""
    st.session_state.available_maps = list(ALL_MAPS)
    st.session_state.banned_maps = []
    st.session_state.picked_maps = []
    st.session_state.history = []
    st.rerun()


# --- Main app logic ---
def main():
    set_background_image()
    initialize_session_state()

    st.title("Valorant Map Veto Tool")

    # Team Name Inputs
    st.header("Enter Team Names")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.teams['Team A'] = st.text_input("Team A Name", value=st.session_state.teams['Team A'])
    with col2:
        st.session_state.teams['Team B'] = st.text_input("Team B Name", value=st.session_state.teams['Team B'])

    # Display Attack/Defense Sides
    if st.session_state.teams['Team A'] and st.session_state.teams['Team B']:
        st.subheader("Match Sides")
        st.markdown(f"**First Half:**")
        st.markdown(f"**Attacking:** {st.session_state.teams['Team A']}")
        st.markdown(f"**Defending:** {st.session_state.teams['Team B']}")
        st.markdown(f"**Second Half:**")
        st.markdown(f"**Attacking:** {st.session_state.teams['Team B']}")
        st.markdown(f"**Defending:** {st.session_state.teams['Team A']}")

    # Map Selection Options
    st.header("Map Veto & Selection")
    maps_to_keep = st.selectbox(
        "How many maps should remain?",
        [1, 3, 5, 7, 9, 11]
    )

    if len(st.session_state.available_maps) > maps_to_keep:
        st.subheader("Available Maps:")
        cols = st.columns(3)
        for i, map_name in enumerate(st.session_state.available_maps):
            with cols[i % 3]:
                if st.button(f"Ban {map_name}", key=f"ban_{map_name}"):
                    ban_map(map_name)

    elif len(st.session_state.picked_maps) < maps_to_keep:
        st.subheader("Pick Maps:")
        cols = st.columns(3)
        for i, map_name in enumerate(st.session_state.available_maps):
            with cols[i % 3]:
                if st.button(f"Pick {map_name}", key=f"pick_{map_name}"):
                    pick_map(map_name)
    else:
        st.success("Veto complete! The final maps have been chosen.")

    st.subheader("Final Maps")
    if st.session_state.picked_maps:
        for map_name in st.session_state.picked_maps:
            st.info(map_name)
    else:
        st.info("No maps have been picked yet.")

    st.subheader("Map Ban History")
    for item in st.session_state.history:
        st.text(item)

    if st.button("Reset All"):
        reset_state()


if __name__ == "__main__":
    main()
