# AniNews

A Discord bot that automatically monitors anime news and ranking updates, posting them directly to your Discord server in real time.

## ✨ Features

* 📰 Automatically posts the latest news from **IntoxiAnime** using their RSS feed.
* 🖼️ Extracts and displays the featured image for each article.
* 🚫 Prevents duplicate news posts by storing previously shared links.
* 🔥 Tracks the **Top 20 Anime** ranking from the Jikan API (MyAnimeList).
* ⬆️ Detects when an anime moves up in the ranking.
* ⬇️ Detects when an anime moves down in the ranking.
* 🆕 Notifies when a new anime enters the Top 20.
* ⏱️ Automatically checks for updates every 30 minutes.

## 🛠️ Technologies

* Python 3
* discord.py
* feedparser
* BeautifulSoup4
* requests
* python-dotenv
* Jikan API
* IntoxiAnime RSS Feed

## 📂 Project Structure

```text
AniNews/
│
├── cogs/
│   ├── news.py
│   └── top_anime.py
│
├── posts_enviados.json
├── top_anime.json
├── .env
├── main.py
└── requirements.txt
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/AniNews.git
cd AniNews
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
TOKEN=YOUR_DISCORD_BOT_TOKEN
```

Run the bot:

```bash
python main.py
```

## 🔑 Environment Variables

| Variable | Description            |
| -------- | ---------------------- |
| `TOKEN`  | Your Discord bot token |

## 📡 Data Sources

* **IntoxiAnime RSS Feed** – Latest anime news.
* **Jikan API** – Top anime rankings based on MyAnimeList.

## 🚀 Future Improvements

* Slash commands.
* Customizable update intervals.
* Multiple news sources.
* Anime search commands.
* Character and manga search.
* Server-specific configuration.
* Notification roles.

## 📄 License

This project is open-source and available under the MIT License.
