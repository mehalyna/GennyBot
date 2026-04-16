# GennyBot : Telegram Bot for Nearby Cafes & Restaurants (Python)

## 1. Overview
The system is a Telegram bot that responds to user requests by suggesting nearby cafes and restaurants based on the user's location.

## 2. Functional Requirements

### 2.1 User Interaction
- The bot must respond to `/start` command with a welcome message and instructions.
- The bot must accept user location via:
  - Telegram location sharing
  - Text input (city or address)
- The bot must process user queries like:
  - "Find кафе nearby"
  - "Restaurants near me"

### 2.2 Location Handling
- The bot must extract latitude and longitude from user input.
- If location is not provided, the bot must request it.

### 2.3 Data Retrieval
- The bot must integrate with a Places API (e.g., Google Places API or OpenStreetMap).
- The bot must fetch nearby cafes and restaurants based on location.

### 2.4 Response Generation
- The bot must return a list of 3–5 nearby places.
- Each result must include:
  - Name
  - Address
  - Rating (if available)
- The bot should format responses in a readable message.

## 3. Non-Functional Requirements

### 3.1 Performance
- Response time should not exceed 2–3 seconds.

### 3.2 Reliability
- The bot must handle API failures gracefully.
- The bot must provide fallback messages in case of errors.

### 3.3 Usability
- Messages must be clear and concise.
- The bot must guide users if input is invalid.

## 4. Technical Requirements

### 4.1 Technology Stack
- Language: Python 3.x
- Framework: `aiogram` or `python-telegram-bot`

### 4.2 Integrations
- Telegram Bot API
- External Places API (Google Places / OpenStreetMap)

### 4.3 Deployment
- The bot must be deployable on a cloud server (e.g., AWS, Heroku, or VPS).
- The bot must support webhook or polling mode.

## 5. Security Requirements
- API keys must be stored securely (environment variables).
- The bot must not log sensitive user data.

## 6. Minimal Data Model
- No database required for MVP.
- Optional: store user preferences or last location (in-memory or simple storage).

## 7. Testing Requirements
- Basic testing of:
  - Command handling
  - Location parsing
  - API integration
- Manual testing via Telegram client.

## 8. Future Enhancements (Optional)
- Filtering by cuisine or price
- User ratings and reviews
- Caching results for performance