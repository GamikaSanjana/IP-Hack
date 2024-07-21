# iphack

![iphack Logo](https://example.com/logo.png)

## Overview

`iphack` is a powerful and versatile Python tool designed for IP inquiry and manipulation using advanced anonymization techniques. Whether you're a network security enthusiast, an ethical hacker, or simply someone interested in exploring and interacting with IP addresses and web services securely and anonymously, `iphack` is the tool for you.

## Features

- **Anonymized Requests**: Maintain your anonymity by sending requests through Tor, VPN, or standard web connections.
- **Multiple HTTP Methods**: Supports GET, POST, PUT, DELETE, and HEAD requests for comprehensive interaction with web services.
- **Fake User-Agent**: Disguise the source of your requests to avoid detection.
- **Logging**: Enable or disable detailed logs to monitor the tool's operations.
- **Easy Integration**: Seamlessly integrate `iphack` into other security tools and scripts.

## Installation

Install `iphack` via pip:

```sh```
```pip install iphack```

## Usage
Send a GET Request
<details>
<summary>from iphack import inquiry

response = inquiry.get("https://api.ipify.org/")
print(response.text)</summary>
</details>

## Send a POST Request
<details>
<summary>response = inquiry.post("https://example.com")</summary>
</details>

## Send a PUT Request
<details>
<summary>response = inquiry.put("https://example.com")
</summary>
</details>

## Send a DELETE Request
<details>
<summary>response = inquiry.delete("https://example.com")</summary>
</details>

## Send a HEAD Request
<details>
<summary>response = inquiry.head("https://example.com")</summary>
</details>

## Change Anonymization Method
<details>
<summary>inquiry.rechange("tor")   # Use Tor network
inquiry.rechange("web")   # Use standard web connection
inquiry.rechange("vpn")   # Use VPN connection
</summary>
</details>

## Enable and Disable Logging
<details>
<summary>inquiry.debug(True)  # Enable logging
inquiry.debug(False) # Disable logging</summary>
</details>

## Contribution

We welcome contributions from the community! Feel free to fork the repository and submit a pull request with your enhancements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Connect with Us

Stay updated with our latest developments and tutorials by subscribing to our YouTube Channel.


In this version, the `<details>` and `<summary>` HTML tags are used to create expandable sections for the code snippets. This improves the readability of the `README.md` and provides a more interactive experience for users. However, GitHub doesn't support JavaScript in markdown files, so adding a direct copy button is not possible within GitHub's markdown renderer. For that functionality, you would typically need to host the documentation on a website where you can use JavaScript.
