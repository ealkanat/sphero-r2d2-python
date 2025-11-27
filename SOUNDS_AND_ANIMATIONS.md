# R2D2 Control Script Reference

## Available Sounds

### Test Sounds
- TEST_1497HZ, TEST_200HZ, TEST_2517HZ, TEST_3581HZ, TEST_431HZ, TEST_6011HZ, TEST_853HZ

### BB8 Sounds
#### Alarms
- BB8_ALARM_1, BB8_ALARM_2, BB8_ALARM_3, BB8_ALARM_4, BB8_ALARM_6, BB8_ALARM_7, BB8_ALARM_8, BB8_ALARM_9, BB8_ALARM_10, BB8_ALARM_11, BB8_ALARM_12

#### Chatty
- BB8_CHATTY_1 through BB8_CHATTY_27

#### Excited
- BB8_EXCITED_1, BB8_EXCITED_2, BB8_EXCITED_3, BB8_EXCITED_4

#### Hey
- BB8_HEY_1 through BB8_HEY_13

#### Laugh
- BB8_LAUGH_1, BB8_LAUGH_2

#### Negative
- BB8_NEGATIVE_1 through BB8_NEGATIVE_30

#### Positive
- BB8_POSITIVE_1 through BB8_POSITIVE_16

#### Sad
- BB8_SAD_1 through BB8_SAD_18

#### Other
- BB8_BOOT_UP, BB8_BOOR_UP_2, BB8_DONT_KNOW, BB8_SHORTCUT, BB8_WOW_1

### BB9E Sounds
#### Alarms
- BB9E_ALARM_1 through BB9E_ALARM_5

#### Chatty
- BB9E_CHATTY_1, BB9E_CHATTY_2

#### Excited
- BB9E_EXCITED_1, BB9E_EXCITED_2, BB9E_EXCITED_3

#### Hey
- BB9E_HEY_1, BB9E_HEY_2

#### Negative
- BB9E_NEGATIVE_1 through BB9E_NEGATIVE_4

#### Positive
- BB9E_POSITIVE_1 through BB9E_POSITIVE_5

#### Sad
- BB9E_SAD_1, BB9E_SAD_2

#### Extras
- BB9E_EXTRA_1 through BB9E_EXTRA_7
- BB9E_HEAD_TURN_1, BB9E_HEAD_TURN_2, BB9E_HEAD_TURN_3

### R2D2 Sounds
#### Movement
- R2_FALL
- R2_STEP_1 through R2_STEP_6

#### Hits
- R2_HIT_1 through R2_HIT_11

#### Alarms
- R2_ALARM_1 through R2_ALARM_16

#### Chatty
- R2_CHATTY_1 through R2_CHATTY_62

#### Excited
- R2_EXCITED_1 through R2_EXCITED_16

#### Hey
- R2_HEY_1 through R2_HEY_12

#### Laugh
- R2_LAUGH_1 through R2_LAUGH_4

#### Negative
- R2_NEGATIVE_1 through R2_NEGATIVE_28

#### Positive
- R2_POSITIVE_1 through R2_POSITIVE_23

#### Sad
- R2_SAD_1 through R2_SAD_25

#### Special
- R2_ACCESS_PANELS
- R2_ANNOYED
- R2_BURNOUT
- R2_ENGAGE_HYPER_DRIVE
- R2_HEAD_SPIN
- R2_MOTOR
- R2_SCREAM, R2_SCREAM_2
- R2_SHORT_OUT

### R2Q5 Sounds
- R2Q5_ALARM_1, R2Q5_ALARM_2
- R2Q5_CHATTY_1, R2Q5_CHATTY_2
- R2Q5_HEY_1, R2Q5_HEY_2
- R2Q5_NEGATIVE_1
- R2Q5_POSITIVE_1, R2Q5_POSITIVE_2
- R2Q5_SAD_1
- R2Q5_SHUTDOWN

## Available Animations

### Charger Animations
- CHARGER_1, CHARGER_2, CHARGER_3, CHARGER_4, CHARGER_5, CHARGER_6, CHARGER_7

### Emote Animations
- EMOTE_ALARM
- EMOTE_ANGRY
- EMOTE_ATTENTION
- EMOTE_FRUSTRATED
- EMOTE_DRIVE
- EMOTE_EXCITED
- EMOTE_SEARCH
- EMOTE_SHORT_CIRCUIT
- EMOTE_LAUGH
- EMOTE_NO
- EMOTE_RETREAT
- EMOTE_FIERY
- EMOTE_UNDERSTOOD
- EMOTE_YES
- EMOTE_SCAN
- EMOTE_SURPRISED

### Idle Animations
- IDLE_1, IDLE_2, IDLE_3

### WWM (With the World's Mind) Animations
- WWM_ANGRY
- WWM_ANXIOUS
- WWM_BOW
- WWM_CONCERN
- WWM_CURIOUS
- WWM_DOUBLE_TAKE
- WWM_EXCITED
- WWM_FIERY
- WMM_FRUSTRATED
- WWM_HAPPY
- WWM_JITTERY
- WWM_LAUGH
- WWM_LONG_SHAKE
- WWM_NO
- WWM_OMINOUS
- WWM_RELIEVED
- WWM_SAD
- WWM_SCARED
- WWM_SHAKE
- WWM_SURPRISED
- WWM_TAUNTING
- WWM_WHISPER
- WWM_YELLING
- WWM_YOOHOO

### Other
- MOTOR

## Usage Examples

### Playing Sounds
```bash
# Play an excited sound
python r2.py --sound R2_EXCITED_1

# Play multiple sounds in sequence
python r2.py --sound R2_HEY_1
python r2.py --sound R2_CHATTY_5
```

### Playing Animations
```bash
# Play an animation
python r2.py --animation EMOTE_EXCITED

# Combine with movement
python r2.py --animation EMOTE_HAPPY --move 10 --turn 90 --move 10
```

### Combined Examples
```bash
# Full sequence
python r2.py --sound R2_EXCITED_1 --animation EMOTE_EXCITED --move 20 --turn 90 --move 20

# Head movements
python r2.py --shake-head --sound R2_CHATTY_10

# Dome control
python r2.py --turn-dome 45 --sound R2_HEAD_SPIN
```
