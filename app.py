import streamlit as st

# All 12 standard Valorant maps, including those that may be in or out of rotation.
ALL_MAPS = [
    "Ascent", "Split", "Bind", "Haven", "Icebox", "Breeze",
    "Fracture", "Pearl", "Lotus", "Sunset", "Abyss", "Corrode"
]


def initialize_state():
    """Initializes the session state for a new map banning session."""
    if 'remaining_maps' not in st.session_state:
        st.session_state.remaining_maps = list(ALL_MAPS)
    if 'banned_maps' not in st.session_state:
        st.session_state.banned_maps = []
    if 'target_maps_set' not in st.session_state:
        st.session_state.target_maps_set = False
    if 'target_maps_count' not in st.session_state:
        st.session_state.target_maps_count = 0
    if 'ban_history' not in st.session_state:
        st.session_state.ban_history = []
    if 'selected_maps' not in st.session_state:
        st.session_state.selected_maps = []


def ban_map(map_to_ban):
    """Handles the map banning logic."""
    if map_to_ban in st.session_state.remaining_maps:
        st.session_state.remaining_maps.remove(map_to_ban)
        st.session_state.banned_maps.append(map_to_ban)
        st.session_state.ban_history.append(f"Banned: {map_to_ban}")


def select_map(map_to_select):
    """Handles the map selection logic."""
    if map_to_select in st.session_state.remaining_maps:
        st.session_state.remaining_maps.remove(map_to_select)
        st.session_state.selected_maps.append(map_to_select)
        st.session_state.ban_history.append(f"Selected: {map_to_select}")


def reset_session():
    """Resets the session to start a new ban phase."""
    st.session_state.remaining_maps = list(ALL_MAPS)
    st.session_state.banned_maps = []
    st.session_state.target_maps_set = False
    st.session_state.target_maps_count = 0
    st.session_state.ban_history = []
    st.session_state.selected_maps = []


def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="Valorant Map Ban Tool",
        layout="centered"
    )

    initialize_state()

    st.title("Valorant Map Ban Tool 🛡️")
    st.markdown("Select a series type to begin your map ban process.")

    st.divider()

    if not st.session_state.target_maps_set:
        st.subheader("1. Choose a Series Type")
        target_count = st.selectbox(
            "Select the number of maps to play:",
            options=[1, 3, 5],
            index=1
        )
        if st.button("Start Ban Phase"):
            st.session_state.target_maps_count = target_count
            st.session_state.target_maps_set = True
            st.rerun()
    else:
        st.subheader(f"2. Current Series: Best-of-{st.session_state.target_maps_count}")

        if len(st.session_state.remaining_maps) > st.session_state.target_maps_count:
            st.info(
                f"There are {len(st.session_state.remaining_maps)} maps left. Ban maps to reach your target of {st.session_state.target_maps_count}.")

            # Display available maps as clickable buttons
            cols = st.columns(3)
            for i, map_name in enumerate(st.session_state.remaining_maps):
                with cols[i % 3]:
                    if st.button(map_name, key=f"ban_{map_name}"):
                        ban_map(map_name)
                        st.rerun()
        else:
            st.header("Map Selection Complete! 🎉")
            st.success("The final maps for your series are:")
            for map_name in st.session_state.remaining_maps:
                st.markdown(f"- {map_name}")

    st.divider()

    st.subheader("Map History")
    for action in st.session_state.ban_history:
        st.write(action)

    if st.session_state.target_maps_set:
        if st.button("Reset Session", key="reset"):
            reset_session()
            st.rerun()


if __name__ == "__main__":
    main()
