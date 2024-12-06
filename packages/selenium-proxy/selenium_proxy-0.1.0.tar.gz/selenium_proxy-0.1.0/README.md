# Selenium Proxy Extension
Considering that there is no function that works very well natively in Selenium for using proxys with authentication in chromedriver, this is an effective way to solve this problem.

## Usage

First, we import the extension, using the following syntax:
```python
from extension import proxies
```

Then we can use the syntax to set the proxy
```python
proxies_extension = proxies("username", "password", "host", "port")
```

It looks like this:
```python
chrome_options = webdriver.ChromeOptions()
proxies_extension = proxies("username", "password", "host", "port")
chrome_options.add_extension(proxies_extension)
service = Service(executable_path='./chromedriver.exe') 
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://api.my-ip.io/v2/ip.json")
```

## How it works?
This extension works in a very simple way, when calling the proxies function, it creates a javascript extension that configures the proxy in the browser, and this extension is injected when starting the browser
