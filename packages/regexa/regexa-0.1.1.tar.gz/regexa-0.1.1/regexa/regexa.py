import re
from typing import List, Optional, Union, Pattern, Dict, Any
from datetime import datetime

class Regexa:
    """
    A comprehensive library to simplify regex usage in Python with complete features

    The Regexa class provides a collection of methods for common text processing tasks
    using regular expressions, including:
    - Email, phone number, and URL validation
    - Password strength validation
    - Text extraction and cleaning
    - Date extraction
    - File path processing
    - Network-related validations
    - Credit card validation

    Examples:
        >>> rx = Regexa()

        # Validate email
        >>> rx.match_email("user@example.com")
        True

        # Validate password strength
        >>> rx.validate_password_strength("MyStr0ng#Pass")
        {
            'score': 5,
            'strength': 'Excellent',
            'feedback': ['Password length sufficient', 'Has uppercase', ...],
            'is_valid': True
        }

        # Extract data from text
        >>> rx.extract_all("Contact me at user@email.com or #support")
        {
            'emails': ['user@email.com'],
            'hashtags': ['#support'],
            ...
        }
    """

    def __init__(self):
        """
        Initialize Regexa with predefined regex patterns for common validations
        """
        self.pattern = None
        self._patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone_id': r'^(\+62|62|0)[0-9]{9,12}$',
            'url': r'^(http|https):\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/\S*)?$',
            'ipv4': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
            'ipv6': r'^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$',
            'mac_address': r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',
            'credit_card': r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})$'
        }

    def match_pattern(self, text: str, pattern_type: str) -> bool:
        """
        Match text against a predefined pattern

        Args:
            text (str): Text to validate
            pattern_type (str): Type of pattern to match against

        Returns:
            bool: True if text matches the pattern, False otherwise

        Raises:
            ValueError: If pattern_type is not found in predefined patterns
        """
        if pattern_type not in self._patterns:
            raise ValueError(f"Pattern type '{pattern_type}' not available")
        return bool(re.match(self._patterns[pattern_type], text))

    def match_email(self, text: str) -> bool:
        """
        Check if text is a valid email address

        Args:
            text (str): Email address to validate

        Returns:
            bool: True if email is valid, False otherwise
        """
        return self.match_pattern(text, 'email')

    def match_phone_id(self, text: str) -> bool:
        """
        Check if text is a valid Indonesian phone number

        Args:
            text (str): Phone number to validate

        Returns:
            bool: True if phone number is valid, False otherwise
        """
        return self.match_pattern(text, 'phone_id')

    def match_url(self, text: str) -> bool:
        """
        Check if text is a valid URL

        Args:
            text (str): URL to validate

        Returns:
            bool: True if URL is valid, False otherwise
        """
        return self.match_pattern(text, 'url')

    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Validate password strength with detailed scoring

        Args:
            password (str): Password to validate

        Returns:
            dict: Dictionary containing:
                - score (int): Password strength score (0-5)
                - strength (str): Description of password strength
                - feedback (list): List of feedback messages
                - is_valid (bool): True if password meets minimum requirements
        """
        score = 0
        feedback = []

        if len(password) >= 8:
            score += 1
            feedback.append("Password length sufficient")
        else:
            feedback.append("Password too short")

        if re.search(r'[A-Z]', password):
            score += 1
            feedback.append("Has uppercase letters")
        else:
            feedback.append("Needs uppercase letters")

        if re.search(r'[a-z]', password):
            score += 1
            feedback.append("Has lowercase letters")
        else:
            feedback.append("Needs lowercase letters")

        if re.search(r'\d', password):
            score += 1
            feedback.append("Has numbers")
        else:
            feedback.append("Needs numbers")

        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
            feedback.append("Has special characters")
        else:
            feedback.append("Needs special characters")

        strength = {
            0: "Very Weak",
            1: "Weak",
            2: "Medium",
            3: "Strong",
            4: "Very Strong",
            5: "Excellent"
        }

        return {
            'score': score,
            'strength': strength[score],
            'feedback': feedback,
            'is_valid': score >= 3
        }

    def extract_all(self, text: str) -> Dict[str, List[str]]:
        """
        Extract various types of data from text

        Args:
            text (str): Text to process

        Returns:
            dict: Dictionary containing lists of:
                - emails: Email addresses
                - phones: Phone numbers
                - urls: URLs
                - hashtags: Hashtags
                - mentions: @mentions
                - numbers: Numeric values
                - words: Individual words
        """
        mention_pattern = r'(?<!\w)@\w+'

        return {
            'emails': re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text),
            'phones': re.findall(r'(\+62|62|0)[0-9]{9,12}', text),
            'urls': re.findall(r'(http|https):\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/\S*)?', text),
            'hashtags': re.findall(r'#\w+', text),
            'mentions': re.findall(mention_pattern, text),
            'numbers': re.findall(r'\d+', text),
            'words': re.findall(r'\b\w+\b', text)
        }

    def clean_text(self, text: str, remove_spaces: bool = False) -> str:
        """
        Clean text from special characters

        Args:
            text (str): Text to clean
            remove_spaces (bool): Whether to remove spaces

        Returns:
            str: Cleaned text
        """
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        if remove_spaces:
            cleaned = re.sub(r'\s+', '', cleaned)
        return cleaned

    def extract_dates(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract dates in various formats from text

        Args:
            text (str): Text containing dates

        Returns:
            list: List of dictionaries containing:
                - date (str): Matched date string
                - format (str): Format of the date
                - position (tuple): Start and end positions of the match
        """
        patterns = {
            'dd/mm/yyyy': r'\b(\d{2}/\d{2}/\d{4})\b',
            'yyyy-mm-dd': r'\b(\d{4}-\d{2}-\d{2})\b',
            'dd-mm-yyyy': r'\b(\d{2}-\d{2}-\d{4})\b',
            'natural': r'\b(\d{1,2}\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4})\b'
        }

        results = []
        for format_name, pattern in patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                results.append({
                    'date': match.group(),
                    'format': format_name,
                    'position': match.span()
                })
        return results

    def extract_filename(self, path: str) -> Dict[str, str]:
        """
        Extract information from file path

        Args:
            path (str): File path to process

        Returns:
            dict: Dictionary containing:
                - directory: Directory path
                - filename: File name without extension
                - extension: File extension
                - full_path: Complete file path
        """
        pattern = r'^(.*/)?(?:$|(.+?)(?:(\.[^.]*$)|$))'
        match = re.match(pattern, path)
        if match:
            directory = match.group(1) or ''
            filename = match.group(2) or ''
            extension = match.group(3) or ''
            return {
                'directory': directory,
                'filename': filename,
                'extension': extension.lstrip('.'),
                'full_path': path
            }
        return {}

    def validate_ip(self, ip: str) -> Dict[str, Any]:
        """
        Validate IP address

        Args:
            ip (str): IP address to validate

        Returns:
            dict: Dictionary containing:
                - is_valid (bool): Whether IP is valid
                - type (str): IP version (IPv4/IPv6)
                - private (bool): Whether IPv4 is private (only for IPv4)
        """
        self._patterns['ipv6'] = r'^(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}$'

        is_ipv4 = self.match_pattern(ip, 'ipv4')
        is_ipv6 = bool(re.match(self._patterns['ipv6'], ip.upper()))

        result = {
            'is_valid': is_ipv4 or is_ipv6,
            'type': 'IPv4' if is_ipv4 else ('IPv6' if is_ipv6 else 'Invalid'),
        }

        if is_ipv4:
            result['private'] = self._is_private_ip(ip)

        return result

    def _is_private_ip(self, ip: str) -> bool:
        """
        Check if IP is private

        Args:
            ip (str): IP address to check

        Returns:
            bool: True if IP is private, False otherwise
        """
        ip_parts = ip.split('.')
        if len(ip_parts) != 4:
            return False

        first_octet = int(ip_parts[0])
        second_octet = int(ip_parts[1])

        return (
            first_octet == 10 or
            (first_octet == 172 and 16 <= second_octet <= 31) or
            (first_octet == 192 and second_octet == 168)
        )

    def count_matches(self, text: str, pattern: str) -> Dict[str, Any]:
        """
        Count pattern matches in text

        Args:
            text (str): Text to search in
            pattern (str): Regex pattern to search for

        Returns:
            dict: Dictionary containing:
                - count (int): Number of matches
                - positions (list): List of match positions and content
                - pattern (str): Used pattern
        """
        matches = re.finditer(pattern, text)
        count = 0
        positions = []

        for match in matches:
            count += 1
            positions.append({
                'start': match.start(),
                'end': match.end(),
                'match': match.group()
            })

        return {
            'count': count,
            'positions': positions,
            'pattern': pattern
        }

    def validate_credit_card(self, number: str) -> Dict[str, Any]:
        """
        Validate credit card number

        Args:
            number (str): Credit card number to validate

        Returns:
            dict: Dictionary containing:
                - is_valid (bool): Whether number is valid
                - card_type (str): Type of card (visa, mastercard, etc.)
                - number (str): Cleaned card number
        """
        patterns = {
            'visa': r'^4[0-9]{12}(?:[0-9]{3})?$',
            'mastercard': r'^5[1-5][0-9]{14}$',
            'amex': r'^3[47][0-9]{13}$',
            'discover': r'^6(?:011|5[0-9]{2})[0-9]{12}$'
        }

        number = re.sub(r'\D', '', number)

        for card_type, pattern in patterns.items():
            if re.match(pattern, number):
                return {
                    'is_valid': True,
                    'card_type': card_type,
                    'number': number
                }

        return {
            'is_valid': False,
            'card_type': None,
            'number': number
        }
