# Algorithmic Trading Bot

This project is an algorithmic trading bot that collects, processes, and analyzes financial data for making trading decisions.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/trading_bot.git
   cd trading_bot
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```
   alembic upgrade head
   ```

5. Create a `.env` file in the project root and add your configuration:
   ```
   DB_HOST=localhost
   DB_NAME=trading_bot_db
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

## Usage

To run the main data collection and processing pipeline:
