version = "1.1.0"
configVersion = "1.0.0"
print(f"Anyone's Fortnite StW Profile Dumper v{version} by PRO100KatYT\n")
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

# Start a new requests session.
session = requests.Session()

# Error with a custom message.
def customError(text):
    input(f"ERROR: {text}\n\nPress ENTER to close the program.\n")
    exit()

# Error for invalid config values.
def configError(key, value, validValues): customError(f"You set the wrong {key} value in config.ini ({value}). Valid values: {validValues}. Please change it and run this program again.")

# Input loop until it's one of the correct values.
def validInput(text, values):
    response = input(f"{text}\n")
    print()
    while True:
        if response in values: break
        response = input("You priovided a wrong value. Please input it again.\n")
        print()
    return response

# Get the text from a request and check for errors.
def requestText(request, bCheckError):
    requestText = json.loads(request.text)
    if ((bCheckError) and ("errorMessage" in requestText)):
        if "because it was not found" in requestText['errorMessage']: customError(f"{displayName} doesn't have access to Save the World or has never played it before.")
        else: customError(requestText['errorMessage'])
    return requestText

# Send token request.
def reqToken(loginLink):
    webbrowser.open_new_tab(loginLink)
    print(f"If the program didnt open it, copy this link to your browser: {(loginLink)}\n")
    reqTokenText = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "authorization_code", "code": input("Insert the auth code:\n")}))
    return reqTokenText

# Round the file size.
def roundSize(filePathToSave):
    fileSize = round(os.path.getsize(filePathToSave)/1024, 1)
    if str(fileSize).endswith(".0"): fileSize = round(fileSize)
    return fileSize

# Create and/or read the config.ini file.
config = ConfigParser()
configPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "config.ini")
if not os.path.exists(configPath):
    print("Starting to generate the config.ini file.\n")
    bStartSetup = validInput("Type 1 if you want to start the config setup and press ENTER.\nType 2 if you want to use the default config values and press ENTER.", ["1", "2"])
    if bStartSetup == "1":
        iAuthorization_Type = validInput("Which authentication method do you want the program to use?\nToken auth metod generates a refresh token to log in. After 23 days of not using this program this token will expire and you will have to regenerate the auth file.\nDevice auth method generates authorization credentials that don't have an expiration date, but can after some time cause epic to ask you to change your password.\nValid vaules: token, device.", ["token", "device"])
        iDump_Campaign = validInput("Do you want the program to dump the campaign profile?\nValid vaules: true, false.", ["true", "false"])
        iDump_Common_Public = validInput("Do you want the program to dump the common_public profile?\nValid vaules: true, false.", ["true", "false"])
    else: iAuthorization_Type, iDump_Campaign, iDump_Common_Public = ["token", "true", "true"]
    with open(configPath, "w") as configFile: configFile.write(f"[Anyones_Fortnite_STW_Profile_Dumper_Config]\n\n# Which authentication method do you want the program to use?\n# Token auth metod generates a refresh token to log in. After 23 days of not using this program this token will expire and you will have to regenerate the auth file.\n# Device auth method generates authorization credentials that don't have an expiration date, but can after some time cause epic to ask you to change your password.\n# Valid vaules: token, device.\nAuthorization_Type = {iAuthorization_Type}\n\n# Do you want the program to dump the campaign profile?\n# Valid vaules: true, false.\nDump_Campaign = {iDump_Campaign}\n\n# Do you want the program to dump the common_public profile?\n# Valid vaules: true, false.\nDump_Common_Public = {iDump_Common_Public}\n\n# Do not change anything below.\n[Config_Version]\nVersion = AFSTWPDC_{configVersion}")
    print("The config.ini file was generated successfully.\n")
boolOptions = ["Dump_Campaign", "Dump_Common_Public"]
try:
    config.read(configPath)
    configVer, authType, bDumpCampaign, bDumpCommonPublic = [config['Config_Version']['Version'], config['Anyones_Fortnite_STW_Profile_Dumper_Config']['Authorization_Type'].lower(), config['Anyones_Fortnite_STW_Profile_Dumper_Config']['Dump_Campaign'].lower(), config['Anyones_Fortnite_STW_Profile_Dumper_Config']['Dump_Common_Public'].lower()]
except: customError("The program is unable to read the config.ini file. Delete the config.ini file and run this program again to generate a new one.\n\nPress ENTER to close the program.\n")
checkValuesJson, profilesList = [{"Authorization_Type": {"value": authType, "validValues": ["token", "device"]}, "Dump_Campaign": {"value": bDumpCampaign, "validValues": ["true", "false"]}, "Dump_Common_Public": {"value": bDumpCommonPublic, "validValues": ["true", "false"]}}, {"Dump_Campaign": "campaign", "Dump_Common_Public": "common_public"}]
for option in checkValuesJson:
    if checkValuesJson[option]['value'] == "false": profilesList.pop(option)
    if not (checkValuesJson[option]['value'] in checkValuesJson[option]['validValues']): configError(option, checkValuesJson[option]['value'], checkValuesJson[option]['validValues'])
if not (configVer == f"AFSTWPDC_{configVersion}"): customError("The config file is outdated. Delete the config.ini file and run this program again to generate a new one.")

# Create and/or read the auth.json file.
authPath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "auth.json")
if not os.path.exists(authPath):
    isLoggedIn = validInput("Starting to generate the auth.json file.\n\nAre you logged into your Epic account that you would like the program to use in your browser?\nType 1 if yes and press ENTER.\nType 2 if no and press ENTER.\n", ["1", "2"])
    input("The program is going to open an Epic Games webpage.\nTo continue, press ENTER.\n")
    if isLoggedIn == "1": loginLink = links.loginLink1
    else: loginLink = links.loginLink2
    if authType == "token":
        reqToken = reqToken(loginLink.format("34a02cf8f4414e29b15921876da36f9a"))
        refreshToken, accountId, expirationDate = [reqToken["refresh_token"], reqToken["account_id"], reqToken["refresh_expires_at"]]
        with open(authPath, "w") as authFile: json.dump({"WARNING": "Don't show anyone the contents of this file, because it contains information with which the program logs into the account.", "authType": "token", "refreshToken": refreshToken, "accountId": accountId, "refresh_expires_at": expirationDate}, authFile, indent = 2)
    else:
        reqToken = reqToken(loginLink.format("3446cd72694c4a4485d81b77adbb2141"))
        accessToken, accountId = [reqToken["access_token"], reqToken["account_id"]]
        reqDeviceAuth = requestText(session.post(links.getDeviceAuth.format(accountId), headers={"Authorization": f"bearer {accessToken}"}, data={}), True)
        deviceId, secret = [reqDeviceAuth["deviceId"], reqDeviceAuth["secret"]]
        with open(authPath, "w") as authFile: json.dump({"WARNING": "Don't show anyone the contents of this file, because it contains information with which the program logs into the account.", "authType": "device",  "deviceId": deviceId, "accountId": accountId, "secret": secret}, authFile, indent = 2)
    print("\nThe auth.json file was generated successfully.\n")
try:
    getAuthJson = json.loads(open(authPath, "r").read())
    if authType == "token":
        expirationDate, refreshToken = [getAuthJson["refresh_expires_at"], getAuthJson["refreshToken"]]
        if getAuthJson["authType"] == "device": customError("The authorization type in config is set to token, but the auth.json file contains device auth credentials.\nDelete the auth.json file and run this program again to generate a token one or change authorization type back to device in config.ini.")
        if expirationDate < datetime.now().isoformat(): customError("The refresh token has expired. Delete the auth.json file and run this program again to generate a new one.")
    if authType == "device":
        deviceId, secret = [getAuthJson["deviceId"], getAuthJson["secret"]]
        if getAuthJson["authType"] == "token": customError("The authorization type in config is set to device, but the auth.json file contains token auth credentials.\nDelete the auth.json file and run this program again to generate a device one or change authorization type back to token in config.ini.")
    accountId = getAuthJson["accountId"]
except:
    customError("The program is unable to read the auth.json file. Delete the auth.json file and run this program again to generate a new one.")

# Log in.
if authType == "token":
    reqRefreshToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y="}, data={"grant_type": "refresh_token", "refresh_token": refreshToken}), True)
    with open(authPath, "r") as getAuthFile: authFile = json.loads(getAuthFile.read())
    authFile['refreshToken'], authFile['refresh_expires_at'] = [reqRefreshToken["refresh_token"], reqRefreshToken["refresh_expires_at"]]
    with open(authPath, "w") as getAuthFile: json.dump(authFile, getAuthFile, indent = 2)
    reqExchange = requestText(session.get(links.getOAuth.format("exchange"), headers={"Authorization": f"bearer {reqRefreshToken['access_token']}"}, data={"grant_type": "authorization_code"}), True)
    reqToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "exchange_code", "exchange_code": reqExchange["code"], "token_type": "eg1"}), True)
if authType == "device": reqToken = requestText(session.post(links.getOAuth.format("token"), headers={"Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="}, data={"grant_type": "device_auth", "device_id": deviceId, "account_id": accountId, "secret": secret, "token_type": "eg1"}), True)
accessToken, displayName = [reqToken['access_token'], reqToken['displayName']]
print(f"Logged in as {displayName}.\n")

if len(profilesList) == 0: print(f"You set everything the program can save to false in the config. Why are we still here? Just to suffer?\n")
headers = {"Authorization": f"bearer {accessToken}", "Content-Type": "application/json"}

if len(profilesList) >= 1:

    # Get the account id using displayname.
    while True:
        reqGetAccountId = requestText(session.get(links.getAccountIdByName.format(input("Insert the epic displayname of the account whose Save the World profiles you'd want the program to save:\n")), headers=headers, data="{}"), False)
        if not ("errorMessage" in reqGetAccountId): break
        else: print(f"ERROR: {reqGetAccountId['errorMessage']}. Please try again with a different username.\n")
    accountId, displayName = [reqGetAccountId['id'], reqGetAccountId['displayName']]

    currentDate = datetime.today().strftime('%Y-%m-%d %H-%M-%S')
    profilePath = os.path.join(os.path.split(os.path.abspath(__file__))[0], "Dumped files")
    profilePath = os.path.join(profilePath, f"{displayName}'s STW Profiles")
    profilePath = os.path.join(profilePath, currentDate)
    if not os.path.exists(profilePath): os.makedirs(profilePath)

    # Get and dump the profiles.
    profilesWord, haveWord = ["profiles", "have"]
    if len(profilesList) == 1: profilesWord, haveWord = ["profile", "has"]
    print(f"\nDumping {len(profilesList)} {displayName}'s Save the World {profilesWord}\n")
    profileCount = 0
    for profile in profilesList:
        profile = profilesList[profile]
        reqGetProfile = requestText(session.post(links.profileRequest.format(accountId, profile), headers=headers, data="{}"), True)
        profileFilePath = os.path.join(profilePath, f"{profile}.json")
        with open(profileFilePath, "w") as profileFile: json.dump(reqGetProfile['profileChanges'][0]['profile'], profileFile, indent = 2)
        fileSize = roundSize(profileFilePath)
        profileCount += 1
        print(f"{profileCount}: Dumped the {profile} profile ({fileSize} KB)")
    print(f"\n{displayName}'s Save the World {profilesWord} {haveWord} been successfully saved in {profilePath}.\n")

input("Press ENTER to close the program.\n")
exit()