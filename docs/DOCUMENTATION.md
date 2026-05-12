# JSON Fetch and Filter Application - Detailed Documentation

## Overview
A Python CLI application that demonstrates fetching JSON data from public APIs, filtering it based on various conditions, and displaying results in user-friendly formats.

## Architecture

### Main Components

```
┌───────────────────────────────────────────────────────┐
│                 fetch_and_filter.py                   │
├───────────────────┬───────────────────┬───────────────┤
│   Data Fetching    │   Data Filtering   │  Display Logic │
└───────────────────└───────────────────└───────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────────────┐
│                    User Interaction                    │
│  (Input/Output via console interface)                  │
└───────────────────────────────────────────────────────┘
```

## Detailed Function Documentation

### 1. Data Fetching Functions

#### `fetch_data_from_api(url)`

**Purpose**: Downloads JSON data from a given API endpoint

**Parameters**:
- `url` (str): The API endpoint URL to fetch data from

**Returns**:
- `list` or `dict`: Parsed JSON data from the API
- `None`: If the request fails

**Methodology**:
1. Uses `requests.get()` to send HTTP GET request
2. `response.raise_for_status()` validates HTTP status code
3. `response.json()` parses JSON response into Python objects
4. Exception handling for network errors and invalid responses

**Error Handling**:
- Catches `requests.exceptions.RequestException` for network issues
- Returns `None` on failure with error message

**Example Usage**:
```python
data = fetch_data_from_api('https://jsonplaceholder.typicode.com/posts')
```

### 2. Data Filtering Functions

#### `filter_posts_by_user_id(posts, user_id)`

**Purpose**: Filters a list of posts to return only those matching a specific user ID

**Parameters**:
- `posts` (list): List of post dictionaries
- `user_id` (int): The user ID to filter by

**Returns**:
- `list`: Filtered list of posts matching the user_id

**Algorithm**:
- Linear search through posts list
- Dictionary key lookup: `post['userId']`
- Exact match comparison

**Time Complexity**: O(n) where n is number of posts

**Example**:
```python
user1_posts = filter_posts_by_user_id(all_posts, 1)
```

#### `filter_users_by_city(users, city_name)`

**Purpose**: Filters users by their city name (nested dictionary access)

**Parameters**:
- `users` (list): List of user dictionaries
- `city_name` (str): City name to filter by (case-insensitive)

**Returns**:
- `list`: Users from the specified city

**Methodology**:
- Uses `.get()` method for safe nested dictionary access
- Case-insensitive comparison with `.lower()`
- Handles missing keys gracefully with default empty string

**Nested Access Pattern**:
```python
user.get('address', {}).get('city', '')
```

**Example**:
```python
chicago_users = filter_users_by_city(all_users, 'Chicago')
```

#### `filter_by_multiple_conditions(posts, user_id=None, min_id=None)`

**Purpose**: Advanced filtering with multiple optional conditions

**Parameters**:
- `posts` (list): List of post dictionaries
- `user_id` (int, optional): Filter by user ID
- `min_id` (int, optional): Filter posts with ID > min_id

**Returns**:
- `list`: Posts matching all specified conditions

**Logic**:
- Uses boolean logic with `and` operator
- Each condition is optional (None means ignore)
- Conditions are combined: `(user_match) AND (id_match)`

**Example**:
```python
# Get posts from user 2 with ID > 50
filtered = filter_by_multiple_conditions(posts, user_id=2, min_id=50)
```

### 3. Display Functions

#### `display_results(data, title="Results")`

**Purpose**: Pretty-print results with formatting

**Parameters**:
- `data` (list or dict): Data to display
- `title` (str): Section title for output

**Methodology**:
- Uses `json.dumps()` with `indent=2` for pretty printing
- Handles both list and dictionary data types
- Adds visual separators and item numbering
- Colorful output with emoji indicators

**Output Format**:
```
======================================================================
📊 Posts by User 1
======================================================================
Found 10 items:

--- Item 1 ---
{
  "id": 1,
  "title": "sunt aut facere...",
  "userId": 1
}

======================================================================
```

#### `display_summary(data)`

**Purpose**: Show concise summary without full details

**Parameters**:
- `data` (list): List of dictionaries to summarize

**Methodology**:
- Iterates through items with enumeration
- Conditional display based on available keys:
  - Shows `id` and `title` for posts (truncated to 50 chars)
  - Shows `id` and `name` for users
  - Fallback to full item display if keys not found

**Example Output**:
```
======================================================================
📋 Summary
======================================================================
1. ID: 1, Title: sunt aut facere repellat provident occaecati...
2. ID: 2, Title: qui est esse...
======================================================================
```

### 4. Main Program Functions

#### `main()`

**Purpose**: Entry point and control flow manager

**Methodology**:
1. Displays welcome message
2. Presents API selection menu
3. Validates user choice
4. Calls appropriate handler function
5. Handles exceptions and keyboard interrupts

**Control Flow**:
```
Start → Display Menu → Get Choice → Validate → Fetch Data → 
        ↓
Handle Posts/Users → Filter Data → Display Results → End
```

#### `handle_posts(posts)`

**Purpose**: Manage posts filtering workflow

**Workflow**:
1. Prompt for user ID input
2. Call `filter_posts_by_user_id()`
3. Display summary
4. Offer detailed view option
5. Call `display_results()` if requested

**User Interaction**:
- `input("Enter User ID to filter (e.g., 1): ")`
- `input("Show detailed view? (y/n): ")`

#### `handle_users(users)`

**Purpose**: Manage users filtering workflow

**Workflow**:
1. Prompt for city name input
2. Call `filter_users_by_city()`
3. Display summary and results
4. Handle empty results case

**User Interaction**:
- `input("Enter city name to filter (e.g., 'South Elvis'): ")`

## Technical Details

### Data Structures

**Post Object Structure**:
```python
{
  "userId": int,      # ID of the user who created the post
  "id": int,          # Unique post identifier
  "title": str,       # Post title
  "body": str         # Post content
}
```

**User Object Structure**:
```python
{
  "id": int,          # Unique user identifier
  "name": str,        # User's full name
  "username": str,    # Username
  "email": str,       # Email address
  "address": {        # Nested address object
    "street": str,
    "suite": str,
    "city": str,       # Used for filtering
    "zipcode": str,
    "geo": {
      "lat": str,
      "lng": str
    }
  },
  "phone": str,
  "website": str,
  "company": {
    "name": str,
    "catchPhrase": str,
    "bs": str
  }
}
```

### Error Handling Strategies

1. **Network Errors**: Caught by `requests.exceptions.RequestException`
2. **Invalid User Input**: Type conversion with validation
3. **Keyboard Interrupt**: Graceful exit with message
4. **Unexpected Errors**: Global exception handler in `main()`

### Input Validation

- Menu choice validation: `if choice not in api_urls`
- Integer conversion: `int(input(...))`
- Empty input handling: `.strip()` method

### Output Formatting

- **Separators**: `="=" * 70` for visual separation
- **Emoji**: 📥, ✅, ❌, 📊, 📋, 🚀, 👋 for visual cues
- **Indentation**: `json.dumps(indent=2)` for readability
- **Truncation**: Title truncation to 50 characters in summary

## Usage Examples

### Example 1: Filtering Posts

```
Choose an API to fetch data from:
1. Posts (JSONPlaceholder)
2. Users (JSONPlaceholder)

Enter your choice (1-2): 1
📥 Fetching data from: https://jsonplaceholder.typicode.com/posts
✅ Successfully fetched data!

--- Posts Filtering ---

Enter User ID to filter (e.g., 1): 2

======================================================================
📋 Summary
======================================================================
1. ID: 11, Title: et ea vero quia laudantium autem...
2. ID: 12, Title: in quibusdam tempore odit est dolorem...
...
======================================================================

Show detailed view? (y/n): y

======================================================================
📊 Posts by User 2
======================================================================
Found 10 items:

--- Item 1 ---
{
  "body": "et ea vero quia laudantium autem...",
  "id": 11,
  "title": "et ea vero quia laudantium autem",
  "userId": 2
}
...
======================================================================
```

### Example 2: Filtering Users

```
Choose an API to fetch data from:
1. Posts (JSONPlaceholder)
2. Users (JSONPlaceholder)

Enter your choice (1-2): 2
📥 Fetching data from: https://jsonplaceholder.typicode.com/users
✅ Successfully fetched data!

--- Users Filtering ---

Enter city name to filter (e.g., 'South Elvis'): Gwenborough

======================================================================
📋 Summary
======================================================================
1. ID: 1, Name: Leanne Graham
======================================================================

======================================================================
📊 Users from Gwenborough
======================================================================
Found 1 items:

--- Item 1 ---
{
  "address": {
    "city": "Gwenborough",
    "geo": {
      "lat": "-37.3159",
      "lng": "81.1496"
    },
    "street": "Kulas Light",
    "suite": "Apt. 556",
    "zipcode": "92998-3874"
  },
  "company": {
    "bs": "harness real-time e-markets",
    "catchPhrase": "Multi-layered client-server neural-net",
    "name": "Romaguera-Crona"
  },
  "email": "Sincere@april.biz",
  "id": 1,
  "name": "Leanne Graham",
  "phone": "1-770-736-8031 x56442",
  "username": "Bret",
  "website": "hildegard.org"
}

======================================================================
```

## Implementation Patterns

### 1. Modular Design
- Separation of concerns: fetching, filtering, displaying
- Single responsibility principle for each function
- Reusable components

### 2. Defensive Programming
- Safe dictionary access with `.get()` method
- Exception handling at appropriate levels
- Input validation and sanitization

### 3. User Experience
- Clear prompts and instructions
- Visual feedback with emoji and separators
- Summary before detailed view option
- Graceful error messages

### 4. Code Organization
- Function docstrings with Args/Returns
- Section comments (STEP 1, STEP 2, etc.)
- Logical grouping of related functions

## Performance Considerations

- **Memory**: Loads entire dataset into memory (suitable for small APIs)
- **Speed**: Linear search algorithms (O(n) complexity)
- **Network**: Single API request per session

## Limitations

1. No pagination for large datasets
2. No caching of API responses
3. Limited to two hardcoded API endpoints
4. No persistent storage
5. Basic error handling only

## Future Enhancements

1. Add more API endpoints
2. Implement caching mechanism
3. Add pagination support
4. Export results to file (JSON, CSV)
5. Add more filter conditions
6. Implement command-line arguments
7. Add unit tests
8. Support for authentication if needed

## Development Notes

### Testing
- Manual testing with various inputs
- Edge case testing (empty results, invalid inputs)
- Network error simulation

### Dependencies
- Only requires `requests` library
- No external configuration needed
- Works with Python 3.x standard library

### Deployment
- Single file application
- No installation required (except requests)
- Portable across platforms

## Conclusion

This application demonstrates:
- API integration with Python
- JSON data processing
- Data filtering techniques
- User interface design
- Error handling best practices
- Modular code organization

The code serves as a practical example for learning Python data processing and API interaction patterns.