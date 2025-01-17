# This function will get a player's headshot image
import requests
from bs4 import BeautifulSoup


def get_player_image(player_id):
    # The image will be retrieved from this URL
    url = f'https://www.nba.com/stats/player/{player_id}'

    # Make an HTTP GET request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the player image tag using the appropriate class
    img_tag = soup.find('img', {'class': 'PlayerImage_image__wH_YX PlayerSummary_playerImage__sysif'})

    # Extract and return the src attribute if the img tag is found
    if img_tag and 'src' in img_tag.attrs:
        return img_tag['src']

    # Return message if the image tag is not found
    return print("Player image not found.")
