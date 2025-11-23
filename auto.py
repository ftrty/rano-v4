from pynput.mouse import Button, Controller, Listener
import threading, time, random, math

mouse = Controller()
clicking = False

logo = r"""
 ________  ________  ________   ________          ___      ___ ___   ___     
|\   __  \|\   __  \|\   ___  \|\   __  \        |\  \    /  /|\  \ |\  \    
\ \  \|\  \ \  \|\  \ \  \\ \  \ \  \|\  \       \ \  \  /  / | \  \\_\  \   
 \ \   _  _\ \   __  \ \  \\ \  \ \  \\\  \       \ \  \/  / / \ \______  \  
  \ \  \\  \\ \  \ \  \ \  \\ \  \ \  \\\  \       \ \    / /   \|_____|\  \ 
   \ \__\\ _\\ \__\ \__\ \__\\ \__\ \_______\       \ \__/ /           \ \__\
    \|__|\|__|\|__|\|__|\|__| \|__|\|_______|        \|__|/             \|__|
                                                                                                                                                          
                                                                             
"""

print(logo)
print("      Hold SIDE MOUSE BUTTON ")


def click_loop():
    global clicking

    t = 0

    while True:
        if clicking:

            # Main CPS target (14–17)
            base_cps = random.uniform(14, 17)

            # Layer 1: smooth sinusoidal drift
            wave = math.sin(t * random.uniform(2.5, 6.0)) * random.uniform(-4, 4)

            # Layer 2: jitter
            jitter = random.uniform(-5, 5)

            # Layer 3: unstable flicks
            spike = random.uniform(-12, 12) if random.random() < 0.15 else 0

            # Combined CPS
            cps = max(5, base_cps + wave + jitter + spike)

            # Convert to delay
            delay = 1 / cps

            # Layer 4: micro timing noise
            delay += random.uniform(-0.006, 0.010)

            # Layer 5: occasional slow hand adjustment
            if random.random() < 0.025:
                time.sleep(random.uniform(0.03, 0.09))

            # Layer 6: burst mode (super fast waving)
            if random.random() < 0.03:
                for _ in range(random.randint(2, 6)):
                    mouse.click(Button.left)
                    time.sleep(random.uniform(0.001, 0.009))

            # Layer 7: random click suppression
            if random.random() < 0.04:
                time.sleep(delay)
                t += 0.02
                continue

            # Actual click
            mouse.click(Button.left)
            time.sleep(max(0.001, delay))

            # Time progression
            t += random.uniform(0.01, 0.04)

        else:
            time.sleep(0.01)
            t = 0  # reset waves when not clicking


def on_click(x, y, button, pressed):
    global clicking
    if button == Button.x1:
        clicking = pressed


threading.Thread(target=click_loop, daemon=True).start()

with Listener(on_click=on_click) as listener:
    listener.join()
