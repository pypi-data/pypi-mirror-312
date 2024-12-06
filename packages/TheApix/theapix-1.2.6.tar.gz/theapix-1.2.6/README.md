Welcome to the **TheApix!** This library allows you to easily interact with the API using asynchronous options.

#### Installation

```sh
pip install TheApix
```

##### FilePath Class
The `FilePath` class is a wrapper around a file path string, adding an additional `delete()` method to handle file deletion.

```python
class FilePath(str):
    """
    A wrapper around a file path string that provides an additional delete method.

    Attributes:
        path (str): The file path to the media file.

    Methods:
        delete(): Attempts to delete the file at the specified path.
                  If deletion fails, it handles the exception gracefully.
    """

    def delete(self):
        """Deletes the file at the specified path, handling exceptions if deletion fails."""
        try:
            os.remove(self)
        except Exception:
            pass
```

##### Usage Example

Whenever a media path is returned, it will be wrapped in a `FilePath` object. You can then call `delete()` on that object to delete the file if it exists.

```python
from TheApi import api

# Example of using the API to get a file path
file_path = await api.blackpink(query='Pokemon')  # Returns the file path where the blackpink media is saved

print(file_path)  # Print the file path

file_path.delete()  # Delete the file if it exists
```

In the example above, `file_path` will be an instance of the `FilePath` class, which allows you to easily delete the file associated with the media once you are done with it.

---

# 📘 API Documentation

## Status

| Function           | Status |
|--------------------|--------|
| [1. Animechan](#1-animechan) | ✅
| [2. Avatar](#2-avatar) | ✅
| [3. Bing Image](#3-bing-image) | ✅
| [4. Blackpink](#4-blackpink) | ✅
| [5. Carbon](#5-carbon) | ✅
| [6. Cat](#6-cat) | ✅
| [7. Dog](#7-dog) | ✅
| [8. Domain Search](#8-domain-search) | ✅
| [9. Fakerapi](#9-fakerapi) | ✅
| [10. Fox](#10-fox) | ✅
| [11. Gen Qr](#11-gen-qr) | ✅
| [12. Generate Pdf](#12-generate-pdf) | ✅
| [13. Get Advice](#13-get-advice) | ✅
| [14. Get Btc Value](#14-get-btc-value) | ✅
| [15. Get Fake Addresses](#15-get-fake-addresses) | ✅
| [16. Get Fake Credit Cards](#16-get-fake-credit-cards) | ✅
| [17. Get Fake Images](#17-get-fake-images) | ✅
| [18. Get Hindi Jokes](#18-get-hindi-jokes) | ✅
| [19. Get Jokes](#19-get-jokes) | ✅
| [20. Get Uselessfact](#20-get-uselessfact) | ✅
| [21. Get Word Definitions](#21-get-word-definitions) | ✅
| [22. Github Search](#22-github-search) | ✅
| [23. Hindi Quote](#23-hindi-quote) | ✅
| [24. Hug](#24-hug) | ✅
| [25. Meme](#25-meme) | ✅
| [26. Neko](#26-neko) | ✅
| [27. Pypi](#27-pypi) | ✅
| [28. Quote](#28-quote) | ✅
| [29. Random Word](#29-random-word) | ✅
| [30. Riddle](#30-riddle) | ✅
| [31. Stackoverflow Search](#31-stackoverflow-search) | ✅
| [32. Upload Image](#32-upload-image) | ✅
| [33. Wikipedia](#33-wikipedia) | ✅
| [34. Words](#34-words) | ✅
| [35. Write](#35-write) | ✅


## 🎓 How to Use Each Function

### 1. Animechan

**Description**:
Fetches a random anime quote from the AnimeChan API.

**Returns:**
  - **dict**: Contains the quote content, anime name, and character details.

```python
from Pokemon import api

result = await api.animechan()
print(result)
```

#### Expected Output

```json
{
    "content": "A man who raises his hands on a woman is trash. If I have to become trash in order to survive... It'll be just like dying.",
    "anime": {
        "id": 222,
        "name": "Bleach"
    },
    "character": {
        "id": 2236,
        "name": "Abarai Renji"
    }
}
```

### 2. Avatar

**Description**:
Fetches a random avatars from the thedobby.club API.

**Returns:**
  - **dict**: Contains the file name, file type, and file URL.

```python
from Pokemon import api

result = await api.avatar()
print(result)
```

#### Expected Output

```json
{
    "file_name": "driver",
    "file_type": "image/jpeg",
    "file_url": "https://cofuvfbkdyfchroaxcvi.supabase.co/storage/v1/object/public/avatars/driver.jpg"
}
```

### 3. Bing Image

**Description**:
Searches Bing for images based on a query and retrieves image URLs.

**Args:**
  - **query (str)**: The search query string for finding images.
  - **limit (int, optional)**: The maximum number of image URLs to return. Defaults to 3.

**Returns:**
  - **list**: A list of image URLs retrieved from the Bing search results.

```python
from TheApi import api

result = await api.bing_image(query='Pokemon', limit=3)
print(result)
```

#### Expected Output

```text
https://townsquare.media/site/622/files/2016/08/poke-feat.jpg?w=1200&amp;h=0&amp;zc=1&amp;s=0&amp;a=t&amp;q=89
https://images5.alphacoders.com/130/thumb-1920-1308338.jpg
http://www.animextremist.com/imagenes/pokemon/pokemon103.jpg
```

### 4. Blackpink

**Description**:
Creates a stylized "Blackpink"-themed image with custom text, color, and optional border.
**Args:**
  - **query (str)**: The text to display on the image.
  - **color (str, optional)**: The primary color of the text and gradient background in hex format.
    Defaults to "#ff94e0" (a pink shade).
  - **border_color (str, optional)**: The color of the image border in hex format.
    If not provided, defaults to the value of `color`.
**Returns:**
  - **FilePath**: The file path of the generated image with delete attribute.

```python
from TheApi import api

result = await api.blackpink(query='Pokemon', color='#ff94e0', border_color=None)
print(result)
```

#### Expected Output

```text
/home/runner/work/TheApi/TheApi/downloads/blackpink_YFSm8FMs.jpg
```

### 5. Carbon

**Description**:
Generates a code snippet image using the Carbon API, saves it to the downloads folder, uploads it, and returns the URL of the uploaded image.

**Args:**
  - **query (str)**: The code snippet to be rendered as an image.

**Returns:**
  - **FilePath**: The file path of the saved image.

```python
from TheApi import api

result = await api.carbon(query='Pokemon')
print(result)
```

#### Expected Output

```text
/home/runner/work/TheApi/TheApi/downloads/carbon_VOB0WjSF.png
```

### 6. Cat

**Description**:
Fetches a random cat image URL.

**Returns:**
  - **str or None**: The URL of a random cat image if available; None if no response is received.

```python
from Pokemon import api

result = await api.cat()
print(result)
```

#### Expected Output

```text
https://cdn2.thecatapi.com/images/a4g.jpg
```

### 7. Dog

**Description**:
Fetches a random dog image URL.

**Returns:**
  - **str or None**: The URL of a random dog image if available; None if no response is received.

```python
from Pokemon import api

result = await api.dog()
print(result)
```

#### Expected Output

```text
https://random.dog/42e97d6a-c825-4191-9434-32cea191fc21.jpeg
```

### 8. Domain Search

**Description**:
Fetches domain information from the DomainsDB API.

**Args:**
  - **domain (str)**: The domain name to search for (e.g., "facebook").
  - **zone (str)**: The domain zone to search within (e.g., "com").Default is "com".

**Returns:**
  - **dict**: A dictionary containing the results of the domain search.

```python
from TheApi import api

result = await api.domain_search(domain='Pokemon', zone='com')
print(result)
```

#### Expected Output

```json
{
    "domains": [
        {
            "domain": "pokemon-insurgence.com",
            "create_date": "2024-11-28T23:57:45.053478",
            "update_date": "2024-11-28T23:57:45.053481",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-cheats.com",
            "create_date": "2024-11-28T23:57:45.053290",
            "update_date": "2024-11-28T23:57:45.053292",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-worlds.com",
            "create_date": "2024-11-28T23:57:45.053698",
            "update_date": "2024-11-28T23:57:45.053700",
            "country": "CA",
            "isDead": "False",
            "A": [
                "23.227.38.70"
            ],
            "NS": [
                "ns-cloud-b1.googledomains.com",
                "ns-cloud-b2.googledomains.com",
                "ns-cloud-b3.googledomains.com",
                "ns-cloud-b4.googledomains.com"
            ],
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-battle-arena.com",
            "create_date": "2024-11-27T09:08:01.526222",
            "update_date": "2024-11-27T09:08:01.526225",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-room.com",
            "create_date": "2024-11-23T21:12:22.020090",
            "update_date": "2024-11-23T21:12:22.020092",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-steam.com",
            "create_date": "2024-11-20T12:22:24.695961",
            "update_date": "2024-11-20T12:22:24.695963",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-showdown.com",
            "create_date": "2024-11-16T21:44:25.062255",
            "update_date": "2024-11-16T21:44:25.062258",
            "country": "CA",
            "isDead": "False",
            "A": [
                "162.0.215.28"
            ],
            "NS": [
                "dns1.namecheaphosting.com",
                "dns2.namecheaphosting.com"
            ],
            "CNAME": null,
            "MX": [
                {
                    "exchange": "smx4.web-hosting.com",
                    "priority": 40
                },
                {
                    "exchange": "smx3.web-hosting.com",
                    "priority": 30
                },
                {
                    "exchange": "smx2.web-hosting.com",
                    "priority": 20
                },
                {
                    "exchange": "smx1.web-hosting.com",
                    "priority": 10
                }
            ],
            "TXT": [
                "v=spf1 +a +mx +ip4:162.213.251.158 include:spf.web-hosting.com ~all"
            ]
        },
        {
            "domain": "pokemon-towerdefense3.com",
            "create_date": "2024-11-16T21:44:25.062423",
            "update_date": "2024-11-16T21:44:25.062425",
            "country": "CA",
            "isDead": "False",
            "A": [
                "172.96.187.228"
            ],
            "NS": [
                "ns2.hawkhost.com",
                "ns1.hawkhost.com"
            ],
            "CNAME": null,
            "MX": [
                {
                    "exchange": "pokemon-towerdefense3.com",
                    "priority": 0
                }
            ],
            "TXT": [
                "v=spf1 +a +mx +ip4:172.96.187.2 +include:_spf.arandomserver.com ~all"
            ]
        },
        {
            "domain": "pokemon-pcg-pocket.com",
            "create_date": "2024-11-13T12:59:34.788589",
            "update_date": "2024-11-13T12:59:34.788591",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "the-pokemon-store.com",
            "create_date": "2024-11-10T12:00:23.641438",
            "update_date": "2024-11-10T12:00:23.641441",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-tcgp.com",
            "create_date": "2024-11-07T08:41:00.387999",
            "update_date": "2024-11-07T08:41:00.388001",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-collect.com",
            "create_date": "2024-11-07T08:41:00.387827",
            "update_date": "2024-11-07T08:41:00.387830",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-glazed.com",
            "create_date": "2024-11-04T00:30:39.204506",
            "update_date": "2024-11-04T00:30:39.204508",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-energy.com",
            "create_date": "2024-11-04T00:30:39.204309",
            "update_date": "2024-11-04T00:30:39.204312",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-italy.com",
            "create_date": "2024-11-04T00:30:39.204707",
            "update_date": "2024-11-04T00:30:39.204709",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-autochess.com",
            "create_date": "2024-11-02T08:33:16.991832",
            "update_date": "2024-11-02T08:33:16.991834",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "play-pokemon-online.com",
            "create_date": "2024-11-02T08:33:16.825655",
            "update_date": "2024-11-02T08:33:16.825658",
            "country": "US",
            "isDead": "False",
            "A": [
                "104.148.94.51"
            ],
            "NS": [
                "jm1.dns.com",
                "jm2.dns.com"
            ],
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "japanese-pokemon-cards.com",
            "create_date": "2024-11-02T08:33:00.325331",
            "update_date": "2024-11-02T08:33:00.325336",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-dynasty.com",
            "create_date": "2024-10-18T03:14:43.852622",
            "update_date": "2024-10-18T03:14:43.852624",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-quiz.com",
            "create_date": "2024-10-15T03:36:57.588519",
            "update_date": "2024-10-15T03:36:57.588522",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-tcg-pocket-dex.com",
            "create_date": "2024-10-07T13:29:47.356011",
            "update_date": "2024-10-07T13:29:47.356013",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-mystery-boxes.com",
            "create_date": "2024-10-07T13:29:47.355854",
            "update_date": "2024-10-07T13:29:47.355856",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-oise.com",
            "create_date": "2024-10-06T00:23:47.700295",
            "update_date": "2024-10-06T00:23:47.700297",
            "country": "BE",
            "isDead": "False",
            "A": [
                "62.213.245.149"
            ],
            "NS": [
                "ns3.ipower.be",
                "ns2.ipower.be",
                "ns1.ipower.be"
            ],
            "CNAME": null,
            "MX": [
                {
                    "exchange": "mail.pokemon-oise.com",
                    "priority": 10
                }
            ],
            "TXT": null
        },
        {
            "domain": "pokemon-pocketdex.com",
            "create_date": "2024-10-03T10:22:44.808048",
            "update_date": "2024-10-03T10:22:44.808050",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-aventure.com",
            "create_date": "2024-09-30T10:50:27.835203",
            "update_date": "2024-09-30T10:50:27.835206",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-news.com",
            "create_date": "2024-09-24T09:20:31.631508",
            "update_date": "2024-09-24T09:20:31.631511",
            "country": "US",
            "isDead": "False",
            "A": [
                "198.54.114.204"
            ],
            "NS": [
                "dns1.namecheaphosting.com",
                "dns2.namecheaphosting.com"
            ],
            "CNAME": null,
            "MX": [
                {
                    "exchange": "mail.pokemon-news.com",
                    "priority": 0
                }
            ],
            "TXT": null
        },
        {
            "domain": "pokemon-pcmaster.com",
            "create_date": "2024-09-24T09:20:31.631693",
            "update_date": "2024-09-24T09:20:31.631695",
            "country": "US",
            "isDead": "False",
            "A": [
                "154.221.215.205"
            ],
            "NS": [
                "now1.dns.com",
                "now2.dns.com"
            ],
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-pokedex.com",
            "create_date": "2024-09-21T21:40:29.481566",
            "update_date": "2024-09-21T21:40:29.481568",
            "country": "US",
            "isDead": "False",
            "A": [
                "207.244.67.214"
            ],
            "NS": [
                "ns1.dnsnuts.com",
                "ns2.dnsnuts.com"
            ],
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-gba.com",
            "create_date": "2024-09-18T23:10:09.788582",
            "update_date": "2024-09-18T23:10:09.788584",
            "country": "JP",
            "isDead": "False",
            "A": [
                "219.94.203.121"
            ],
            "NS": [
                "ns5.xserver.jp",
                "ns3.xserver.jp",
                "ns1.xserver.jp",
                "ns4.xserver.jp",
                "ns2.xserver.jp"
            ],
            "CNAME": null,
            "MX": [
                {
                    "exchange": "pokemon-gba.com",
                    "priority": 0
                }
            ],
            "TXT": null
        },
        {
            "domain": "pokemon-dp.com",
            "create_date": "2024-09-18T23:10:09.788393",
            "update_date": "2024-09-18T23:10:09.788395",
            "country": "JP",
            "isDead": "False",
            "A": [
                "211.5.69.234"
            ],
            "NS": [
                "ns1.c008jp5381.info",
                "ns2.c008jp5381.info"
            ],
            "CNAME": null,
            "MX": [
                {
                    "exchange": "pokemon-dp.com",
                    "priority": 0
                }
            ],
            "TXT": null
        },
        {
            "domain": "pokemon-underground.com",
            "create_date": "2024-09-18T23:10:09.788937",
            "update_date": "2024-09-18T23:10:09.788939",
            "country": "JP",
            "isDead": "False",
            "A": [
                "61.198.74.245"
            ],
            "NS": [
                "ns1.value-domain.com",
                "ns2.value-domain.com"
            ],
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-aona.com",
            "create_date": "2024-09-18T23:10:09.788186",
            "update_date": "2024-09-18T23:10:09.788190",
            "country": "US",
            "isDead": "False",
            "A": [
                "13.249.39.146",
                "13.249.39.52",
                "13.249.39.37",
                "13.249.39.224"
            ],
            "NS": [
                "ns-1376.awsdns-44.org",
                "ns-1782.awsdns-30.co.uk",
                "ns-394.awsdns-49.com",
                "ns-599.awsdns-10.net"
            ],
            "CNAME": null,
            "MX": [
                {
                    "exchange": "mx.pokemon-aona.com.cust.hostedemail.com",
                    "priority": 10
                }
            ],
            "TXT": null
        },
        {
            "domain": "pokemon-legends.com",
            "create_date": "2024-09-08T09:54:29.699715",
            "update_date": "2024-09-08T09:54:29.699717",
            "country": "US",
            "isDead": "False",
            "A": [
                "3.33.152.147",
                "15.197.142.173"
            ],
            "NS": [
                "ns17.domaincontrol.com",
                "ns18.domaincontrol.com"
            ],
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-calculation-sv.com",
            "create_date": "2024-09-06T21:30:18.924253",
            "update_date": "2024-09-06T21:30:18.924256",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-dimension.com",
            "create_date": "2024-09-05T09:12:56.181647",
            "update_date": "2024-09-05T09:12:56.181650",
            "country": "FR",
            "isDead": "False",
            "A": [
                "87.98.174.30"
            ],
            "NS": [
                "dns1.e-c.com",
                "dns2.e-c.com"
            ],
            "CNAME": null,
            "MX": [
                {
                    "exchange": "pokemon-dimension.com",
                    "priority": 0
                }
            ],
            "TXT": [
                "v=spf1 ip4:87.98.174.30 +a +mx +ip4:87.98.153.102 ~all"
            ]
        },
        {
            "domain": "pokemon-go-home.com",
            "create_date": "2024-09-02T10:21:29.718289",
            "update_date": "2024-09-02T10:21:29.718291",
            "country": "US",
            "isDead": "False",
            "A": [
                "142.91.174.104"
            ],
            "NS": [
                "ns1.openprovider.nl",
                "ns2.openprovider.be",
                "ns3.openprovider.eu"
            ],
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-card-artwalk.com",
            "create_date": "2024-08-30T09:32:21.700506",
            "update_date": "2024-08-30T09:32:21.700509",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "eternara-pokemon-auto-chess.com",
            "create_date": "2024-08-30T09:31:51.471595",
            "update_date": "2024-08-30T09:31:51.471600",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-sea.com",
            "create_date": "2024-08-27T09:19:17.135535",
            "update_date": "2024-08-27T09:19:17.135538",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-master.com",
            "create_date": "2024-08-24T09:08:58.027448",
            "update_date": "2024-08-24T09:08:58.027450",
            "country": "JP",
            "isDead": "False",
            "A": [
                "150.95.8.162"
            ],
            "NS": [
                "01.dnsv.jp",
                "02.dnsv.jp",
                "03.dnsv.jp",
                "04.dnsv.jp"
            ],
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-rps.com",
            "create_date": "2024-08-24T09:08:58.027988",
            "update_date": "2024-08-24T09:08:58.027991",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-unite-matome.com",
            "create_date": "2024-08-22T21:11:38.525011",
            "update_date": "2024-08-22T21:11:38.525013",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-overdose.com",
            "create_date": "2024-08-21T09:47:14.599538",
            "update_date": "2024-08-21T09:47:14.599540",
            "country": "US",
            "isDead": "False",
            "A": [
                "104.18.49.225",
                "104.18.48.225"
            ],
            "NS": [
                "coco.ns.cloudflare.com",
                "sri.ns.cloudflare.com"
            ],
            "CNAME": null,
            "MX": [
                {
                    "exchange": "mail.pokemon-overdose.com",
                    "priority": 10
                }
            ],
            "TXT": null
        },
        {
            "domain": "pokemon-sprites-ethereum-blockchain-nfts-nintendo-collec.com",
            "create_date": "2024-08-05T17:00:04.645397",
            "update_date": "2024-08-05T17:00:04.645400",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-irl.com",
            "create_date": "2024-07-18T17:04:27.841240",
            "update_date": "2024-07-18T17:04:27.841243",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-event-kujisystem.com",
            "create_date": "2024-07-18T17:04:27.841055",
            "update_date": "2024-07-18T17:04:27.841057",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-display.com",
            "create_date": "2024-07-11T05:39:11.089164",
            "update_date": "2024-07-11T05:39:11.089166",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-cg-pocket22-blog.com",
            "create_date": "2024-07-08T14:33:48.093159",
            "update_date": "2024-07-08T14:33:48.093162",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-online-shop.com",
            "create_date": "2024-06-29T11:03:49.095970",
            "update_date": "2024-06-29T11:03:49.095972",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        },
        {
            "domain": "pokemon-gratuit.com",
            "create_date": "2024-06-29T11:03:49.095786",
            "update_date": "2024-06-29T11:03:49.095789",
            "country": null,
            "isDead": "False",
            "A": null,
            "NS": null,
            "CNAME": null,
            "MX": null,
            "TXT": null
        }
    ],
    "total": 357,
    "time": "4",
    "next_page": null
}
```

### 9. Fakerapi

**Description**:
Fetch data from the FakerAPI using aiohttp.

**Args:**
  - **endpoint (str)**: The resource endpoint. Valid endpoints are:
    - companies
    - addresses
    - books
    - CreditCards
    - images
    - persons
    - places
    - products
    - texts
    - users

**Description**:
quantity (int, optional): Number of rows to fetch (default: 3, max: 1000). locale (str, optional): Locale for the data (default: 'en_US').  See Valid locale [ From Here ](https://github.com/Vivekkumar-IN/TheApi/blob/main/src%2FTheApi%2Fapi.py#L185-L261)

**Raises:**
  - **ValueError**: If the locale is invalid, the endpoint is invalid, or the quantity
    is outside the allowed range.

**Returns:**
  - **dict**: Response data from the API.


### 10. Fox

**Description**:
Fetches a random fox image URL.

**Returns:**
  - **str or None**: The URL of the fox image if available, otherwise None.

```python
from Pokemon import api

result = await api.fox()
print(result)
```

#### Expected Output

```text
https://randomfox.ca/?i=64
```

### 11. Gen Qr

**Description**:
Generate a QR code using api.qrserver.com and save it as a PNG file.

**Args:**
  - **data (str)**: The content for the QR code.
  - **size (str)**: The size of the QR code in the format 'WIDTHxHEIGHT' (default: '150x150').
  - **foreground_color (str)**: The color of the QR code (default: '000000' - black).
  - **background_color (str)**: The background color of the QR code (default: 'FFFFFF' - white).
  - **file_path (str, optional)**: The file path to save the QR code.
    Defaults to "downloads/{random_str}_qr.png".

**Returns:**
  - **FilePath**: The file path where the QR code was saved.

```python
from TheApi import api

result = await api.gen_qr(data='Pokemon', size='150x150', foreground_color='000000', background_color='FFFFFF', file_path=None)
print(result)
```

#### Expected Output

```text
/home/runner/work/TheApi/TheApi/downloads/bjwRoLCP_qr.png
```

### 12. Generate Pdf

**Description**:
Generates a PDF from a URL or an HTML string and saves it to a file.

**Args:**
  - **source (str)**: The URL of the website (if `from_url=True`) or the HTML string (if `from_url=False`).
  - **file_path (str, optional)**: The file path to save the generated PDF.
    Defaults to "downloads/<random_str>_generated.pdf".
  - **from_url (bool, optional)**: Whether to generate the PDF from a URL (True) or an HTML string (False).

**Returns:**
  - **FilePath**: The file path where the PDF was saved.

**Raises:**
  - **ValueError**: If `from_url` is True and `source` is not a valid URL.


### 13. Get Advice

**Description**:
Fetches a random piece of advice.

**Returns:**
  - **str**: A random advice message.

```python
from Pokemon import api

result = await api.get_advice()
print(result)
```

#### Expected Output

```text
Everyone has their down days. Don't take it out on innocent bystanders.
```

### 14. Get Btc Value

**Description**:
Fetches the current value of Bitcoin (BTC) for the specified currency or all currencies.

**Args:**
  - **currency (str, optional)**: The currency code (e.g., 'eur', 'usd', 'gbp').
    If None, fetches BTC value for all currencies.

**Returns:**
  - **dict**: The response containing BTC value(s) for the specified currency or all currencies.

**Raises:**
  - **ValueError**: If the provided currency is invalid or the request fails.

```python
from TheApi import api

result = await api.get_btc_value(currency=None)
print(result)
```

#### Expected Output

```json
{
    "EUR": {
        "code": "EUR",
        "description": "Euro",
        "rate": "91,216.364",
        "rate_float": 91216.364,
        "symbol": "&euro;"
    },
    "GBP": {
        "code": "GBP",
        "description": "British Pound Sterling",
        "rate": "75,791.77",
        "rate_float": 75791.7702,
        "symbol": "&pound;"
    },
    "USD": {
        "code": "USD",
        "description": "United States Dollar",
        "rate": "96,505.645",
        "rate_float": 96505.6454,
        "symbol": "&#36;"
    }
}
```

### 15. Get Fake Addresses

**Description**:
Fetch fake address data from the FakerAPI.

**Args:**
  - **quantity (int, optional)**: Number of address entries to fetch (default: 1).
  - **locale (str, optional)**: Locale for the address data (default: "en_US").

**Returns:**
  - **dict**: Response data from the API.

```python
from TheApi import api

result = await api.get_fake_addresses(quantity=1, locale='en_US')
print(result)
```

#### Expected Output

```json
{
    "status": "OK",
    "code": 200,
    "locale": "en_US",
    "seed": null,
    "total": 1,
    "data": [
        {
            "id": 1,
            "street": "740 Gleason Dam",
            "streetName": "Bruen Inlet",
            "buildingNumber": "125",
            "city": "Rodville",
            "zipcode": "90752",
            "country": "Madagascar",
            "country_code": "MG",
            "latitude": 49.378333,
            "longitude": -126.438744
        }
    ]
}
```

### 16. Get Fake Credit Cards

**Description**:
Fetch fake credit card data from the FakerAPI.

**Args:**
  - **locale (str, optional)**: Locale for the credit card data (default: "en_US").
  - **amount (int, optional)**: Number of credit card entries to fetch (default: 1).

**Returns:**
  - **dict**: Response data from the API.

```python
from TheApi import api

result = await api.get_fake_credit_cards(locale='en_US', quantity=1)
print(result)
```

#### Expected Output

```json
{
    "status": "OK",
    "code": 200,
    "locale": "en_US",
    "seed": null,
    "total": 1,
    "data": [
        {
            "type": "American Express",
            "number": "2221151383909249",
            "expiration": "11/25",
            "owner": "Agustin Terry"
        }
    ]
}
```

### 17. Get Fake Images

**Description**:
Fetch fake image data from the FakerAPI.

**Args:**
  - **quantity (int, optional)**: Number of images to fetch (default: 1).
  - **locale (str, optional)**: Locale for the images (default: "en_US").
  - **type (str, optional)**: Type of image (e.g., 'any', 'animals', 'business', etc.; default: "any").
  - **width (int, optional)**: Width of the images (default: 640).
  - **height (int, optional)**: Height of the images (default: 480).

**Returns:**
  - **dict**: Response data from the API.

```python
from TheApi import api

result = await api.get_fake_images(quantity=1, locale='en_US', type='any', width=640, height=480)
print(result)
```

#### Expected Output

```json
{
    "status": "OK",
    "code": 200,
    "locale": "en_US",
    "seed": null,
    "total": 1,
    "data": [
        {
            "title": "Dolore laudantium qui quia.",
            "description": "Dolores tempore est nihil cum molestias vel consequatur. Maxime modi aliquam necessitatibus ut neque omnis. Sit natus omnis omnis odit quasi assumenda et.",
            "url": "https://picsum.photos/640/480"
        }
    ]
}
```

### 18. Get Hindi Jokes

**Description**:
Fetches a random Hindi joke.

**Returns:**
  - **str**: A random Hindi joke if available, or "No joke found" if not available.

```python
from Pokemon import api

result = await api.get_hindi_jokes()
print(result)
```

#### Expected Output

```text
एक मोटरसाइकिल वाले ने  पता पूछने के लिए संता से पूछा : Excuse me मुझे लाल किला जाना है  संता : तो जा ना भाई ऐसे हर किसी को बताते बताते जायेगा तो पहुँचेगा कब? 😆🤣😋😉 
```

### 19. Get Jokes

**Description**:
Fetches a specified number of jokes.

**Args:**
  - **amount (int, optional)**: The number of jokes to retrieve. Defaults to 1.

**Returns:**
  - **str**: A single joke if `amount` is 1. If `amount` > 1, returns numbered jokes as a formatted string.

```python
from TheApi import api

result = await api.get_jokes(amount=1)
print(result)
```

#### Expected Output

```text
Four engineers get into a car. The car won't start.
The Mechanical engineer says "It's a broken starter".
The Electrical engineer says "Dead battery".
The Chemical engineer says "Impurities in the gasoline".
The IT engineer says "Hey guys, I have an idea: How about we all get out of the car and get back in".
```

### 20. Get Uselessfact

**Description**:
Fetches a random useless fact.

**Returns:**
  - **str**: A random useless fact.

```python
from Pokemon import api

result = await api.get_uselessfact()
print(result)
```

#### Expected Output

```text
Oak trees do not produce acorns until they are fifty years of age or older.
```

### 21. Get Word Definitions

**Description**:
Fetch definitions for a word from the Dictionary API.

**Args:**
  - **word (str)**: The word to fetch definitions for.

**Returns:**
  - **list**: A list of dictionaries containing the word definitions.

**Raises:**
  - **ValueError**: If the `word` is not provided or the API request fails.

```python
from TheApi import api

result = await api.get_word_definitions(word='Pokemon')
print(result)
```

#### Expected Output

```json
{
    "title": "No Definitions Found",
    "message": "Sorry pal, we couldn't find definitions for the word you were looking for.",
    "resolution": "You can try the search again at later time or head to the web instead."
}
```

### 22. Github Search

**Description**:
Searches GitHub for various types of content.

**Args:**
  - **query (str)**: The search query.
  - **search_type (str, optional)**: The type of search. Can be one of:
    - "repositories"
    - "users"
    - "organizations"
    - "issues"
    - "pull_requests"
    - "commits"
    - "topics"

**Description**:
Defaults to "repositories". max_results (int, optional): The maximum number of results to return. Defaults to 3.

**Returns:**
  - **list**: A list of search results or an error message.

```python
from TheApi import api

result = await api.github_search(query='Pokemon', search_type='repositories', max_results=3)
print(result)
```

#### Expected Output

```json
[
    {
        "name": "PokemonGo-Map",
        "full_name": "AHAAAAAAA/PokemonGo-Map",
        "description": "\ud83c\udf0f Live visualization of all the pokemon in your area... and more! (shutdown)",
        "url": "https://github.com/AHAAAAAAA/PokemonGo-Map",
        "language": null,
        "stargazers_count": 7528,
        "forks_count": 2815
    },
    {
        "name": "pokemon-showdown",
        "full_name": "smogon/pokemon-showdown",
        "description": "Pok\u00e9mon battle simulator.",
        "url": "https://github.com/smogon/pokemon-showdown",
        "language": "TypeScript",
        "stargazers_count": 4815,
        "forks_count": 2806
    },
    {
        "name": "PokemonGo-Bot",
        "full_name": "PokemonGoF/PokemonGo-Bot",
        "description": "The Pokemon Go Bot, baking with community.",
        "url": "https://github.com/PokemonGoF/PokemonGo-Bot",
        "language": "Python",
        "stargazers_count": 3875,
        "forks_count": 1541
    }
]
```

### 23. Hindi Quote

**Description**:
Fetches a random Hindi quote.

**Returns:**
  - **str**: The content of a random Hindi quote.

```python
from Pokemon import api

result = await api.hindi_quote()
print(result)
```

#### Expected Output

```text
ये रोटी भी सस्ती नहीं है यारो, कोई इसे कमाने को दौड़ता है तो कोई इसे पचाने को..
```

### 24. Hug

**Description**:
Fetches a specified number hug gif from the Nekos.Best API.

**Args:**
  - **amount (int)**: The number of neko images to fetch. Defaults to 1.

**Returns:**
  - **list**: A list of dictionaries containing information about each fetched neko image or GIF.
    Each dictionary typically includes:
    - anime_name (str): The name of the anime.
    - url (str): The URL of the GIF.

```python
from TheApi import api

result = await api.hug(amount=1)
print(result)
```

#### Expected Output

```json
[
    {
        "anime_name": "Original (???)",
        "url": "https://nekos.best/api/v2/hug/e93c3408-fa92-43ea-a6ff-106a5d88de85.gif"
    }
]
```

### 25. Meme

**Description**:
Fetches a random meme image URL.

**Returns:**
  - **str or None**: The URL of the meme image if available, otherwise None.

```python
from Pokemon import api

result = await api.meme()
print(result)
```

#### Expected Output

```text
https://preview.redd.it/h49jx3u77n3e1.png?width=1080&crop=smart&auto=webp&s=85f7d646c43e4306d1448d915a29214f6ec24999
```

### 26. Neko

**Description**:
Fetches a specified number of neko images or GIFs from the Nekos.Best API.

**Args:**
  - **endpoint (str)**: The endpoint category to fetch content from. Default is "neko".
    Valid image endpoints:
    - "husbando", "kitsune", "neko", "waifu"
    Valid GIF endpoints:
    - "baka", "bite", "blush", "bored", "cry", "cuddle", "dance", "facepalm",
    "feed", "handhold", "handshake", "happy", "highfive", "hug", "kick",
    "kiss", "laugh", "lurk", "nod", "nom", "nope", "pat", "peck", "poke",
    "pout", "punch", "shoot", "shrug", "slap", "sleep", "smile", "smug",
    "stare", "think", "thumbsup", "tickle", "wave", "wink", "yawn", "yeet"
    amount (int): The number of items to fetch. Default is 3.

**Returns:**
  - **dict**: A dictionary containing the results of the request. The dictionary has a key `"results"`,
    which holds a list of items.

**Raises:**
  - **ValueError**: If the endpoint is not a valid category.

```python
from TheApi import api

result = await api.neko(endpoint='neko', amount=3)
print(result)
```

#### Expected Output

```json
{
    "results": [
        {
            "artist_href": "https://www.pixiv.net/en/users/46271917",
            "artist_name": "Cynthia",
            "source_url": "https://www.pixiv.net/en/artworks/88148474",
            "url": "https://nekos.best/api/v2/neko/93498f13-abee-4dc4-8003-00772ba11b00.png"
        },
        {
            "artist_href": "https://www.pixiv.net/en/users/16643815",
            "artist_name": "\u30b7\u30e5\u30f4\u30a3",
            "source_url": "https://www.pixiv.net/en/artworks/91790338",
            "url": "https://nekos.best/api/v2/neko/27191713-b5f9-4902-94c6-76ac7faea9f0.png"
        },
        {
            "artist_href": "https://www.pixiv.net/en/users/7321921",
            "artist_name": "Nami",
            "source_url": "https://www.pixiv.net/en/artworks/83870090",
            "url": "https://nekos.best/api/v2/neko/b1d29e53-9cd4-4bb2-b591-edd7e8c866bc.png"
        }
    ]
}
```

### 27. Pypi

**Description**:
Retrieves metadata information about a specified Python package from the PyPI API.

**Args:**
  - **package_name (str)**: The name of the package to search for on PyPI.

**Returns:**
  - **dict or None**: A dictionary with relevant package information if found, containing:
    - name (str): Package name.
    - version (str): Latest package version.
    - summary (str): Short description of the package.
    - author (str): Package author.
    - author_email (str): Email of the package author.
    - license (str): License type.
    - home_page (str): URL of the package's homepage.
    - package_url (str): URL of the package on PyPI.
    - requires_python (str): Minimum Python version required.
    - keywords (str): Keywords associated with the package.
    - classifiers (list): List of PyPI classifiers.
    - project_urls (dict): Additional project URLs (e.g., source code, documentation).
    Returns None if the package is not found or there is an error.

```python
from TheApi import api

result = await api.pypi(package_name='Pokemon')
print(result)
```

#### Expected Output

```json
{
    "name": "pokemon",
    "version": "0.36",
    "summary": "ascii database of pokemon... in Python!",
    "author": "Vanessa Sochat",
    "author_email": "vsoch@noreply.github.users.com",
    "license": "LICENSE",
    "home_page": "https://github.com/vsoch/pokemon",
    "package_url": "https://pypi.org/project/pokemon/",
    "requires_python": "",
    "keywords": "pokemon,avatar,ascii,gravatar",
    "classifiers": [],
    "project_urls": {
        "Homepage": "https://github.com/vsoch/pokemon"
    }
}
```

### 28. Quote

**Description**:
Fetches a random quote.

**Returns:**
  - **str**: The content of a random quote followed by the author's name.

```python
from Pokemon import api

result = await api.quote()
print(result)
```

#### Expected Output

```text
Important principles may, and must, be inflexible.

author - Abraham Lincoln
```

### 29. Random Word

**Description**:
Fetches a random word.

**Returns:**
  - **str**: A random word if available; "None" if an error occurs.

```python
from Pokemon import api

result = await api.random_word()
print(result)
```

#### Expected Output

```text
gawkishnesses
```

### 30. Riddle

**Description**:
Fetches a random riddle from the Riddles API.

**Returns:**
  - **dict**: The riddle data in JSON format.

```python
from Pokemon import api

result = await api.riddle()
print(result)
```

#### Expected Output

```json
{
    "riddle": "I'm as big as an elephant, but lighter than a feather. What am I?",
    "answer": "The Wind"
}
```

### 31. Stackoverflow Search

**Description**:
Searches Stack Overflow for questions based on a query, returning results sorted by relevance or another specified criteria.

**Args:**
  - **query (str)**: The search query string.
  - **max_results (int, optional)**: The maximum number of results to return. Defaults to 3.
  - **sort_type (str, optional)**: The sorting criteria for the results, such as "relevance" or "votes". Defaults to "relevance".

**Returns:**
  - **list**: A list of search results in JSON format, with each entry containing Stack Overflow question details.

**Raises:**
  - **ValueError**: If there is an issue with the request to the Stack Overflow API.

```python
from TheApi import api

result = await api.stackoverflow_search(query='Pokemon', max_results=3, sort_type='relevance')
print(result)
```

#### Expected Output

```json
[
    {
        "tags": [
            "ios",
            "flutter",
            "dart"
        ],
        "owner": {
            "account_id": 19921816,
            "reputation": 3,
            "user_id": 14597469,
            "user_type": "registered",
            "profile_image": "https://lh6.googleusercontent.com/-aT6u2l_JT94/AAAAAAAAAAI/AAAAAAAAAAA/AMZuuclcxb94zp_q0Q2R8DQN7b6X3kgo6w/s96-c/photo.jpg?sz=256",
            "display_name": "Senem Sedef",
            "link": "https://stackoverflow.com/users/14597469/senem-sedef"
        },
        "is_answered": false,
        "view_count": 125,
        "answer_count": 0,
        "score": 0,
        "last_activity_date": 1701515081,
        "creation_date": 1622231772,
        "last_edit_date": 1701515081,
        "question_id": 67744802,
        "content_license": "CC BY-SA 4.0",
        "link": "https://stackoverflow.com/questions/67744802/the-getter-pokemon-was-called-on-null-receiver-null-tried-calling-pokemon",
        "title": "The getter &#39;pokemon&#39; was called on null. Receiver: null Tried calling: pokemon"
    },
    {
        "tags": [
            "reactjs",
            "random",
            "axios"
        ],
        "owner": {
            "account_id": 17931576,
            "reputation": 1,
            "user_id": 13028884,
            "user_type": "registered",
            "profile_image": "https://www.gravatar.com/avatar/7ebcdd2f784bca5dc54a1a0e17354f86?s=256&d=identicon&r=PG&f=y&so-version=2",
            "display_name": "GieGie",
            "link": "https://stackoverflow.com/users/13028884/giegie"
        },
        "is_answered": false,
        "view_count": 1999,
        "answer_count": 2,
        "score": 0,
        "last_activity_date": 1652730812,
        "creation_date": 1642222168,
        "last_edit_date": 1642223800,
        "question_id": 70718940,
        "content_license": "CC BY-SA 4.0",
        "link": "https://stackoverflow.com/questions/70718940/pokemon-api-request-generate-5-pok%c3%a9mon-at-a-time",
        "title": "Pokemon API request generate 5 Pok&#233;mon at a time"
    },
    {
        "tags": [
            "java"
        ],
        "owner": {
            "account_id": 919945,
            "reputation": 43,
            "user_id": 951797,
            "user_type": "registered",
            "profile_image": "https://www.gravatar.com/avatar/26b06d5d95992fa3780383abe5f49a3d?s=256&d=identicon&r=PG",
            "display_name": "Brian",
            "link": "https://stackoverflow.com/users/951797/brian"
        },
        "is_answered": true,
        "view_count": 32658,
        "accepted_answer_id": 7942409,
        "answer_count": 3,
        "score": 3,
        "last_activity_date": 1577442848,
        "creation_date": 1319931614,
        "question_id": 7942384,
        "content_license": "CC BY-SA 3.0",
        "link": "https://stackoverflow.com/questions/7942384/simple-java-pokemon-fight-simulator",
        "title": "Simple Java Pokemon Fight Simulator"
    }
]
```

### 32. Upload Image

**Description**:
Uploads an image to https://envs.sh.

**Args:**
  - **file_path (Union[str, bytes, BytesIO])**: The image file to upload.
    Can be a file path (str), binary data (bytes), or a BytesIO object.

**Returns:**
  - **str**: The URL or confirmation message of the uploaded image if the upload is successful.
    Returns "Unexpected response format" if the response format is not as expected.

**Raises:**
  - **ValueError**: If the file is not found, the input type is invalid,
    or the upload request fails.


### 33. Wikipedia

**Description**:
Searches Wikipedia for a given query and retrieves the top result's summary, URL, and image.

**Args:**
  - **query (str)**: The search term to look up on Wikipedia.

**Returns:**
  - **dict**: A dictionary containing information about the top search result, with keys:
    - title (str): The title of the Wikipedia article.
    - summary (str): A brief summary of the article's content.
    - url (str): The URL link to the full Wikipedia article.
    - image_url (str): The URL of the article's thumbnail image, or "No image available" if none exists.

**Description**:
If no results are found, returns a dictionary with an "error" key.

```python
from TheApi import api

result = await api.wikipedia(query='Pokemon')
print(result)
```

#### Expected Output

```json
{
    "title": "Pok\u00e9mon",
    "summary": "Pok\u00e9mon is a Japanese media franchise consisting of video games, animated series and films, a trading card game, and other related media. The franchise takes place in a shared universe in which humans co-exist with creatures known as Pok\u00e9mon, a large variety of species endowed with special powers. The franchise's target audience is children aged 5 to 12, but it is known to attract people of all ages.\nThe franchise originated as a pair of role-playing games developed by Game Freak, from an original concept by its founder, Satoshi Tajiri. Released on the Game Boy on February 27, 1996, the games became sleeper hits and were followed by manga series, a trading card game, and anime series and films. From 1998 to 2000, Pok\u00e9mon was exported to the rest of the world, creating an unprecedented global phenomenon dubbed \"Pok\u00e9mania\". By 2002, the craze had ended, after which Pok\u00e9mon became a fixture in popular culture, with new products being released to this day. In the summer of 2016, the franchise spawned a second craze with the release of Pok\u00e9mon Go, an augmented reality game developed by Niantic. Pok\u00e9mon has since been estimated to be the world's highest-grossing media franchise and one of the best-selling video game franchises.\nPok\u00e9mon has an uncommon ownership structure. Unlike most IPs, which are owned by one company, Pok\u00e9mon is jointly owned by three: Nintendo, Game Freak, and Creatures. Game Freak develops the core series role-playing games, which are published by Nintendo exclusively for their consoles, while Creatures manages the trading card game and related merchandise, occasionally developing spin-off titles. The three companies established The Pok\u00e9mon Company (TPC) in 1998 to manage the Pok\u00e9mon property within Asia. The Pok\u00e9mon anime series and films are co-owned by Shogakukan. Since 2009, The Pok\u00e9mon Company International (TPCi), a subsidiary of TPC, has managed the franchise in all regions outside of Asia.",
    "url": "https://en.wikipedia.org/?curid=23745",
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pok%C3%A9mon_logo.svg/500px-International_Pok%C3%A9mon_logo.svg.png"
}
```

### 34. Words

**Description**:
Fetches a specified number of random words.

**Args:**
  - **num_words (int)**: The number of random words to retrieve.

**Returns:**
  - **list**: A list of random words if available; an empty list if no response is received.

```python
from TheApi import api

result = await api.words(num_words=2)
print(result)
```

#### Expected Output

```text
craterlike
commonweal
```

### 35. Write

**Description**:
Creates an image with text written on it, using a predefined template and font, and uploads the image after generation.

**Args:**
  - **text (str)**: The text to be written on the image. Text exceeding 55 characters
    per line will be wrapped, with up to 25 lines displayed.

**Returns:**
  - **str**: The URL of the uploaded image.

**Description**:
Notes: A temporary image file is created, saved, and removed after uploading.

```python
from TheApi import api

result = await api.write(text='Pokemon')
print(result)
```

#### Expected Output

```text
/home/runner/work/TheApi/TheApi/downloads/write_hfajMfzb.jpg
```


This Project is Licensed under [MIT License](https://github.com/Vivekkumar-IN/TheApi/blob/main/LICENSE)