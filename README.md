# BeyondHorizon Twitter Bot

A companion project to [beyondhorizoncalc.com](https://beyondhorizoncalc.com) that automatically shares fascinating Long Line of Sight (LoS) views from around the world. This project posts regular updates about remarkable viewpoints where distant landmarks or locations are visible from specific observation points, demonstrating the effects of Earth's curvature on visibility.

## Features

- Automatic posting of preset long line of sight views
- Integration with BeyondHorizonCalc's preset database
- Tweet history tracking and preset rotation
- Support for testing and preview modes

## Project Structure

```
BeyondHorizon_Twitter/
├── config/            # Configuration files (.env)
├── data/             # SQLite databases
├── docs/             # Project documentation
├── src/              # Source code
└── README.md         # Project overview
```

## Getting Started

For detailed setup instructions, see our [Quickstart Guide](docs/quickstart.md).

1. Clone this repository
2. Install Python 3.8 or higher
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Copy `config/.env.template` to `config/.env`
   - Add your Twitter API credentials
   - Configure environment settings

## Twitter API Setup

1. Go to https://developer.twitter.com/
2. Create a new Project and App
3. Set up the app as "Web App, Automated App or Bot"
4. Enable OAuth 1.0a with Read and Write permissions
5. Generate API keys and tokens
6. Add them to your `.env` file:
   ```
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_SECRET=your_access_secret
   ```

## Documentation

For detailed project information, please refer to:
- [Quickstart Guide](docs/quickstart.md)
- [Architecture Overview](docs/architecture.md)
- [Preset Manager Documentation](docs/preset_manager.md)

## Deployment

This project is designed to run on PythonAnywhere:
1. Upload the project to PythonAnywhere
2. Set up environment variables in PythonAnywhere dashboard
3. Configure the task scheduler for automated posting

## Security Notes

⚠️ IMPORTANT: Never commit API keys or sensitive credentials to this repository!
- Always use environment variables for sensitive data
- Keep your `.env` file private and local
- Use `.env.template` as a template for required environment variables

## License

This is a non-commercial project. All rights reserved.

## Contributing

This is a personal project, but suggestions and feedback are welcome through the Twitter bot's interaction features.
