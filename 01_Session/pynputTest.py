from pynput import keyboard

flagStatus = True

def on_press(key):
  global flagStatus
  print(f"Pressed: {key}")
  if key == keyboard.Key.esc or (key.char == 'q'):
    flagStatus = False

listener = keyboard.Listener(on_press=on_press)
listener.start()

try:
  while flagStatus:
    pass
except KeyboardInterrupt:
  listener.stop()