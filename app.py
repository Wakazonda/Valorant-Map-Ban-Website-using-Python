import streamlit as st
import base64

# All 12 standard Valorant maps
ALL_MAPS = [
    "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus",
    "Pearl", "Split", "Sunset", "Abyss", "Corrode"
]

def get_base64_image(image_path):
    """Load an image file and return its base64 encoding."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def set_background_and_styles():
    """Set a background image + CSS for styling the app more aesthetically."""
    # You can use a local image or a URL
    # If local, you might do something like: img_base64 = get_base64_image("background.jpg")
    # Then use `url("data:image/jpeg;base64,{img_base64}")`
    background_image_url = "https://images.alphacoders.com/131/1319702.jpeg"

    st.markdown(
        f"""
        <style>
        /* Background image for the app */
        .stApp {{
            background: url("{background_image_url}") no-repeat center center fixed;
            background-size: cover;
        }}

        /* Style for main container to add semi-transparent backdrop */
        .css-1d391kg .main {{
            background-color: rgba(0, 0, 0, 0.6);
            padding: 2rem;
            border-radius: 15px;
        }}

        /* Titles */
        h1 {{
            color: #FFD700;  /* gold-ish */
            text-align: center;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }}

        h2, h3 {{
            color: #FFB14E;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: #FD4556;
            color: white;
            border-radius: 8px;
            border: 2px solid white;
            padding: 0.5rem 1rem;
            font-weight: bold;
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

        /* Inputs / Selectboxes */
        .stTextInput, .stSelectbox, .stNumberInput {{
            background-color: rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 0.5rem;
            color: white;
        }}

        /* Map names in final maps: different color */
        .final-map {{
            color: #7FFF00; /* chartreuse green */
            font-size: 1.2rem;
            font-weight: bold;
        }}

        /* Map ban history style */
        .ban-history {{
            color: #FFA07A; /* light salmon */
            font-size: 1rem;
        }}

        /* To ensure text is readable over background */
        .css-1v3fvcr, .css-ffhzg2 {{ /* adjust these container classes if needed */
            color: white;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )

def initialize_session_state():
    if 'available_maps' not in st.session_state:
        st.session_state.available_maps = list(ALL_MAPS)
    if 'banned_maps' not in st.session_state:
        st.session_state.banned_maps = []
    if 'teams' not in st.session_state:
        st.session_state.teams = {'Team A': '', 'Team B': ''}
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'final_map_count' not in st.session_state:
        st.session_state.final_map_count = 0
    if 'veto_started' not in st.session_state:
        st.session_state.veto_started = False
    if 'veto_finished' not in st.session_state:
        st.session_state.veto_finished = False

def ban_map(map_name):
    if map_name in st.session_state.available_maps:
        st.session_state.available_maps.remove(map_name)
        st.session_state.banned_maps.append(map_name)
        st.session_state.history.append(f"Banned: {map_name}")
        # if we’ve reached the final map count, mark finished
        if len(st.session_state.available_maps) == st.session_state.final_map_count:
            st.session_state.veto_finished = True
        st.experimental_rerun()

def reset_state():
    st.session_state.available_maps = list(ALL_MAPS)
    st.session_state.banned_maps = []
    st.session_state.teams = {'Team A': '', 'Team B': ''}
    st.session_state.history = []
    st.session_state.final_map_count = 0
    st.session_state.veto_started = False
    st.session_state.veto_finished = False
    st.experimental_rerun()

def main():
    set_background_and_styles()
    initialize_session_state()

    st.title("Valorant Map Veto Tool")
    st.subheader("Select maps fairly before the match")

    # Team names
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.teams['Team A'] = st.text_input("Team A Name", value=st.session_state.teams['Team A'])
    with col2:
        st.session_state.teams['Team B'] = st.text_input("Team B Name", value=st.session_state.teams['Team B'])

    if st.session_state.teams['Team A'] and st.session_state.teams['Team B']:
        st.markdown(f"**First Half**: {st.session_state.teams['Team A']} (Attacking) vs {st.session_state.teams['Team B']} (Defending)")
        st.markdown(f"**Second Half**: {st.session_state.teams['Team B']} (Attacking) vs {st.session_state.teams['Team A']} (Defending)")

    st.markdown("---")  # a divider line

    # Veto & Selection
    st.header("Map Veto & Selection")

    if not st.session_state.veto_started:
        maps_to_keep = st.selectbox(
            "How many maps should remain?",
            [1, 3, 5, 7, 9, 11],
            key='map_count_selector'
        )
        if st.button("Start Ban Phase"):
            st.session_state.final_map_count = maps_to_keep
            st.session_state.veto_started = True
            st.experimental_rerun()

    else:
        if not st.session_state.veto_finished:
            # still banning
            st.subheader(f"Available Maps: {len(st.session_state.available_maps)}")
            cols = st.columns(3)
            for i, map_name in enumerate(st.session_state.available_maps):
                with cols[i % 3]:
                    # custom button key so CSS/class might apply
                    if st.button(f"Ban {map_name}", key=f"ban_{map_name}"):
                        ban_map(map_name)
        else:
            # finished veto
            st.success("✅ Veto complete!")
            final = st.session_state.available_maps
            final_line = ", ".join(final)
            st.markdown(f"**Final {len(final)} Map(s) Selected:**")
            # Use styled spans to apply CSS class “final-map”
            st.markdown(
                "<p class='final-map'>" + final_line + "</p>",
                unsafe_allow_html=True
            )

    st.markdown("---")

    # Ban history
    st.header("Map Ban History")
    if st.session_state.history:
        for item in st.session_state.history:
            st.markdown(f"<span class='ban-history'>{item}</span>", unsafe_allow_html=True)
    else:
        st.write("No bans yet.")

    st.markdown("---")

    if st.button("Reset All"):
        reset_state()

if __name__ == "__main__":
    main()
