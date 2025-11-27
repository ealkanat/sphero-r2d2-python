import argparse
import time
import math
import os
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.sphero_edu import Color
from spherov2.toy.r2d2 import R2D2
from spherov2.commands.animatronic import Animatronic, R2LegActions
from spherov2.commands.power import Power
from spherov2.helper import to_bytes
from spherov2.sphero_edu import Stance
from spherov2.utils import ToyUtil

class OrderedAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not hasattr(namespace, 'commands'):
            setattr(namespace, 'commands', [])
        namespace.commands.append((self.dest, values))

def parse_color(color_str):
    try:
        r, g, b = map(int, color_str.split(','))
        return Color(r, g, b)
    except ValueError:
        print(f"Invalid color format: {color_str}. Use r,g,b (e.g., 255,0,0)")
        return None

def drive_distance(api, heading, distance_cm, speed=100):
    heading = int(heading) # Ensure heading is int
    print(f"Driving {distance_cm}cm at heading {heading}...")
    api.set_heading(heading)
    start_loc = api.get_location()
    start_x = start_loc['x']
    start_y = start_loc['y']
    
    api.set_speed(speed)
    
    while True:
        curr_loc = api.get_location()
        curr_x = curr_loc['x']
        curr_y = curr_loc['y']
        dist = math.sqrt((curr_x - start_x)**2 + (curr_y - start_y)**2)
        
        if dist >= distance_cm:
            break
        time.sleep(0.05)
        
    api.stop_roll()
    print(f"Reached distance: {dist:.2f}cm")

def get_sounds_list():
    return ", ".join([name for name, member in R2D2.Audio.__members__.items()])

def get_animations_list():
    return ", ".join([name for name, member in R2D2.Animations.__members__.items()])

def execute_single_command(action, value, r2d2, toy, state):
    """Execute a single command and update state"""
    heading = state['heading']
    locked_dome_direction = state['locked_dome_direction']
    current_speed = state['current_speed']
    
    if action == 'set_volume':
        print(f"Setting volume to {value}")
        toy.set_audio_volume(value)
    
    elif action == 'front_led':
        color = parse_color(value)
        if color:
            print(f"Setting front LED to {color}")
            r2d2.set_front_led(color)
    
    elif action == 'back_led':
        color = parse_color(value)
        if color:
            print(f"Setting back LED to {color}")
            r2d2.set_back_led(color)
            
    elif action == 'holo_projector_led':
        intensity = max(0, min(255, int(value)))
        print(f"Setting holo projector LED to {intensity}")
        ToyUtil.set_multiple_leds(toy, {R2D2.LEDs.HOLO_PROJECTOR: intensity})
        
    elif action == 'logic_display_led':
        intensity = max(0, min(255, int(value)))
        print(f"Setting logic display LED to {intensity}")
        ToyUtil.set_multiple_leds(toy, {R2D2.LEDs.LOGIC_DISPLAYS: intensity})
    
    elif action == 'stance':
        print(f"Setting stance to {value}...")
        if value == "bipod":
            r2d2.set_stance(Stance.Bipod)
        elif value == "tripod":
            r2d2.set_stance(Stance.Tripod)
        time.sleep(2)
    
    elif action == 'sound':
        try:
            sound_enum = getattr(R2D2.Audio, value)
            print(f"Playing sound: {value}")
            r2d2.play_sound(sound_enum)
        except AttributeError:
            print(f"Error: Sound '{value}' not found.")
    
    elif action == 'animation':
        try:
            anim_enum = getattr(R2D2.Animations, value)
            print(f"Playing animation: {value}")
            packet = Animatronic._encode(toy, 5, None, to_bytes(anim_enum, 2))
            toy._Toy__packet_queue.put(packet.build())
            time.sleep(3)
        except AttributeError:
            print(f"Error: Animation '{value}' not found.")
    
    elif action == 'shake_head':
        print("Shaking head...")
        r2d2.set_dome_position(45)
        time.sleep(0.5)
        r2d2.set_dome_position(-45)
        time.sleep(0.5)
        r2d2.set_dome_position(0)
    
    elif action == 'move':
        drive_distance(r2d2, int(heading), value, speed=current_speed)
    
    elif action == 'move_back':
        # Move backward in current heading (180 degrees opposite)
        backward_heading = (heading + 180) % 360
        drive_distance(r2d2, int(backward_heading), value, speed=current_speed)
    
    elif action == 'square':
        side = value
        print(f"Driving square with side {side}cm (turning right)...")
        for i, turn_amount in enumerate([0, 90, 90, 90]):
            if i > 0:
                heading += turn_amount
                heading = heading % 360
                r2d2.set_heading(int(heading))
                time.sleep(0.5)
                if locked_dome_direction is not None:
                    relative_dome = (locked_dome_direction - heading) % 360
                    if relative_dome > 180:
                        relative_dome -= 360
                    r2d2.set_dome_position(relative_dome)
                    print(f"  → Dome adjusted to {relative_dome:.1f}° to maintain lock at {locked_dome_direction}°")
            drive_distance(r2d2, int(heading), side, speed=current_speed)
            time.sleep(0.3)
        heading += 90
        heading = heading % 360
        r2d2.set_heading(int(heading))
        time.sleep(0.5)
        if locked_dome_direction is not None:
            relative_dome = (locked_dome_direction - heading) % 360
            if relative_dome > 180:
                relative_dome -= 360
            r2d2.set_dome_position(relative_dome)
            print(f"  → Dome adjusted to {relative_dome:.1f}° to maintain lock at {locked_dome_direction}°")
        print(f"Square complete. Returned to starting orientation (heading: {heading}°)")
    
    elif action == 'square_left':
        side = value
        print(f"Driving square with side {side}cm (turning left)...")
        for i, turn_amount in enumerate([0, -90, -90, -90]):
            if i > 0:
                heading += turn_amount
                heading = heading % 360
                r2d2.set_heading(int(heading))
                time.sleep(0.5)
                if locked_dome_direction is not None:
                    relative_dome = (locked_dome_direction - heading) % 360
                    if relative_dome > 180:
                        relative_dome -= 360
                    r2d2.set_dome_position(relative_dome)
                    print(f"  → Dome adjusted to {relative_dome:.1f}° to maintain lock at {locked_dome_direction}°")
            drive_distance(r2d2, int(heading), side, speed=current_speed)
            time.sleep(0.3)
        heading += -90
        heading = heading % 360
        r2d2.set_heading(int(heading))
        time.sleep(0.5)
        if locked_dome_direction is not None:
            relative_dome = (locked_dome_direction - heading) % 360
            if relative_dome > 180:
                relative_dome -= 360
            r2d2.set_dome_position(relative_dome)
            print(f"  → Dome adjusted to {relative_dome:.1f}° to maintain lock at {locked_dome_direction}°")
        print(f"Square complete. Returned to starting orientation (heading: {heading}°)")
    
    elif action == 'circle':
        diameter = value
        circumference = math.pi * diameter
        estimated_velocity = 30.0
        duration = circumference / estimated_velocity
        
        print(f"Driving circle (approx diameter {diameter}cm)...")
        if locked_dome_direction is not None:
            print(f"  Note: Dome lock active but continuous adjustment during spin not fully supported")
            relative_dome = (locked_dome_direction - heading) % 360
            if relative_dome > 180:
                relative_dome -= 360
            r2d2.set_dome_position(relative_dome)
        
        r2d2.set_speed(current_speed)
        r2d2.spin(360, duration)
        r2d2.set_speed(0)
        
        if locked_dome_direction is not None:
            relative_dome = (locked_dome_direction - heading) % 360
            if relative_dome > 180:
                relative_dome -= 360
            r2d2.set_dome_position(relative_dome)
            print(f"  → Dome re-locked to {locked_dome_direction}° after spin")
    
    elif action == 'move':
        drive_distance(r2d2, int(heading), value, speed=current_speed)
    
    elif action == 'turn':
        heading += value
        heading = heading % 360
        print(f"Turning body by {value} degrees (New heading: {heading})")
        r2d2.set_heading(int(heading))
        time.sleep(1)
        if locked_dome_direction is not None:
            relative_dome = (locked_dome_direction - heading) % 360
            if relative_dome > 180:
                relative_dome -= 360
            r2d2.set_dome_position(relative_dome)
            print(f"  → Dome adjusted to {relative_dome:.1f}° to maintain lock at {locked_dome_direction}°")
    
    elif action == 'turn_dome':
        print(f"Turning dome by {value} degrees...")
        try:
            current_dome = toy.get_head_position()
            new_dome = current_dome + value
            r2d2.set_dome_position(new_dome)
        except Exception as e:
            print(f"Error turning dome: {e}")
            r2d2.set_dome_position(value)
    
    elif action == 'lock_dome':
        locked_dome_direction = value % 360
        relative_dome = (locked_dome_direction - heading) % 360
        if relative_dome > 180:
            relative_dome -= 360
        r2d2.set_dome_position(relative_dome)
        print(f"Dome locked to absolute direction {locked_dome_direction}° (relative position: {relative_dome:.1f}°)")
    
    elif action == 'speed':
        current_speed = max(0, min(255, int(value)))
        print(f"Speed set to {current_speed}")
    
    # Update state
    state['heading'] = heading
    state['locked_dome_direction'] = locked_dome_direction
    state['current_speed'] = current_speed

def stream_mode(filename, r2d2, toy):
    """Monitor a file and execute commands as new lines are added"""
    print(f"\n{'='*50}")
    print(f"STREAM MODE: Monitoring {filename}")
    print(f"Add commands to the file (e.g., '--move 10')")
    print(f"Type 'exit' in a new line to stop")
    print(f"Press Ctrl+C to force quit")
    print(f"{'='*50}\n")
    
    # Initialize state
    state = {
        'heading': 0,
        'locked_dome_direction': None,
        'current_speed': 100
    }
    
    # Get initial file size
    if not os.path.exists(filename):
        print(f"Creating file: {filename}")
        with open(filename, 'w') as f:
            f.write("# R2D2 Command Stream\n")
            f.write("# Add commands below (one per line)\n")
    
    file_position = 0
    
    try:
        while True:
            time.sleep(0.5)  # Poll every 0.5 seconds
            
            with open(filename, 'r') as f:
                f.seek(file_position)
                new_lines = f.readlines()
                file_position = f.tell()
            
            for line in new_lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if line.lower() == 'exit':
                    print("\nExit command received. Stopping stream mode.")
                    return
                
                # Parse and execute command
                try:
                    # Parse the line as arguments
                    parts = line.split()
                    parser = create_parser()
                    
                    # Catch argparse errors (invalid arguments, etc.)
                    try:
                        cmd_args = parser.parse_args(parts)
                    except SystemExit:
                        # argparse calls sys.exit() on error, catch it
                        print(f"Error: Invalid command syntax in '{line}'")
                        continue
                    
                    # Execute commands
                    if hasattr(cmd_args, 'commands') and cmd_args.commands:
                        print(f"\nExecuting: {line}")
                        for action, value in cmd_args.commands:
                            execute_single_command(action, value, r2d2, toy, state)
                except Exception as e:
                    print(f"Error executing '{line}': {e}")
    
    except KeyboardInterrupt:
        print("\n\nStream mode interrupted by user.")
    except Exception as e:
        print(f"\nStream mode error: {e}")

def create_parser():
    """Create and return the argument parser"""
    parser = argparse.ArgumentParser(description="Control R2D2 via command line.", 
                                     formatter_class=argparse.RawTextHelpFormatter)
    
    sound_help = f"Name of the sound to play.\\nAvailable sounds:\\n{get_sounds_list()}"
    anim_help = f"Name of the animation to play.\\nAvailable animations:\\n{get_animations_list()}"

    parser.add_argument("--sound", type=str, action=OrderedAction, help=sound_help)
    parser.add_argument("--shake-head", action=OrderedAction, nargs=0, help="Shake head right and left")
    parser.add_argument("--stance", type=str, action=OrderedAction, choices=["bipod", "tripod"], help="Set stance (bipod or tripod)")
    parser.add_argument("--animation", type=str, action=OrderedAction, help=anim_help)
    
    parser.add_argument("--front-led", type=str, action=OrderedAction, help="Front LED color (r,g,b)")
    parser.add_argument("--back-led", type=str, action=OrderedAction, help="Back LED color (r,g,b)")
    parser.add_argument("--holo-projector-led", type=int, action=OrderedAction, help="Holo projector LED intensity (0-255)")
    parser.add_argument("--logic-display-led", type=int, action=OrderedAction, help="Logic display LED intensity (0-255)")
    parser.add_argument("--set-volume", type=int, action=OrderedAction, help="Set volume level (0-255)")
    
    parser.add_argument("--move", type=float, action=OrderedAction, help="Move forward in the current heading by cm")
    parser.add_argument("--move-back", type=float, action=OrderedAction, help="Move backward in the current heading by cm")
    
    parser.add_argument("--circle", type=float, action=OrderedAction, help="Drive in a circle with diameter in cm")
    parser.add_argument("--square", type=float, action=OrderedAction, help="Drive in a square with side length in cm (turns right/clockwise)")
    parser.add_argument("--square-left", type=float, action=OrderedAction, help="Drive in a square with side length in cm (turns left/counterclockwise)")

    parser.add_argument("--turn", type=float, action=OrderedAction, help="Turn body by degrees (signed)")
    parser.add_argument("--turn-dome", type=float, action=OrderedAction, help="Turn dome by degrees (signed). Relative to current position.")
    parser.add_argument("--lock-dome", type=float, action=OrderedAction, help="Lock dome to absolute world direction (0-360). Dome will maintain this direction when body turns.")
    parser.add_argument("--speed", type=int, action=OrderedAction, help="Set movement speed (0-255). Affects subsequent movement commands.")
    
    parser.add_argument("--stream", type=str, help="Monitor a text file and execute commands as new lines are added. Each line should contain command arguments.")
    
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    # Find toy
    print("Scanning for R2D2...")
    toy = scanner.find_R2D2()
    if not toy:
        print("R2D2 not found.")
        return
    print(f"Found: {toy}")
    
    with SpheroEduAPI(toy) as r2d2:
        # --- Status Reporting ---
        # --- Status Reporting ---
        print("-" * 20)
        print("Status Report:")
        
        # Battery Voltage State
        try:
            voltage_state = Power.get_battery_voltage_state(toy)
            print(f"Battery Voltage State: {voltage_state.name}")
        except Exception:
            pass

        # Battery Percentage (New)
        try:
            battery_pct = Power.get_battery_percentage(toy)
            print(f"Battery Percentage: {battery_pct}%")
        except Exception:
            pass
            
        # Charger State
        try:
            charger_state = Power.get_charger_state(toy)
            print(f"Charger State: {charger_state}")
        except Exception:
            pass
        print("-" * 20)

        # Initial Setup (Defaults)
        toy.set_audio_volume(255)
        
        # --- Stream Mode ---
        if args.stream:
            stream_mode(args.stream, r2d2, toy)
            return

        # --- Execute Commands in Order ---
        if hasattr(args, 'commands') and args.commands:
            state = {
                'heading': 0,
                'locked_dome_direction': None,
                'current_speed': 100
            }
            
            for action, value in args.commands:
                execute_single_command(action, value, r2d2, toy, state)

if __name__ == "__main__":
    main()