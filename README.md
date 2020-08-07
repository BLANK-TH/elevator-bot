# Main Elevator Server Bot
This bot takes care of most fun, moderation, automation commands and functions
for the Elevator server. Currently this bot is not usable for other servers as
things like role ids, channel ids, role names, etc are hard-coded into the bot.
[Click here for a list of commands for this bot
](https://github.com/BLANK-TH/elevator-bot-resources/blob/info/commands.md).

## Contributing
If you would like to contribute to this bot, make sure you are in the Elevator
Discord server (Here is the invite: https://discord.gg/Cr43nuF). Once you are
in the server, contact BLANK#7086 to get a Developer role which grants access
to dev channels and permissions. Make sure you have Python 3.8 installed
(and added to PATH). This tutorial is for Windows, if you need to install it on
Linux or Mac, google how to do it, the process is pretty standard.

### Setup
#### Fork the Repo
Click the fork button on the top right of this page to create your own copy
of this code.

#### Clone the repo to your local machine
Open command prompt (Windows + R, enter `cmd`) then change your working
directory to the directory you want the code to be stored in. Then run
`git clone https://github.com/your-github-username/elevator-bot.git`. Replace
your-github-username with your GitHub username.

#### Install requirements
After you cloned the repo, install the required modules for the bot. To do that
run `pip install -r requirements.txt`.

#### Create secrets
The bot needs to have 2 secrets. One is the Discord Bot Token, the second is a
GitHub personal access token (certain commands need to create, edit, or delete
files in the
[elevator-bot-resources](https://github.com/BLANK-TH/elevator-bot-resources)
repo)
##### OPTION 1: Add to environment variables
Run `setx BOT_TOKEN your_discord_token_here`. Replace `your_discord_token_here`
with a discord bot token.  
Run `setx GITHUB_TOKEN your_github_personal_access_token_here`. Replace
`your_github_personal_access_token_here` with a GitHub personal access token for
your account. To learn how to get that token,
[Click Here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).
Make sure that token has the following permissions: `repo` AND `read:packages` AND `write:packages`.
Run `setx KRAKEN_TOKEN your_gitkraken_boards_pat_here`. Replace `your_gitkraken_boards_pat_here` with
a GitKraken account person access token with read + write permissions for both board and user.

##### OPTION 2: Create a .env file
In the folder in which you are storing the project files (make sure it's the
same folder as the one with `bot.py` in it) create a new file called `.env`
(no name, just the extension .env) and add the following lines into it:
```
GITHUB_TOKEN="your_github_personal_access_token_here"
BOT_TOKEN="your_discord_token_here"
KRAKEN_TOKEN="your_gitkraken_boards_pat_here"
```
Replace `your_discord_token_here` with your discord bot token. Replace
`your_github_personal_access_token_here` with a GitHub personal access token for
your account. To learn how to get that token,
[Click Here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).
Make sure that token has the following permissions: `repo` AND `read:packages`
AND `write:packages`. Replace `your_gitkraken_boards_pat_here` with
a GitKraken account person access token with read + write permissions for both board and user.

#### DONE!
