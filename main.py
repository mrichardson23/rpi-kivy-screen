import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

import RPi.GPIO as GPIO
from time import sleep

# Set up GPIO:
beepPin = 17
ledPin = 27
buttonPin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(beepPin, GPIO.OUT)
GPIO.output(beepPin, GPIO.LOW)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.LOW)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def my_press_callback(obj):
	print("Button pressed,", obj.text)
	if obj.text == 'BEEP!':
		buzzer_on(.1)
	if obj.text == 'LED':
		if obj.state == "down":
			print ("button on")
			GPIO.output(ledPin, GPIO.HIGH)
		else:
			print ("button off")
			GPIO.output(ledPin, GPIO.LOW)

def buzzer_on(time):
	GPIO.output(beepPin, GPIO.HIGH)
	Clock.schedule_once(buzzer_off, time)

def buzzer_off(dt):
	GPIO.output(beepPin, GPIO.LOW)

class InputButton(Button):
	def update(self, dt):
		if GPIO.input(buttonPin) == True:
			self.state = 'normal'
		else:
			self.state = 'down'

class MyApp(App):

	def build(self):
		# Set up the layout:
		layout = GridLayout(cols=4, spacing=30, padding=30, row_default_height=150)

		# Make the background gray:
		with layout.canvas.before:
			Color(.2,.2,.2,1)
			self.rect = Rectangle(size=(800,600), pos=layout.pos)

		# Establish the UI elements (and bind them to events, if necessary):
		inputDisplay = InputButton(text="Input")
		Clock.schedule_interval(inputDisplay.update, 1.0/10.0)
		outputControl = ToggleButton(text="LED")
		outputControl.bind(on_press=my_press_callback)
		beepButton = Button(text="BEEP!")
		beepButton.bind(on_press=my_press_callback)
		wimg = Image(source='logo.png')

		# Add the UI elements to the layout:
		layout.add_widget(wimg)
		layout.add_widget(inputDisplay)
		layout.add_widget(outputControl)
		layout.add_widget(beepButton)

		return layout

if __name__ == '__main__':
	MyApp().run()
