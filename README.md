# Beyond Horizon Twitter Bot

An AI-powered Twitter bot that shares fascinating Long Line of Sight (LoS) views from around the world. This project automatically generates and posts content about remarkable viewpoints where distant landmarks or locations are visible from specific observation points.

## Project Structure

```
BeyondHorizon_Twitter/
├── docs/               # Project documentation
├── src/               # Source code
├── tests/             # Test files
├── config/            # Configuration files
└── README.md          # Project overview
```

## Getting Started

1. Clone this repository
2. Install Python 3.8 or higher
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Copy `config/config.template.env` to `config/.env`
   - Add your API keys to the `.env` file:
     - OpenAI API key from https://platform.openai.com/
     - Twitter API credentials from https://developer.twitter.com/
   - NEVER commit the `.env` file to the repository

## API Keys Setup

### Twitter API Setup
1. Go to https://developer.twitter.com/
2. Create a new Project and App
3. Set up the app as "Web App, Automated App or Bot"
4. Enable OAuth 1.0a with Read and Write permissions
5. Generate API keys and tokens
6. Add them to your `.env` file

### OpenAI API Setup
1. Go to https://platform.openai.com/
2. Generate an API key
3. Add it to your `.env` file

## Documentation

For detailed project information, please refer to:
- [Project Plan](docs/project_plan.md)

## Security Notes

⚠️ IMPORTANT: Never commit API keys or sensitive credentials to this repository!
- Always use environment variables for sensitive data
- Keep your `.env` file private and local
- Use `config.template.env` as a template for required environment variables

## License

This is a non-commercial project. All rights reserved.

## Contributing

This is a personal project, but suggestions and feedback are welcome through the Twitter bot's interaction features.
