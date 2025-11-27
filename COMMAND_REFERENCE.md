# R2D2 Command Reference for AI Assistants

This document explains R2D2 robot commands conceptually - what they do, their parameters, and their behavior. This is a pure command reference without usage instructions.

---

## Movement Commands

### `--move <distance_cm>`
**Purpose**: Move the robot forward in its current heading direction.

**Parameters**:
- `distance_cm`: Distance to travel in centimeters (float)

**Behavior**:
- Robot moves forward relative to its current heading
- Uses position tracking (locator sensor) for accuracy
- Speed determined by current `--speed` setting
- Distance-based, not time-based (same distance at any speed)
- Heading unchanged after movement

**Example Values**: `10`, `25.5`, `100`

---

### `--move-back <distance_cm>`
**Purpose**: Move the robot backward in its current heading direction.

**Parameters**:
- `distance_cm`: Distance to travel in centimeters (float)

**Behavior**:
- Robot moves backward (180° from current heading)
- Same accuracy and speed control as `--move`
- Essentially moves in heading + 180°
- Heading unchanged after movement

**Example Values**: `10`, `15.3`, `50`

---

### `--speed <value>`
**Purpose**: Set movement speed for all subsequent movement commands.

**Parameters**:
- `value`: Speed value from 0-255 (integer)

**Behavior**:
- Affects: `--move`, `--move-back`, `--square`, `--square-left`, `--circle`
- Lower values = slower, more accurate
- Higher values = faster, less accurate
- Default: 100
- State persists until changed

**Example Values**: `50` (slow), `100` (default), `200` (fast), `255` (maximum)

---

## Rotation Commands

### `--turn <degrees>`
**Purpose**: Rotate the robot body by specified degrees.

**Parameters**:
- `degrees`: Rotation amount in degrees, signed (float)
  - Positive: Rotate right (clockwise)
  - Negative: Rotate left (counterclockwise)

**Behavior**:
- Rotates robot body in place
- Heading state accumulates (new_heading = old_heading + degrees)
- Range wraps at 360° (modulo 360)
- If dome is locked, dome compensates to maintain absolute direction
- Takes ~1 second to complete

**Example Values**: `90`, `-45`, `180`, `30.5`

---

## Pattern Commands

### `--square <side_cm>`
**Purpose**: Drive in a square pattern, turning right at corners.

**Parameters**:
- `side_cm`: Length of each side in centimeters (float)

**Behavior**:
- Drives 4 sides of specified length
- Turns 90° right at each corner
- Returns to starting orientation with final 90° turn
- Uses current speed setting
- Heading updated through pattern (4 turns = 360°)
- If dome locked, compensates at each turn
- Total path: drive → turn → drive → turn → drive → turn → drive → turn

**Example Values**: `20`, `30.5`, `50`

---

### `--square-left <side_cm>`
**Purpose**: Drive in a square pattern, turning left at corners.

**Parameters**:
- `side_cm`: Length of each side in centimeters (float)

**Behavior**:
- Same as `--square` but turns left (-90°) at corners
- Counterclockwise motion
- Returns to starting orientation
- Dome compensation if locked

**Example Values**: `20`, `25`, `40`

---

### `--circle <diameter_cm>`
**Purpose**: Drive in a circular pattern.

**Parameters**:
- `diameter_cm`: Approximate diameter of circle in centimeters (float)

**Behavior**:
- Uses spin motion (less precise than other movements)
- Completes 360° rotation while moving
- Speed affects circle execution
- Heading unchanged after full circle
- Dome lock maintained before and after (not during spin)
- Duration calculated from circumference and estimated velocity

**Example Values**: `30`, `50`, `75`

---

## Dome Control Commands

### `--turn-dome <degrees>`
**Purpose**: Rotate the dome (head) relative to its current position.

**Parameters**:
- `degrees`: Rotation amount in degrees, signed (float)
  - Positive: Rotate dome right
  - Negative: Rotate dome left

**Behavior**:
- Rotates dome independently of body
- Relative to current dome position
- Does not affect dome lock state
- Dome position is robot-relative (not world-relative)

**Example Values**: `45`, `-90`, `180`, `30`

---

### `--lock-dome <absolute_degrees>`
**Purpose**: Lock dome to point at an absolute world direction.

**Parameters**:
- `absolute_degrees`: World direction in degrees, 0-360 (float)
  - `0°`: Forward/North (original facing)
  - `90°`: Right/East
  - `180°`: Back/South
  - `270°`: Left/West

**Behavior**:
- Sets dome to point at absolute world direction
- Dome automatically compensates when body turns
- Lock persists until dome manually moved or new lock set
- Compensation calculation: dome_position = locked_direction - body_heading
- Dome position normalized to ±180° range

**Example Values**: `0`, `90`, `180`, `270`, `45`

---

## Audio Commands

### `--sound <SOUND_NAME>`
**Purpose**: Play a sound effect from the robot's library.

**Parameters**:
- `SOUND_NAME`: Name of sound (case-sensitive string)

**Behavior**:
- Plays audio file immediately
- Volume determined by current volume setting
- Does not block other commands
- Names are enum values from R2D2.Audio class

**Sound Categories**:
- **Excited**: `R2_EXCITED_1` through `R2_EXCITED_16`
- **Greetings**: `R2_HEY_1` through `R2_HEY_12`
- **Chatty**: `R2_CHATTY_1` through `R2_CHATTY_62`
- **Positive**: `R2_POSITIVE_1` through `R2_POSITIVE_23`
- **Negative**: `R2_NEGATIVE_1` through `R2_NEGATIVE_28`
- **Sad**: `R2_SAD_1` through `R2_SAD_25`
- **Laugh**: `R2_LAUGH_1` through `R2_LAUGH_4`
- **Special**: `R2_SCREAM`, `R2_ANNOYED`, `R2_BURNOUT`, `R2_HEAD_SPIN`, `R2_MOTOR`

**Example Values**: `R2_EXCITED_1`, `R2_HEY_5`, `R2_SCREAM`

---

### `--set-volume <value>`
**Purpose**: Set audio playback volume.

**Parameters**:
- `value`: Volume level from 0-255 (integer)
  - `0`: Mute
  - `255`: Maximum

**Behavior**:
- Affects all subsequent sound playback
- State persists until changed
- Default: 255 (maximum)

**Example Values**: `100`, `200`, `255`

---

## Animation Commands

### `--animation <ANIMATION_NAME>`
**Purpose**: Play a physical animation (dome/body movement sequence).

**Parameters**:
- `ANIMATION_NAME`: Name of animation (case-sensitive string)

**Behavior**:
- Plays pre-programmed movement sequence
- May involve dome rotation, body shake, LED changes
- Pauses ~3 seconds for animation completion
- Names are enum values from R2D2.Animations class

**Animation Categories**:
- **Emotes**: `EMOTE_EXCITED`, `EMOTE_HAPPY`, `EMOTE_ANGRY`, `EMOTE_SAD`, `EMOTE_SURPRISED`, `EMOTE_FRUSTRATED`, `EMOTE_LAUGH`, `EMOTE_NO`, `EMOTE_YES`, `EMOTE_ALARM`, `EMOTE_RETREAT`, `EMOTE_FIERY`, `EMOTE_UNDERSTOOD`
- **WWM (Expressive)**: `WWM_BOW`, `WWM_SHAKE`, `WWM_SCARED`, `WWM_SURPRISED`, `WWM_HAPPY`, `WWM_SAD`, `WWM_ANGRY`, `WWM_ANXIOUS`, `WWM_TAUNTING`, `WWM_YELLING`, `WWM_WHISPER`
- **Idle**: `IDLE_1`, `IDLE_2`, `IDLE_3`
- **Charger**: `CHARGER_1` through `CHARGER_7`

**Example Values**: `EMOTE_EXCITED`, `WWM_BOW`, `EMOTE_SURPRISED`

---

## Physical Action Commands

### `--shake-head`
**Purpose**: Shake the dome left and right.

**Parameters**: None

**Behavior**:
1. Rotate dome 45° right
2. Wait 0.5 seconds
3. Rotate dome 45° left (total -45° from start)
4. Wait 0.5 seconds
5. Return dome to center (0°)
- Total duration: ~1 second
- Dome returns to neutral position

---

### `--stance <mode>`
**Purpose**: Set robot's leg configuration.

**Parameters**:
- `mode`: Stance type (string)
  - `bipod`: Two legs (third leg retracted)
  - `tripod`: Three legs (third leg extended)

**Behavior**:
- **Bipod**: Retracts third leg, less stable, can't move
- **Tripod**: Extends third leg, stable, required for movement
- Transition takes ~2 seconds
- Movement commands require tripod stance

**Example Values**: `bipod`, `tripod`

---

## LED Commands

### `--front-led <r,g,b>`
**Purpose**: Set front LED color.

**Parameters**:
- `r,g,b`: RGB color values, comma-separated (integers 0-255)

**Behavior**:
- Sets front LED to specified color
- Immediate effect
- Color persists until changed
- Default: Pink (255,58,255)

**Example Values**: `255,0,0` (red), `0,255,0` (green), `0,0,255` (blue), `255,255,0` (yellow)

---

### `--back-led <r,g,b>`
**Purpose**: Set back LED color.

**Parameters**:
- `r,g,b`: RGB color values, comma-separated (integers 0-255)

**Behavior**:
- Sets back LED to specified color
- Independent from front LED
- Immediate effect
- Default: Pink (255,58,255)

**Example Values**: `255,0,0` (red), `0,255,0` (green), `128,0,128` (purple)

---

### `--holo-projector-led <value>`
**Purpose**: Set holo projector LED intensity.

**Parameters**:
- `value`: Brightness level from 0-255 (integer)

**Behavior**:
- Sets the white holo projector LED brightness
- Immediate effect
- Persists until changed
- Default: 0 (off)

**Example Values**: `0` (off), `128` (half), `255` (max)

---

### `--logic-display-led <value>`
**Purpose**: Set logic display LED intensity.

**Parameters**:
- `value`: Brightness level from 0-255 (integer)

**Behavior**:
- Sets the front logic display LEDs brightness
- Immediate effect
- Persists until changed
- Default: 0 (off)

**Example Values**: `0` (off), `255` (max)

---

## State Variables

### Heading
- **Type**: Float (0-360 degrees)
- **Initial Value**: 0° (forward)
- **Modified By**: `--turn`, `--square`, `--square-left`
- **Used By**: `--move`, `--move-back`, dome lock compensation
- **Persistence**: Within single execution or stream session
- **Behavior**: Accumulates as robot turns, wraps at 360°

### Dome Lock Direction
- **Type**: Float (0-360 degrees) or None
- **Initial Value**: None (unlocked)
- **Modified By**: `--lock-dome`
- **Used By**: Automatic compensation during turns
- **Persistence**: Until dome moved or new lock set
- **Behavior**: Dome auto-adjusts to maintain absolute world direction

### Speed
- **Type**: Integer (0-255)
- **Initial Value**: 100
- **Modified By**: `--speed`
- **Used By**: All movement commands
- **Persistence**: Until changed
- **Behavior**: Lower = slower/more accurate, higher = faster/less accurate

---

## Units and Ranges

| Parameter | Unit | Range | Notes |
|-----------|------|-------|-------|
| **Distance** | Centimeters | 0-∞ | Practical max ~200cm |
| **Angle** | Degrees | -∞ to ∞ | Normalized to 0-360 |
| **Speed** | Unitless | 0-255 | 0=stop, 255=max |
| **RGB Values** | Integer | 0-255 | Standard RGB |
| **Volume** | Integer | 0-255 | 0=mute, 255=max |

---

## Command Execution Order

Commands execute sequentially in the order specified:
1. Previous command completes fully
2. Next command begins
3. State updates accumulate
4. No parallel execution

---

## Key Behaviors

### Distance Measurement
- Uses robot's locator sensor (accelerometer-based)
- Tracks X,Y position in coordinate space
- Calculates actual distance traveled: `√(Δx² + Δy²)`
- Speed-independent accuracy (same distance at any speed)

### Heading System
- 0° = initial forward direction ("north")
- Clockwise positive (90° = right, 180° = back, 270° = left)
- Accumulative (turn 90° twice = 180° total heading)
- Modulo 360 normalization

### Dome Lock Mechanics
- Absolute world reference (not robot-relative)
- Compensation formula: `dome_angle = (lock_direction - body_heading) % 360`
- Normalized to ±180° range for natural movement
- Automatic compensation on every turn

### Speed vs Accuracy
- Lower speed (30-80): High accuracy, slow execution
- Medium speed (80-150): Balanced
- High speed (150-255): Fast execution, reduced accuracy
- Affects movement distance precision

---

## Error Conditions

### Invalid Parameters
- Out of range values: Clamped or error
- Invalid sound/animation name: Error logged, execution continues
- Invalid color format: Error logged, execution continues

### Physical Limitations
- Movement requires tripod stance
- Dome range: approximately ±180°
- Maximum practical movement: ~200cm per command
- Turning accuracy degrades at very high speeds

---

## Special Notes

1. **All angles in degrees** (not radians)
2. **All distances in centimeters** (not meters)
3. **Case-sensitive names** for sounds and animations
4. **State accumulates** within execution context
5. **Position-based movement** not time-based
6. **Dome compensation automatic** when locked
7. **Sequential execution** only (no parallelism)
