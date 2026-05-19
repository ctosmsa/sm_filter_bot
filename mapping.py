# mappings.py

# -------------------------
# SERVICE MAPPING
# -------------------------


SERVICE_MAP = {

    "1": "Study Abroad Guidance",

    "2": "Language Training",

    "3": "Education Loans",

    "4": "Exam Date Booking",

    "5": "Migration Services",

    "6": "Visa Assistance",

    "7": "Tours and Travels",

    "8": "Forex Services",

    "9": "Other Enquiries"

}

# -------------------------
# SERVICE GROUPS
# -------------------------

SERVICE_GROUP_MAP = {

    "1": "full_branch",

    "2": "full_branch",

    "4": "exam_branch",

    "5": "fixed_cochin"   # Migration Services

}


# -------------------------
# FULL BRANCH LIST (1 & 2)
# -------------------------

FULL_BRANCH_MAP = {
    "1": "Kanhangad",
    "2": "Kannur",
    "3": "Iritty",
    "4": "Calicut",
    "5": "Thiruvambady",
    "6": "Kalpetta",
    "7": "Perinthalmanna",
    "8": "Palakkad",
    "9": "Thrissur",
    "10": "Mala",
    "11": "Angamaly",
    "12": "Cochin",
    "13": "Kothamangalam",
    "14": "Muvattupuzha",
    "15": "Kattapana",
    "16": "Thodupuzha",
    "17": "Pala",
    "18": "Kottayam",
    "19": "Kanjirappally",
    "20": "Cherthala",
    "21": "Mavelikara",
    "22": "Thiruvalla",
    "23": "Pathanamthitta",
    "24": "Kollam",
    "25": "Kottarakkara",
    "26": "Trivandrum",
    
    "27": "Central Bangalore",
    "28": "South Bangalore",
    "29": "Mangalore",
    "30": "Chennai",
    "31": "Coimbatore",
    "32": "Hyderabad",
    "33": "Abu Dhabi",
    "34": "Bahrain"
}


# -------------------------
# EXAM BRANCH LIST (3)
# -------------------------

EXAM_BRANCH_MAP = {
    "1": "Cochin",
    "2": "Kollam",
    "3": "Kottayam",
    "4": "Pala",
    "5": "Thrissur",
    "6": "Thiruvalla",
    "7": "Trivandrum"
}


# -------------------------
# HELPERS
# -------------------------

def map_service(code):
    return SERVICE_MAP.get(str(code), "Unknown")


def map_branch(service_code, branch_code):

    service_code = str(service_code)
    branch_code = str(branch_code)

    group = SERVICE_GROUP_MAP.get(service_code, "full_branch")

    # 🔥 Special rule: Migration Services → always Cochin
    if group == "fixed_cochin":
        return "Cochin"

    if group == "full_branch":
        return FULL_BRANCH_MAP.get(branch_code, "")

    if group == "exam_branch":
        return EXAM_BRANCH_MAP.get(branch_code, "")

    return ""