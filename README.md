# Karmer (short for "KARMa metER")
> is a dynamic online reputation measurement service that evaluates users based
> on the weighted impact of likes and dislikes they receive,
> offering a nuanced view of individual influence and community standing

## Quick start

Create `.env` file and change values

```shell
echo "API_ID=1234567
API_HASH=1234567890abcdefghijklmnopqrstuv
PHONE=+8123456789" > parse-server/.env
```

## TODO
- [x] Connect the **Telethon** library in Python
- [x] Retrieve **reactions** from a Telegram chat
- [ ] Research _"how"_ and _"in what form"_ reactions can be retrieved
- [ ] Implement this **MVP** into a server
- [ ] Create a **Docker image** from the server
- [ ] Set up a Docker **DB** image for collecting reactions
- [ ] Wrap everything in **Docker Compose** for backend and DB integration
- [ ] Develop a backend that provides **analytics on reactions**
- [ ] Integrate the analytics backend with **Telegram**
