import json
import time
import ssl
import urllib.request
import urllib.error
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver


def retrieve_phone_code(driver: WebDriver) -> str:
    """
    Retrieves the phone confirmation code from Chrome DevTools logs.

    Args:
        driver (WebDriver): The Chrome driver instance.

    Returns:
        str: The numeric confirmation code extracted from network logs.

    Raises:
        Exception: If no code is found after multiple attempts.
    """
    for _ in range(10):
        try:
            logs = [
                log["message"]
                for log in driver.get_log('performance')
                if 'api/v1/number?number' in log.get("message", "")
            ]

            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                request_id = message_data["params"]["requestId"]

                response_body = driver.execute_cdp_cmd(
                    'Network.getResponseBody', {'requestId': request_id}
                )

                code = ''.join(filter(str.isdigit, response_body['body']))
                if code:
                    return code

        except WebDriverException:
            time.sleep(1)
        except Exception as e:
            print(f"[Error] While retrieving phone code: {e}")
            time.sleep(1)

    raise Exception(
        "❌ Could not retrieve phone confirmation code from browser logs.\n"
        "👉 Make sure the code was requested in the app *before* calling retrieve_phone_code()."
    )


def is_url_reachable(url: str) -> bool:
    """
    Verifies if a given URL is reachable by attempting an HTTPS request.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is reachable, False otherwise.
    """
    try:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(url, context=ssl_ctx, timeout=5) as response:
            return response.status == 200

    except (urllib.error.URLError, urllib.error.HTTPError, ssl.SSLError) as e:
        print(f"[URL Error] {e}")
        return False
    except Exception as e:
        print(f"[Unexpected Error] {e}")
        return False
