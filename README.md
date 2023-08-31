# Chirp-Bot 🐦

Automate personalized Twitter responses with Chirp-Bot—a Python-based bot leveraging the Selenium framework and TweetGPT Chrome Extension. Perfect for customer service, engagement, or just for fun!

## Features

- Automated Twitter replies
- Easy to configure
- Built with Selenium and the TweetGPT Chrome Extension

## Prerequisites

- Python 3.x
- Google Chrome (Version 94)
- ChromeDriver (Version 94.0.4606.41)

## Setup

### Virtual Environment

1. Create a virtual environment: `python3 -m venv my_project_env`
2. Activate the virtual environment: 

#### Linux
`source venv/bin/activate`

#### Windows
`source venv\Scripts\activate`

### Install Dependencies

Install required *Python* packages:

```bash
pip install -r requirements.txt
```

### ChromeDriver

This repository includes `chromedriver.exe` which is compatible with Chrome Version 94 on Windows.

⚠️ **Note**: The current version of ChromeDriver is 94.0.4606.41. If you have a different version of Chrome, you may need to download the corresponding ChromeDriver from the [official site](https://sites.google.com/a/chromium.org/chromedriver/downloads).

### Configuration

Place your settings and credentials in `config/settings.json`.

### Running the Bot

Navigate to the `src/` directory and run:

```bash
python main.py