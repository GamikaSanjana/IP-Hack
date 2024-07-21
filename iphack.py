#!/usr/bin/env python3

import logging
from iphack import inquiry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_request(method, url, *args, **kwargs):
    """Make a request using the specified HTTP method."""
    try:
        response = method(url, *args, **kwargs)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.info(f"Request to {url} succeeded: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request to {url} failed: {e}")
        return None

def main():
    # Set up anonymous browsing
    inquiry.rechange("tor")  # Default to Tor for anonymity
    
    # Example GET request
    get_response = make_request(inquiry.get, "https://api.ipify.org/")
    if get_response:
        print(f"IP Address: {get_response.text}")
    
    # Example POST request
    post_response = make_request(inquiry.post, "https://example.com", data={"key": "value"})
    
    # Example PUT request
    put_response = make_request(inquiry.put, "https://example.com", data={"key": "value"})
    
    # Example DELETE request
    delete_response = make_request(inquiry.delete, "https://example.com")
    
    # Example HEAD request
    head_response = make_request(inquiry.head, "https://example.com")
    
    # Enable and disable logging
    inquiry.debug()  # Enable log
    inquiry.debug()  # Disable log

if __name__ == "__main__":
    main()
