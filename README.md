# R2D2 Python Control

This is a hobby project developed using AI with **Google Antigravity**. Its purpose is to help users revive and control old Sphero R2-D2 droids using computer assistance.

This project provides a powerful Python script (`r2.py`) to control the Sphero R2-D2 droid. It allows for precise movement, playing sounds and animations, controlling LEDs, and even a real-time "Stream Mode" for dynamic control.

## Prerequisites

- **Python 3.7+**
- **Bluetooth Low Energy (BLE)** support on your computer.
- **spherov2 library**:
  ```bash
  pip install spherov2
  ```

## Usage

Run the script from the terminal. The script will automatically scan for and connect to the nearest R2-D2 unit.

```bash
python r2.py [arguments]
```

### Available Commands

You can chain multiple commands together. They will be executed in the order they appear.

**Movement:**
- `--move <cm>`: Move forward by the specified distance in centimeters.
- `--move-back <cm>`: Move backward by the specified distance.
- `--turn <degrees>`: Turn the body by the specified degrees (positive = clockwise/right, negative = counter-clockwise/left).
- `--speed <0-255>`: Set the movement speed for subsequent move commands (default: 100).
- `--square <side_cm>`: Drive in a square pattern (turns right).
- `--square-left <side_cm>`: Drive in a square pattern (turns left).
- `--circle <diameter_cm>`: Drive in a circle.

**Head/Dome Control:**
- `--turn-dome <degrees>`: Turn the dome relative to its current position.
- `--lock-dome <degrees>`: Lock the dome to an absolute direction (0-360). It will stay facing that way even if the body turns.
- `--shake-head`: Perform a "no" head shake animation.

**Audio & Animations:**
- `--sound <SOUND_NAME>`: Play a built-in sound (e.g., `R2_HAPPY`, `R2_SAD`, `BB8_LAUGH_1`).
- `--animation <ANIMATION_NAME>`: Play a built-in animation (e.g., `EMOTE_ALARM`, `EMOTE_EXCITED`).
- `--set-volume <0-255>`: Set the speaker volume.

**LEDs:**
- `--front-led <r,g,b>`: Set front LED color (e.g., `255,0,0` for red).
- `--back-led <r,g,b>`: Set back LED color.
- `--holo-projector-led <0-255>`: Set brightness of the holo projector.
- `--logic-display-led <0-255>`: Set brightness of the logic displays.

**Stance:**
- `--stance <bipod|tripod>`: Retract (bipod) or deploy (tripod) the third leg.

### Stream Mode

Stream mode allows you to control R2-D2 in real-time by writing commands to a text file. This is useful for integrating with other software or creating interactive scripts.

```bash
python r2.py --stream r2d2_commands.txt
```

Once running, simply append commands to `r2d2_commands.txt`.

**Python Example:**
You can easily control the droid from another Python script by writing to the file:

```python
import time

def send_command(cmd):
    with open("r2d2_commands.txt", "a") as f:
        f.write(f"{cmd}\n")

# Example sequence
send_command("--sound R2_HAPPY")
time.sleep(2)
send_command("--turn 90")
time.sleep(1)
send_command("--move 20")
```

## Examples

**1. Patrol Pattern:**
Move forward, turn around, and come back.
```bash
python r2.py --move 50 --turn 180 --move 50
```

**2. Happy Dance:**
Play a sound, shake head, and spin.
```bash
python r2.py --sound R2_EXCITED --shake-head --turn 360
```

**3. Stealth Mode:**
Turn off lights and move slowly.
```bash
python r2.py --front-led 0,0,0 --back-led 0,0,0 --speed 50 --move 100
```

## References

For a complete list of available sounds, animations, and detailed command behaviors, please refer to:

- **[Sounds and Animations](SOUNDS_AND_ANIMATIONS.md)**: Full list of all sound effects and animation names.
- **[Command Reference](COMMAND_REFERENCE.md)**: Detailed explanation of every command and its parameters.

## Credits

This project is built using the excellent [spherov2](https://github.com/artificial-intelligence-class/spherov2) library, which provides the reverse-engineered interface for Sphero droids.
