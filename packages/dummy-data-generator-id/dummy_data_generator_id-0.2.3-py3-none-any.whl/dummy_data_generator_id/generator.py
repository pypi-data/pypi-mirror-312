import random
import string
from datetime import datetime, timedelta
import uuid


class DummyDataGeneratorId:
    @staticmethod
    def generate_name(input_param=None, gender=None):
        """
        Generate random name(s) with optional gender specification

        Args:
            input_param: Can be either count (int) or gender (str)
            gender (str, optional): 'male' or 'female'. Defaults to random.

        Returns:
            str or list: Single name or list of names
        """
        if isinstance(input_param, int):
            return [DummyDataGeneratorId.generate_name(gender=gender) for _ in range(input_param)]
        elif isinstance(input_param, str):
            gender = input_param

        first_names_male = [
            'Ahmad', 'Muhammad', 'Budi', 'Dedi', 'Rudi', 'Adi', 'Eko', 'Agus',
            'Hadi', 'Iwan', 'Bambang', 'Slamet', 'Hendro', 'Yulio', 'Taufik'
        ]
        first_names_female = [
            'Siti', 'Ani', 'Dewi', 'Rina', 'Maya', 'Fitri', 'Indah', 'Rita',
            'Nurul', 'Rini', 'Lia', 'Susan', 'Erni', 'Wati', 'Yuni'
        ]
        last_names = [
            'Setiawan', 'Susanto', 'Wijaya', 'Pranoto', 'Santoso', 'Kurniawan',
            'Hidayat', 'Saputra', 'Nugroho', 'Hartono', 'Prasetyo', 'Andriani',
            'Sirait', 'Gunawan', 'Hutapea'
        ]

        if gender is None:
            gender = random.choice(['male', 'female'])

        first_name = random.choice(
            first_names_male if gender == 'male' else first_names_female)
        last_name = random.choice(last_names)

        return f"{first_name} {last_name}"

    @staticmethod
    def generate_email(input_param=None):
        """
        Generate random email(s) based on name or completely random

        Args:
            input_param: Can be either count (int) or name (str)

        Returns:
            str or list: Single email or list of emails
        """
        if isinstance(input_param, int):
            return [DummyDataGeneratorId.generate_email() for _ in range(input_param)]

        name = input_param
        if name is None:
            name = DummyDataGeneratorId.generate_name()

        username = name.lower().replace(' ', '.') + str(random.randint(10, 99))
        domains = ['gmail.com', 'yahoo.com',
                   'hotmail.com', 'outlook.com', 'example.com']

        return f"{username}@{random.choice(domains)}"

    @staticmethod
    def generate_phone(input_param=None, country_code='62'):
        """
        Generate Indonesian phone number(s)

        Args:
            input_param: Count of phone numbers to generate
            country_code (str, optional): Country code. Defaults to '62'.

        Returns:
            str or list: Single phone number or list of phone numbers
        """
        if isinstance(input_param, int):
            return [DummyDataGeneratorId.generate_phone(country_code=country_code) for _ in range(input_param)]

        prefixes = ['811', '812', '813', '814', '815', '816', '817', '818',
                    '819', '821', '822', '823', '852', '853', '855', '856', '857', '858']
        return f"{country_code}{random.choice(prefixes)}{''.join(str(random.randint(0, 9)) for _ in range(8))}"

    @staticmethod
    def generate_address(input_param=None, province=None):
        """
        Generate random Indonesian address(es)

        Args:
            input_param: Count of addresses to generate
            province (str, optional): Specific province. Defaults to None.

        Returns:
            dict or list: Single address or list of addresses
        """
        if isinstance(input_param, int):
            return [DummyDataGeneratorId.generate_address(province=province) for _ in range(input_param)]

        provinces = [
            'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur',
            'Banten', 'Bali', 'Sumatera Utara', 'Sumatera Barat'
        ]

        streets = [
            'Jalan Merdeka', 'Jalan Sudirman', 'Jalan Gatot Subroto',
            'Jalan Ahmad Yani', 'Jalan Diponegoro', 'Jalan Veteran'
        ]

        selected_province = province or random.choice(provinces)

        return {
            'street': f"{random.choice(streets)} No. {random.randint(1, 100)}",
            'city': f"Kota {selected_province}",
            'province': selected_province,
            'postal_code': f"{random.randint(10000, 99999)}"
        }

    @staticmethod
    def generate_job(count=None):
        """
        Generate random job title(s)

        Args:
            count (int, optional): Number of job titles to generate

        Returns:
            str or list: Single job title or list of job titles
        """
        if isinstance(count, int):
            return [DummyDataGeneratorId.generate_job() for _ in range(count)]

        industries = [
            'IT', 'Finance', 'Marketing', 'Sales', 'Engineering',
            'Education', 'Healthcare', 'Design', 'Consulting'
        ]

        job_levels = ['Junior', 'Senior', 'Lead', 'Staff', 'Principal']
        job_types = ['Manager', 'Specialist', 'Analyst',
                     'Coordinator', 'Developer', 'Engineer']

        return f"{random.choice(job_levels)} {random.choice(job_types)} - {random.choice(industries)}"

    @staticmethod
    def generate_company(count=None):
        """
        Generate random company name(s)

        Args:
            count (int, optional): Number of company names to generate

        Returns:
            str or list: Single company name or list of company names
        """
        if isinstance(count, int):
            return [DummyDataGeneratorId.generate_company() for _ in range(count)]

        prefixes = ['PT', 'CV', 'Yayasan']
        company_types = [
            'Teknologi', 'Inovasi', 'Global', 'Mandiri', 'Utama',
            'Sejahtera', 'Maju', 'Kreatif', 'Internasional'
        ]

        return f"{random.choice(prefixes)} {DummyDataGeneratorId.generate_random_word()} {random.choice(company_types)}"

    @staticmethod
    def generate_birthdate(input_param=None, min_age=18, max_age=65):
        """
        Generate random birthdate(s)

        Args:
            input_param: Count of birthdates to generate
            min_age (int, optional): Minimum age. Defaults to 18.
            max_age (int, optional): Maximum age. Defaults to 65.

        Returns:
            datetime or list: Single birthdate or list of birthdates
        """
        if isinstance(input_param, int):
            return [DummyDataGeneratorId.generate_birthdate(min_age=min_age, max_age=max_age) for _ in range(input_param)]

        today = datetime.now()
        years_ago = random.randint(min_age, max_age)
        birthdate = today - timedelta(days=years_ago*365)
        birthdate -= timedelta(days=random.randint(0, 365))

        return birthdate

    @staticmethod
    def generate_credit_card(count=None):
        """
        Generate dummy credit card detail(s)

        Args:
            count (int, optional): Number of credit cards to generate

        Returns:
            dict or list: Single credit card details or list of credit card details
        """
        if isinstance(count, int):
            return [DummyDataGeneratorId.generate_credit_card() for _ in range(count)]

        card_types = ['Visa', 'MasterCard', 'American Express']
        card_type = random.choice(card_types)

        def generate_card_number(prefix, length):
            number = prefix + ''.join(str(random.randint(0, 9))
                                      for _ in range(length - len(prefix) - 1))
            number += str(DummyDataGeneratorId.luhn_checksum(number))
            return number

        card_numbers = {
            'Visa': generate_card_number('4', 16),
            'MasterCard': generate_card_number('51', 16),
            'American Express': generate_card_number('34', 15)
        }

        return {
            'type': card_type,
            'number': card_numbers[card_type],
            'expiry_date': (datetime.now() + timedelta(days=random.randint(365, 1825))).strftime('%m/%y'),
            'cvv': ''.join(str(random.randint(0, 9)) for _ in range(3))
        }

    @staticmethod
    def generate_username(count=None):
        """
        Generate random username(s)

        Args:
            count (int, optional): Number of usernames to generate

        Returns:
            str or list: Single username or list of usernames
        """
        if isinstance(count, int):
            return [DummyDataGeneratorId.generate_username() for _ in range(count)]

        words = [DummyDataGeneratorId.generate_random_word() for _ in range(2)]
        numbers = ''.join(str(random.randint(0, 9))
                          for _ in range(random.randint(1, 3)))
        return f"{''.join(words)}{numbers}"

    @staticmethod
    def luhn_checksum(card_number):
        """
        Generate Luhn algorithm checksum for credit card validation

        Args:
            card_number (str): Card number without checksum

        Returns:
            int: Checksum digit
        """
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return (10 - (checksum % 10)) % 10

    @staticmethod
    def generate_random_word(count=None, min_length=3, max_length=10):
        """
        Generate random word(s)

        Args:
            count (int, optional): Number of words to generate
            min_length (int, optional): Minimum word length. Defaults to 3.
            max_length (int, optional): Maximum word length. Defaults to 10.

        Returns:
            str or list: Single word or list of words
        """
        if isinstance(count, int):
            return [DummyDataGeneratorId.generate_random_word(min_length=min_length, max_length=max_length) for _ in range(count)]

        length = random.randint(min_length, max_length)
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length)).capitalize()

    @staticmethod
    def generate_uuid(count=None):
        """
        Generate unique identifier(s)

        Args:
            count (int, optional): Number of UUIDs to generate

        Returns:
            str or list: Single UUID or list of UUIDs
        """
        if isinstance(count, int):
            return [DummyDataGeneratorId.generate_uuid() for _ in range(count)]

        return str(uuid.uuid4())
