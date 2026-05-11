"""
1. Download JSON from a free API
2. Parse the JSON data
3. Filter data based on conditions (city name, user id)
4. Display filtered results

"""

import requests  # Library to download data from the internet
import json     # Library to work with JSON data


# STEP 1: FETCH JSON FROM API

def fetch_data_from_api(url):
    """
    Downloads JSON data from a given URL.
    
    Args:
        url (str): The API endpoint to fetch from
        
    Returns:
        list or dict: Parsed JSON data
        
    Raises:
        Exception: If the request fails
    """
    try:
        print(f"📥 Fetching data from: {url}\n")
        
        response = requests.get(url)  # Send request to the API
        response.raise_for_status()   # Raise error if request failed
        
        data = response.json()  # Convert response to Python object
        print(f"✅ Successfully fetched data!\n")
        
        return data
    
    except requests.exceptions.RequestException as error:
        print(f"❌ Error fetching data: {error}")
        return None


# STEP 2: FILTER DATA BASED ON CONDITIONS

def filter_posts_by_user_id(posts, user_id):
    """
    Filters posts by user ID.
    
    Args:
        posts (list): List of post dictionaries
        user_id (int): The user ID to filter by
        
    Returns:
        list: Filtered posts matching the user_id
    """
    filtered = []
    
    for post in posts:
        if post['userId'] == user_id:
            filtered.append(post)
    
    return filtered


def filter_by_multiple_conditions(posts, user_id=None, min_id=None):
    """
    Advanced filtering with multiple conditions.
    
    Args:
        posts (list): List of post dictionaries
        user_id (int): Filter by user ID
        min_id (int): Filter posts with ID greater than this value
        
    Returns:
        list: Filtered posts
    """
    filtered = []
    
    for post in posts:
        # Check if conditions match
        user_match = (user_id is None) or (post['userId'] == user_id)
        id_match = (min_id is None) or (post['id'] > min_id)
        
        # Add to filtered list if all conditions match
        if user_match and id_match:
            filtered.append(post)
    
    return filtered


def filter_users_by_city(users, city_name):
    """
    Filters users by city name.
    
    Args:
        users (list): List of user dictionaries
        city_name (str): The city name to filter by
        
    Returns:
        list: Filtered users from the specified city
    """
    filtered = []
    
    for user in users:
        # Access nested dictionary: user['address']['city']
        if user.get('address', {}).get('city', '').lower() == city_name.lower():
            filtered.append(user)
    
    return filtered


# STEP 3: DISPLAY RESULTS

def display_results(data, title="Results"):
    """
    Pretty print the results.
    
    Args:
        data (list or dict): Data to display
        title (str): Title for the output
    """
    print("\n" + "=" * 70)
    print(f"📊 {title}")
    print("=" * 70)
    
    if isinstance(data, list):
        print(f"Found {len(data)} items:\n")
        
        for i, item in enumerate(data, 1):
            print(f"--- Item {i} ---")
            # Pretty print with indentation
            print(json.dumps(item, indent=2))
            print()
    else:
        print(json.dumps(data, indent=2))
    
    print("=" * 70 + "\n")


def display_summary(data):
    """
    Display a summary without full details.
    
    Args:
        data (list): List of dictionaries
    """
    print("\n" + "=" * 70)
    print("📋 Summary")
    print("=" * 70)
    
    for i, item in enumerate(data, 1):
        # Show only key information
        if 'id' in item and 'title' in item:
            print(f"{i}. ID: {item['id']}, Title: {item['title'][:50]}...")
        elif 'id' in item and 'name' in item:
            print(f"{i}. ID: {item['id']}, Name: {item['name']}")
        else:
            print(f"{i}. {item}")
    
    print("=" * 70 + "\n")


# ============================================================================
# STEP 4: MAIN PROGRAM
# ============================================================================

def main():
    """Main function that runs the entire program."""
    
    print("🚀 Welcome to JSON Filter App!\n")
    
    # Choose which API to use
    print("Choose an API to fetch data from:")
    print("1. Posts (JSONPlaceholder)")
    print("2. Users (JSONPlaceholder)\n")
    
    choice = input("Enter your choice (1-2): ").strip()
    
    # Define API URLs
    api_urls = {
        '1': {
            'url': 'https://jsonplaceholder.typicode.com/posts',
            'name': 'Posts'
        },
        '2': {
            'url': 'https://jsonplaceholder.typicode.com/users',
            'name': 'Users'
        }
    }
    
    # Get the selected API
    if choice not in api_urls:
        print("❌ Invalid choice!")
        return
    
    selected_api = api_urls[choice]
    url = selected_api['url']
    api_name = selected_api['name']
    
    # Fetch data from API
    data = fetch_data_from_api(url)
    
    if data is None:
        return
    
    # Handle different API responses
    if api_name == 'Posts':
        handle_posts(data)
    elif api_name == 'Users':
        handle_users(data)


def handle_posts(posts):
    """Handle filtering of posts data."""
    
    print("\n--- Posts Filtering ---\n")
    
    # Filter by User ID
    user_id = int(input("Enter User ID to filter (e.g., 1): ").strip())
    filtered_posts = filter_posts_by_user_id(posts, user_id)
    
    display_summary(filtered_posts)
    
    # Advanced filtering
    show_details = input("Show detailed view? (y/n): ").strip().lower()
    if show_details == 'y':
        display_results(filtered_posts, f"Posts by User {user_id}")


def handle_users(users):
    """Handle filtering of users data."""
    
    print("\n--- Users Filtering ---\n")
    
    # Filter by City
    city = input("Enter city name to filter (e.g., 'Apt. 692'): ").strip()
    filtered_users = filter_users_by_city(users, city)
    
    if filtered_users:
        display_summary(filtered_users)
        display_results(filtered_users, f"Users from {city}")
    else:
        print(f"❌ No users found in {city}")



# ============================================================================
# RUN THE PROGRAM
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user. Goodbye!")
    except Exception as error:
        print(f"\n❌ An unexpected error occurred: {error}")
