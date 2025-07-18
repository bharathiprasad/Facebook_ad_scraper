# 📊 Facebook Ad Scraper - Web App

A web-based interface for scraping and analyzing Facebook ad data. This project allows users to enter a Facebook Ad Library URL, extract relevant ad metadata, and display the results in a structured format.

## 🌐 Features

- Enter Facebook Ad Library URLs via a simple web UI
- Scrape ad information such as advertiser name, ad text, impressions, and more
- Display results in an organized table
- Built-in error handling for invalid URLs or missing data

## ⚙️ Tech Stack

- **Frontend**: HTML, CSS (via Bootstrap)
- **Backend**: Flask (Python)
- **Web Scraping**: BeautifulSoup, Requests

## 📸 Screenshots

> _Add a screenshot of your web UI and sample scraped results_

![Web App Screenshot](path/to/screenshot.png)

## 🚀 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/bharathiprasad/Facebook_ad_scraper.git
   cd Facebook_ad_scraper/web_app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask app**
   ```bash
   python app.py
   ```

5. **Access in browser**
   Visit `http://localhost:5000` in your web browser.

## 🗂️ Project Structure

```
web_app/
│
├── static/              # CSS and static assets
│
├── templates/           # HTML templates
│   └── index.html
│
├── app.py               # Main Flask application
├── scraper.py           # Web scraping logic
├── requirements.txt     # Python dependencies
└── README.md
```

## 🧪 Future Improvements

- Export results to CSV
- Support bulk URL input
- Add visualizations for ad analytics
- Improve robustness of scraping logic

## 🤝 Contributing

Pull requests and feature suggestions are welcome.  
Please open an issue to discuss your ideas or fixes.


**Author:** [Bharathi Prasad](https://github.com/bharathiprasad)
