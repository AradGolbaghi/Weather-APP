import tkinter as tk
from tkinter import messagebox, END
import requests
from PIL import Image, ImageTk
import dotenv
import os

dotenv.load_dotenv()

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

# ========================== FUNCTIONS ========================== #

def _scaled_icon(path, max_w=280, max_h=280):
    img = Image.open(path)
    img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)  # keeps aspect ratio
    return ImageTk.PhotoImage(img)

IMAGES = {}

def cloudy_image():
    IMAGES["cloudy"] = _scaled_icon("./src/cloudy.jpg", 280, 280)
    canvas.delete("all")
    canvas.create_image(200, 200, image=IMAGES["cloudy"], anchor="center")

def sunny_image():
    IMAGES["sunny"] = _scaled_icon("./src/sunny.jpg", 280, 280)
    canvas.delete("all")
    canvas.create_image(200, 200, image=IMAGES["sunny"], anchor="center")

def windy_image():
    IMAGES["windy"] = _scaled_icon("./src/windy.png", 280, 280)
    canvas.delete("all")
    canvas.create_image(200, 200, image=IMAGES["windy"], anchor="center")

def clear_image():
    IMAGES["clear"] = _scaled_icon("./src/cloudy.jpg", 280, 280)
    canvas.delete("all")
    canvas.create_image(200, 200, image=IMAGES["clear"], anchor="center")

def normal_image():
    IMAGES["normal"] = _scaled_icon("./src/normal.png", 280, 280)
    canvas.delete("all")
    canvas.create_image(200, 200, image=IMAGES["normal"], anchor="center")

def pick_image(event=None):
    city = city_entry.get().strip()

    if not city or city == "Please Enter Your City":
        messagebox.showerror(message="Please provide a city name", title="City Name")
        return

    parameter = {"key": WEATHER_API_KEY, "q": city}
    response = requests.get("http://api.weatherapi.com/v1/current.json", params=parameter)
    data = response.json()

    condition = data["current"]["condition"]["text"].lower()

    # --- Condition mapping ---
    if any(word in condition for word in ["clear"]):
        clear_image()
    elif any(word in condition for word in ["sunny"]):
        sunny_image()
    elif any(word in condition for word in ["wind", "breeze", "gust"]):
        windy_image()
    elif any(word in condition for word in ["cloud", "Partly cloudy"]):
        cloudy_image()
    else:
        normal_image()

    day = "Day" if data['current']['is_day'] == 1 else "Night"

    res = (
        f"{data['location']['country']}, {data['location']['region']}\n"
        f"Local Time: {data['location']['localtime']}\n"
        f"lat, lon: {data['location']['lat']}, {data['location']['lon']}\n"
        f"temp: {data['current']['temp_c']}°C, {data['current']['temp_f']}°F\n"
        f"Wind MPH: {data['current']['wind_mph']}\n"
        f"It is {day}"
    )
    result.config(text=res, bg="black", fg="white")

# ========================== UI ========================== #

window = tk.Tk()
window.title("⛅ Weather APP")
window.maxsize(width=600, height=1000)
window.config(bg="black", padx=20, pady=20)

label = tk.Label(text="Weather APP", bg="black", fg="white", pady=20, font=("Arial", 26, "bold"))
label.pack()

city_entry = tk.Entry(width=34, bg="black", fg="white", highlightthickness=0)
city_entry.insert(END, "Please Enter Your City")
city_entry.pack()

check_weather_button = tk.Button(text="Check Weather", width=16, bg="black", fg="white", highlightthickness=0, command=pick_image)
check_weather_button.pack()

canvas = tk.Canvas(window, width=420, height=420, bg="black", highlightthickness=0)
canvas.pack()

result = tk.Label(text="", bg="black", fg="white", pady=20)
result.pack()

window.bind('<Return>', func=pick_image)

window.mainloop()