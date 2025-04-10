import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
from googlesearch import search
from bs4 import BeautifulSoup
import re
import os
from colorama import init, Fore, Style

init(autoreset=True)

def print_heading():
    print(Fore.CYAN + "="*65)
    print(Fore.GREEN + Style.BRIGHT + "         RAHUL BHAI KA LEVEL 3 CYBER TOOL - ADVANCED")
    print(Fore.YELLOW + "   Phone Number OSINT + Social + IP Tracer (Free APIs Only)")
    print(Fore.CYAN + "="*65 + "\n")

def get_basic_info(phone):
    try:
        parsed = phonenumbers.parse(phone)
        if phonenumbers.is_valid_number(parsed):
            location = geocoder.description_for_number(parsed, "en")
            sim_carrier = carrier.name_for_number(parsed, "en")
            timezones = timezone.time_zones_for_number(parsed)
            return {
                "location": location,
                "carrier": sim_carrier,
                "timezone": list(timezones)
            }
    except:
        return None

def get_google_mentions(phone):
    try:
        print(Fore.MAGENTA + "   [+] Searching Google...")
        dork = f'"{phone}" OR intext:{phone} OR site:pastebin.com {phone}'
        results = list(search(dork, num_results=10))
        return results
    except Exception as e:
        print(Fore.RED + f"   [!] Google search failed: {e}")
        return []

def extract_names_and_locations(links):
    names = set()
    locations = set()
    name_pattern = re.compile(r'\b[A-Z][a-z]+ [A-Z][a-z]+')
    location_pattern = re.compile(r'\b[A-Z][a-z]+, [A-Z][a-z]+')

    for link in links:
        try:
            res = requests.get(link, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            text = soup.get_text()
            names.update(name_pattern.findall(text))
            locations.update(location_pattern.findall(text))
        except:
            continue
    return list(names), list(locations)

def get_social_profiles(phone):
    profiles = {}
    username = phone.replace("+", "").replace(" ", "")
    try:
        print(Fore.MAGENTA + "   [+] Checking limited social profiles...")
        urls = {
            "Facebook": f"https://facebook.com/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "Twitter": f"https://twitter.com/{username}"
        }
        for platform, url in urls.items():
            r = requests.get(url)
            if r.status_code == 200 and "Page Not Found" not in r.text:
                profiles[platform] = url
    except:
        pass
    return profiles

def get_ip_location():
    try:
        ip = requests.get("https://api.ipify.org").text
        loc = requests.get(f"http://ip-api.com/json/{ip}").json()
        return {
            "ip": ip,
            "city": loc.get("city"),
            "region": loc.get("regionName"),
            "country": loc.get("country")
        }
    except:
        return None

def show_results(phone):
    print_heading()
    print(Fore.BLUE + f"Target Phone Number: {phone}\n")

    basic = get_basic_info(phone)
    print(Fore.CYAN + "[+] Basic Info:")
    if basic:
        print(Fore.GREEN + f"   Location : {basic['location']}")
        print(Fore.GREEN + f"   Carrier  : {basic['carrier']}")
        print(Fore.GREEN + f"   Timezone : {', '.join(basic['timezone'])}")
    else:
        print(Fore.RED + "   [!] Could not fetch basic info")

    links = get_google_mentions(phone)
    print(Fore.CYAN + "\n[+] Google Mentions:")
    if links:
        for i, link in enumerate(links, 1):
            print(Fore.YELLOW + f"   [{i}] {link}")
    else:
        print(Fore.RED + "   [!] No mentions found")

    names, locations = extract_names_and_locations(links)
    print(Fore.CYAN + "\n[+] Extracted Names:")
    if names:
        for name in names:
            print(Fore.GREEN + f"   - {name}")
    else:
        print(Fore.RED + "   [!] No names extracted")

    print(Fore.CYAN + "\n[+] Extracted Locations:")
    if locations:
        for loc in locations:
            print(Fore.GREEN + f"   - {loc}")
    else:
        print(Fore.RED + "   [!] No locations extracted")

    print(Fore.CYAN + "\n[+] WhatsApp Link:")
    print(Fore.GREEN + f"   https://wa.me/{phone.replace('+', '')}")

    ip_info = get_ip_location()
    print(Fore.CYAN + "\n[+] Your IP Location:")
    if ip_info:
        print(Fore.GREEN + f"   {ip_info['ip']} - {ip_info['city']}, {ip_info['region']}, {ip_info['country']}")
    else:
        print(Fore.RED + "   [!] Could not fetch IP location")

    profiles = get_social_profiles(phone)
    print(Fore.CYAN + "\n[+] Social Media Links:")
    if profiles:
        for k, v in profiles.items():
            print(Fore.GREEN + f"   {k}: {v}")
    else:
        print(Fore.RED + "   [!] No public profiles found")

    print(Fore.CYAN + "\n[✓] Scan complete.")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    phone = input(Fore.YELLOW + "Enter phone number with country code (e.g. +919876543210): ")
    show_results(phone)
