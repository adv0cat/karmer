# Karmer (short for "KARMa metER")
> is a dynamic online reputation measurement service that evaluates users based
> on the weighted impact of likes and dislikes they receive,
> offering a nuanced view of individual influence and community standing

## Quick start

Create `.env` file and change values

```shell
echo "# Telegram MTProto
API_ID=1234567
API_HASH=1234567890abcdefghijklmnopqrstuv
PHONE=+8123456789
# optional
PASSWORD=123qwerty

# Postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=mydb
POSTGRES_USER=my-user
POSTGRES_PASSWORD=my-password
" > parse-server/.env
```

## TODO
- [x] Connect the **Telethon** library in Python
- [x] Retrieve **reactions** from a Telegram chat
- [x] Research _"how"_ and _"in what form"_ reactions can be retrieved
- [x] Set up a Docker **DB** image for collecting reactions
- [ ] Implement this **MVP** into a server
- [ ] Create a **Docker image** from the server
- [ ] Wrap everything in **Docker Compose** for backend and DB integration
- [ ] Develop a backend that provides **analytics on reactions**
- [ ] Integrate the analytics backend with **Telegram**
