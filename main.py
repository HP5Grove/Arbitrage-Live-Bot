import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils import get_sports_odds


def send_email(subject, body, receivers): #Input individualised sender email, the smtp server adress (this will depend on the email provider), and app password
    sender_email = "" 
    smtp_server = ""
    smtp_port = 587 
    password = "" 

    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            msg['To'] = "".join(receivers) #paste email within quotation
            server.sendmail(sender_email, receivers, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def display_sports_odds(api_key):
    try:
        events = get_sports_odds(api_key)
        if not events:
            print("No sports events found.")
        else:
            for event in events:
                sport_name = event.get('sport_title', 'Unknown Sport')
                home_team = event['home_team']
                away_team = event['away_team']

                bookmakers = event.get('bookmakers', [])
                if bookmakers:
                    best_odds = {}
                    for bookmaker in bookmakers:
                        markets = bookmaker.get('markets', [])
                        for market in markets:
                            if market['key'] == 'h2h':
                                odds = market.get('outcomes', [])
                                if odds:
                                    for outcome in odds:
                                        outcome_name = outcome['name']
                                        if outcome_name not in best_odds or outcome['price'] > best_odds[outcome_name][
                                            'price']:
                                            best_odds[outcome_name] = {
                                                'price': outcome['price'],
                                                'bookmaker': bookmaker['title']
                                            }

                    
                    arbitrage_decimal = sum(1 / details['price'] for details in best_odds.values())
                    
                    roi = (1 / arbitrage_decimal - 1) * 100
                    
                    if roi > 1: #Change value based upon what ROI threshold wanted
                        print(f"ARBITRAGE OPPORTUNITY FOUND! ({sport_name})")
                        print(f"  ROI: {roi:.2f}%")
                        print(f"  Match: {home_team} vs {away_team}")

                        
                        total_stake = 100 # change to alter hypothetical stake, this will also change the stakes calculated and sent via email
                        for outcome_name, details in best_odds.items():
                            stake = (total_stake / details['price']) / arbitrage_decimal
                            print(f"  Stake for {outcome_name}: ${stake:.2f} (Bookmaker: {details['bookmaker']})")

                       
                        subject = f"Arbitrage Opportunity Found! ({sport_name})"
                        body = f"ROI: {roi:.2f}%\n"
                        body += f"Match: {home_team} vs {away_team}\n"
                        for outcome_name, details in best_odds.items():
                            stake = (total_stake / details['price']) / arbitrage_decimal
                            body += f"Stake for {outcome_name}: ${stake:.2f} (Best odds: {details['price']} - Bookmaker: {details['bookmaker']})\n"

                            
                            receivers = [""] #paste your email here

                        send_email(subject, body, receivers)
                        print("\n")

    except Exception as e:
        print(f"Error: {e}")


def main():
    api_key = "" #Paste API key here
    while True:
        print("Checking for arbitrage opportunities across all sports...")
        display_sports_odds(api_key)
        print("Waiting for the next check in 1 minutes...")
        time.sleep(60)


if __name__ == "__main__":
    main()
