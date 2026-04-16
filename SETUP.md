# GennyBot Setup Guide

## Prerequisites
- Python 3.8 or higher
- Telegram account
- Google Cloud account (for Places API)

## Step 1: Get Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token provided

## Step 2: Get Google Places API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Places API" and "Geocoding API"
4. Go to Credentials and create an API key
5. Copy the API key

## Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and add your tokens:
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token
GOOGLE_PLACES_API_KEY=your_actual_api_key
```

## Step 5: Run the Bot

```bash
python bot.py
```

## Usage

1. Open Telegram and find your bot
2. Send `/start` command
3. Share your location or type a city name
4. Ask for cafes or restaurants:
   - "Find cafe nearby"
   - "Show restaurants"
   - "Кафе рядом"

## Troubleshooting

- **Bot not responding**: Check that TELEGRAM_BOT_TOKEN is correct
- **No places found**: Verify GOOGLE_PLACES_API_KEY and API is enabled
- **Location errors**: Make sure Geocoding API is enabled in Google Cloud

## Notes

- The bot searches within 1.5 km radius
- Returns up to 5 results
- No database required for basic functionality
