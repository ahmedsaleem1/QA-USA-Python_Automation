def retrieve_phone_code(driver) -> str:
    import json
    import time
    from selenium.common.exceptions import WebDriverException

    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
                if code:
                    return code
        except WebDriverException:
            time.sleep(1)
            continue
    raise Exception("No phone confirmation code found.\n"
                    "Please use retrieve_phone_code only after the code was requested in your application.")


def is_url_reachable(url: str) -> bool:
    import ssl
    import urllib.request
    import urllib.error

    try:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(url, context=ssl_ctx, timeout=5) as response:
            return response.status == 200
    except (urllib.error.URLError, urllib.error.HTTPError, ssl.SSLError) as e:
        print(f"URL not reachable: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error checking URL: {e}")
        return False
