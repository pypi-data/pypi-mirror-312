import datetime
import logging
import random
import re
import sys
import time

import requests
import yaml

# Set up logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Create a logger
logger = logging.getLogger(__name__)


######### Custom exceptions ##########


class NoPlayerToProcess(Exception):
    def __init__(self):
        logger.error(
            "Did not find any players. "
            "Please check Read.me how to pass user login and password"
        )


class NoActivityIdToProcess(Exception):
    def __init__(self):
        logger.error(
            "Did not find activity id. " "Please check Read.me how to pass activity id"
        )


class NotFoundCSRFToken(Exception):
    def __init__(self, message):
        logger.error(
            f"Unable to proceed without server returning CSRF token in html, "
            f"check server response: {yaml.dump(message)}"
        )


class UnauthorizedLogin(Exception):

    def __init__(self, message):
        logger.error(
            f"Unable to proceed without getting 200 response from login request, "
            f"check user credentials and server response: {yaml.dump(message)}"
        )


class NotFoundActivity(Exception):

    def __init__(self, search, output):
        logger.error(
            f"Unable to find activity using {search}. Server response: {yaml.dump(output)}"
        )


class NotOpenEnrollment(Exception):
    def __init__(self, message):
        logger.error(
            f"Unable to proceed without getting 200 response from enrollment call, "
            f"check server response: {message}"
        )


class UserNotSelected(Exception):
    def __init__(self, message):
        logger.error(
            f"Unable to proceed without getting 200 response from user selection call, "
            f"check server response: {yaml.dump(message)}"
        )


class ActivityNotAddedToCart(Exception):

    def __init__(self, message):
        logger.error(
            f"Unable to proceed without getting 200 response from add activity to cart, "
            f"check if all inputs to add activity are correct. Server response: {yaml.dump(message)}"
        )


class CheckoutFailed(Exception):
    def __init__(self, message):
        logger.error(
            f"Getting non-success response code for final submission, "
            f"please debug server response: {message}"
        )


class CamdenClient:
    """
    Class to act as a client for the
    Camden Volleyball registration.
    """

    # use them only for the initial call to initiate
    # user session and get csrf token
    NOT_AUTHENTICATED_HEADERS = {
        "user-agent": " ".join(
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "AppleWebKit/537.36 (KHTML, like Gecko)",
                "Chrome/129.0.0.0 Safari/537.36",
            ]
        ),
        "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        "host": "anc.apm.activecommunities.com",
        "referer": "https://anc.apm.activecommunities.com/",
        "upgrade-insecure-requests": "1",
        "sec-fetch-mode": "navigate",
        "sec-fetch-dest": "document",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-user": "1",
        "Sec-Fetch-Site": "same-site",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept": "*/*",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    }

    # use them for making requests to api endpoints (REST)
    API_HEADERS = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        "connection": "keep-alive",
        "content-type": "application/json;charset=utf-8",
        "host": "anc.apm.activecommunities.com",
        "origin": "https://anc.apm.activecommunities.com",
        "page_info": '{"page_number":1,"total_records_per_page":20}',
        "referer": 'https://anc.apm.activecommunities.com/sanjoseparksandrec/signin?onlineSiteId=0&locale=en-US&from_original_cui=true&override_partial_error=False&custom_amount=False&params=aHR0cHM6Ly9hcG0uYWN0aXZlY29tbXVuaXRpZXMuY29tL3Nhbmpvc2VwYXJrc2FuZHJlYy9BY3RpdmVOZXRfSG9tZT9GaWxlTmFtZT1hY2NvdW50b3B0aW9ucy5zZGkmZnJvbUxvZ2luUGFnZT10cnVl',
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": " ".join(
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "AppleWebKit/537.36 (KHTML, like Gecko)",
                "Chrome/129.0.0.0 Safari/537.36",
            ]
        ),
        "x-csrf-token": None,  # make sure to update after getting token
        "x-requested-with": "XMLHttpRequest",
    }

    def __init__(
        self,
        login,
        password,
        keywords="Drop In Volleyball",
        activity_id=None,
    ):
        self.user_login = login
        self.user_password = password
        self.keywords = keywords
        self.activity_id = activity_id

        # placeholders
        self.session = requests.session()
        self.session.cookies = requests.cookies.RequestsCookieJar()
        self.csrf_token = None
        self.enrolled = False
        self.test_mode = False
        self.receipt = None

        self.start_time = time.perf_counter()

    def authorize(self):
        """
        Method to authorize client by:

        1. getting CSRF token
        2. posting login and updating session cookies

        :return:
        """

        self._get_csrf_token()

        self._update_cookies_after_login()

    def register(self):

        self.test_mode = False

        self.authorize()

        self.start_time = time.perf_counter()

        self._enroll()

        self._select_user()

        if not self.enrolled:
            self._add_to_cart()
            self._checkout()
            self._get_cart_receipt()

            logger.info(
                f"User {self.user_login} registered in "
                f"{round(time.perf_counter() - self.start_time, 2)} seconds"
            )

        return self.enrolled, self.receipt

    def test(self):

        self.test_mode = True

        self.authorize()

        self._enroll()

        self._select_user()

        self._add_to_cart()

        logger.info(
            f"User {self.user_login} test PASSED. Registration time: "
            f"{round(time.perf_counter() - self.start_time, 2)} seconds"
        )

        return True

    ############# Private methods ################

    def _get_csrf_token(self):
        """ """
        logger.info(f"User {self.user_login} requested csrf token")

        res = self.session.get(
            (
                "https://anc.apm.activecommunities.com/sanjoseparksandrec/signin?"
                "onlineSiteId=0&locale=en-US&"
                "from_original_cui=true&"
                "override_partial_error=False&"
                "custom_amount=False&"
                "params=aHR0cHM6Ly9hcG0uYWN0aXZlY29tbXVuaXRpZXMuY29tL3Nhbmpvc2VwYXJrc2FuZHJlYy9BY3RpdmVOZXRfSG9tZT9GaWxlTmFtZT1hY2NvdW50b3B0aW9ucy5zZGkmZnJvbUxvZ2luUGFnZT10cnVl"
            ),
            headers=CamdenClient.NOT_AUTHENTICATED_HEADERS,
        )

        # Regex pattern to extract the CSRF token
        csrf_token_pattern = r'window\.__csrfToken = "([a-f0-9-]+)"'

        # Applying the regex pattern to extract the CSRF token
        csrf_token_match = re.search(csrf_token_pattern, res.text)

        # Check if the regex match was successful
        if csrf_token_match:
            csrf_token = csrf_token_match.group(1)
            logger.info(f"User {self.user_login} CSRF Token: {csrf_token}")
            self.csrf_token = csrf_token

        else:
            raise NotFoundCSRFToken(res.text)

        self.session.cookies.update(res.cookies)

    def _update_cookies_after_login(self):

        if not self.user_login and not self.user_password:
            raise RuntimeError("Unable to proceed without credentials")

        logger.info(f"User {self.user_login} simulate login and update session cookies")

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "login_name": self.user_login,
            "password": self.user_password,
            "recaptcha_response": "",
            "signin_source_app": "0",
            "locale": "en-US",
            "ak_properties": None,
        }

        res = self.session.post(
            "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/user/signin?locale=en-US",
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if res.status_code == 200:
            self.customer_id = res.json()["body"]["result"]["customer"]["customer_id"]
            self.session.cookies.update(res.cookies)
            logger.info(f"User {self.user_login} got customerId: {self.customer_id}")
        else:
            raise UnauthorizedLogin(res.text)

    def _get_activity_id(self):

        if self.activity_id:
            logger.info(
                f"User {self.user_login} using known activity id: {self.activity_id}"
            )
            return self.activity_id

        if self.test_mode:
            keywords = ""
            date_before = ""
            date_after = ""
        else:
            keywords = self.keywords
            current_date = datetime.date.today()
            date_before = (current_date + datetime.timedelta(days=1)).strftime(
                "%Y-%m-%d"
            )
            date_after = current_date.strftime("%Y-%m-%d")

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "activity_search_pattern": {
                "skills": [],
                "time_after_str": "",
                "days_of_week": "0010100",
                "activity_select_param": 2,
                "center_ids": [],
                "time_before_str": "",
                "open_spots": None,
                "activity_id": None,
                "activity_category_ids": [],
                "date_before": date_before,
                "min_age": 18,
                "date_after": date_after,
                "activity_type_ids": [],
                "site_ids": [],
                "for_map": False,
                "geographic_area_ids": [],
                "season_ids": [],
                "activity_department_ids": [],
                "activity_other_category_ids": [],
                "child_season_ids": [],
                "activity_keyword": keywords,
                "instructor_ids": [],
                "max_age": "45",
                "custom_price_from": "0",
                "custom_price_to": "0",
            },
            "activity_transfer_pattern": {},
        }

        url = (
            "https://anc.apm.activecommunities.com/sanjoseparksandrec"
            "/rest/activities/list?locale=en-US"
        )

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        all_activities = []

        if res.status_code == 200:
            all_activities = res.json()["body"]["activity_items"]

        if not all_activities:
            raise NotFoundActivity(keywords, res.text)

        logger.info(
            f"User {self.user_login} search returned "
            f"{len(all_activities)} activities using keywords <{keywords}> "
            f"and date interval: <{date_after} - {date_before}>"
        )

        # For testing purposes will select random activity
        if self.test_mode:
            activity = random.choice(all_activities)
            logger.info(
                f"User {self.user_login} selected random activity: <{activity.get('desc')[:22]}>"
            )
        else:
            # filter out paid activities
            all_activities = [
                activity
                for activity in all_activities
                if activity["fee"]["label"] == "Free"
            ]

            activity = all_activities[0]
            logger.info(
                f"User {self.user_login} selected first activity "
                f"{activity['id']}: {activity.get('desc')[:22]}"
            )

        self.activity_id = activity["id"]

        return self.activity_id

    def _enroll(self):
        """
        Requires valid activity id

        Possible cases:

        - not open for enrollment

        """

        activity_id = self._get_activity_id()

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "activity_id": activity_id,
            "transfer_out_transaction_id": 0,
            "reg_type": 0,
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/activity/enrollment?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if res.status_code == 200:
            logger.info(
                f"User {self.user_login} was enrolled after {time.perf_counter() - self.start_time}"
            )
            self.session.cookies.update(res.cookies)
        else:
            server_response = res.json().get("headers", {}).get("response_message")
            raise NotOpenEnrollment(f"{self.user_login}: {server_response}")

    def _select_user(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "reno": 1,
            "customer_id": self.customer_id,
            "overrides": [],
            "is_edit_transfer": False,
            "transfer_out_transaction_id": 0,
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/activity/enrollment/participant?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if res.status_code == 200:
            self.session.cookies.update(res.cookies)
            logger.info(
                f"User {self.user_login} was selected "
                f"after {time.perf_counter() - self.start_time}"
            )
        else:
            if "Already Enrolled" in res.text:
                # that is considered successful execution, we can exit
                logger.info(f"User {self.user_login} already enrolled")
                self.enrolled = True
                self._get_cart_receipt()
            else:
                raise UserNotSelected(res.text)

    def _add_to_cart(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "reno": 1,
            "participant_note": "",
            "question_answers": [
                {
                    "reno": 1,
                    "question_id": 2,
                    "customquestion_index": "1",
                    "parent_question_id": 0,
                    "user_entry_answer": "None",
                    "answer_id": [],
                },
                {
                    "reno": 1,
                    "question_id": 157,
                    "customquestion_index": "2",
                    "parent_question_id": 0,
                    "user_entry_answer": "",
                    "answer_id": [1031],
                },
            ],
            "donation_param": [],
            "waivers": [],
            "pickup_customers": [],
            "participant_usa_hockey_number": {
                "usah_code": "",
                "position_id": 1,
            },
            "token": "",
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/activity/enrollment/addtocart?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if not res.status_code == 200:
            raise ActivityNotAddedToCart(res.text)
        else:
            self.enrolled = True
            logger.info(
                f"User {self.user_login} added to cart "
                f"after {time.perf_counter() - self.start_time}"
            )

    def _checkout(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "waiver_initials_online_text": True,
            "online_waiver_initials": "",
            "initials": [],
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/checkout?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if res.status_code == 200:
            logger.info(
                f"User {self.user_login} checked out after {time.perf_counter() - self.start_time}"
            )
        else:
            raise CheckoutFailed(res.text)

    ############ Not required for registration, just FYI #########

    def _get_cart_receipt(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        # 1729101431907
        ui_random = int(time.time() * 1000)

        url = (
            f"https://anc.apm.activecommunities.com/sanjoseparksandrec"
            f"/rest/cartReceipt?locale=en-US&ui_random={ui_random}"
        )

        res = self.session.get(
            url,
            cookies=self.session.cookies,
            headers=headers,
        )

        self.session.cookies.update(res.cookies)

        receipt_number = res.json().get("body", {}).get("receipt_number")
        if receipt_number:
            self.receipt = f"{self.user_login} confirmation receipt {receipt_number.split('.')[0]}"

        logger.info(f"User {self.user_login} confirmation receipt {receipt_number.split('.')[0]}")

    def _get_user_account(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        url = (
            "https://anc.apm.activecommunities.com/sanjoseparksandrec/myaccount?"
            "locale=en-US"
        )

        res = self.session.get(
            url,
            cookies=self.session.cookies,
            headers=headers,
        )

        self.session.cookies.update(res.cookies)

    def _get_enrollment_details(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        url = (
            f"https://anc.apm.activecommunities.com/sanjoseparksandrec"
            f"/rest/activity/detail/{self.activity_id}?locale=en-US"
        )

        res = self.session.get(
            url,
            cookies=self.session.cookies,
            headers=headers,
        )

        self.session.cookies.update(res.cookies)

    def _get_login_check(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        url = (
            "https://anc.apm.activecommunities.com/sanjoseparksandrec"
            "/rest/common/logincheck?locale=en-US"
        )

        res = self.session.get(
            url,
            cookies=self.session.cookies,
            headers=headers,
        )

        self.session.cookies.update(res.cookies)
