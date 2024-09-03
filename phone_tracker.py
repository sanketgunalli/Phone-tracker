import tkinter
from colorama import Style
from numpy import insert
import tkintermapview
import phonenumbers
import opencage

from key import key

from phonenumbers import geocoder
from phonenumbers import carrier

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from opencage.geocoder import OpenCageGeocode

root = tkinter.Tk()
root.geometry("500x500")

label1 = Label(text="Phone Number Tracker")
label1.pack()

def clear_placeholder(event):
    if number.get("1.0", END).strip() == "Enter phone number here":
        number.delete("1.0", END)

def getResult():
    num = number.get("1.0", END).strip()
    if not num:
        messagebox.showerror("Error", "Number box is empty or input is not a number!")
        return
    
    try:
        num1 = phonenumbers.parse(num)
    except:
        messagebox.showerror("Error", "Invalid phone number format!")
        return
    
    location = geocoder.description_for_number(num1, "en")
    service_provider = carrier.name_for_number(num1, "en")
    
    ocg = OpenCageGeocode(key)
    query = str(location)
    results = ocg.geocode(query)
    
    lat = results[0]['geometry']['lat']
    lng = results[0]['geometry']['lng']
    
    my_label = LabelFrame(root)
    my_label.pack(pady=20)
    
    map_widget = tkintermapview.TkinterMapView(my_label, width=450, height=450, corner_radius=0)
    map_widget.set_position(lat, lng)
    map_widget.set_marker(lat, lng, text="Phone Location")
    map_widget.set_zoom(10)
    map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    map_widget.pack()
    
    adr = tkintermapview.convert_coordinates_to_address(lat, lng)
    
    result.insert(END, "The country of this number is: " + location)
    result.insert(END, "\nThe sim card of this number is: " + service_provider)
    
    result.insert(END, "\nLatitude is: " + str(lat))
    result.insert(END, "\nLongitude is: " + str(lng))
    
    result.insert(END, "\nStreet Address is: " + adr.street)
    result.insert(END, "\nCity Address is: " + adr.city)
    result.insert(END, "\nPostal Code is: " + adr.postal)

number = Text(height=1)
number.pack()

# Add default text to the input box
number.insert("1.0", "Enter phone number here")

# Bind the focus event to clear the placeholder text
number.bind("<FocusIn>", clear_placeholder)

style = Style()
style.configure("TButton", font=('calibri', 20, 'bold'), borderwidth='4')
style.map('TButton', foreground=[('active', '!disabled', 'green')],
                     background=[('active', 'black')])

button = Button(text="Search", command=getResult)
button.pack(pady=10, padx=100)

result = Text(height=7)
result.pack()

root.mainloop()
