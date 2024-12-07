import requests
from bs4 import BeautifulSoup

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo",
    "Virgo", "Libra", "Scorpio", "Sagittarius",
    "Capricorn", "Aquarius", "Pisces"
]

def get_horoscope(zodiac_sign: int, day: str) -> str:
    if not (1 <= zodiac_sign <= len(ZODIAC_SIGNS)):
        return "Invalid zodiac sign number. Please select a number between 1 and 12."
    
    if day not in ["yesterday", "today", "tomorrow"]:
        return "Invalid day. Please enter 'yesterday', 'today', or 'tomorrow'."
    
    url = (
        "https://www.horoscope.com/us/horoscopes/general/"
        f"horoscope-general-daily-{day}.aspx?sign={zodiac_sign}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        horoscope_text = soup.find("div", class_="main-horoscope").p.text.strip()
        return horoscope_text
    except requests.exceptions.RequestException as e:
        return f"Error fetching horoscope: {str(e)}"
    except AttributeError:
        return "Failed to scrape the horoscope. The website structure might have changed."

def astrogate():
    print("Welcome to Astrogator: Your Daily Horoscope\n")

    print("Select your Zodiac Sign:")
    for index, sign in enumerate(ZODIAC_SIGNS, start=1):
        print(f"{index}. {sign}")
    
    try:
        zodiac_sign = int(input("\nEnter the number of your Zodiac Sign: ").strip())
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 12.")
        return
    
    if not (1 <= zodiac_sign <= 12):
        print("Invalid zodiac sign selection. Please select a number between 1 and 12.")
        return
    
    print("\nChoose a day:")
    print("1. yesterday\n2. today\n3. tomorrow")
    
    day_options = {1: "yesterday", 2: "today", 3: "tomorrow"}
    try:
        day_choice = int(input("Enter the day (1/2/3): ").strip())
        day = day_options.get(day_choice, None)
    except ValueError:
        print("Invalid input. Please enter 1, 2, or 3.")
        return
    
    if not day:
        print("Invalid day selection. Please enter 1, 2, or 3.")
        return
    
    selected_sign = ZODIAC_SIGNS[zodiac_sign - 1]
    print(f"\nYour selected Zodiac Sign: {selected_sign}")
    print(f"Day: {day.capitalize()}")
    horoscope_text = get_horoscope(zodiac_sign, day)
    print("\nYour Horoscope:")
    print(horoscope_text)
