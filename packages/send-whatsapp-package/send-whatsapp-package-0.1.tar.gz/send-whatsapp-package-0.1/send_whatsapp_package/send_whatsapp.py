# send_whatsapp_package/send_whatsapp.py
import pyautogui as pg
import time
import webbrowser as web

def send_whatsapp_instant_message(phone_number, message, no_of_times=1):
    try:
        web.open(f"https://web.whatsapp.com/send?phone={phone_number}")
        time.sleep(5)

        pg.click(pg.size().width / 2, pg.size().height / 2)

        time.sleep(2)

        for i in range(no_of_times):
            pg.typewrite(message)
            time.sleep(1)
            pg.press("enter")

        print("Message sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
