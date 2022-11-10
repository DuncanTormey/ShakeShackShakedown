import requests

from bs4 import BeautifulSoup
import pandas as pd
import reverse_geocode

response = requests.get("https://shakeshack.com/locations#/")
soup = BeautifulSoup(response.text, 'html.parser')
geo_locations = soup.find_all("div", {"class": "geolocation-location"})
df = pd.DataFrame([e.attrs for e in geo_locations])
df['data-lat'] = df['data-lat'].astype(float)
df['data-lng'] = df['data-lng'].astype(float)
# Edit line 77 of reverse_encode open() call. add "encoding="UTF-8""
df["location"] = df.apply(lambda r: reverse_geocode.search(((r["data-lat"], r["data-lng"]),))[0], axis=1)
df["country_code"] = df.location.apply(lambda x: x["country_code"])
df["city"] = df.location.apply(lambda x: x["city"])
df["country"] = df.location.apply(lambda x: x["country"])
df = df[['data-lat', 'data-lng', 'country', 'country_code', 'city']]
df = df[df.country_code == "US"]
df.to_csv("./shake_shack_us_locations.csv", index=False)

