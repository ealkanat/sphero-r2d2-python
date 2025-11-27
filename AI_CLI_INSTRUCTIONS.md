# AI Instructions: R2D2 Direct Command-Line Control

## Overview
This guide teaches AI assistants how to control the R2D2 robot using direct command-line arguments (non-stream mode). Commands are executed immediately and the robot disconnects after completion.

## Basic Usage Pattern
```bash
python r2.py [ARGUMENTS]
```

All arguments are executed in the **exact order** they are provided on the command line.

---

## Command-Line Arguments Reference

### Movement Arguments
Commands for moving the robot in space.

#### `--move <distance_cm>`
Move forward in the current heading direction.
```bash
python r2.py --move 20
```

#### `--move-back <distance_cm>`
Move backward in the current heading direction.
```bash
python r2.py --move-back 15
```

#### `--speed <0-255>`
Set movement speed for all subsequent movement commands.
- Default: 100
- Range: 0-255
- Affects: `--move`, `--move-back`, `--square`, `--square-left`, `--circle`

```bash
python r2.py --speed 50 --move 10 --speed 200 --move 20
# First move at speed 50, second move at speed 200
```

---

### Rotation Arguments

#### `--turn <degrees>`
Turn the robot by specified degrees (signed).
- **Positive values**: Turn right (clockwise)
- **Negative values**: Turn left (counterclockwise)
- Heading accumulates across multiple turns

```bash
python r2.py --turn 90        # Turn right 90°
python r2.py --turn -45       # Turn left 45°
```

---

### Pattern Arguments

#### `--square <side_cm>`
Drive in a square pattern (clockwise), returns to starting orientation.
- Automatically turns 90° right at each corner
- Completes with final turn to face original direction
- Dome lock compatible

```bash
python r2.py --square 25
```

#### `--square-left <side_cm>`
Drive in a square pattern (counterclockwise).
- Automatically turns 90° left at each corner
- Returns to starting orientation

```bash
python r2.py --square-left 30
```

#### `--circle <diameter_cm>`
Drive in a circular pattern.
- Approximate diameter in centimeters
- Uses spin motion (less precise than other movements)

```bash
python r2.py --circle 40
```

---

### Dome Control Arguments

#### `--turn-dome <degrees>`
Turn the dome relative to its current position (signed).
- **Positive**: Turn dome right
- **Negative**: Turn dome left
- Relative to current dome position

```bash
python r2.py --turn-dome 45
python r2.py --turn-dome -90
```

#### `--lock-dome <absolute_degrees>`
Lock dome to point at an absolute world direction.
- `0°`: Forward/North
- `90°`: Right/East
- `180°`: Back/South
- `270°`: Left/West
- **Dome compensates automatically** when body turns

```bash
python r2.py --lock-dome 0 --turn 90 --move 20
# Dome stays pointing forward while body turns and moves right
```

---

### Audio Arguments

#### `--sound <SOUND_NAME>`
Play a sound effect. Sound names are case-sensitive.

**Common Sounds:**
- Excited: `R2_EXCITED_1` through `R2_EXCITED_16`
- Greetings: `R2_HEY_1` through `R2_HEY_12`
- Chatty: `R2_CHATTY_1` through `R2_CHATTY_62`
- Positive: `R2_POSITIVE_1` through `R2_POSITIVE_23`
- Negative: `R2_NEGATIVE_1` through `R2_NEGATIVE_28`
- Sad: `R2_SAD_1` through `R2_SAD_25`
- Laugh: `R2_LAUGH_1` through `R2_LAUGH_4`
- Special: `R2_SCREAM`, `R2_ANNOYED`, `R2_BURNOUT`, `R2_HEAD_SPIN`

```bash
python r2.py --sound R2_EXCITED_1
python r2.py --sound R2_HEY_5 --move 10
```

#### `--set-volume <0-255>`
Set audio volume level.
```bash
python r2.py --set-volume 200
```

---

### Animation Arguments

#### `--animation <ANIMATION_NAME>`
Play an animation. Animation names are case-sensitive.

**Emote Animations:**
- `EMOTE_EXCITED`, `EMOTE_HAPPY`, `EMOTE_ANGRY`, `EMOTE_SAD`
- `EMOTE_SURPRISED`, `EMOTE_FRUSTRATED`, `EMOTE_SEARCH`
- `EMOTE_LAUGH`, `EMOTE_NO`, `EMOTE_YES`, `EMOTE_ALARM`
- `EMOTE_RETREAT`, `EMOTE_FIERY`, `EMOTE_UNDERSTOOD`

**WWM (With the World's Mind) Animations:**
- `WWM_BOW`, `WWM_SHAKE`, `WWM_SCARED`, `WWM_SURPRISED`
- `WWM_HAPPY`, `WWM_SAD`, `WWM_ANGRY`, `WWM_ANXIOUS`
- `WWM_TAUNTING`, `WWM_YELLING`, `WWM_WHISPER`

```bash
python r2.py --animation EMOTE_EXCITED
python r2.py --animation WWM_BOW --sound R2_POSITIVE_1
```

---

### Physical Action Arguments

#### `--shake-head`
Shake the dome left and right.
```bash
python r2.py --shake-head
```

#### `--stance <bipod|tripod>`
Set the robot's stance.
- **`bipod`**: Retracts third leg (2-legged stance)
- **`tripod`**: Extends third leg (3-legged stance, required for movement)

```bash
python r2.py --stance tripod
python r2.py --stance bipod
```

---

### LED Arguments

#### `--front-led <r,g,b>`
Set front LED color using RGB values (0-255).
```bash
python r2.py --front-led 255,0,0      # Red
python r2.py --front-led 0,255,0      # Green
python r2.py --front-led 255,255,0    # Yellow
```

#### `--back-led <r,g,b>`
Set back LED color using RGB values.
```bash
python r2.py --back-led 0,0,255       # Blue
```

#### `--holo-projector-led <0-255>`
Set holo projector LED intensity.
```bash
python r2.py --holo-projector-led 255 # Max brightness
```

#### `--logic-display-led <0-255>`
Set logic display LED intensity.
```bash
python r2.py --logic-display-led 128  # Half brightness
```

---

## Argument Ordering and State

### Execution Order
Arguments are executed **left to right** in the exact order specified:
```bash
python r2.py --move 10 --turn 90 --move 10
# 1. Move forward 10cm
# 2. Turn right 90°
# 3. Move forward 10cm (now in new direction)
```

### State Persistence
State persists **only within a single command execution**:

1. **Heading State**: Starts at 0°, accumulates with each turn
   ```bash
   python r2.py --turn 90 --turn 45 --move 20
   # Heading is now 135°, moves in that direction
   ```

2. **Speed State**: Defaults to 100, changes persist
   ```bash
   python r2.py --speed 50 --move 10 --speed 200 --move 10
   # First move slow, second move fast
   ```

3. **Dome Lock State**: Once locked, persists through turns
   ```bash
   python r2.py --lock-dome 0 --turn 90 --turn 90
   # Dome stays pointing at 0° throughout
   ```

---

## Best Practices

### 1. Complex Navigation
Break complex paths into turn + move sequences:
```bash
python r2.py --move 30 --turn 45 --move 20 --turn -90 --move 15
```

### 2. Expressive Behaviors
Combine sounds, animations, and movement:
```bash
python r2.py --animation EMOTE_EXCITED --sound R2_EXCITED_1 --shake-head --move 10
```

### 3. Precision Control
Use lower speeds for accurate movements:
```bash
python r2.py --speed 50 --move 5 --move 3 --move 1
# Slow approach to target
```

### 4. Dome Tracking
Lock dome to watch a direction during maneuvers:
```bash
python r2.py --lock-dome 90 --square 20
# Dome watches right (90°) while driving square
```

### 5. Return to Origin
Calculate reverse path:
```bash
python r2.py --move 20 --turn 90 --move 15
# To return:
python r2.py --turn 180 --move 15 --turn -90 --move 20 --turn 180
```

---

## Common Patterns

### Patrol Square
```bash
python r2.py --lock-dome 0 --speed 150 --square 30 --animation EMOTE_HAPPY
```

### Search Pattern
```bash
python r2.py --move 20 --turn 90 --move 10 --turn 90 --move 20 --turn 90 --move 10
```

### Greeting Sequence
```bash
python r2.py --shake-head --sound R2_HEY_1 --animation WWM_BOW
```

### Scan Area
```bash
python r2.py --lock-dome 0 --turn-dome 0 --circle 50
# Dome points forward while body spins
```

### Excited Dance
```bash
python r2.py --animation EMOTE_EXCITED --sound R2_EXCITED_1 --turn 360 --shake-head
```

---

## Example: Complete Mission

Navigate to a point 30cm forward and 20cm to the right, then return:

```bash
# Go to target
python r2.py --lock-dome 0 --speed 150 --move 30 --turn 90 --move 20 --sound R2_POSITIVE_1

# Return home  
python r2.py --turn 180 --move 20 --turn -90 --move 30 --turn 180 --sound R2_CHATTY_5
```

---

## Viewing Available Commands

### Get Help
```bash
python r2.py --help
```

### List All Sounds
The help output includes all available sound names (400+ sounds).

### List All Animations  
The help output includes all available animation names (50+ animations).

---

## Quick Reference

| Category | Argument | Example |
|----------|----------|---------|
| **Move** | `--move <cm>` | `--move 25` |
| **Move Back** | `--move-back <cm>` | `--move-back 10` |
| **Turn** | `--turn <deg>` | `--turn 90` |
| **Speed** | `--speed <val>` | `--speed 150` |
| **Square** | `--square <cm>` | `--square 20` |
| **Circle** | `--circle <cm>` | `--circle 30` |
| **Lock Dome** | `--lock-dome <deg>` | `--lock-dome 45` |
| **Turn Dome** | `--turn-dome <deg>` | `--turn-dome -90` |
| **Sound** | `--sound <NAME>` | `--sound R2_HEY_1` |
| **Animation** | `--animation <NAME>` | `--animation EMOTE_EXCITED` |
| **Shake Head** | `--shake-head` | `--shake-head` |
| **Stance** | `--stance <mode>` | `--stance bipod` |
| **LED** | `--front-led <r,g,b>` | `--front-led 255,0,0` |
| **Volume** | `--set-volume <val>` | `--set-volume 200` |

---

## Important Notes for AI

1. **All distances are in centimeters**
2. **All angles are in degrees** (0-360)
3. **Commands execute sequentially** - robot completes each before next
4. **Heading starts at 0°** and accumulates
5. **Speed range is 0-255** (lower = more accurate, higher = faster)
6. **Dome lock is absolute** (0° = forward in world, not robot-relative)
7. **Sound/animation names are case-sensitive**
8. **Program exits after all commands complete**
9. **For continuous control, use stream mode instead** (see AI_INSTRUCTIONS.md)

---

## Error Handling

If a command fails:
- Error message is printed
- Remaining commands still execute
- Robot disconnects normally at end

Common errors:
- Invalid sound/animation name → Error printed, continues
- Invalid color format → Error printed, continues  
- Robot not found → Program exits immediately
- Bluetooth disconnect → Program exits

---

## Comparison: Direct vs Stream Mode

| Feature | Direct Mode | Stream Mode |
|---------|-------------|-------------|
| **Usage** | `python r2.py --move 10` | `echo "--move 10" >> file.txt` |
| **Connection** | Connects, runs, disconnects | Stays connected |
| **Execution** | Immediate, all at once | Real-time as lines added |
| **Best For** | Single sequences | Interactive/remote control |
| **State** | Within single execution | Persists across commands |

Choose **direct mode** for:
- Scripted sequences
- One-time commands
- Simple automation

Choose **stream mode** for:
- Interactive control
- Long-running sessions  
- Dynamic command generation
- Remote control scenarios
