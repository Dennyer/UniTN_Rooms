# 🏢 Rooms-UNITN Bot

**Inspiration**: This bot was inspired by [LocusPocusBot](https://github.com/matteocontrini/locuspocusbot) and aims to improve upon its features.

## 🌟 Features
- 🔍 **Search Capabilities**: Find rooms across various buildings.
- ❤️ **Favorites**: Save your preferred buildings for quicker access.
- 📅 **Schedule Overview**: View the complete schedule of a room for a chosen date.
- 🐳 **Docker Support**: Easy deployment using Docker and Docker Compose.

## 🚀 Future Plans
- Integrate a course schedule feature similar to [this bot](https://t.me/unitnEasyroomBot). Implementation is subject to time constraints.

## 🛠 Prerequisites
- MySQL server
- Python 3

## 📋 Installation & Setup

### Docker Setup 🐳
1. **Configuration**: Copy `.env` to `.env.local` and set the necessary environment variables.
2. **Build and Run**: Execute `docker-compose up --build` to build and start the bot and database containers.

### Traditional Setup 👷🏻‍♂️
1. **Configuration**: Copy `.env` to `.env.local` and set the necessary environment variables.
2. **Database Setup**: Execute the `database.sql` script to create and structure the database.
3. **Python Dependencies**: Install the required Python libraries (refer to the requirements file in the Source folder).
4. **Run the Bot**: Execute `main.py` to start the bot.

## 🔧 Core Components
- 🎹 **Keyboards**: Defines the bot's interactive keyboard layouts.
- 📡 **API Interactions**: Manages communications with external services for room details, schedules, etc.
- 💾 **Database Management**: Handles user data and preferences related to headquarters.
- 🗓 **Calendar**: Provides a user-friendly calendar interface for date selections.
- 🤖 **Bot Interactions** (`main.py`):
  - 🚀 **Initialization**: Sets up logging, API key loading, database connections, and bot dispatchers.
  - 📜 **Command Handling**: Manages bot commands like `start` and `help`.
  - 💬 **Message Management**: Processes user messages and callback queries.
  - 🏢 **Room Info**: Displays room events based on selected dates and user queries.
- 🔄 **Update**: Used during downtimes to reply with a predefined maintenance message
- ⚙️ **Maintenance**: Sends a message containing the changes made in the new version and the fact that it's online.

## 🤝 Contribution
Feedback and contributions are always welcome. Feel free to raise issues or submit pull requests.