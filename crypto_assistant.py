import os
import requests
import ollama
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import re

load_dotenv()

class CryptoAssistant:
    def __init__(self):
        self.top_coins = self._load_top_coins()
    
    def _load_top_coins(self):
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {
            'start': '1',
            'limit': '50',
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': os.getenv("COINMARKETCAP_API_KEY"),
        }
        
        try:
            response = requests.get(url, headers=headers, params=parameters)
            data = response.json()
            return {coin['symbol']: coin for coin in data['data']}
        except Exception as e:
            st.error(f"Error fetching top coins: {e}")
            return {}

    def get_coin_info(self, coin_symbol: str):
        coin = self.top_coins.get(coin_symbol.upper())
        if not coin:
            raise ValueError(f"Coin {coin_symbol} not in top 50")
        return coin
    
    def get_coin_news(self, coin_symbol: str, limit: int = 3):
        url = "https://cryptopanic.com/api/v1/posts/"
        params = {
            'auth_token': os.getenv("NEWS_API_KEY"),
            'currencies': coin_symbol.upper(),
            'public': 'true',
            'limit': limit
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if 'results' in data:
                return data['results']
            else:
                return []
        except Exception as e:
            # Не показываем ошибку в UI, чтобы не засорять
            return []
    
    def get_coin_price(self, coin_symbol: str):
        symbol = f"{coin_symbol.upper()}USDT"
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        try:
            response = requests.get(url)
            price = float(response.json().get('price', 0))
            if price == 0:
                raise ValueError("Price zero from Binance")
            return price
        except:
            coin = self.get_coin_info(coin_symbol)
            return coin['quote']['USD']['price']
    
    def generate_response(self, query: str, context: dict):
        prompt = f"""
        [INST]You are a professional crypto assistant. Answer the user's question using the provided data.
        
        **Rules:**
        - Use PROPER SPACING between numbers and words (e.g., "$2,540.09 with a market cap of $306.23B").
        - Separate numbers and text clearly.
        - Avoid concatenated words like "2540.09with".

        Question: {query}
        
        Context:
        - Coin: {context.get('symbol', 'N/A')}
        - Current price: ${context.get('price', 'N/A'):.2f}
        - Price change (24h): {context.get('price_change_24h', 'N/A'):.2f}%
        - Market cap: ${context.get('market_cap', 'N/A'):,.2f}
        - Rank: #{context.get('rank', 'N/A')}
        - Latest news: {[n['title'] for n in context.get('news', [])]}
        
        Provide a clear, professional answer in English. Be informative but concise.
        Use only the provided data.[/INST]
        """
        
        try:
            response = ollama.generate(
                model='mistral',
                prompt=prompt,
                options={
                    'temperature': 0.5,
                    'num_ctx': 4096
                }
            )
            return response['response']
        except Exception as e:
            return self._fallback_response(context)
    
    def _fallback_response(self, context: dict):
        return f"""
        Information about {context.get('symbol', 'the coin')}:
        - Price: ${context.get('price', 'N/A'):.2f}
        - Market cap: ${context.get('market_cap', 'N/A'):,.2f}
        - Rank: #{context.get('rank', 'N/A')}
        - News: {', '.join(n['title'] for n in context.get('news', []))}
        """

def extract_coin_from_query(query: str, top_coins: dict) -> str:
    query_lower = query.lower()

    for symbol in top_coins:
        if re.search(r'\b' + re.escape(symbol.lower()) + r'\b', query_lower):
            return symbol

    for symbol, data in top_coins.items():
        coin_name = data['name'].lower()
        if re.search(r'\b' + re.escape(coin_name) + r'\b', query_lower):
            return symbol

    for symbol, data in top_coins.items():
        coin_name = data['name'].lower()
        words = coin_name.split()
        for w in words:
            if re.search(r'\b' + re.escape(w) + r'\b', query_lower):
                return symbol

    return None

assistant = CryptoAssistant()

st.set_page_config(page_title="Crypto Assistant", layout="wide")

st.markdown("""
    <style>
    .response-text {
        font-size: 16px;
        line-height: 1.6;
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: transparent !important;
        text-shadow: none !important;
        padding: 10px;
    }
    .coin-table {
        font-size: 14px;
    }
    .according-text {
        font-size: 12px;
        color: #bbb;
        font-style: italic;
        margin-top: -8px;
        margin-bottom: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.title("AI Crypto Assistant")

col_coins, col_chat = st.columns([1, 2])

with col_coins:
    st.subheader("Top 50 Cryptocurrencies")
    coins_data = []
    for symbol in assistant.top_coins:
        coin = assistant.top_coins[symbol]
        coins_data.append({
            "Symbol": symbol,
            "Price": f"${coin['quote']['USD']['price']:.2f}",
            "24h %": f"{coin['quote']['USD']['percent_change_24h']:.1f}%",
            "Market Cap": f"${coin['quote']['USD']['market_cap']/1e9:.1f}B"
        })
    st.dataframe(
        pd.DataFrame(coins_data),
        height=600,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Symbol": st.column_config.TextColumn(width="small"),
            "Price": st.column_config.TextColumn(width="small"),
            "24h %": st.column_config.TextColumn(width="small"),
            "Market Cap": st.column_config.TextColumn(width="small")
        }
    )
    st.markdown('<div class="according-text">Data according to CoinMarketCap API</div>', unsafe_allow_html=True)

with col_chat:
    st.subheader("Chat with Assistant")
    user_query = st.text_input(
        "Ask about any top 50 cryptocurrency",
        placeholder="E.g. 'What's the price of Bitcoin?' or 'ETH news'"
    )
    if user_query:
        coin_symbol = extract_coin_from_query(user_query, assistant.top_coins)
        if not coin_symbol:
            st.error("Please mention a top 50 cryptocurrency (e.g. 'BTC' or 'Ethereum')")
        else:
            with st.spinner("Gathering data..."):
                try:
                    coin_info = assistant.get_coin_info(coin_symbol)
                    context = {
                        "symbol": coin_symbol,
                        "price": assistant.get_coin_price(coin_symbol),
                        "price_change_24h": coin_info['quote']['USD']['percent_change_24h'],
                        "market_cap": coin_info['quote']['USD']['market_cap'],
                        "rank": coin_info['cmc_rank'],
                        "news": assistant.get_coin_news(coin_symbol, limit=3)
                    }
                    response = assistant.generate_response(user_query, context)
                    st.write(f'<div class="response-text">{response}</div>', unsafe_allow_html=True)
                    with st.expander("Details"):
                        st.metric(
                            label="Current Price",
                            value=f"${context['price']:.2f}",
                            delta=f"{context['price_change_24h']:.2f}% (24h)"
                        )
                        st.write(f"**Rank:** #{context['rank']}")
                        st.write(f"**Market Cap:** ${context['market_cap']:,.2f}")
                        if context['news']:
                            st.write("**Latest News:**")
                            for news in context['news']:
                                published_at = datetime.strptime(news['published_at'], '%Y-%m-%dT%H:%M:%SZ')
                                st.markdown(f"- [{news['title']}]({news['url']}) ({published_at.strftime('%d.%m.%Y %H:%M')})")
                        else:
                            st.write("No recent news found.")
                except Exception as e:
                    st.error(f"Error processing request: {e}")
