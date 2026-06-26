# python -m pip install guizero

from guizero import App, Text
app = App(title="Hello world")


welcome_message = Text(app, text="welcome to my app")
# All widget code should go here

app.display()