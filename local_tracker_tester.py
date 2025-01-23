import tkinter as tk
from local_tracker import Receiver, Tracker

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
TRACKER_RADIUS = 8
STEP_SIZE = 2


def init_receivers():
    """Initialize receivers with predefined positions."""
    return {
        "Rec1": Receiver("Rec1", 200, 200),
        "Rec2": Receiver("Rec2", 200, 400),
        "Rec3": Receiver("Rec3", 400, 200),
        "Rec4": Receiver("Rec4", 400, 400),
        "Rec5": Receiver("Rec5", 600, 200),
        "Rec6": Receiver("Rec6", 600, 400),
    }


def draw_circle(cx, cy, radius, fill=None, outline=None, tag="temp"):
    """Draw a circle on the canvas."""
    canvas.create_oval(
        cx - radius, cy - radius, cx + radius, cy + radius,
        outline=outline, fill=fill, tags=tag
    )


def move_with_arrows(event):
    """Handle tracker movement with arrow keys."""
    global xpos, ypos
    key_actions = {
        "Left": (-STEP_SIZE, 0),
        "Right": (STEP_SIZE, 0),
        "Up": (0, -STEP_SIZE),
        "Down": (0, STEP_SIZE),
    }

    dx, dy = key_actions.get(event.keysym, (0, 0))
    xpos = max(0, min(CANVAS_WIDTH, xpos + dx))
    ypos = max(0, min(CANVAS_HEIGHT, ypos + dy))

    xpos_entry.delete(0, tk.END)
    ypos_entry.delete(0, tk.END)
    xpos_entry.insert(0, str(xpos))
    ypos_entry.insert(0, str(ypos))

    update_tracker_position()


def update_tracker_position():
    """Update the tracker position on the canvas and move it."""
    global xpos, ypos
    try:
        xpos = float(xpos_entry.get())
        ypos = float(ypos_entry.get())
        xpos = max(0, min(CANVAS_WIDTH, xpos))
        ypos = max(0, min(CANVAS_HEIGHT, ypos))

    except ValueError as e:
        handle_error(e)
        return

    canvas.delete("tracker")
    draw_circle(xpos, ypos, TRACKER_RADIUS, fill="red", outline="red", tag="tracker")
    tracker_label.place(x=xpos + 10, y=ypos + 10)
    tracker_label.config(text=tracker.id)
    
    move()


def move():
    """Recalculate and display the tracker's position."""
    try:
        print("moving to: ", xpos, ",", ypos)
        tracker.move_to(xpos, ypos)
        calculated_x, calculated_y, receivers_used = tracker.find_position(active_receivers)

    except ValueError as e:
        handle_error(e)
        return

    draw_receiver_data(calculated_x, calculated_y, receivers_used)
    update_coord_labels(calculated_x, calculated_y)


def handle_error(e):
    """Handle errors during position calculation."""
    print(f"Error: {e.args[0]}")
    text_label.config(bg="red")
    error_label.config(text=e.args[0], font=("Arial", 11))
    error_label.grid()

    x_label.config(text="x = ?")
    y_label.config(text="y = ?")
    
    if len(e.args) > 1:
        calculated_x, calculated_y, receivers_used = e.args[1]
        draw_receiver_data(calculated_x, calculated_y, receivers_used)
    else:
        canvas.delete("temp")


def update_coord_labels(calculated_x, calculated_y):
    """Update the coordinate labels."""
    error_label.grid_remove()
    x_label.config(text=f"x = {calculated_x:.2f}")
    y_label.config(text=f"y = {calculated_y:.2f}")

    if round(calculated_x, 2) != xpos or round(calculated_y, 2) != ypos:
        text_label.config(bg="red")
    else:
        text_label.config(bg="black")


def draw_receiver_data(tx, ty, receivers_used):
    """Draw the receiver data and connections on the canvas."""
    canvas.delete("temp")
    if isinstance(tx, tuple):  # Indeterminate position case
        for sub_x, sub_y in zip(tx, ty):
            draw_circle(sub_x, sub_y, 10, fill="red", outline="red")
    else:
        draw_circle(tx, ty, 10, fill="blue", outline="blue")

    # Update each receiver's display
    for rec_id, rec in active_receivers.items():
        distance = tracker.report(rec)

        if rec_id in receivers_used:
            # Draw line between tracker and receiver
            if isinstance(tx, tuple):  # Indeterminate position
                for sub_x, sub_y in zip(tx, ty):
                    canvas.create_line(sub_x, sub_y, rec.x, rec.y, fill="blue", tags="temp")
            else:
                canvas.create_line(tx, ty, rec.x, rec.y, fill="blue", tags="temp")
            
            if rec_id == receivers_used[0] or rec_id == receivers_used[1]:
                draw_circle(rec.x, rec.y, distance, outline="blue")

        receiver_labels[rec_id].config(
            text=f"{rec_id}: {distance:.2f}", 
            bg="orange" if rec_id in receivers_used else "green",
            fg="black" if rec_id in receivers_used else "white"
        )


def update_receiver_status():
    """Update active receivers based on checkbutton states."""
    active_receivers.clear()
    canvas.delete("rec")
    for rec_id, var in receiver_vars.items():
        if var.get() == 1:
            active_receivers[rec_id] = receivers[rec_id]
            receiver_labels[rec_id].place(x=receivers[rec_id].x + 15, y=receivers[rec_id].y - 30)
            draw_circle(receivers[rec_id].x, receivers[rec_id].y, 8,
                        fill="green", outline="green", tag="rec")
        else:
            receiver_labels[rec_id].place_forget()

    move()


# Initialize
receivers = init_receivers()
active_receivers = receivers.copy()
tracker = Tracker("John", 0, 0)
xpos, ypos = 550, 50  # Initial position

# Tkinter UI setup
root = tk.Tk()
root.title("Local Tracker Tester")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.config(bg="black")
root.option_add("*Background", "black")
root.option_add("*Foreground", "white")

# Background image
bg_image = tk.PhotoImage(file="./images/sample_layout.png")
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.pack(side="top", fill=tk.BOTH)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

tracker_label = tk.Label(canvas, text=tracker.id)
tracker_label.place(x=xpos + 10, y=ypos + 10)
draw_circle(xpos, ypos, TRACKER_RADIUS, fill="red", outline="red", tag="tracker")

# Bottom frame with labels and button
bot_frame = tk.Frame(root)
bot_frame.config(bg="black")
bot_frame.pack(side="bottom", fill=tk.BOTH)

xpos_label = tk.Label(bot_frame, text="xPos:")
xpos_label.grid(row=2, column=1)
xpos_entry = tk.Entry(bot_frame, width=10)
xpos_entry.insert(0, xpos)
xpos_entry.grid(row=2, column=2)

ypos_label = tk.Label(bot_frame, text="yPos:")
ypos_label.grid(row=2, column=3)
ypos_entry = tk.Entry(bot_frame, width=10)
ypos_entry.insert(0, ypos)
ypos_entry.grid(row=2, column=4)

move_button = tk.Button(bot_frame, text="LOCATE", command=update_tracker_position,
                        bg= "yellow", fg="black")
move_button.grid(row=2, column=5)

x_label = tk.Label(bot_frame, text="x = ?", fg="yellow")
x_label.grid(row=1, column=2)
y_label = tk.Label(bot_frame, text="y = ?", fg="yellow")
y_label.grid(row=1, column=4)
text_label = tk.Label(bot_frame, text="   CALCULATED POSITION   ", 
                      fg="yellow", font=("Arial", 18))
text_label.grid(row=0, column=2, columnspan=3)

error_label = tk.Label(bot_frame, text="  Move with the keyboard arrows to\n dynamically test the tracker",
                       bg="black", fg="yellow", font=("Arial", 18))
error_label.grid(row=0, column=7, rowspan=3)

# Checkbuttons for enabling/disabling receivers and its labels
rec_label = tk.Label(root, text="ACTIVE\nRECEIVERS", font="bold")
rec_label.place(x=CANVAS_WIDTH + 2, y=20)

receiver_labels = {rec_id: tk.Label(canvas, text=rec_id, bg="green") for rec_id in receivers}
receiver_vars = {rec_id: tk.IntVar(value=1) for rec_id in receivers}
chk_y = 80

for rec_id, rec in receivers.items():
    checkbutton = tk.Checkbutton(
        root,
        text=rec_id,
        variable=receiver_vars[rec_id],
        onvalue=1,
        offvalue=0,
        font=14,
        command=update_receiver_status
    )
    checkbutton.place(x=CANVAS_WIDTH + 15, y=chk_y)
    chk_y += 35

    receiver_labels[rec_id].place(x=rec.x + 15, y=rec.y - 30)
    draw_circle(rec.x, rec.y, 8, fill="green", outline="green", tag="rec")

kb_image = tk.PhotoImage(file="images/kb_arr.png")
kb_image_lbl = tk.Label(root, image=kb_image)
kb_image_lbl.place(x=CANVAS_WIDTH + 10, y=470)

# Bind arrow keys for movement
root.bind('<Left>', move_with_arrows)
root.bind('<Right>', move_with_arrows)
root.bind('<Up>', move_with_arrows)
root.bind('<Down>', move_with_arrows)

root.mainloop()