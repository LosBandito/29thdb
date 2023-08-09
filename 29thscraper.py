import requests
from bs4 import BeautifulSoup


award_list= []
# Get the content of the website
def get_website_response():
    url = "https://www.29th.org/about/awards"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)
        return response.text
    else:
        print(f"Failed to retrieve website. Status code: {response.status_code}")
        return None

# Extract and print the award info
def award_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    ranks = soup.findAll("div", attrs={"class": "media mb-4"})
    for info in ranks:
        title = info.find("h5", attrs={"class": "mt-0"})
        text = info.find("div", attrs={"class": "media-body"})
        images = info.find("div", attrs={"class": "award-images"}).findAll("img")

        # Assuming the first image is the 'presentation image' and the second is the 'ribbon image'
        img_big = images[0]['src'] if len(images) > 0 else None
        img_sm = images[1]['src'] if len(images) > 1 else None

        if title:
            text_content = text.text
            text_content = text_content.replace(title.text, "").strip()

            award_list.append([title.text, text_content, img_big, img_sm])


website_content = get_website_response()
if website_content:  # Ensure the website content was fetched successfully
    award_info(website_content)


print(award_list)