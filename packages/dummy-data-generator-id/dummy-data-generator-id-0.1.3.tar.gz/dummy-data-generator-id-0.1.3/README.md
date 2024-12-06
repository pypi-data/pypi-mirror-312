# DummyDataGeneratorId

A Python utility class for generating realistic dummy data with Indonesian context. This generator can create various types of data including names, emails, addresses, phone numbers, and more.

## Installation

```bash
pip install dummy-data-generator-id
```

# Usage
## Basic Usage
```python
from dummy_data_generator_id import DummyDataGeneratorId

# Generate a single complete user data
user = DummyDataGeneratorId.generate_user_data()

# Generate multiple user data
users = DummyDataGeneratorId.generate_user_data(count=5)
```

# Individual Data Generation
## Generate Name
```python
# Random gender name
name = DummyDataGeneratorId.generate_name()

# Specific gender name
male_name = DummyDataGeneratorId.generate_name(gender='male')
female_name = DummyDataGeneratorId.generate_name(gender='female')
```

## Generate Email
```python
# Random email
email = DummyDataGeneratorId.generate_email()

# Email based on name
email = DummyDataGeneratorId.generate_email(name="John Doe")
```

## Generate Phone Number
```python
# Indonesian phone number (default)
phone = DummyDataGeneratorId.generate_phone()

# Custom country code
phone = DummyDataGeneratorId.generate_phone(country_code='60')
```

## Generate Address
```python
# Random address
address = DummyDataGeneratorId.generate_address()

# Address with specific province
address = DummyDataGeneratorId.generate_address(province='DKI Jakarta')
```

## Generate Job Title
```python
job = DummyDataGeneratorId.generate_job()
```

## Generate Company Name
```python
company = DummyDataGeneratorId.generate_company()
```

## Generate Birthdate
```python
# Default age range (18-65)
birthdate = DummyDataGeneratorId.generate_birthdate()

# Custom age range
birthdate = DummyDataGeneratorId.generate_birthdate(min_age=25, max_age=45)
```

## Generate Credit Card Details
```python
credit_card = DummyDataGeneratorId.generate_credit_card()
```

## Generate Username
```python
username = DummyDataGeneratorId.generate_username()
```

## Generate UUID
```python
uuid = DummyDataGeneratorId.generate_uuid()
```

# Output Examples
Single User Data
```python
{
    'id': '123e4567-e89b-12d3-a456-426614174000',
    'name': 'Ahmad Setiawan',
    'email': 'ahmad.setiawan76@gmail.com',
    'username': 'BlueKangaroo123',
    'gender': 'male',
    'phone': '6281234567890',
    'birthdate': datetime.datetime(1990, 5, 15),
    'address': {
        'street': 'Jalan Merdeka No. 45',
        'city': 'Kota DKI Jakarta',
        'province': 'DKI Jakarta',
        'postal_code': '12345'
    },
    'job': 'Senior Developer - IT',
    'company': 'PT Teknologi Maju',
    'credit_card': {
        'type': 'Visa',
        'number': '4532015112830366',
        'expiry_date': '05/25',
        'cvv': '123'
    }
}
```
# Features
- Generate Indonesian-context dummy data
- Support for both single and bulk data generation
- Customizable parameters for most generators
- Realistic data patterns
- Built-in validation (e.g., Luhn algorithm for credit card numbers)

# Data Types Available
- Full Names (Gender-specific)
- Email Addresses
- Phone Numbers (Indonesian format)
- Addresses (Indonesian provinces)
- Job Titles
- Company Names
- Birthdates
- Credit Card Details
- Usernames
- UUIDs

# Notes
- All generated data is fictional and should only be used for testing purposes
- Credit card numbers are valid format but not real cards
- Phone numbers follow Indonesian mobile number formats
- Addresses use Indonesian provinces and city naming conventions

# Requirements
- Python 3.6+
- UUID library

# License
MIT License
