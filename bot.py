#!/usr/bin/env python3
"""
GennyBot - Telegram Bot for Nearby Cafes & Restaurants
"""
import os
import logging
from typing import Optional
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    location_button = KeyboardButton(text="📍 Share Location", request_location=True)
    keyboard = [[location_button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    welcome_message = (
        "👋 Welcome to GennyBot!\n\n"
        "I help you find nearby cafes and restaurants.\n\n"
        "How to use:\n"
        "1. Share your location using the button below\n"
        "2. Or send me a city/address as text\n"
        "3. Ask me to find cafes or restaurants\n\n"
        "Try: 'Find cafe nearby' or 'Restaurants near me'"
    )

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle location sharing."""
    location = update.message.location
    latitude = location.latitude
    longitude = location.longitude

    # Store location in user context
    context.user_data['latitude'] = latitude
    context.user_data['longitude'] = longitude

    await update.message.reply_text(
        f"✅ Location received!\n"
        f"Now you can ask me to find cafes or restaurants.\n\n"
        f"Try: 'Find cafe' or 'Show restaurants'"
    )


async def geocode_address(address: str) -> Optional[tuple]:
    """Convert address to coordinates using Google Geocoding API."""
    if not GOOGLE_PLACES_API_KEY:
        return None

    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': GOOGLE_PLACES_API_KEY
    }

    try:
        response = requests.get(geocode_url, params=params, timeout=5)
        data = response.json()

        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            return (location['lat'], location['lng'])
    except Exception as e:
        logger.error(f"Geocoding error: {e}")

    return None


def fetch_nearby_places(latitude: float, longitude: float, place_type: str = 'restaurant') -> list:
    """Fetch nearby places using Google Places API."""
    if not GOOGLE_PLACES_API_KEY:
        return []

    params = {
        'location': f'{latitude},{longitude}',
        'radius': 1500,  # 1.5 km radius
        'type': place_type,
        'key': GOOGLE_PLACES_API_KEY
    }

    try:
        response = requests.get(PLACES_API_URL, params=params, timeout=5)
        data = response.json()

        if data['status'] == 'OK':
            return data['results'][:5]  # Return top 5 results
        else:
            logger.warning(f"Places API returned status: {data['status']}")
    except Exception as e:
        logger.error(f"Places API error: {e}")

    return []


def format_place_info(place: dict) -> str:
    """Format place information for display."""
    name = place.get('name', 'Unknown')
    address = place.get('vicinity', 'Address not available')
    rating = place.get('rating', 'N/A')

    return f"📍 {name}\n   {address}\n   ⭐ Rating: {rating}"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    text = update.message.text.lower()

    # Check if message is asking for cafes or restaurants
    is_cafe_query = any(word in text for word in ['cafe', 'кафе', 'coffee'])
    is_restaurant_query = any(word in text for word in ['restaurant', 'ресторан', 'eat', 'food'])

    if is_cafe_query or is_restaurant_query:
        # Check if we have user's location
        latitude = context.user_data.get('latitude')
        longitude = context.user_data.get('longitude')

        if not latitude or not longitude:
            await update.message.reply_text(
                "❌ Please share your location first!\n"
                "Use the button or send me your city/address."
            )
            return

        # Determine place type
        place_type = 'cafe' if is_cafe_query else 'restaurant'

        await update.message.reply_text("🔍 Searching for nearby places...")

        # Fetch places
        places = fetch_nearby_places(latitude, longitude, place_type)

        if not places:
            await update.message.reply_text(
                "😕 Sorry, I couldn't find any places nearby.\n"
                "Try a different location or check your API configuration."
            )
            return

        # Format and send results
        response = f"🎯 Found {len(places)} nearby {'cafes' if is_cafe_query else 'restaurants'}:\n\n"
        response += "\n\n".join([format_place_info(place) for place in places])

        await update.message.reply_text(response)

    else:
        # Assume it's a location (city or address)
        await update.message.reply_text(f"🔍 Looking up location: {update.message.text}")

        coords = await geocode_address(update.message.text)

        if coords:
            context.user_data['latitude'] = coords[0]
            context.user_data['longitude'] = coords[1]
            await update.message.reply_text(
                f"✅ Location set!\n"
                f"Now ask me to find cafes or restaurants."
            )
        else:
            await update.message.reply_text(
                "❌ Couldn't find that location.\n"
                "Please try again or share your location using the button."
            )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")

    if update and update.message:
        await update.message.reply_text(
            "❌ An error occurred. Please try again later."
        )


def main() -> None:
    """Start the bot."""
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        return

    if not GOOGLE_PLACES_API_KEY:
        logger.warning("GOOGLE_PLACES_API_KEY not found. Location features will be limited.")

    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # Start bot
    logger.info("Starting GennyBot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
