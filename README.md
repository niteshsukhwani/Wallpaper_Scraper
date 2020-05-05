# Wallpaper_Scraper
Scrape the wallpaper from wallpaper.cc given the search query and number of wallpaper need to be scraped

## Usage

```python
# If you have chromedriver setup in your system
from Wallpaper_Scraper import Wallpaper_Scraper

object = Wallpaper_Scraper()
object.wallpaper_scraper(search_query = 'beast', num_of_img = 20)


# If you don't have chromedriver and want to scrape using BeautifulSoup
from wallpaper_scraper_beautifulsoup import Wallpaper_Scraper

object = Wallpaper_Scraper()
object.wallpaper_scraper(search_query = 'beast', num_of_img = 20)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
