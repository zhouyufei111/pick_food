import requests
import base64

def search_food_heat(keyword, page=1):
    """
    Search for food heat information using the mxnzp API
    
    Args:
        keyword (str): Food name to search for
        page (int): Page number for pagination
        
    Returns:
        dict: API response data
    """
    # API endpoint
    url = "https://www.mxnzp.com/api/food_heat/food/search"
    
    # You need to register for your own app_id and app_secret
    # Visit: https://mp.weixin.qq.com/s/UvKr0SG73_Py63ICUnLBPw
    params = {
        "keyword": keyword,
        "page": page,
        "app_id": "qtnozkkmgienmqav",  # Replace with your actual app_id
        "app_secret": "uMalUpkv60aTwXkj2cWoAqZYPTqC6yza"  # Replace with your actual app_secret
    }
    
    response = requests.get(url, params=params)
    return response.json()


def search_nutrition(food_id):
    url = "https://www.mxnzp.com/api/food_heat/food/details"
    params = {
        "foodId": food_id,
        "app_id": "qtnozkkmgienmqav",  # Replace with your actual app_id
        "app_secret": "uMalUpkv60aTwXkj2cWoAqZYPTqC6yza"  # Replace with your actual app_secret
    }
    response = requests.get(url, params=params)
    return response.json()

def get_fatsecret_food(food_id, access_token):
    """
    Retrieve food information from the FatSecret API
    
    Args:
        food_id (str): The ID of the food to retrieve
        access_token (str): OAuth access token for FatSecret API
        
    Returns:
        dict: API response data
    """
    url = "https://platform.fatsecret.com/rest/food/v4"
    
    # Set up headers with authorization
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    # Set up parameters
    params = {
        "food_id": food_id,
        "format": "json"
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_fatsecret_token(client_id, client_secret):
    """
    Get OAuth access token from FatSecret API
    
    Args:
        client_id (str): Your FatSecret API client ID
        client_secret (str): Your FatSecret API client secret
        
    Returns:
        dict: Token response containing access_token, token_type, expires_in, etc.
    """
    # OAuth token endpoint
    url = "https://oauth.fatsecret.com/connect/token"
    
    # Create the Authorization header using Basic authentication
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Request body parameters
    data = {
        "grant_type": "client_credentials",
        "scope": "basic"
    }
    
    # Make the POST request
    response = requests.post(url, headers=headers, data=data)
    return response.json()

if __name__ == "__main__":
    
    # a = get_fatsecret_token("1e4b4b6ae2774064b0fc681c23b6a802","b5b576016b4e4b6087b1922f37d5750b")
    
    get_fatsecret_food("33691","eyJhbGciOiJSUzI1NiIsImtpZCI6IjEwOEFEREZGRjZBNDkxOUFBNDE4QkREQTYwMDcwQzE5NzNDRjMzMUUiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJFSXJkX19ha2tacWtHTDNhWUFjTUdYUFBNeDQifQ.eyJuYmYiOjE3NDM5MjUxODksImV4cCI6MTc0NDAxMTU4OSwiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mYXRzZWNyZXQuY29tIiwiYXVkIjoiYmFzaWMiLCJjbGllbnRfaWQiOiIxZTRiNGI2YWUyNzc0MDY0YjBmYzY4MWMyM2I2YTgwMiIsInNjb3BlIjpbImJhc2ljIl19.sTZ9Hjm6ZMY1jyuB5NfC1ql0LOB3G0UUVs9NOZ8swux-UuauHDZB-e3nTuUbWU7dzCC-r1R_Pd_RVNA26b61VPRNC7ib8XxsHRe1ds-h4Q7u2SgZGiqK-rglR-CZl8RjuIcaLR5_7lAraCwDc05BWYHnzB7AF--jj3cyn906_TzS7H1uhB6H0lBNR0N_g5U0Zv9wIqxZMHvW0UzRoFnHgwk3ZuMjzxOJPFQiFnoedZOlekGq1xp3pg4Zo3JS3EP-hw0lfiCOdhHYXGn5SYosHhcGUGk1VabWUTHKN_qx82ELUSRNcpleRBsuHzTyqfovYoYokUBI6R_GZJgL_BfjsEBXvRh5y0EMVtwm-mTm6x9lGwjR3Tz0tfQGzsLp1LyLJzPHz7LwQaI7SJenia1C--zSdgjMHWer4und98VV-dOCDVb9ouOL9753bJTNcF7SK0vAzhl2f9dIIj1S6s4M1U0OWtXZhakK-8oFfiH7S_zflTVjLu3Av5GYl7Zm-xkFcUd1RqaOBuUwsYQvThTY82wK8LVGr2VMLAh1raDWFEyUEHukJzAwhTehdA4Y6cMWbs3me867ohYuVntdMD6yA-wvUaz-ayJXfjNvJpJXLDX1jZiE4bBEude00y8emO-VGdsaFPyV1o2oUCtV1yLBBCeef6rZL_vv2rhXGvcuKB4")
    
    
    # food_id = '26992e46910bbc2c'
    
    # result = search_nutrition(food_id)
    # print(result)
    # Example usage
    result = search_food_heat("烧鸭饭")  # Searching for "apple"
    print(result)
    
    food_id = result['data']['list'][0]['foodId']
    
    result = search_nutrition(food_id)
    print(result)
    
    
    # # If the API call is successful, you can process the data
    # if result.get("code") == 1:  # Assuming code 1 means success
    #     data = result.get("data")
    #     print(f"Found {len(data)} results")
    #     for item in data:
    #         print(item)
    # else:
    #     print(f"Error: {result.get('msg')}")
