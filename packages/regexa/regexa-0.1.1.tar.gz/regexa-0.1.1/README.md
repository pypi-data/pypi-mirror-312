# Regexa - Python Regex Utility Library

Regexa is a comprehensive Python library that simplifies working with regular expressions for common text processing tasks. It provides an easy-to-use interface for validations, extractions, and text processing operations.

## Features

- Email, phone number and URL validation
- Password strength validation with detailed feedback
- Text extraction (emails, phones, URLs, hashtags, mentions etc)
- Date extraction in multiple formats
- File path processing
- Network validations (IP address, MAC address)
- Credit card validation
- Text cleaning utilities
- Pattern matching and counting

## Installation

```bash
pip install regexa
```

# Basic Usage
## Initialization
```python
from regexa import Regexa

rx = Regexa()
```

## 1. Email validation
```python
email = "john.doe@example.com"
print(f"Is email valid? {rx.match_email(email)}")

# Result: Is email valid? True
# Comment: The email is valid as it follows the standard email format
```

## 2. Password strength check
```python
password = "MyStr0ng#Pass"
strength = rx.validate_password_strength(password)
print(f"Password strength: {strength['strength']}")
print(f"Password feedback: {strength['feedback']}")

# Result:
# Password strength: Excellent
# Password feedback: ['Password length sufficient', 'Has uppercase letters', 'Has lowercase letters', 'Has numbers', 'Has special characters']
# Comment: The password is excellent because it meets all criteria: length, uppercase, lowercase, numbers, and special characters
```

## 3. Extract all data from text
```python
text = """
Contact me at john.doe@example.com or call +6281234567890
Visit our website: https://example.com
Follow us @company #tech #python
Meeting on 25/12/2023 and 2023-12-31
Credit card: 4111111111111111
"""

extracted = rx.extract_all(text)
print("\nExtracted data:")
for key, value in extracted.items():
    print(f"{key}: {value}")

# Result:
# emails: ['john.doe@example.com']
# phones: ['+6281234567890']
# urls: ['https://example.com']
# hashtags: ['#tech', '#python']
# mentions: ['@company']
# numbers: ['6281234567890', '25', '12', '2023', '2023', '12', '31']
# words: ['Contact', 'me', 'at', 'john', 'doe', 'example', 'com', ...]
# Comment: Successfully extracted all different types of data from the text
```

## 4. Date extraction
```python
dates = rx.extract_dates(text)
print("\nFound dates:")
for date in dates:
    print(f"Date: {date['date']} (Format: {date['format']})")

# Result:
# Date: 25/12/2023 (Format: dd/mm/yyyy)
# Date: 2023-12-31 (Format: yyyy-mm-dd)
# Comment: Detected dates in different formats
```

## 5. URL validation
```python
url = "https://example.com"
print(f"\nIs URL valid? {rx.match_url(url)}")

# Result: Is URL valid? True
# Comment: URL is valid as it contains the correct protocol and domain format
```

## 6. Credit card validation
```python
card_number = "4111111111111111"
card_validation = rx.validate_credit_card(card_number)
print(f"\nCredit card validation: {card_validation}")

# Result: Credit card validation: {'is_valid': True, 'card_type': 'visa', 'number': '4111111111111111'}
# Comment: Detected as a valid Visa card number
```

## 7. Clean text
```python
cleaned_text = rx.clean_text("Hello, World! @#$%")
print(f"\nCleaned text: {cleaned_text}")

# Result: Cleaned text: Hello World
# Comment: Removed all special characters, leaving only alphanumeric characters and spaces
```

## 8. IP validation
```python
ip = "192.168.1.1"
ip_validation = rx.validate_ip(ip)
print(f"\nIP validation: {ip_validation}")

# Result: IP validation: {'is_valid': True, 'type': 'IPv4', 'private': True}
# Comment: Valid IPv4 address identified as a private IP address
```

# Documentation
## Email Validation
```python
rx.match_email(text: str) -> bool
```
Validates if a string is a properly formatted email address.

## Phone Number Validation
```python
rx.match_phone_id(text: str) -> bool
```
Validates Indonesian phone numbers.

## URL Validation
```python
rx.match_url(text: str) -> bool
```
Checks if a string is a valid URL with HTTP/HTTPS protocol.

## Password Validation
```python
rx.validate_password_strength(password: str) -> Dict[str, Any]
```
Validates password strength and provides detailed feedback:

- Score (0-5)
- Strength level
- Specific feedback
- Overall validity

## Text Extraction
```python
rx.extract_all(text: str) -> Dict[str, List[str]]
```
Extracts various elements from text:

- Email addresses
- Phone numbers
- URLs
- Hashtags
- @mentions
- Numbers
- Words

## Text Cleaning
```python
rx.clean_text(text: str, remove_spaces: bool = False) -> str
```
Cleans text by removing special characters. Optional space removal.

## Date Extraction
```python
rx.extract_dates(text: str) -> List[Dict[str, Any]]
```
Extracts dates in various formats:

- dd/mm/yyyy
- yyyy-mm-dd
- dd-mm-yyyy
- Natural format (e.g. "25 December 2023")

## File Path Processing
```python
rx.extract_filename(path: str) -> Dict[str, str]
```
Extracts components from file paths:

- Directory
- Filename
- Extension
- Full path

## IP Address Validation
```python
rx.validate_ip(ip: str) -> Dict[str, Any]
```
Validates IPv4 and IPv6 addresses and provides:

- Validity status
- IP version
- Private network status (IPv4)

## Pattern Matching
```python
rx.count_matches(text: str, pattern: str) -> Dict[str, Any]
```
Counts pattern matches in text and provides:

- Match count
- Match positions
- Used pattern

## Credit Card Validation
```python
rx.validate_credit_card(number: str) -> Dict[str, Any]
```
Validates credit card numbers and identifies card type:

- Visa
- Mastercard
- American Express
- Discover

# Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

# License
This project is licensed under the MIT License - see the LICENSE file for details.
