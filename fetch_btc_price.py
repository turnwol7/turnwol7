# fetch_btc_price.py
import requests
import datetime
import time

def get_bitcoin_price():
    # Add retry logic with timeout
    max_retries = 3
    timeout = 10  # seconds
    
    for attempt in range(max_retries):
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            return data['bitcoin']['usd']
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1)  # Wait before retrying

def update_readme(price):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open("README.md", 'r') as file:
            content = file.read()
        
        btc_section = f"\n### Bitcoin Price Update\nLast updated: {current_time}\nCurrent price: ${price:,.2f} USD\n"
        
        if "### Bitcoin Price Update" in content:
            start_idx = content.find("### Bitcoin Price Update")
            end_idx = content.find("\n\n", start_idx)
            if end_idx == -1:
                end_idx = len(content)
            content = content[:start_idx] + btc_section + content[end_idx:]
        else:
            content += btc_section
        
        with open("README.md", 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error updating README: {e}")
        raise

if __name__ == "__main__":
    try:
        price = get_bitcoin_price()
        update_readme(price)
        print(f"Successfully updated Bitcoin price: ${price:,.2f}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)