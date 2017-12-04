import urllib.request
import threading
import pyautogui

def server_time():

    f = urllib.request.urlopen("http://" + url)

    my_data = f.info()["Date"]
    
    hour = int(my_data[-12:-10]) + 9
    minute = int(my_data[-9:-7])
    second = int(my_data[-6:-4])
    
    print("\rhttp://" + url + " " + str(hour) + ":" + str(minute) + ":" + str(second) + " ", end='')

    timer = threading.Timer(0.01, server_time)

    if hour == user_hour and minute == user_minute and second == user_second :

        # pyautogui.moveTo(currentMouseX, currentMouseY)
        # pyautogui.click()
        pyautogui.press('enter')

        timer.cancel()

        print("\n작업 종료")

    else:
        
        timer.start()


if __name__ == "__main__":

    url = input("원하는 서버의 주소를 입력해주세요. (example : cafe.daum.net)\n\n주소 : ")

    # print("\n\n클릭할 버튼 위로 마우스를 옮긴 후, Enter 키를 누르세요.\n")
    
    # input()

    # currentMouseX, currentMouseY = pyautogui.position()

    # print(currentMouseX, currentMouseY)

    # print("버튼을 클릭할 시간을 입력합니다. (24시간 단위, example : 20시 30분 2초)")
    user_hour = int(input("\nHour : "))
    user_minute = int(input("Minute : "))
    user_second = int(input("Second : "))

    print()
    
    server_time()
