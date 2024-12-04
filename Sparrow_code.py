# importing all the required libraries
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import json
import tkinter as tk
from tkinter import ttk, PhotoImage
import threading
import time
import pygame
from PIL import Image, ImageTk
 
# creating class constructor to handle the collection of functions
class VirtualAssistant:
   
    # initializing the text to speech engine
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.reminders = []
        self.alarms = []
        self.timers = []
        pygame.mixer.init()
   
    # converting text to speech and repeating it
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
 
    #listening to user input and converting that into text
    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                return text.lower()
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return ""
            except Exception as e:
                print(f"An error occurred: {e}")
                return ""
    # playing the alarm sound        
    def play_alarm_sound(self):
        pygame.mixer.music.load("c:/Users/bharg/Downloads/mixkit-digital-clock-digital-alarm-buzzer-992.wav")
        pygame.mixer.music.play()
   
    # setting the reminder
    def set_reminder(self, task, time):
        self.reminders.append((task, time))
        self.speak(f"Reminder set for {task} at {time}")
 
    # setting an alarm
    def set_alarm(self, alarm_time):
        def check_alarm():
            while True:
                current_time = datetime.datetime.now().strftime("%H:%M")
                if current_time == alarm_time:
                    self.play_alarm_sound()
                    self.speak("Alarm ringing!")
                    break
                time.sleep(10)
 
        self.alarms.append(alarm_time)
        threading.Thread(target=check_alarm).start()
        self.speak(f"Alarm set for {alarm_time}")
 
    # setting a timer
    def set_timer(self, duration):
        def countdown(t):
            while t:
                mins, secs = divmod(t, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                print(timer, end="\r")
                time.sleep(1)
                t -= 1
            self.play_alarm_sound()
            self.speak("Timer finished!")
 
        self.timers.append(time.time() + duration)
        threading.Thread(target=countdown, args=(duration,)).start()
        self.speak(f"Timer set for {duration} seconds")
 
    # getting the weather details using openweather api
    def get_weather(self, city):
        api_key = "6bbec2388e350a4d0873d63c7c0f5582"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = json.loads(response.text)
        if data["cod"] != "404":
            main = data["main"]
            temperature = main["temp"]
            humidity = main["humidity"]
            weather_desc = data["weather"][0]["description"]
            return f"The weather in {city} is {weather_desc}. Temperature is {temperature}°C and humidity is {humidity}%"
        else:
            return "City not found"
 
    # using google for web search to get information
    def search_web(self, query):
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        self.speak(f"I've opened a web search for {query}")
 
    # filtering the input to search the action that needs to be done
    def process_command(self, command):
        if "reminder" in command:
            parts = command.split("reminder for")
            if len(parts) > 1:
                task = parts[1].strip()
                time = datetime.datetime.now().strftime("%H:%M")
                self.set_reminder(task, time)
            else:
                self.speak("Please specify what to set a reminder for.")
        elif "timer" in command:
            parts = command.split("timer for")
            if len(parts) > 1:
                try:
                    duration = int(parts[1].strip().split()[0])
                    self.set_timer(duration)
                except ValueError:
                    self.speak("Please specify a valid duration in seconds.")
            else:
                self.speak("Please specify the duration for the timer.")
        elif "alarm" in command:
            parts = command.split("alarm for")
            if len(parts) > 1:
                time_str = parts[1].strip()
                try:
                    datetime.datetime.strptime(time_str, "%H:%M")
                    self.set_alarm(time_str)
                except ValueError:
                    self.speak("Please provide a valid time in HH:MM format.")
            else:
                self.speak("Please specify the time for the alarm.")
        elif "weather" in command:
            parts = command.split("weather in")
            if len(parts) > 1:
                city = parts[1].strip()
                weather_info = self.get_weather(city)
                self.speak(weather_info)
            else:
                self.speak("Please specify a city for the weather information.")
        elif "search" in command:
            parts = command.split("search for")
            if len(parts) > 1:
                query = parts[1].strip()
                self.search_web(query)
            else:
                self.speak("Please specify what to search for.")
        else:
            self.speak("I'm sorry, I didn't understand that command")
class GUI:
    def __init__(self, assistant):
        # Initialize the GUI with the virtual assistant object
        self.assistant = assistant
        self.root = tk.Tk()
        self.root.title("Virtual Assistant")        
 
        # Load and set a semi-transparent background image
        self.background_image = Image.open("c:/Users/bharg/Downloads/voice1.png").convert("RGBA")
        width, height = self.background_image.size
        alpha = 200
        self.background_image.putalpha(alpha)
 
        # Convert the image for Tkinter compatibility and add it to a canvas
        self.background_image_tk = ImageTk.PhotoImage(self.background_image)
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.place(relwidth=1, relheight=1)
        self.canvas.create_image(0, 0, image=self.background_image_tk, anchor="nw")
 
        # Add a status label at the top of the window
        self.status_label = ttk.Label(self.root, text="Press 'Mic' to start/stop listening", background="lightblue", font=("Helvetica", 12))
        self.status_label.pack(pady=20)
       
        # Add a microphone button with an image to start/stop listening
        self.microphone_photo = PhotoImage(file="c:/Users/bharg/Downloads/imagee.png")
        self.mic_button = ttk.Button(self.root, image=self.microphone_photo, command=self.toggle_listening)
        self.mic_button.pack(pady=10)
       
        # Add an entry field for text commands
        self.command_entry = ttk.Entry(self.root, width=50)
        self.command_entry.insert(0, "Enter command here (e.g. weather, reminder)")
        self.command_entry.bind("<FocusIn>", self.clear_placeholder)
        self.command_entry.bind("<FocusOut>", self.add_placeholder)
        self.command_entry.pack(pady=10)
 
        # Add a submit button to process the entered command
        self.submit_button = ttk.Button(self.root, text="Submit", command=self.submit_command, style="TButton")
        self.submit_button.pack(pady=10)
 
        # Add a text widget to display output or assistant responses
        self.output_text = tk.Text(self.root, height=10, width=50)
        self.output_text.pack(pady=10)
 
        style = ttk.Style()
        style.configure("TButton",
                        background="lightgreen",
                        foreground="black",
                        font=("Helvetica", 14, "bold"),
                        padding=10)
        style.map("TButton",
                  background=[("active", "lightgreen"), ("pressed", "darkgreen")])
 
    def submit_command(self):
        command = self.command_entry.get()
        if command:
            threading.Thread(target=self.assistant.process_command, args=(command,)).start()
            self.output_text.insert(tk.END, f"You said: {command}\n")
            self.command_entry.delete(0, tk.END)
 
    def toggle_listening(self):
        if not self.assistant.is_listening:
            threading.Thread(target=self.start_listening).start()
        else:
            print("Stopping listening...")
            self.assistant.is_listening = False
 
    def start_listening(self):
        print("Starting listening...")
        self.assistant.is_listening = True
        while self.assistant.is_listening:
            command = self.assistant.listen()
            if command:
                if "stop" in command:
                    break
                else:
                    print(f"Processing command: {command}")
                    self.output_text.insert(tk.END, f"You said: {command}\n")
                    threading.Thread(target=self.assistant.process_command, args=(command,)).start()
 
    def clear_placeholder(self, event):
        if self.command_entry.get() == "Enter command here (e.g. weather, reminder)":
            self.command_entry.delete(0, tk.END)
 
    def add_placeholder(self, event):
        if not self.command_entry.get():
            self.command_entry.insert(0, "Enter command here (e.g. weather, reminder)")
 
    def run(self):
        self.root.mainloop()
 
def main():
    assistant = VirtualAssistant()
    gui = GUI(assistant)
    gui.run()
 
if __name__ == "__main__":
    main()