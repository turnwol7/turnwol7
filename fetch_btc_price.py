import requests
import datetime
import subprocess
import time
from pathlib import Path

def get_bitcoin_price():
    # Using CoinGecko API (free, no API key required)
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data['bitcoin']['usd']

def update_readme(price):
    readme_path = Path("README.md")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Read current README content
    with open(readme_path, 'r') as file:
        content = file.read()
    
    # Add or update Bitcoin price section
    btc_section = f"\n### Bitcoin Price Update\nLast updated: {current_time}\nCurrent price: ${price:,.2f} USD\n"
    
    if "### Bitcoin Price Update" in content:
        # Update existing section
        start_idx = content.find("### Bitcoin Price Update")
        end_idx = content.find("\n\n", start_idx)
        if end_idx == -1:
            end_idx = len(content)
        content = content[:start_idx] + btc_section + content[end_idx:]
    else:
        # Add new section
        content += btc_section
    
    # Write updated content
    with open(readme_path, 'w') as file:
        file.write(content)

def commit_changes():
    # Configure git user
    subprocess.run(['git', 'config', 'user.name', 'turnwol7'])
    subprocess.run(['git', 'config', 'user.email', 'justinb.developer@gmail.com'])
    
    # Add and commit changes
    subprocess.run(['git', 'add', 'README.md'])
    subprocess.run(['git', 'commit', '-m', f'Update Bitcoin price - {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'])
    subprocess.run(['git', 'push'])

def main():
    while True:
        try:
            price = get_bitcoin_price()
            update_readme(price)
            commit_changes()
            print(f"Updated Bitcoin price: ${price:,.2f}")
        except Exception as e:
            print(f"Error occurred: {e}")
        
        # Wait for 6 hours (4 times per day)
        time.sleep(6 * 60 * 60)

if __name__ == "__main__":
    main()
