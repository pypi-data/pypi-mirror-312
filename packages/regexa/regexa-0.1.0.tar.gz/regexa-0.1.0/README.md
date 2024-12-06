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
# Quick Start
```python
from regexa import Regexa
```
# Initialize
```
rx = Regexa()

# Email validation
is_valid = rx.match_email("user@example.com")
print(is_valid)  # True

# Password strength check
result = rx.validate_password_strength("MyStr0ng#Pass")
print(result)
# {
#     'score': 5,
#     'strength': 'Excellent',
#     'feedback': ['Password length sufficient', 'Has uppercase', ...],
#     'is_valid': True
# }

# Extract data from text
data = rx.extract_all("Contact me at user@email.com or #support")
print(data)
# {
#     'emails': ['user@email.com'],
#     'hashtags': ['#support'],
#     'phones': [],
#     'urls': [],
#     'mentions': [],
#     'numbers': [],
#     'words': ['Contact', 'me', 'at', 'user', 'email', 'com', 'or', 'support']
# }
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
