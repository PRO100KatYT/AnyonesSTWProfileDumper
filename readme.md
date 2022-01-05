# Anyone's Fortnite Save the World Profile Dumper

This program allows you to dump anyone's Fortnite Save the World Profiles.

---
### Changelog:
What's new in the 1.1.0 update:
- The program's performance is significantly better.
- Added an option to use the config setup or use the default config values.
- If the provided username doesn't exist, the program will ask again for a new one.
- Changed the file size info to show an additional tenth of the size.
- Fixed an issue with files paths on mobile devices.
- Tweaked the program's code a little bit.
---

### How to use it?

- After starting the AnyonesSTWProfileDumper.py for the first time (or after deleting the config.ini file) you will be asked if you want to start the config setup process or use the default config values. If you want to start the setup, type 1, if no, type 2.

- Next, you will be asked if you are logged into your Epic account in your browser. If yes, type 1, if no, type 2.

- After you'll press ENTER, an Epic Games website will open. From there, login if you are not already logged into your Epic account.

- Then a page should open with content similar to this:

```json
{"redirectUrl":"https://localhost/launcher/authorized?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
```
or this:
```json
{"redirectUrl":"com.epicgames.fortnite://fnauth/?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
```

- Copy the code (e.g. 930884289b5852842271e9027376a527), paste it into the program and press enter.

- If all went well, the program will say it has generated the auth.json file successfully.

- Now you will be asked to insert the epic displayname of the account whose Save the World profiles you want the program to save.

- After that it should start to dump the profiles.

- Congratulations, you just dumped someone's Fortnite Save the World profiles!