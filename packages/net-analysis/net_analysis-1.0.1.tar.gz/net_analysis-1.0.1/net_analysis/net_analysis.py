import requests
from countryinfo import CountryInfo
from typing import Literal
from loguru import logger
from .static import get_locale_by_country_code


class NetAnalysis:
    """
    A network analysis utility to gather information about the user's IP, geographical location, browser details,
    and other metadata using various lookup methods. It supports configurable proxies, custom user agents,
    and logging levels.

    Attributes:
        ip (str): The detected public IP address.
        country (str): The country of the detected IP.
        city (str): The city of the detected IP.
        state (str): The state/region of the detected IP.
        lat (float): The latitude of the detected IP.
        lon (float): The longitude of the detected IP.
        country_code (str): The ISO code of the detected country.
        continent (str): The continent of the detected IP.
        countries_in_continent (list[str]): A list of countries within the detected continent.
        browser (str): The browser name derived from the user agent.
        browser_version (str): The version of the detected browser.
        os (str): The operating system derived from the user agent.
        isp (str): The Internet Service Provider (ISP) of the detected IP.
        time_zone (str): The time zone of the detected IP.
        zip_code (str): The postal/ZIP code of the detected location.
        is_anonymous_proxy (bool): Indicates if the connection is via an anonymous proxy.
        area (str): Additional location details, such as a region or metro area.

    Parameters:
        proxy dict or str: A proxy configuration for network requests.
            - If `str`, the same proxy is used for both HTTP and HTTPS.
            - If `dict`, specify different proxies for HTTP and HTTPS.
        user_agent dict, optional: Custom User-Agent for network requests. If not provided,
        logger_level "INFO", "DEBUG", "WARNING", "ERROR": Logging level for the class.

    Example:
        >>> analyzer = NetAnalyzer(proxy = "http://...")
        >>> print(analyzer.ip, analyzer.country, analyzer.city)
    """

    def __init__(
        self,
        proxy: dict | str = None,
        user_agent: dict = None,
        logger_level: Literal["INFO", "DEBUG", "WARNING", "ERROR"] = "INFO",
    ) -> None:
        logger.level(name=logger_level)
        self.__proxy: dict = (
            {"http": proxy, "https": proxy} if isinstance(proxy, str) else proxy
        )
        self.__header: dict = {
            "User-Agent": user_agent
            or "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        }
        self.ip: str = None
        self.country: str = None
        self.city: str = None
        self.state: str = None
        self.lat: float = None
        self.lon: float = None
        self.country_code: str = None
        self.continent: str = None
        self.countries_in_continent: list[str] = None
        self.browser: str = None
        self.browser_version: str = None
        self.os: str = None
        self.isp: str = None
        self.time_zone: str = None
        self.zip_code: str = None
        self.is_anonymous_proxy: bool = False
        self.area: str = None
        self.locale: str = None

        self.__ip_api_lookup() or self.__smart_lookup() or self.__old_lookup()

    def __send_requests(self, url: str) -> requests.Response:
        for attempt in range(3):
            try:
                response = requests.get(
                    url=url,
                    proxies=self.__proxy,
                    headers=self.__header,
                )
                return response
            except requests.exceptions.RequestException as e:
                logger.error(
                    f"[NetAnalyzer] Network error in getting IP lookup: '{e}',trying again !"
                )
            except Exception as e:
                logger.error(f"[NetAnalyzer] Unexpected error: '{e}'")

    def __ip_api_lookup(self):
        try:
            response = self.__send_requests(
                url="http://ip-api.com/json?fields=3403775"
            ).json()

            self.country = response["country"]
            self.country_code = response["countryCode"]
            self.continent = response["continent"]
            self.ip = response["query"]
            self.is_anonymous_proxy = not response["proxy"]
            self.city = response["city"]
            self.state = response["regionName"]
            self.time_zone = response["timezone"]
            self.zip_code = response["zip"]
            self.isp = response["isp"]
            self.lat = response["lat"]
            self.lon = response["lon"]
            self.isp = response["isp"]
            self.locale = get_locale_by_country_code(response["countryCode"])

            logger.info(f"[ip_api_lookup] Analyse IP {self.ip} with IP-API ✔")
            info = CountryInfo(country_name=self.country_code)
            countries_in_continent = [
                country
                for country, value in info._CountryInfo__countries.items()
                if value.get("region") == self.continent
            ]
            if "united kingdom" in countries_in_continent:
                countries_in_continent.append("england")

            self.countries_in_continent = countries_in_continent
            if self.country_code in info._CountryInfo__countries:
                self.area = info.subregion()
            else:
                self.area = self.continent
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"[ip_api_lookup] Error in getting IP details: {e}")

    def __smart_lookup(self):
        try:
            response = self.__send_requests(url="https://ip.smartproxy.com/json").json()

            self.country = response["country"]["name"]
            self.country_code = response["country"]["code"]
            self.continent = response["country"]["continent"]
            self.ip = response["proxy"]["ip"]
            self.is_anonymous_proxy = response["proxy"].get("is_anonymous_proxy", False)
            self.city = response["city"]["name"]
            self.state = response["city"]["state"]
            self.time_zone = response["city"]["time_zone"]
            self.zip_code = response["city"]["zip_code"]
            self.isp = response["isp"]["isp"]
            self.browser = response["browser"].get("name", "undefined")
            self.browser_version = response["browser"].get("version", "undefined")
            self.os = f'{response["platform"].get("os", "undefined")} {response["platform"].get("type", "undefined")}'
            self.locale = get_locale_by_country_code(response["country"]["code"])

            logger.info(
                f"[smart_lookup] Analyse IP {self.ip} with Smart Lookup (Advance) ✔"
            )
            info = CountryInfo(country_name=self.country_code)
            countries_in_continent = [
                country
                for country, value in info._CountryInfo__countries.items()
                if value.get("region") == self.continent
            ]
            if "united kingdom" in countries_in_continent:
                countries_in_continent.append("england")

            self.countries_in_continent = countries_in_continent
            if self.country_code in info._CountryInfo__countries:
                self.area = info.subregion()
            else:
                self.area = self.continent
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"[smart_lookup] Error in getting IP details: {e}")

    def __old_lookup(self):
        try:
            response = self.__send_requests(url="http://api.myip.com/").json()

            self.country = response["country"]
            self.ip = response["ip"]
            self.country_code = response["cc"]
            self.locale = get_locale_by_country_code(response["cc"])

            info = CountryInfo(country_name=self.country_code)
            self.continent = info.region()

            logger.info(f"[old_lookup] Analyse IP {self.ip} with Old Lookup (Basic) ✔")
            countries_in_continent = [
                country
                for country, value in info._CountryInfo__countries.items()
                if value.get("region") == self.continent
            ]
            if "united kingdom" in countries_in_continent:
                countries_in_continent.append("england")

            self.countries_in_continent = countries_in_continent
            if self.country_code in info._CountryInfo__countries:
                self.area = info.subregion()
            else:
                self.area = self.continent
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"[old_lookup] Error in getting IP details: {e}")

    def check_proxy(self) -> str | None:
        """
        Checks if the current network connection is using a proxy.

        Example:
            >>> analyzer = NetAnalyzer(proxy="http://...")
            >>> proxy_name = analyzer.check_proxy()
            >>> if proxy_name:
            ...     print(f"Proxy detected: {proxy_name}")
            ... else:
            ...     print("No proxy detected.")
        """
        try:
            headers = {
                "Connection": "close",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
                "Host": "connectivitycheck.gstatic.com",
            }
            response = requests.get(
                "http://connectivitycheck.gstatic.com/generate_204",
                headers=headers,
                proxies=self.__proxy,
            )
            if "Proxy" in response.text or "Proxy-Agent" in response.headers:
                name = response.headers.get("Proxy-Agent", "Unknown-proxy")
                logger.info(f"[check_proxy] Find Proxy Active in your IP {name} !")
                return name
            logger.info("[check_proxy] No Proxy Active in your IP")
            return None
        except Exception as e:
            logger.error(f"[check_proxy] Unexpected error: {e}")
