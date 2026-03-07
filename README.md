# 🤖 Discord Bot

<div align="center">

**Meet Berda Bot**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-blue.svg)](https://github.com/Rapptz/discord.py)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

</div>

---

##  About

Berda Bot lives in our private discord server. Feel free to add a feature if you know how to do that sort of thing.

##  Contributing Pre-Process

### Prerequisites

- Python 3.8 or higher
- Git
- A Discord Bot Token ([How to get one](https://discord.com/developers/applications))

### 🍴 Fork & Clone

1. **Fork this repository** by clicking the "Fork" button at the top right of this page

2. **Clone your fork** to your local machine:
   ```bash
   git clone https://github.com/YOUR-USERNAME/discord-bot.git
   cd discord-bot
   ```

3. **Add the upstream remote** (to keep your fork synced):
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/discord-bot.git
   ```

### 🐍 Set Up Virtual Environment

Create and activate a virtual environment to keep dependencies isolated:

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 🔑 Configure Environment Variables

Create a `.env` file in the root directory:
```bash
DISCORD_TOKEN=your_bot_token_here
```

> ⚠️ **Never commit your `.env` file!** Make sure it's in `.gitignore`

---

## 🛠️ Contributing

Here's how to add your own features:

###  Create a Branch

Always create a new branch for your feature:

```bash
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
Go crazy! I dont care at all tbh

###  Add Your Feature

###  Test Your Changes

Run the bot locally and test your new feature:

```bash
python bot.py
```

###  Commit Your Changes

```bash
git add .
git commit -m "feat: add cool new feature"
```

**Commit message format:**
- `feat:` - new feature
- `fix:` - bug fix
- `docs:` - documentation changes
- `refactor:` - code refactoring

###  Push to Your Fork

```bash
git push origin feature/your-feature-name
```

###  Create a PR

---

## License
Do whatever you want with this 🤷‍♂️

---

<div align="center">
</div>
