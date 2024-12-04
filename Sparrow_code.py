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