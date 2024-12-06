# Net Analysis

Net Analysis is a Python package that provides utilities for analyzing network information including IP lookup, proxy detection, and more.

## Features

- **IP Lookup**: Analyze IP addresses to retrieve details such as country, city, state, time zone, ISP, and more.
- **Proxy Detection**: Detect active proxies and retrieve information about them.
- **User-Agent Customization**: Ability to set custom User-Agent headers for HTTP requests.

## Installation

You can install Net Analysis using pip:

```bash
pip install net-analysis
```

## Usage

```python
from net_analysis import NetAnalysis

# Initialize net_Analysis instance
Analysis = NetAnalysis("http://user:pass@12.34.567.89:12345")

# Retrieve network information
print("City:", Analysis.city)
print("Country:", Analysis.country)
print("IP Address:", Analysis.ip)
# More attributes available, such as state, time_zone, ISP, etc.

# Check for active proxies
proxy_name = Analysis.check_proxy()
if proxy_name:
    print("Active Proxy:", proxy_name)
else:
    print("No active proxy found.")

```

## Dependencies

- [requests](https://pypi.org/project/requests/): For making HTTP requests.
- [countryinfo](https://pypi.org/project/countryinfo/): For retrieving country information.
- [loguru](https://pypi.org/project/loguru/): For logging.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.