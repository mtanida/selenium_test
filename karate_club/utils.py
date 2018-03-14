import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError

DEFAULT_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/61.0.3163.79 Chrome/61.0.3163.79 Safari/537.36'

def download_url(url, user_agent=DEFAULT_USER_AGENT, silent=True, 
                 num_retries=2):
    if not silent:
        print('Downloading ' + url + ' ...')

    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)

    for i in range(num_retries):
        try:
            html = urllib.request.urlopen(request).read()
            if not silent:
                print('Done.')
            return html
        except (URLError, HTTPError, ContentTooShortError) as e:
            if not silent:
                print('Download Error: ' + e.reason())
                if i < num_retries - 1:
                    print('Retrying...')
                else:
                    print('Download failed.')
    return None


