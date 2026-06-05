from phone_utils import process_phone
from mapping import map_service, map_branch
import json

def clean(value):
    return (value or "").strip()


def transform_sm_general_bot(data):

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            # Fallback or error logging if string is completely malformed
            pass

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
        "label": "15132"
    }

def transform_sm_filter_bot(data):

    phone_data = process_phone(data.get("phone"))

    campaign_id = str(data.get("campaign_id", "")).strip().lower()

    parts = campaign_id.split("_")

    nearest_branch = ""

    # Branch = everything before last 3 parts
    if len(parts) > 3:
        branch_part = "_".join(parts[:-3])
        nearest_branch = branch_part.replace("_", " ").title()

    remarks = (
        f"Interest: {clean(data.get('interest'))} | "
        f"CampaignID: {campaign_id} | "
        f"CountryCode: {phone_data['CountryCode']}"
    )

    return {
        "name": clean(data.get("name")),
        "Email": "",
        "Phone": phone_data["Phone"],
        "DesiredCourse": "",
        "NearestBranch": nearest_branch,
        "Remarks": remarks,
        "label": "14920"
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
        "label": "15133"
    }

def get_transformer(source):

    if source == "sm_general_bot":
        return transform_sm_general_bot

    if source == "sm_filter_bot":
        return transform_sm_filter_bot
    
    if source == "sm_general_insta_bot":
        return transform_sm_general_insta_bot

    return None