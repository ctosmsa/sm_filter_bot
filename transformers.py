from phone_utils import process_phone
from mapping import map_service, map_branch


def clean(value):
    return (value or "").strip()


def transform_sm_general_bot(data):

    phone_data = process_phone(data.get("phone"))

    remarks = (
        f"Service: {clean(data.get('service'))} | "
        f"Comments: {clean(data.get('comments'))} | "
        f"CountryCode: {phone_data['CountryCode']}"
    )

    return {
        "name": clean(data.get("name")),
        "Email": clean(data.get("email")).lower(),
        "Phone": phone_data["Phone"],
        "DesiredCourse": "",
        "NearestBranch": clean(data.get("branch")),
        "Remarks": remarks,
        "label": "14920"
    }

def transform_sm_filter_bot(data):

    phone_data = process_phone(data.get("phone"))

    remarks = (
        f"Interest: {clean(data.get('interest'))} | "
        f"CampaignID: {data.get('campaign_id', '')} | "
        f"CountryCode: {phone_data['CountryCode']}"
    )

    return {
        "name": clean(data.get("name")),
        "Email": "",  # not provided
        "Phone": phone_data["Phone"],
        "DesiredCourse": "",  # keep empty as decided
        "NearestBranch": "",  # not available
        "Remarks": remarks,
        "label": "14920"  # confirm if same label
    }

def transform_sm_general_insta_bot(data):

    phone_data = process_phone(data.get("phone"))

    service_code = str(data.get("service", "")).strip()
    branch_code = str(data.get("branch", "")).strip()

    service = map_service(service_code)
    branch = map_branch(service_code, branch_code)

    remarks = (
        f"Service: {service} | "
        f"Comments: {clean(data.get('comments'))} | "
        f"CountryCode: {phone_data['CountryCode']}"
    )

    return {
        "name": clean(data.get("name")),
        "Email": clean(data.get("email")).lower(),
        "Phone": phone_data["Phone"],
        "DesiredCourse": "",
        "NearestBranch": branch,
        "Remarks": remarks,
        "label": "14920"
    }

def get_transformer(source):

    if source == "sm_general_bot":
        return transform_sm_general_bot

    if source == "sm_filter_bot":
        return transform_sm_filter_bot
    
    if source == "sm_general_insta_bot":
        return transform_sm_general_insta_bot

    return None