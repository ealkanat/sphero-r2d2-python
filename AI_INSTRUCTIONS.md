# AI Instructions: R2D2 Robot Control via Stream Mode

## Overview
You are controlling a physical R2D2 robot using a text file-based command system. Commands are written to a text file (`r2d2_commands.txt`), and the robot executes them in real-time as they are added.

## Starting Stream Mode
The robot is controlled by running:
```bash
python r2.py --stream r2d2_commands.txt
```
Once started, the robot stays connected and monitors the file continuously.

## How to Send Commands
Append commands to the file using:
```bash
echo "COMMAND" >> r2d2_commands.txt
```

Each line in the file should contain one command or a sequence of related commands.

---

## Available Commands

### Movement Commands
- `--move <distance_cm>` - Move forward in current heading direction
- `--move-back <distance_cm>` - Move backward in current heading direction
- `--speed <0-255>` - Set movement speed (affects all subsequent movements)

**Example:**
```bash
echo "--speed 150" >> r2d2_commands.txt
echo "--move 20" >> r2d2_commands.txt
echo "--move-back 10" >> r2d2_commands.txt
```

### Rotation Commands
- `--turn <degrees>` - Turn by degrees (positive = right, negative = left)

**Example:**
```bash
echo "--turn 90" >> r2d2_commands.txt
echo "--turn -45" >> r2d2_commands.txt
```

### Pattern Commands
- `--square <side_cm>` - Drive in a square (clockwise), returns to start orientation
- `--square-left <side_cm>` - Drive in a square (counterclockwise), returns to start orientation
- `--circle <diameter_cm>` - Drive in a circle

**Example:**
```bash
echo "--square 25" >> r2d2_commands.txt
echo "--circle 30" >> r2d2_commands.txt
```

### Dome Control
- `--turn-dome <degrees>` - Turn dome relative to current position (signed)
- `--lock-dome <absolute_degrees>` - Lock dome to point at absolute world direction (0-360)
  - Once locked, dome maintains direction even when body turns
  - 0° = forward/north, 90° = right/east, 180° = back/south, 270° = left/west

**Example:**
```bash
echo "--lock-dome 0" >> r2d2_commands.txt
echo "--turn 90" >> r2d2_commands.txt
# Dome stays pointing at 0° (forward) while body turns
```

### Audio Commands
- `--sound <SOUND_NAME>` - Play a sound effect
- `--set-volume <0-255>` - Set audio volume

**Common Sounds:**
- `R2_EXCITED_1` through `R2_EXCITED_16`
- `R2_HEY_1` through `R2_HEY_12`
- `R2_CHATTY_1` through `R2_CHATTY_62`
- `R2_POSITIVE_1` through `R2_POSITIVE_23`
- `R2_SCREAM`, `R2_LAUGH_1`, `R2_ANNOYED`

**Example:**
```bash
echo "--sound R2_EXCITED_1" >> r2d2_commands.txt
echo "--set-volume 200" >> r2d2_commands.txt
```

### Animation Commands
- `--animation <ANIMATION_NAME>` - Play an animation

**Common Animations:**
- `EMOTE_EXCITED`, `EMOTE_HAPPY`, `EMOTE_ANGRY`, `EMOTE_SAD`
- `EMOTE_SURPRISED`, `EMOTE_LAUGH`, `EMOTE_NO`, `EMOTE_YES`
- `WWM_BOW`, `WWM_SHAKE`, `WWM_SCARED`

**Example:**
```bash
echo "--animation EMOTE_EXCITED" >> r2d2_commands.txt
```

### Physical Actions
- `--shake-head` - Shake head right and left
- `--stance <bipod|tripod>` - Set stance (bipod retracts third leg)

**Example:**
```bash
echo "--shake-head" >> r2d2_commands.txt
echo "--stance bipod" >> r2d2_commands.txt
```

### LED Control
- `--front-led <r,g,b>` - Set front LED color (RGB values 0-255)
- `--back-led <r,g,b>` - Set back LED color
- `--holo-projector-led <0-255>` - Set holo projector brightness
- `--logic-display-led <0-255>` - Set logic display brightness

**Example:**
```bash
echo "--front-led 255,0,0" >> r2d2_commands.txt
echo "--back-led 0,255,0" >> r2d2_commands.txt
echo "--holo-projector-led 255" >> r2d2_commands.txt
echo "--logic-display-led 128" >> r2d2_commands.txt
```

---

## State Management

### Heading State
The robot maintains a **heading state** (0-360 degrees) that persists across commands:
- Starts at 0° (forward)
- `--turn` commands modify this heading
- `--move` and `--move-back` use the current heading
- Heading accumulates: `--turn 90` then `--turn 45` = 135° total

### Dome Lock State
- `--lock-dome` sets an absolute world direction for the dome
- The dome automatically adjusts when the body turns to maintain the lock
- Clear lock by turning dome manually with `--turn-dome`

### Speed State
- `--speed` sets movement speed for all subsequent movements
- Default is 100 (range: 0-255)
- Persists until changed

---

## Command Composition

You can combine multiple commands on one line:
```bash
echo "--speed 200 --move 15 --turn 90 --move 10" >> r2d2_commands.txt
```

Commands execute in the exact order specified.

---

## Best Practices for AI Control

### 1. Navigation Patterns
**Square dance:**
```bash
echo "--lock-dome 0" >> r2d2_commands.txt
echo "--square 20" >> r2d2_commands.txt
# Dome points forward throughout
```

**Explore area:**
```bash
echo "--move 30" >> r2d2_commands.txt
echo "--turn 90" >> r2d2_commands.txt
echo "--move 20" >> r2d2_commands.txt
echo "--turn 90" >> r2d2_commands.txt
```

### 2. Expressive Behaviors
**Excited greeting:**
```bash
echo "--sound R2_EXCITED_1" >> r2d2_commands.txt
echo "--animation EMOTE_EXCITED" >> r2d2_commands.txt
echo "--shake-head" >> r2d2_commands.txt
```

**Scan environment:**
```bash
echo "--lock-dome 0" >> r2d2_commands.txt
echo "--circle 50" >> r2d2_commands.txt
# Dome points forward while body spins
```

### 3. Precision Movement
**Approach target slowly:**
```bash
echo "--speed 50" >> r2d2_commands.txt
echo "--move 10" >> r2d2_commands.txt
echo "--move 5" >> r2d2_commands.txt
echo "--move 2" >> r2d2_commands.txt
```

**Return to start:**
```bash
echo "--turn 180" >> r2d2_commands.txt
echo "--move 50" >> r2d2_commands.txt
echo "--turn 180" >> r2d2_commands.txt
```

### 4. Error Handling
- Invalid commands are logged but don't crash the system
- Robot state persists even if a command fails
- Stream mode continues monitoring the file

### 5. Stopping
To exit stream mode:
```bash
echo "exit" >> r2d2_commands.txt
```
Or press `Ctrl+C` in the terminal running the stream.

---

## Example: Complete Patrol Sequence

```bash
# Lock dome to watch forward
echo "--lock-dome 0" >> r2d2_commands.txt

# Set speed
echo "--speed 150" >> r2d2_commands.txt

# Patrol in a square
echo "--move 30" >> r2d2_commands.txt
echo "--sound R2_HEY_1" >> r2d2_commands.txt
echo "--turn 90" >> r2d2_commands.txt

echo "--move 30" >> r2d2_commands.txt
echo "--turn 90" >> r2d2_commands.txt

echo "--move 30" >> r2d2_commands.txt
echo "--turn 90" >> r2d2_commands.txt

echo "--move 30" >> r2d2_commands.txt
echo "--turn 90" >> r2d2_commands.txt

# Celebrate
echo "--animation EMOTE_EXCITED" >> r2d2_commands.txt
echo "--sound R2_EXCITED_1" >> r2d2_commands.txt
```

---

## Quick Reference Card

| Category | Command | Example |
|----------|---------|---------|
| **Move** | `--move <cm>` | `--move 20` |
| **Move Back** | `--move-back <cm>` | `--move-back 10` |
| **Turn** | `--turn <deg>` | `--turn 90` |
| **Speed** | `--speed <0-255>` | `--speed 200` |
| **Square** | `--square <cm>` | `--square 25` |
| **Circle** | `--circle <cm>` | `--circle 30` |
| **Dome Lock** | `--lock-dome <deg>` | `--lock-dome 45` |
| **Sound** | `--sound <NAME>` | `--sound R2_EXCITED_1` |
| **Animation** | `--animation <NAME>` | `--animation EMOTE_HAPPY` |
| **LED** | `--front-led <r,g,b>` | `--front-led 255,0,0` |

---

## Notes for AI Assistants

1. **Distance is measured in centimeters** - typical room navigation uses 20-100cm movements
2. **Heading accumulates** - keep track mentally or use absolute patterns like `--square`
3. **Dome lock is powerful** - use it to maintain "looking" direction during complex maneuvers
4. **Speed affects accuracy** - slower speeds (50-100) are more accurate for short distances
5. **Commands execute sequentially** - robot completes each command before the next
6. **Stream mode is non-blocking** - you can add commands while previous ones execute
7. **Robot has momentum** - rapid direction changes may be less accurate

## Full Command Reference
For a complete list of sounds and animations, run:
```bash
python r2.py --help
```
