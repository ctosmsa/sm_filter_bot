import phonenumbers
from phonenumbers import NumberParseException


def process_phone(raw_phone: str) -> dict:

    if not raw_phone:
        return {
            "Phone": "",
            "CountryCode": ""
        }

    phone = raw_phone.strip()

    # Step 1: Normalize
    if phone.startswith("+"):
        normalized = phone
    elif phone.isdigit():
        if len(phone) == 10:
            normalized = f"+91{phone}"  # India default
        else:
            normalized = f"+{phone}"
    else:
        normalized = phone

    try:
        parsed = phonenumbers.parse(normalized, None)

        return {
            "Phone": str(parsed.national_number),
            "CountryCode": f"+{parsed.country_code}"
        }

    except NumberParseException:
        return {
            "Phone": phone,
            "CountryCode": ""
        }