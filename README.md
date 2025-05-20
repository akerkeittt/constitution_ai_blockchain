# Crypto Assistant - README

## Overview

Crypto Assistant is a Streamlit-based web application that provides real-time cryptocurrency information and AI-powered assistance for the top 50 cryptocurrencies. The application combines data from CoinMarketCap, Binance, and CryptoPanic APIs with the Mistral AI model to deliver comprehensive crypto insights.

## Features

- **Real-time Crypto Data**: Fetches and displays information about the top 50 cryptocurrencies
- **AI-Powered Q&A**: Answers user questions about specific cryptocurrencies using contextual data
- **Comprehensive Data Display**:
  - Current prices
  - 24-hour price changes
  - Market capitalization
  - Coin rankings
  - Latest news articles
- **User-Friendly Interface**: Clean, responsive design with a dashboard layout

## Technical Stack

- **Backend**: Python
- **Frontend**: Streamlit
- **APIs**:
  - CoinMarketCap (for coin listings and basic data)
  - Binance (for price data)
  - CryptoPanic (for news)
- **AI**: Ollama with Mistral model
- **Environment**: Python-dotenv for configuration

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/crypto-assistant.git
   cd crypto-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   COINMARKETCAP_API_KEY=your_api_key_here
   NEWS_API_KEY=your_cryptopanic_key_here
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. The left panel displays a table of the top 50 cryptocurrencies with key metrics
2. Use the chat interface on the right to ask questions about specific cryptocurrencies
3. Example queries:
   - "What's the price of Bitcoin?"
   - "Show me Ethereum news"
   - "What's the market cap of Solana?"

## Requirements

- Python 3.8+
- Required packages (see `requirements.txt`):
  - streamlit
  - requests
  - ollama
  - python-dotenv
  - pandas

## API Requirements

To use this application, you need:
1. A CoinMarketCap API key (free tier available)
2. A CryptoPanic API key (free tier available)

## Limitations

- Only supports the top 50 cryptocurrencies by market cap
- Requires internet connection to fetch real-time data
- News availability depends on CryptoPanic's coverage

## Screenshot

![image](https://github.com/user-attachments/assets/16d09961-e319-44da-982d-e66e5b2cc35a)

![image](https://github.com/user-attachments/assets/14d38265-d176-4924-a9da-57e45f39d999)

![image](https://github.com/user-attachments/assets/7eb785cd-0e3b-4b9a-9e23-b49eb226444c)

![image](https://github.com/user-attachments/assets/cc2dee69-217f-423c-bc8a-c3ccdaa96535)

![image](https://github.com/user-attachments/assets/de3b3fd8-151c-4e3b-ab7a-1b2ccf17fbd9)

if not from top-50:

![image](https://github.com/user-attachments/assets/b03dfd07-0451-4a82-8cf5-57d071b041c6)

![image](https://github.com/user-attachments/assets/937cb5bc-2cbd-4fbf-a304-aff9ffa246ae)


## License

This project is licensed under the MIT License. See the LICENSE file for details.
