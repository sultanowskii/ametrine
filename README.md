# ametrine
**ametrine** is a set of tools for managing CTFs hosted on CTFd. Later full guide will be added.

### List of utils:
- **[OnlineTable](src/OnlineTable/OnlineTable.py)** provides information about competition as Flask-based website. Requires [leagues.json](example/leagues.json)

### List of scripts:
- **[Setup](src/Setup.py)** registrates users, teams and adds users to their teams using admin's account on CTFd platform. Checkout [users.csv](example/users.csv), [teams.csv](example/users.csv) and [leagues.json](example/leagues.json) to see the structure of these required files.
- **[TelegramCredentialsSender](src/TelegramCredentialsSender.py)** sends CTFd credentials to particiapnts via telegram. Of course, [users.csv](example/users.csv) must contain logins, passwords and telegram handles of users.
- **[Statistics](src/Statistics.py)** gets list of all teams with their solves and generates table which allows to easily see solved tasks of all teams. In future it will become html-table and later page on CTFd
