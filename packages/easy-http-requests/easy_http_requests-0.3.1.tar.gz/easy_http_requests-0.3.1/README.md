## Easy HTTP Requests

### usage
```python
from easy_http_requests.easy_http_request import EasyHttpRequest

# Create an instance of EasyHttpRequests
easy_http_requests = EasyHttpRequest()

# GET request
response = easy_http_requests.get('https://jsonplaceholder.typicode.com/posts')

print(response.status_code)

# POST request
response = easy_http_requests.post('https://jsonplaceholder.typicode.com/posts', data={'title': 'foo', 'body': 'bar', 'userId': 1})

print(response.status_code)
```