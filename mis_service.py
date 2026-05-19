import httpx
import asyncio
import logging
import smtplib

from email.mime.text import MIMEText
from datetime import datetime
from zoneinfo import ZoneInfo

from config import MIS_API_URL, EMAIL_USER, EMAIL_PASS, EMAIL_TO


# 🔹 Get IST time
def get_ist_time():
    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%Y-%m-%d %H:%M:%S")


# 🔹 Email alert function
def send_email_alert(payload, error):

    subject = "Lead Middleware Failure Alert"

    body = f"""
🚨 Lead Middleware Failure

A lead failed after retries.

----------------------------------------

Payload:
{payload}

----------------------------------------

Error:
{error}

----------------------------------------

Time:
{get_ist_time()}
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    try:

        # ✅ SMTP timeout added
        with smtplib.SMTP(
            "smtp.gmail.com",
            587,
            timeout=10
        ) as server:

            server.starttls()

            server.login(
                EMAIL_USER,
                EMAIL_PASS
            )

            server.sendmail(
                EMAIL_USER,
                [EMAIL_TO],
                msg.as_string()
            )

        logging.info("EMAIL ALERT SENT")

    except Exception as e:

        logging.error(
            f"EMAIL FAILED | ERROR={str(e)}"
        )


# 🔹 Core MIS sending logic
async def send_to_mis(payload):

    last_error = None

    for attempt in range(3):

        try:

            async with httpx.AsyncClient() as client:

                response = await client.post(
                    MIS_API_URL,
                    json=payload,
                    timeout=5
                )

            # ✅ Success
            if response.status_code == 200:

                logging.info(
                    f"SUCCESS | DATA={payload}"
                )

                return

            # 🔁 Retry on server errors
            elif response.status_code >= 500:

                last_error = (
                    f"Server Error "
                    f"{response.status_code}"
                )

                logging.warning(
                    f"RETRY | "
                    f"Attempt={attempt+1} | "
                    f"Status={response.status_code} | "
                    f"DATA={payload}"
                )

            # ❌ Client errors (no retry)
            else:

                logging.error(
                    f"CLIENT ERROR | "
                    f"Status={response.status_code} | "
                    f"Response={response.text} | "
                    f"DATA={payload}"
                )

                return

        except httpx.RequestError as e:

            last_error = str(e)

            logging.error(
                f"RETRY | "
                f"Attempt={attempt+1} | "
                f"Exception={last_error} | "
                f"DATA={payload}"
            )

        # ✅ Non-blocking sleep
        await asyncio.sleep(1)

    # 🔴 FINAL FAILURE
    logging.critical(
        f"FAILED AFTER RETRIES | "
        f"DATA={payload}"
    )

    send_email_alert(
        payload,
        last_error or "MIS API failed after retries"
    )

    raise Exception(
        f"MIS API failed: {last_error}"
    )