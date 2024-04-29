import datetime
import subprocess
import tkinter as tk

def draw_segment(canvas, coords, fill='grey'):
    return canvas.create_polygon(coords, fill=fill, outline='black')

def int_to_bcd(x):
    return ((x // 10) << 4) | (x % 10)

def get_time_bcd():
    now = datetime.datetime.now()
    hours = now.hour
    minutes = now.minute
    seconds = now.second
    
    hours_tens_bcd = int_to_bcd(hours // 10)
    hours_units_bcd = int_to_bcd(hours % 10)
    minutes_tens_bcd = int_to_bcd(minutes // 10)
    minutes_units_bcd = int_to_bcd(minutes % 10)
    seconds_tens_bcd = int_to_bcd(seconds // 10)
    seconds_units_bcd = int_to_bcd(seconds % 10)
    
    return [hours_tens_bcd, hours_units_bcd, minutes_tens_bcd, minutes_units_bcd, seconds_tens_bcd, seconds_units_bcd]

def run_verilog_simulation(bcd_values):
    with open('bcd_value.dat', 'w') as f:
        for val in bcd_values:
            f.write(f"{val:08b}\n")
    subprocess.run(["iverilog", "-o", "simv", "bcd_to_7seg.v", "tb_segment7.v"], check=True)
    subprocess.run(["vvp", "simv"], check=True)
    with open('seg_output.dat', 'r') as f:
        seg_output = f.readlines()
    return [line.strip() for line in seg_output]

root = tk.Tk()
root.title("SEVEN SEGMENT CLOCK")
canvas_width, canvas_height = 800, 300
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='black')
canvas.pack()

# Define segments for a single digit
seg_height = 100
seg_width = 50
thickness = 10
digit_spacing = 10  # Space between digits
horizontal_offset = thickness / 2
vertical_offset = thickness / 2
seg_gap = 7
# Define the position of the colon relative to the digits
colon_x_offset = (3 * seg_width) + digit_spacing + seg_gap  # Adjusted for right after hours units
colon_y_offset = canvas_height // 3  # Centered vertically

# Define the size of the colon dots
colon_dot_width = thickness
colon_dot_height = thickness
colon_dot_spacing = 30 # Space between the top and bottom dots
colon_center_y = 50 + (seg_height // 2)
# Calculate the top and bottom Y positions for the colon dots
colon_top_y = colon_center_y - (colon_dot_height // 2) - (colon_dot_spacing // 2)
colon_bottom_y = colon_center_y + (colon_dot_height // 2) + (colon_dot_spacing // 2)

# Define the coordinates for the colon dots
colon_top_coords = [
    (colon_x_offset, colon_top_y),
    (colon_x_offset + colon_dot_width, colon_top_y),
    (colon_x_offset + colon_dot_width, colon_top_y + colon_dot_height),
    (colon_x_offset, colon_top_y + colon_dot_height)
]

colon_bottom_coords = [
    (colon_x_offset, colon_bottom_y),
    (colon_x_offset + colon_dot_width, colon_bottom_y),
    (colon_x_offset + colon_dot_width, colon_bottom_y + colon_dot_height),
    (colon_x_offset, colon_bottom_y + colon_dot_height)
]

# Coordinates for segments are defined relative to the digit's top-left corner
segment_coords = {
    'A': [(horizontal_offset, 0), 
          (seg_width - horizontal_offset, 0), 
          (seg_width - horizontal_offset, thickness), 
          (horizontal_offset, thickness)],
    
    'B': [(seg_width, vertical_offset), 
          (seg_width + thickness, vertical_offset), 
          (seg_width + thickness, seg_height / 2 - vertical_offset), 
          (seg_width, seg_height / 2 - vertical_offset)],
    
    'C': [(seg_width, seg_height / 2 + vertical_offset), 
          (seg_width + thickness, seg_height / 2 + vertical_offset), 
          (seg_width + thickness, seg_height - vertical_offset), 
          (seg_width, seg_height - vertical_offset)],
    
    'D': [(horizontal_offset, seg_height), 
          (seg_width - horizontal_offset, seg_height), 
          (seg_width - horizontal_offset, seg_height - thickness), 
          (horizontal_offset, seg_height - thickness)],
    
    'E': [(0, seg_height / 2 + vertical_offset), 
          (thickness, seg_height / 2 + vertical_offset), 
          (thickness, seg_height - vertical_offset), 
          (0, seg_height - vertical_offset)],
    
    'F': [(0, vertical_offset), 
          (thickness, vertical_offset), 
          (thickness, seg_height / 2 - vertical_offset), 
          (0, seg_height / 2 - vertical_offset)],
    
    'G': [(horizontal_offset, seg_height / 2 - thickness / 2), 
          (seg_width - horizontal_offset, seg_height / 2 - thickness / 2), 
          (seg_width - horizontal_offset, seg_height / 2 + thickness / 2), 
          (horizontal_offset, seg_height / 2 + thickness / 2)]
}

# Initialize segment_ids dictionary for all parts of the display
segment_ids = {
    'hours_tens': [], 'hours_units': [],
    'minutes_tens': [], 'minutes_units': [],
    'seconds_tens': [], 'seconds_units': [],
    'first_colon': [], 'second_colon': []
}

# Positions for each part of the display
positions = {
    'hours_tens': (10, 50),
    'hours_units': (seg_width + 30, 50),
    'first_colon': ((2 * seg_width) + 50, 50),
    'minutes_tens': ((2 * seg_width) + 70 + colon_dot_width + digit_spacing, 50),
    'minutes_units': ((3 * seg_width) + 90 + colon_dot_width + digit_spacing * 2, 50),
    'second_colon': ((4 * seg_width) + 110 + colon_dot_width * 2 + digit_spacing * 3, 50),
    'seconds_tens': ((4 * seg_width) + 130 + colon_dot_width * 2 + digit_spacing * 4, 50),
    'seconds_units': ((5 * seg_width) + 150 + colon_dot_width * 2 + digit_spacing * 5, 50),
}

for part, (x_start, y_start) in positions.items():
    if 'colon' in part:
        # Assuming the y_start is the vertical starting point of your segments
        # and seg_height is the height of your digits
        # The middle point of the digits in the y-axis would be:
        digit_middle_y = y_start + seg_height // 2
        
        # Now, set the top_y to be slightly above this middle point,
        # and the bottom_y to be slightly below it
        top_y = digit_middle_y - colon_dot_spacing // 2 - colon_dot_height // 2
        bottom_y = digit_middle_y + colon_dot_spacing // 2 - colon_dot_height // 2
        
        top_coords = [(x_start, top_y), (x_start + colon_dot_width, top_y),
                      (x_start + colon_dot_width, top_y + colon_dot_height), (x_start, top_y + colon_dot_height)]
        bottom_coords = [(x_start, bottom_y), (x_start + colon_dot_width, bottom_y),
                         (x_start + colon_dot_width, bottom_y + colon_dot_height), (x_start, bottom_y + colon_dot_height)]
        
        # Clear any previously drawn colon segments to prevent drawing over them
        for item in segment_ids[part]:
            canvas.delete(item)
        
        # Draw the new colon segments
        segment_ids[part] = [draw_segment(canvas, top_coords, fill='grey'), draw_segment(canvas, bottom_coords, fill='grey')]
    else:
        # For digit segments, nothing changes
        for seg in segment_coords:
            coords = [(x + x_start, y + y_start) for (x, y) in segment_coords[seg]]
            segment_id = draw_segment(canvas, coords, fill='grey')
            segment_ids[part].append(segment_id)

def update_display():
    # Get BCD values for current time
    bcd_values = get_time_bcd()
    binary_values = run_verilog_simulation(bcd_values)

    # Check that we have the expected number of binary strings (one for each digit)
    if len(binary_values) != 6:
        print("Error: Segments data from Verilog simulation is not in the expected format.")
        return

    # Define the new color using its hex value
    active_color = '#7AFD0A'
    off_color = '#393939'
    # Update each segment's color based on the binary values
    segment_order = ['hours_tens', 'hours_units', 'minutes_tens', 'minutes_units', 'seconds_tens', 'seconds_units']
    for part, value in zip(segment_order, binary_values):
        for seg_id, bit in zip(segment_ids[part], value):
            color = active_color if bit == '1' else off_color
            canvas.itemconfig(seg_id, fill=color)

    # Update the colons (make them blink every second)
    current_second = datetime.datetime.now().second
    colon_color = active_color if current_second % 2 == 0 else off_color
    for colon_part in ['first_colon', 'second_colon']:
        for colon_id in segment_ids[colon_part]:
            canvas.itemconfig(colon_id, fill=colon_color)

    # Schedule the next update
    root.after(1000, update_display)
update_display()
root.mainloop()
