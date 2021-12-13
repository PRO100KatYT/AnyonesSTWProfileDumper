# Anyone's Fortnite Save the World Profile Dumper

This program allows you to dump anyone's Fortnite Save the World Profiles.

---

### How to use it?

- After starting the AnyonesSTWProfileDumper.py for the first time (or after deleting the auth.json file), you will be asked if you are logged into your Epic account in your browser. If yes, type 1, if no, type 2.

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