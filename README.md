# StealFromBill - stealer

# ATTENTION!The author does not encourage the theft of personal data, passwords and cookies using this script.This script is written for educational purposes for pentesting.

This script is a stealer designed to extract passwords, cookies from browsers, Discord tokens, FileZilla data, and a screenshot of the desktop. Data about the script’s operation is saved in log.txt, and temporary files are deleted. After the script packs all the data from the computer into a ZIP archive, it will automatically send the file to an email address (see file "usage"  for email configuration)

The script will start collecting data from the computer:
1)Passwords and cookies from browsers (Chrome, Yandex, Chromium, Amigo, Opera).
2)The Discord token.
3)FileZilla data.
4)Screenshot of the screen.
5)Data Saving: The collected data will be saved to text files in the Stalker Data folder in the user's APPDATA directory.
6)Creating a ZIP archive: All text files and screenshots will be packaged in a ZIP archive LOG.zip to the same folder.
7)Sending the archive by email: The ZIP archive will be sent by email to the address specified in the settings.
8)Logging: Messages about the work process will be recorded in log.txt .
9)Cleaning temporary files: Temporary copies of database files will be deleted.
