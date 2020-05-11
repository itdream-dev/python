import requests


class BingImageSearch(object):

    PIXABAY_API_KEY = "3492872-422340267c5af0889cfaa63bc"
    PIXABAY_URL = "https://pixabay.com/api/?key=%s&q=%s"
    API_KEY = "65c3daac6a2340d0ad892d44ae4dbc2e"
    URL = (
        "https://api.cognitive.microsoft.com/bing/v5.0/images/search"
        "?q=%s&count=100&offset=0&mkt=en-us&safeSearch=Moderate"
    )

    def get_image_urls(self, key):
        response = requests.get(
            self.URL % key,
            headers={
                "Ocp-Apim-Subscription-Key": self.API_KEY
            }
        )
        images = (response.json() or {}).get('value')
        # urls = []
        # for image in images:
        #     image_url = image.get('contentUrl', '')
        #     if '.jpg' in image_url:
        #         urls.append(image_url.split('.jpg')[0] + '.jpg')
        #     elif '.png' in image_url:
        #         urls.append(image_url.split('.png')[0] + '.png')
        urls = [
            image['contentUrl'] for image in images
            if 'contentUrl' in image
        ]
        return urls
