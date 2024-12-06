import random
import string
from datetime import datetime, timedelta
import uuid


class DummyDataGeneratorId:
    @staticmethod
    def generate_name(gender=None):
        """
        Generate random name with optional gender specification

        Args:
            gender (str, optional): 'male' or 'female'. Defaults to random.

        Returns:
            str: Full name
        """
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
    def generate_email(name=None):
        """
        Generate random email based on name or completely random

        Args:
            name (str, optional): Name to base email on. Defaults to None.

        Returns:
            str: Email address
        """
        if name is None:
            name = DummyDataGeneratorId.generate_name()

        username = name.lower().replace(' ', '.') + str(random.randint(10, 99))
        domains = ['gmail.com', 'yahoo.com',
                   'hotmail.com', 'outlook.com', 'example.com']

        return f"{username}@{random.choice(domains)}"

    @staticmethod
    def generate_phone(country_code='62'):
        """
        Generate Indonesian phone number

        Args:
            country_code (str, optional): Country code. Defaults to '62'.

        Returns:
            str: Phone number
        """
        prefixes = ['811', '812', '813', '814', '815', '816', '817', '818',
                    '819', '821', '822', '823', '852', '853', '855', '856', '857', '858']
        return f"{country_code}{random.choice(prefixes)}{''.join(str(random.randint(0, 9)) for _ in range(8))}"

    @staticmethod
    def generate_address(province=None):
        """
        Generate random Indonesian address

        Args:
            province (str, optional): Specific province. Defaults to None.

        Returns:
            dict: Address details
        """
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
    def generate_job():
        """
        Generate random job title

        Returns:
            str: Job title
        """
        industries = [
            'IT', 'Finance', 'Marketing', 'Sales', 'Engineering',
            'Education', 'Healthcare', 'Design', 'Consulting'
        ]

        job_levels = ['Junior', 'Senior', 'Lead', 'Staff', 'Principal']
        job_types = ['Manager', 'Specialist', 'Analyst',
                     'Coordinator', 'Developer', 'Engineer']

        return f"{random.choice(job_levels)} {random.choice(job_types)} - {random.choice(industries)}"

    @staticmethod
    def generate_company():
        """
        Generate random company name

        Returns:
            str: Company name
        """
        prefixes = ['PT', 'CV', 'Yayasan']
        company_types = [
            'Teknologi', 'Inovasi', 'Global', 'Mandiri', 'Utama',
            'Sejahtera', 'Maju', 'Kreatif', 'Internasional'
        ]

        return f"{random.choice(prefixes)} {DummyDataGeneratorId.generate_random_word()} {random.choice(company_types)}"

    @staticmethod
    def generate_birthdate(min_age=18, max_age=65):
        """
        Generate random birthdate

        Args:
            min_age (int, optional): Minimum age. Defaults to 18.
            max_age (int, optional): Maximum age. Defaults to 65.

        Returns:
            datetime: Birthdate
        """
        today = datetime.now()
        years_ago = random.randint(min_age, max_age)
        birthdate = today - timedelta(days=years_ago*365)

        # Add some random variation in month and day
        birthdate -= timedelta(days=random.randint(0, 365))

        return birthdate

    @staticmethod
    def generate_credit_card():
        """
        Generate dummy credit card details

        Returns:
            dict: Credit card details
        """
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
    def generate_random_word(min_length=3, max_length=10):
        """
        Generate random word

        Args:
            min_length (int, optional): Minimum word length. Defaults to 3.
            max_length (int, optional): Maximum word length. Defaults to 10.

        Returns:
            str: Random word
        """
        length = random.randint(min_length, max_length)
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length)).capitalize()

    @staticmethod
    def generate_uuid():
        """
        Generate unique identifier

        Returns:
            str: UUID
        """
        return str(uuid.uuid4())

    @staticmethod
    def generate_username():
        """
        Generate random username

        Returns:
            str: Username
        """
        words = [DummyDataGeneratorId.generate_random_word() for _ in range(2)]
        numbers = ''.join(str(random.randint(0, 9))
                          for _ in range(random.randint(1, 3)))
        return f"{''.join(words)}{numbers}"

    @staticmethod
    def generate_user_data(count=1):
        """
        Generate multiple user data

        Args:
            count (int, optional): Number of users to generate. Defaults to 1.

        Returns:
            list: List of user dictionaries
        """
        users = []
        for _ in range(count):
            gender = random.choice(['male', 'female'])
            name = DummyDataGeneratorId.generate_name(gender)

            user = {
                'id': DummyDataGeneratorId.generate_uuid(),
                'name': name,
                'email': DummyDataGeneratorId.generate_email(name),
                'username': DummyDataGeneratorId.generate_username(),
                'gender': gender,
                'phone': DummyDataGeneratorId.generate_phone(),
                'birthdate': DummyDataGeneratorId.generate_birthdate(),
                'address': DummyDataGeneratorId.generate_address(),
                'job': DummyDataGeneratorId.generate_job(),
                'company': DummyDataGeneratorId.generate_company(),
                'credit_card': DummyDataGeneratorId.generate_credit_card()
            }
            users.append(user)

        return users if count > 1 else users[0]
