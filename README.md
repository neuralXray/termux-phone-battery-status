# Phone Battery Status

Telegram bot for phone battery status. It sends a message when the phone is suddenly unplugged while charging. It sends a warning message if the phone remains unplugged for 10 minutes. It sends a confirmation message when the phone is plugged in again.


## Installation commands

```
git clone https://github.com/neuralXray/phone-battery-status.git
cd phone-battery-status
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Edit the `phone_battery_status.conf` file to add the Telegram bot token on the first line and the Telegram user receiver ID on the second line.


## Start the bot in Termux

```
python phone_battery_status.py
```


## Telegram commands

* `help`: List available commands.

* `status`: Whether the phone is plugged in (charging) or not.

* `battery`: The current battery percentage.


## Support the developer

* Bitcoin: 1GDDJ7sLcBwFXg978qzCdsxrC8Ci9Dbgfa

* Monero: 4BGpHVqEWBtNwhwE2FECSt6vpuDMbLzrCFSUJHX5sPG44bZQYK1vN8MM97CbyC9ejSHpJANpJSLpxVrLQ2XT6xEXR8pzdCT

* Litecoin: LdaMXYuayfQmEQ4wsgR2Tp6om78caG3TEG

* Ethereum: 0x7862D03Dd9Dd5F1ebc020B2AaBd107d872ebA58E

* PayPal: paypal.me/neuralXray

