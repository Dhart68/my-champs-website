# news_ticker for stramlit app
# thanks ChatGPT

"""
Features
CSS: The ticker-content is animated using the @keyframes rule to create a scrolling effect.
HTML: The news items are dynamically joined with a separator (|) to form the scrolling text.
Customizable: You can adjust the animation-duration (currently 15 seconds) to make the scrolling faster or slower.
How It Works
The news-ticker div is styled to have an overflow hidden, ensuring only the visible part of the text is displayed.
The ticker-content div animates from right to left using the translateX property.
You can update the news_items list with your desired news content, and it will display seamlessly.

news_items: A list of strings to be displayed in the ticker.

duration: The animation duration (in seconds). Adjust this to control the speed of the scrolling.

"""
import streamlit as st

def display_news_ticker(news_items, duration=15):
    """
    Display a news ticker in a Streamlit app.

    Parameters:
        news_items (list): List of strings to display in the news ticker.
        duration (int): Duration (in seconds) for the scrolling animation.
    """
    # Custom CSS for the news ticker
    ticker_css = f"""
    <style>
    .news-ticker {{
        width: 100%;
        overflow: hidden;
        background-color: #000000;
        padding: 10px 0;
        white-space: nowrap;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }}

    .ticker-content {{
        display: inline-block;
        animation: ticker {duration}s linear infinite;
        font-size: 1.2rem;
        color: #f8f8f8;
    }}

    @keyframes ticker {{
        0% {{ transform: translateX(0%); }}
        100% {{ transform: translateX(-50%); }}
    }}
    </style>
    """

    # Custom HTML for the news ticker
    news_html = f"""
    <div class="news-ticker">
        <div class="ticker-content">
            {' | '.join(news_items)}
        </div>
    </div>
    """

    # Display the CSS and HTML in Streamlit
    st.markdown(ticker_css, unsafe_allow_html=True)
    st.markdown(news_html, unsafe_allow_html=True)
