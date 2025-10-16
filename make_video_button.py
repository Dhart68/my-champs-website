# Function to make button for the video player

import streamlit as st


def make_video_button(label, option_key, player_name, count, index):
    is_active = (
        st.session_state.get("selected_player") == player_name
        and st.session_state.get("selected_option") == option_key
    )

    # Custom style for active button
    button_style = """
        <style>
        div[data-testid="stButton"] > button.active-btn {
            background-color: #1E90FF !important;
            color: white !important;
            font-weight: bold;
            border: 2px solid #0056b3;
        }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    # Use markdown link to scroll to anchor after click
    if st.button(
        f"{label} - {count} sequences",
        key=f"{option_key}_{index}",
        use_container_width=True,
    ):
        st.session_state["selected_player"] = player_name
        st.session_state["selected_option"] = option_key
        # Jump to anchor after rerun
        st.markdown('<meta http-equiv="refresh" content="0; #video_section">', unsafe_allow_html=True)

    # Apply "active" CSS class
    if is_active:
        st.markdown(
            f"<script>document.querySelector('[key=\"{option_key}_{index}\"]').classList.add('active-btn');</script>",
            unsafe_allow_html=True,
        )
