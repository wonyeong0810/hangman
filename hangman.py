import tkinter as tk
from PIL import ImageTk, Image
import tkinter.font as tkFont
from tkinter import messagebox

import requests

# API 엔드포인트
url = "https://random-word-api.herokuapp.com/word?lang=en"

# GET 요청 보내기
response = requests.get(url)

# 응답 확인
if response.status_code == 200:
    # JSON 형식으로 응답을 가져옴
    data = response.json()
    # 가져온 단어 출력
    word = data[0]
else:
    word = "wony"

hideword = ["_"] * len(word) #정답 길이만큼의 _ 리스트에 저장
inword = ""
man_num = 1
correct = 0

def on_key_press(event):
    global inword, hideword, word, man_num, img,window, correct
    yes = 0
    inword = event.char # 입력 받은 알파벳
    # 정답 단어의 길이 만큼 반복
    for i in range(len(word)):
        if(word[i] == inword): # 만약 입력 받은 알파벳이 정답에 있으면 hideword의 같은 위치에 입력 받은 알파벳 저장 
            hideword[i] = inword
            yes = 1
    # 만약 입력 받은 알파벳이 정답에 없으면 이미지 인덱스값 변경
    if yes == 0:
        man_num+=1

    # 행맨의 이미지를 변경
    img = Image.open(f"img/man{man_num}.png")
    img = img.resize((500,500))
    img = ImageTk.PhotoImage(img)
    imglable.config(image=img)

    # 만약 행맨이 마지막 이미지로 가면 게임 오버
    if man_num == 7:
        messagebox.showinfo("패배", f"행맨이 죽었습니다. 단어는 {word}였습니다.")
        window.destroy()
        return
    
    # tkinter에 지금까지 맞춘 정답 출력
    show.config(text=hideword)

    # str1에 hideword리스트를 문자열로 변환 후 저장
    str1 = ''.join(map(str, hideword))

    # 만약 str1이 정답이랑 같으면 게임 승리
    if str1 == word:
        messagebox.showinfo("승리", "행맨을 살렸습니다")
        window.destroy()
        return

# tkinter 초기 설정
window = tk.Tk()
window.title("hangman")
window.geometry("800x800+500+500")
window.resizable(False, False)
fontStyle = tkFont.Font(family="Lucida Grande", size=40)

# 키를 입력 시 on_key_press 함수 실행
window.bind("<Key>", on_key_press)

# 행맨 띄우기
img = Image.open(f"img/man{man_num}.png")
img = img.resize((500,500))
img = ImageTk.PhotoImage(img)
imglable = tk.Label(window, image=img)
imglable.pack(side="top")

# 자신이 맞춘 단어 띄우기
show = tk.Label(window, text=hideword, font=fontStyle)
show.pack(side="bottom", pady=90)

window.mainloop()