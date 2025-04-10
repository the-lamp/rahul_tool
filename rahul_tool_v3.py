import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from googlesearch import search
import re
import time
import os
import requests

try:
    from colorama import init, Fore, Style
except ImportError:
    os.system('pip install colorama')
    from colorama import init, Fore, Style

init(autoreset=True)


def print_heading():
    print(Fore.CYAN + "="*65)
    print(Fore.GREEN + Style.BRIGHT + "         RAHUL BHAI KA LEVEL 3 CYBER TOOL")
    print(Fore.YELLOW + "   Phone Number OSINT + Social + IP Tracer Tool")
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
    except:
        return []


def extract_names_and_locations(results):
    names = set()
    locations = set()
    pattern_name = re.compile(r'\b[A-Z][a-z]+\s[A-Z][a-z]+')
    pattern_location = re.compile(r'in\s+[A-Z][a-z]+')

    for link in results:
        try:
            content = link.lower()
            names.update(pattern_name.findall(content))
            locations.update(pattern_location.findall(content))
        except:
            continue
    return list(names), list(locations)


def get_truecaller_like_data(phone):
    try:
        print(Fore.MAGENTA + "[+] Checking public name lookup...")
        url = f"https://api.apilayer.com/number_verification/validate?number={phone}"
        headers = {"apikey": "REPLACE_WITH_FREE_API_KEY"}  # You need to register on apilayer or numverify
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            return data.get("line_type"), data.get("location"), data.get("carrier"), data.get("country_name")
    except:
        return None, None, None, None


def get_social_profiles(phone):
    profiles = {}
    try:
        print(Fore.MAGENTA + "[+] Searching on social platforms (limited)")
        username = phone.replace("+", "").replace(" ", "")
        platforms = {
            "Twitter": f"https://twitter.com/{username}",
            "Facebook": f"https://facebook.com/{username}",
            "Instagram": f"https://instagram.com/{username}"
        }
        for name, url in platforms.items():
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    profiles[name] = url
            except:
                continue
    except:
        pass
    return profiles


def get_ip_location():
    try:
        print(Fore.MAGENTA + "[+] Getting your current IP-based location...")
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


def export_to_file(phone, basic, names, locations, results, wa_link, ip_info, profiles):
    with open("rahul_report.txt", "w", encoding='utf-8') as f:
        f.write(f"RAHUL BHAI LEVEL 3 TOOL REPORT\nPhone: {phone}\n\n")
        if basic:
            f.write(f"Location: {basic['location']}\n")
            f.write(f"Carrier: {basic['carrier']}\n")
            f.write(f"Timezone: {', '.join(basic['timezone'])}\n")
        f.write(f"\nNames Found:\n")
        for name in names:
            f.write(f" - {name}\n")
        f.write(f"\nLocations Mentioned:\n")
        for loc in locations:
            f.write(f" - {loc}\n")
        f.write(f"\nGoogle Mentions:\n")
        for link in results:
            f.write(f" - {link}\n")
        f.write(f"\nWhatsApp Link: {wa_link}\n")
        if ip_info:
            f.write(f"\nYour IP Location:\n - IP: {ip_info['ip']}, {ip_info['city']}, {ip_info['region']}, {ip_info['country']}\n")
        if profiles:
            f.write(f"\nPossible Social Profiles:\n")
            for k, v in profiles.items():
                f.write(f" - {k}: {v}\n")


def show_results(phone):
    print_heading()
    print(Fore.BLUE + f"Target Phone Number: {phone}\n")

    # Basic Info
    print(Fore.CYAN + "[+] Basic Info:")
    basic = get_basic_info(phone)
    if basic:
        print(Fore.GREEN + f"   Location : {basic['location']}")
        print(Fore.GREEN + f"   Carrier  : {basic['carrier']}")
        print(Fore.GREEN + f"   Timezone : {', '.join(basic['timezone'])}")
    else:
        print(Fore.RED + "   [!] Failed to fetch basic info.")

    # Google Search
    results = get_google_mentions(phone)
    print("\n" + Fore.CYAN + "[+] Google Mentions:")
    if results:
        for i, link in enumerate(results):
            print(Fore.YELLOW + f"   [{i+1}] {link}")
    else:
        print(Fore.RED + "   [!] No public results found.")

    # Extracted Names & Locations
    names, locations = extract_names_and_locations(results)
    print("\n" + Fore.CYAN + "[+] Name Guessing (from Google):")
    if names:
        for name in names:
            print(Fore.GREEN + f"   - {name}")
    else:
        print(Fore.RED + "   [!] No names found.")

    print("\n" + Fore.CYAN + "[+] Locations Mentioned:")
    if locations:
        for loc in locations:
            print(Fore.GREEN + f"   - {loc}")
    else:
        print(Fore.RED + "   [!] No locations found.")

    # WhatsApp Link
    print("\n" + Fore.CYAN + "[+] WhatsApp Link:")
    wa_link = f"https://wa.me/{phone.replace('+', '')}"
    print(Fore.GREEN + f"   {wa_link}")

    # Truecaller-style lookup
result = get_truecaller_like_data(phone)
if result and isinstance(result, tuple) and len(result) == 4:
    lt, loc, car, ctry = result
else:
    lt, loc, car, ctry = "N/A", "N/A", "N/A", "N/A"

print("\n" + Fore.CYAN + "[+] Public Lookup:")
if lt != "N/A" or loc != "N/A" or car != "N/A":
    print(Fore.GREEN + f"   Line Type : {lt}")
    print(Fore.GREEN + f"   Location  : {loc}")
    print(Fore.GREEN + f"   Carrier   : {car}")
    print(Fore.GREEN + f"   Country   : {ctry}")
else:
    print(Fore.RED + "   [!] Failed to fetch public name lookup.")

    
    # IP Geolocation
    ip_info = get_ip_location()
    print("\n" + Fore.CYAN + "[+] Your IP Location:")
    if ip_info:
        print(Fore.GREEN + f"   {ip_info['ip']} - {ip_info['city']}, {ip_info['region']}, {ip_info['country']}")
    else:
        print(Fore.RED + "   [!] IP location fetch failed.")

    # Social Profile Scan
    profiles = get_social_profiles(phone)
    print("\n" + Fore.CYAN + "[+] Social Media Links:")
    if profiles:
        for k, v in profiles.items():
            print(Fore.GREEN + f"   {k}: {v}")
    else:
        print(Fore.RED + "   [!] No public profiles found.")

    # Save to file
    print(Fore.CYAN + "\n[+] Saving full report to 'rahul_report.txt'...")
    export_to_file(phone, basic, names, locations, results, wa_link, ip_info, profiles)
    print(Fore.GREEN + "[✓] All done! Report saved successfully.")


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    phone = input(Fore.YELLOW + "Enter phone number with country code (e.g. +919876543210): ")
    show_results(phone)
