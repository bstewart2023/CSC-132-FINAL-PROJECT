from tkinter import *

HEIGHT = 500
WIDTH = 800

root = Tk()
root.title("Parking Detection")

canvas = Canvas(root, bg = 'black', height=HEIGHT, width=WIDTH)
canvas.pack(expand = YES, fill = BOTH)

background_image = PhotoImage(file='IMAGES/Background.png')
background_label = Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = Frame(root, bg='black')
frame.place(relx=0.655, rely=0.03, relwidth=0.33, relheight=0.6)

button = Button(frame, text="Check Availability", font=40)# command=lambda: 
button.place(relx=0, relheight=.2, relwidth=1)

button = Button(frame, text="Update", font=40)# command=lambda: 
button.place(relx=0, rely=0.25, relheight=.2, relwidth=1)

button = Button(frame, text="Switch View", font=40)# command=lambda: 
button.place(relx=0, rely=0.5, relheight=.2, relwidth=1)

button = Button(frame, text="Reserve Space", font=40)# command=lambda: 
button.place(relx=0, rely=0.75, relheight=.2, relwidth=1)

parking_frame = Frame(root, bg='gray', bd=5)
parking_frame.place(relx=0.02, rely=0.075, relwidth=0.62, relheight=0.70)

output_frame = Frame(root, bg='white', bd=5)
output_frame.place(relx=0.02, rely=0.8, relwidth=0.62, relheight=0.17)

title_frame = Frame(root, bg='gray', bd=2)
title_frame.place(relx=0.02, rely=0.03, relwidth=0.62, relheight=0.04)

label = Label(title_frame, text = "Current View", bg = 'white')
label.place(relwidth=1, relheight=1)

ZeroLot = PhotoImage(file='IMAGES/ZeroLot.png')
ZeroLot_label = Label(parking_frame, image=ZeroLot)
ZeroLot_label.place(relwidth = 1, relheight = 1)
##ZeroLot_label.pack(fill = BOTH)

root.mainloop()
