# Reddit_Post_AIHawk

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Generating Reddit API Keys](#generating-reddit-api-keys)
- [Conclusion](#conclusion)
- [Contributors](#contributors)
- [License](#license)
- [Disclaimer](#disclaimer)

## Introduction

The Reddit Post Generator is a Python script designed to automatically generate and post content on Reddit. By analyzing trending subreddits and top posts, the script creates innovative posts tailored to maximize engagement and upvotes. It uses OpenAI's GPT models and LangChain to generate content based on specific rules and summaries.

## Features

- **Automatic Reddit Posting**: Posts are generated and submitted to trending subreddits.
- **Customizable Content Generation**: Utilizes various post types such as clickbait, humorous, question-oriented, and more.
- **Error Handling**: Robust error management for posting failures, rate limits, and subreddit restrictions.
- **Randomized Posting Intervals**: Avoids detection of automated behavior by introducing random sleep intervals.

## Installation

To set up and use the Reddit Post Generator, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/reddit-post-generator.git
   cd reddit-post-generator
   ```

2. **Create a Virtual Environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```



## Configuration

Ensure you have the following configuration files in place:
Certainly! Here’s the updated section of your README file that includes information about the `config_secrets.py` file for configuration:

---

## Configuration

To generate Reddit API keys, follow these steps:

1. **Create a Reddit Account**:
   - If you don’t already have a Reddit account, sign up at [reddit.com](https://www.reddit.com).

2. **Register a New Application**:
   - Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps).
   - Scroll down to "Developed Applications" and click "Create App".
   - Fill out the form:
     - **name**: Choose a name for your app.
     - **App type**: Select "script" for personal use.
     - **description**: Optional, add a description of your app.
     - **about url**: Leave blank.
     - **permissions**: Leave blank.
     - **callback url**: Set to `http://localhost:8000` (or any URL you prefer for local testing).
     - **permissions**: Select `read` and `submit`.
   - Click "Create app".

3. **Obtain Your API Credentials**:
   - Once created, you'll be able to see your `client_id` and `client_secret`.
   - Use these credentials in your `config_secrets.py` file under the Reddit section.

4. **`config_secrets.py`**:
   - This file contains your sensitive credentials and API keys. It should be placed in the same directory as your main script. Make sure to replace the placeholder values with your actual credentials.

   ```python
   CLIENT_ID = 'YOUR_REDDIT_CLIENT_ID'
   CLIENT_SECRET = 'YOUR_REDDIT_CLIENT_SECRET'
   USERNAME = 'YOUR_REDDIT_USERNAME'
   PASSWORD = 'YOUR_REDDIT_PASSWORD'
   OPENAI_KEY = 'YOUR_OPENAI_API_KEY'
   ```

   - **Explanation**:
     - `CLIENT_ID`: Your Reddit application's client ID.
     - `CLIENT_SECRET`: Your Reddit application's client secret.
     - `USERNAME`: Your Reddit username.
     - `PASSWORD`: Your Reddit account password.
     - `OPENAI_KEY`: Your OpenAI API key.

   **Important**: Ensure this file is kept private and not shared or committed to version control to protect your sensitive information.


## Usage

To use the Reddit Post Generator, execute the script `main.py`. Ensure that the configuration files are correctly set up before running the script.

```bash
python main.py
```

## Conclusion

The Reddit Post Generator is a powerful tool for automating Reddit content creation. By leveraging AI-driven content generation and automation, users can engage with trending topics and generate content that maximizes interaction.

## Contributors

- [feder-cr](https://github.com/feder-cr) - Creator and Lead Developer

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

The use of this script for posting on Reddit is subject to Reddit’s API terms of service. The script is provided "as-is" without any warranties or guarantees. For educational and demonstrative purposes only, this script is intended to showcase how Reddit automation might work and is not recommended for real-world use.

Using this script for actual Reddit posting could lead to account suspension or other penalties if it violates Reddit's guidelines or terms of service. Always use automation responsibly and ensure compliance with Reddit's rules and policies.

We strongly discourage the use of this script for real-world applications and advise against deploying it for any production or large-scale posting activities.
