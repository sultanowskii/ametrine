# ametrine
**ametrine** is a set of tools for managing CTFs hosted on CTFd. Later full guide will be added.

### List of instruments:
- **[auto-registrator](auto_registrator.py)** registrates users, teams and adds users to their teams using admin's account on CTFd platform [leagues.json](example/leagues.json). Checkout [users.csv](example/users.csv) and [teams.csv](example/users.csv) to see the structure of these required files.
- **[telegram-credentials-sender](telegram_credentials_sender.py)** sends CTFd credentials to particiapnts via telegram. Of course, [users.csv](example/users.csv) must contain logins, passwords and telegram handles of users.
- **[tasks-per-team-table-generator](tasks_per_team_generator.py)** gets list of all teams with their solves and generates table which allows to easily see solved tasks of all teams. In future it will become html-table and later page on CTFd
