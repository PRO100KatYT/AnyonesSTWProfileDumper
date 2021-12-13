print("Anyone's Fortnite StW Profile Dumper v1.0.0 by PRO100KatYT\n")
try:
    import json
    import requests
    import os
    from configparser import ConfigParser
    from datetime import datetime
    import webbrowser
except Exception as emsg:
    input(f"ERROR: {emsg}. To run this program, please install it.\n\nPress ENTER to close the program.")
    exit()

# Links that will be used in the later part of code.
class links:
    loginLink1 = "https://www.epicgames.com/id/api/redirect?clientId={0}&responseType=code"
    loginLink2 = "https://www.epicgames.com/id/logout?redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fid%2Flogin%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253D{0}%2526responseType%253Dcode"
    getOAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/{0}"
    getDeviceAuth = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{0}/deviceAuth"
    getAccountIdByName = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/displayName/{0}"
    profileRequest = "https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{0}/public/QueryPublicProfile?profileId={1}"

# Creating and/or reading the config.ini file.
config = ConfigParser()
configPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "config.ini")
if not os.path.exists(configPath):
    print("Starting to generate the config.ini file.\n")
    configFile = open(configPath, "a")
    configFile.write("[Anyones_Fortnite_STW_Profile_Dumper_Config]\n\n# Which authentication method do you want the program to use? Valid vaules: token, device.\n# Token auth metod generates a refresh token to log in. After 23 days of not using this program this token will expire and you will have to regenerate the auth file.\n# Device auth method generates authorization credentials that don't have an expiration date, but can after some time cause epic to ask you to change your password.\nAuthorization_Type = token\n\n# Do you want the program to dump the campaign profile? Valid vaules: true, false.\nDump_Campaign = true\n\n# Do you want the program to dump the common_public profile? Valid vaules: true, false.\nDump_Common_Public = true\n\n# Do not change anything below.\n[Config_Version]\nVersion = AFSTWPDC_1.0.0")
    configFile.close()
    print("The config.ini file was generated successfully.\n")
boolOptions = ["Dump_Campaign", "Dump_Common_Public"]
try:
    getConfigIni = config.read(configPath)
    authType = config['Anyones_Fortnite_STW_Profile_Dumper_Config']['Authorization_Type'].lower()
    configVer = config['Config_Version']['Version']
    for key in boolOptions:
        config['Anyones_Fortnite_STW_Profile_Dumper_Config'][f'{key}']
except:
    input("ERROR: The program is unable to read the config.ini file. Delete the config.ini file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")
    exit()
if not (configVer == "AFSTWPDC_1.0.0"):
    input("ERROR: The config file is outdated. Delete the config.ini file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")
    exit()
profilesList = []
trueValues = 0
for key in boolOptions:
    keyValue = config['Anyones_Fortnite_STW_Profile_Dumper_Config'][f'{key}'].lower()
    if not (keyValue in ("true", "false")):
        input(f"ERROR: You set the wrong {key} value in config.ini ({keyValue}). Valid values: true, false. Change it and run this program again.\n\nPress ENTER to close the program.\n")
        exit()
    if keyValue == "true":
        trueValues += 1
        if key in boolOptions[:5]: profilesList.append((key.split("Dump_")[1]).lower())
if not (authType in ("token", "device")):
    input(f"ERROR: You set the wrong \"Authorization_Type\" value in config.ini ({authType}). Valid values: token, device. Change it and run this program again.\n\nPress ENTER to close the program.\n")
    exit()

# Creating and/or reading the auth.json file.
authPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "auth.json")
if not os.path.exists(authPath):
    isLoggedIn = input("Starting to generate the auth.json file.\n\nAre you logged into your Epic account that you would like the program to use in your browser?\nType 1 if yes and press ENTER.\nType 2 if no and press ENTER.\n")
    while True:
        if (isLoggedIn == "1" or isLoggedIn == "2"): break
        else: isLoggedIn = input("\nYou priovided a wrong value. Please input it again.\n")
    input("\nThe program is going to open an Epic Games webpage.\nTo continue, press ENTER.\n")
    if isLoggedIn == "1": loginLink = links.loginLink1
    else: loginLink = links.loginLink2
    if authType == "token":
        loginLink = loginLink.format("34a02cf8f4414e29b15921876da36f9a")
        webbrowser.open_new_tab(loginLink)
        print(f"If the program didnt open it, copy this link to your browser: {(loginLink)}\n")
        reqToken = requests.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "authorization_code", "code": input("Insert the auth code:\n")})
        reqTokenText = json.loads(reqToken.text)
        if "errorMessage" in reqTokenText:
            input(f"\nERROR: {reqTokenText['errorMessage']}\n\nPress ENTER to close the program.\n") 
            exit()
        else:
            refreshToken = reqTokenText["refresh_token"]
            accountId = reqTokenText["account_id"]
            expirationDate = reqTokenText["refresh_expires_at"]
            jsontosave = ("{\"WARNING\": \"Don't show anyone the contents of this file, because it contains information with which the program logs into the account.\", \"authType\":\"token\", \"refreshToken\":\"{refresh_token}\", \"accountId\":\"{account_id}\", \"refresh_expires_at\":\"{refresh_expires_at}\"}")
            firstjsonreplace = jsontosave.replace("{refresh_token}", refreshToken)
            secondjsonreplace = firstjsonreplace.replace("{account_id}", accountId)
            thirdjsonreplace = secondjsonreplace.replace("{refresh_expires_at}", expirationDate)
            json.dump(json.loads(thirdjsonreplace), open(authPath, "w"), indent = 2)
    if authType == "device":
        loginLink = loginLink.format("3446cd72694c4a4485d81b77adbb2141")
        webbrowser.open_new_tab(loginLink)
        print(f"If the program didnt open it, copy this link to your browser: {loginLink}\n")
        reqToken = requests.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "authorization_code", "code": input("Insert the auth code:\n")})
        reqTokenText = json.loads(reqToken.text)
        if "errorMessage" in reqTokenText:
            input(f"\nERROR: {reqTokenText['errorMessage']}\n\nPress ENTER to close the program.\n") 
            exit()
        else:
            accessToken = reqTokenText["access_token"]
            accountId = reqTokenText["account_id"]
        reqDeviceAuth = requests.post(links.getDeviceAuth.format(accountId), headers={"Authorization": f"bearer {accessToken}"}, data={})
        reqDeviceAuthText = json.loads(reqDeviceAuth.text)
        if "errorMessage" in reqDeviceAuthText:
            input(f"\nERROR: {reqDeviceAuthText['errorMessage']}\n\nPress ENTER to close the program.\n") 
            exit()
        else:
            deviceId = reqDeviceAuthText["deviceId"]
            secret = reqDeviceAuthText["secret"]
            jsontosave = ("{\"WARNING\": \"Don't show anyone the contents of this file, because it contains information with which the program logs into the account.\", \"authType\":\"device\",  \"deviceId\":\"{deviceId}\", \"accountId\":\"{account_id}\", \"secret\":\"{secret}\"}")
            firstjsonreplace = jsontosave.replace("{deviceId}", deviceId)
            secondjsonreplace = firstjsonreplace.replace("{account_id}", accountId)
            thirdjsonreplace = secondjsonreplace.replace("{secret}", secret)
            json.dump(json.loads(thirdjsonreplace), open(authPath, "w"), indent = 2)
    print("\nThe auth.json file was generated successfully.\n")
try:
    getAuthJson = json.loads(open(authPath, "r").read())
    if authType == "token":
        if getAuthJson["authType"] == "device":
            input("The authorization type in config is set to token, but the auth.json file contains device auth credentials.\nDelete the auth.json file and run this program again to generate a token one or change authorization type back to device in config.ini.\n\nPress ENTER to close the program.\n")
            exit = 1
        expirationDate = getAuthJson["refresh_expires_at"]
        if expirationDate < datetime.now().isoformat():
            input("The refresh token has expired. Delete the auth.json file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")
            exit = 1
        refreshToken = getAuthJson["refreshToken"]
    if authType == "device":
        if getAuthJson["authType"] == "token":
            input("The authorization type in config is set to device, but the auth.json file contains token auth credentials.\nDelete the auth.json file and run this program again to generate a device one or change authorization type back to token in config.ini.\n\nPress ENTER to close the program.\n")
            exit = 1
        deviceId = getAuthJson["deviceId"]
        secret = getAuthJson["secret"]
    accountId = getAuthJson["accountId"]
except:
    if exit == 1: exit()
    input("ERROR: The program is unable to read the auth.json file. Delete the auth.json file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")
    exit()
if exit == 1: exit()

# Logging in.
if authType == "token":
    reqRefreshToken = requests.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "refresh_token", "refresh_token": refreshToken})
    reqRefreshTokenText = json.loads(reqRefreshToken.text)
    if "errorMessage" in reqRefreshTokenText:
        input(f"ERROR: At least one variable in the auth.json file is no longer valid. Delete the auth.json file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n") 
        exit()
    getAuthFile = open(authPath, "r").read()
    authReplaceToken = getAuthFile.replace(refreshToken, reqRefreshTokenText["refresh_token"])
    authReplaceDate = authReplaceToken.replace(expirationDate, reqRefreshTokenText["refresh_expires_at"])
    authFile = open(authPath, "w")
    authFile.write(authReplaceDate)
    authFile.close()
    accessToken = reqRefreshTokenText["access_token"]
    reqExchange = requests.get(links.getOAuth.format("exchange"), headers={"Authorization": f"bearer {accessToken}"}, data={"grant_type": "authorization_code"})
    reqExchangeText = json.loads(reqExchange.text)
    exchangeCode = reqExchangeText["code"]
    reqToken = requests.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "exchange_code", "exchange_code": exchangeCode, "token_type": "eg1"})
if authType == "device":
    reqToken = requests.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "device_auth", "device_id": deviceId, "account_id": accountId, "secret": secret, "token_type": "eg1"})
reqTokenText = json.loads(reqToken.text)
if "errorMessage" in reqTokenText:
    input(f"ERROR: At least one variable in the auth.json file is no longer valid. Delete the auth.json file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n") 
    exit()
accessToken = reqTokenText['access_token']
displayName = reqTokenText['displayName']
print(f"Logged in as {displayName}.\n")

if trueValues == 0: print(f"You set everything the program can save to false in the config. Why are we still here? Just to suffer?\n")
headers = {"Authorization": f"bearer {accessToken}", "Content-Type": "application/json"}
currentDate = datetime.today().strftime('%Y-%m-%d %H-%M-%S')

# Getting the account id using displayname.
reqGetAccountId = requests.get(links.getAccountIdByName.format(input("Insert the epic displayname of the account whose Save the World profiles you want the program to save:\n")), headers=headers, data="{}")
reqGetAccountIdText = json.loads(reqGetAccountId.text)
if "errorMessage" in reqGetAccountIdText:
    input(f"\nERROR: {reqGetAccountIdText['errorMessage']}\n\nPress ENTER to close the program.\n") 
    exit()
accountId = reqGetAccountIdText['id']
displayName = reqGetAccountIdText['displayName']

# Getting and dumping the profiles.
if trueValues >= 1:
    profilePath = os.path.join(os.path.split(os.path.abspath(__file__))[0], f"Dumped files\\{currentDate}\\{displayName}'s STW Profiles")
    if not os.path.exists(profilePath): os.makedirs(profilePath)
    profilesWord = "profiles"
    haveWord = "have"
    if len(profilesList) == 1:
        profilesWord = "profile"
        haveWord = "has"
    print(f"\nStarting to dump {len(profilesList)} {displayName}'s Save the World {profilesWord}\n")
    profileCount = 0
    for profile in profilesList:
        reqGetProfile = requests.post(links.profileRequest.format(accountId, profile), headers=headers, data="{}")
        reqGetProfileText = json.loads(reqGetProfile.text)
        if "errorMessage" in reqGetProfileText:
            if "because it was not found" in reqGetProfileText['errorMessage']: input(f"ERROR: {displayName} doesn't have access to Save the World or has never played it before.\n\nPress ENTER to close the program.\n")
            else: input(f"ERROR: {reqGetProfileText['errorMessage']}\n\nPress ENTER to close the program.\n") 
            exit()
        profileFilePath = os.path.join(profilePath, f"{profile}.json")
        json.dump(reqGetProfileText['profileChanges'][0]['profile'], open(profileFilePath, "w"), indent = 2)
        fileSize = round(os.path.getsize(profileFilePath)/1024)
        profileCount += 1
        print(f"{profileCount}: Dumped the {profile} profile ({fileSize} KB)")
    print(f"\n{displayName}'s Save the World {profilesWord} {haveWord} been successfully saved in {profilePath}.\n")

input("Press ENTER to close the program.\n")
exit()