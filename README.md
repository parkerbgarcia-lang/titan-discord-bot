# TITAN - Discord Bot

**TITAN** (Total Infrastructure Tickrate Alignment Normalizer) is a clean, professional Discord bot demonstrating best practices in bot architecture, security, and logging.

## Features

- ✅ Official bot account (not a selfbot)
- ✅ Minimal Discord intents
- ✅ Safe, read-only example commands
- ✅ Comprehensive logging to files and console
- ✅ Professional error handling
- ✅ Clean, maintainable code structure
- ✅ No slash commands, embeds, or database

## Project Structure

```
titan-discord-bot/
├── bot.py                 # Main entry point
├── config.py              # Configuration validation
├── requirements.txt       # Python dependencies
├── .env.example           # Sample environment variables
├── .gitignore             # Git ignore rules
├── cogs/
│   ├── commands.py        # Example commands
│   └── events.py          # Discord event handlers
├── utils/
│   ├── terminal.py        # Terminal output helpers
│   └── logger.py          # Logging configuration
└── logs/                  # Log files (git-ignored)
    ├── titan.log          # Normal activity
    └── errors.log         # Error stack traces
```

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- A Discord server for testing
- A Discord bot token

### 2. Create a Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" tab and click "Add Bot"
4. Under "TOKEN", click "Copy" to copy your bot token
5. **Keep this token secret!** Never commit it to version control

### 3. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/parkerbgarcia-lang/titan-discord-bot.git
cd titan-discord-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env
cp .env.example .env
# Or on Windows:
copy .env.example .env

# Edit .env and add your bot token
# Open .env in your text editor and replace:
# DISCORD_TOKEN=your_bot_token_here
# COMMAND_PREFIX=!
```

### 4. Invite Bot to Server

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your bot application
3. Go to "OAuth2" → "URL Generator"
4. Select scopes: `bot`
5. Select permissions: `Send Messages`, `Read Messages/View Channels`, `Use Slash Commands`
6. Copy the generated URL and open it in your browser
7. Select a test server and authorize

### 5. Run the Bot

```bash
# Make sure your virtual environment is activated
python bot.py
```

You should see:

```
TITAN startup banner
✓ Python 3.x OK
✓ Configuration validated
✓ Bot created
✓ Loaded cogs.events
✓ Loaded cogs.commands
✓ Connecting to Discord...
✓ TITAN is ready
```

### 6. Test Commands

In your Discord server, try:

```
!ping            # Shows latency
!help            # Lists all commands
!about           # Shows bot info
!status          # Shows bot statistics
!userinfo        # Shows user information
!userinfo @user  # Shows another user's info
```

## Configuration

### Environment Variables (`.env`)

```env
DISCORD_TOKEN=your_bot_token_here
COMMAND_PREFIX=!
```

**Never commit `.env` to version control.** It's in `.gitignore` by default.

### Changing the Command Prefix

Edit `.env` and change `COMMAND_PREFIX`:

```env
COMMAND_PREFIX=?
```

Then restart the bot.

## Logging

Logs are stored in the `logs/` directory:

- **`titan.log`** — All log levels (DEBUG and above)
- **`errors.log`** — Warnings and errors with stack traces

Each file rotates at 1MB with 5 backups kept.

### Log Format

```
2026-09-01 12:34:56 | INFO     | titan: Bot ready as TITAN#1234 (ID: 123456789)
```

## Commands

### Public Commands

- `!ping` — Show bot latency
- `!help` — List all available commands
- `!about` — Show information about TITAN
- `!status` — Show bot uptime and statistics
- `!userinfo [member]` — Show user details

All commands log their invocation with username, user ID, guild, and success/failure.

## Development

### Adding a New Command

Edit `cogs/commands.py`:

```python
@commands.command(name="hello")
async def hello(self, ctx: commands.Context) -> None:
    """Say hello to the user."""
    await ctx.send(f"Hello {ctx.author}!")
    logger.info(f"Hello command invoked by {ctx.author}")
```

### Adding an Event Handler

Edit `cogs/events.py`:

```python
@commands.Cog.listener()
async def on_message(self, message: discord.Message) -> None:
    """Called when a message is sent."""
    if message.author == self.bot.user:
        return
    logger.debug(f"Message from {message.author}: {message.content[:50]}")
```

### Terminal Output

Use the helpers in `utils/terminal.py`:

```python
from utils.terminal import print_success, print_warning, print_error

print_success("Operation completed")
print_warning("This might be important")
print_error("Something went wrong")
```

## Security Notes

- ✅ Token is read from `.env` and never logged or printed
- ✅ `.env` is in `.gitignore` to prevent accidental commits
- ✅ Configuration is validated on startup
- ✅ Minimal Discord intents reduce security surface
- ✅ All errors are caught and handled gracefully
- ✅ No sensitive user data is logged by default
- ✅ Rate limits are respected through discord.py's built-in handling

## Troubleshooting

### "DISCORD_TOKEN not found in .env file"

- Make sure you copied `.env.example` to `.env`
- Make sure you added your bot token to `.env`
- The token should start with "Bot" (for bot accounts)

### "Invalid token provided"

- Double-check your token in `.env`
- Tokens are case-sensitive and contain uppercase and lowercase letters
- If unsure, generate a new token in the Developer Portal

### Bot doesn't respond to commands

- Check that the bot has "Send Messages" permission in the channel
- Make sure the bot is invited with the `bot` scope
- Try `!ping` to check if the bot is responsive
- Check the logs in `logs/titan.log`

### "discord.Intents" error

- Make sure you have discord.py 2.0+: `pip install --upgrade discord.py`

## Files and Permissions

- `bot.py` — Executable, read the startup process
- `config.py` — Environment validation and constants
- `cogs/` — Command and event definitions
- `utils/` — Reusable helpers
- `logs/` — Created at runtime, git-ignored

## License

This project is provided as-is for educational purposes.

## Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/)
- [Discord API Documentation](https://discord.com/developers/docs/)

---

**Questions?** Check the logs in `logs/titan.log` for detailed error information.
