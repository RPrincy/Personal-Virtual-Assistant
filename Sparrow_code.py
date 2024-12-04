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
 