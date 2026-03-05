# Contributing to the Dataiku Teams Knowledge Bot

First off, thank you for considering contributing to this project! This bot is designed to be a living, evolving tool for our team.

## 🛠 How to Set Up Your Development Environment

Please **do not** test your code changes on the live production bot or the production Dataiku project.

1. **Clone this repository** to your local machine.
2. **Import the Dataiku Bundle**: Ask the repository maintainer for the latest `.zip` project bundle and import it into your own Dataiku sandbox environment.
3. **Create a Dev Teams Bot**:
   * Go to the Microsoft Teams Developer Portal.
   * Upload the `manifest/manifest.json` file to create your own isolated test bot.
   * Update the `validDomains` in the manifest to point to your specific Dataiku webapp URL.
4. **Local Python Setup**: Run `pip install -r requirements.txt` to ensure you are using the correct dependencies (especially `markupsafe==2.0.1`).

## 🚀 How to Submit Changes

1. Create a new branch for your feature
2. Make your changes in the `src/` Python files or the `manifest/` JSON.
3. Test your changes in your isolated Dataiku/Teams environment.
4. Commit your changes and push your branch to GitHub.
5. Open a **Pull Request (PR)** and include a screenshot if you changed something visual!

## ⚠️ Security Warning
**Never commit API keys, Tenant IDs, or App Passwords.** Always use `os.environ.get()` or Dataiku Project Variables for credentials.
