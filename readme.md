# Anyone's Fortnite Save the World Profile Dumper

This program allows you to dump anyone's Fortnite Save the World Profiles.

---
### Changelog:
What's new in the 1.2.0 update:
- The program is now able to dump the profile0 profile.
  - Since this profile is no longer obtainable from Epic servers, the program recreates it using the profiles it was split to that are obtainable and public (campaign and common_public) plus fixes the survivor portraits and adds maxed out Skill Tree and Research nodes in order to give the profile more functionality.
- Fixed the program displaying the ```the authorization code you supplied was not issued for your client``` error message when device auth was selected.
- If the ```Sorry the authorization code you supplied was not found. It is possible that it was no longer valid.``` error message will pop up, the program will no longer close. It will ask you to input the code again instead.
- Added the ```Found a bug?``` section to the readme.
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

---

### Found a bug?
Feel free to [open an issue](https://github.com/PRO100KatYT/AnyonesSTWProfileDumper/issues/new "Click here if you want to open an issue.") if you encounter any bugs or just have a question.