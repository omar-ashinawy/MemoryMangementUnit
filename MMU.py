from tkinter import *
from tkinter import messagebox
from tkinter import ttk
#########################################################################
#Ibrahim's part
class Segment:
	def __init__(self, process_name = "NULL", name = "UNK", size = 0):
		self.process_name = process_name
		self.name = name
		self.size = size

class free_hole:
	def __init__(self, base = 0, size = 0 ):
		self.size = size
		self.base = base

def edit_fh(memo, fh):
	temp = 0
	count = 0
	flag = 0 
	fh.clear()
	for i in range(len(memo)):
		if memo[i].process_name == "free":
			count += 1
			temp = i
			flag = 1
		elif flag == 1:
			fh.append(free_hole(temp - count + 1, count))
			count = 0
			flag = 0 
	if flag == 1:
		fh.append(free_hole(temp - count + 1, count))

def Allocate(s, algorithm, memo, fh):
	temp = 0 
	flag = 0
	for i in range(len(fh)):
		if fh[i].size >= s.size:
			if algorithm == "FF":
				for j in range(s.size):
					memo[j + fh[i].base] = Segment(s.process_name, s.name, size = 1)
				edit_fh(memo, fh)
				return True
			elif algorithm == "BF":
				if flag == 0:
					temp = i
					flag = 1
				elif fh[i].size < fh[temp].size:
					temp = i
	if flag == 0:
		return False
	else:
		for j in range(s.size):
			memo[j + fh[temp].base] = Segment(s.process_name, s.name, size = 1)
		edit_fh(memo, fh)
		return True

def hole(b, s, memo, fh):
	for j in range(s):
		memo[j + b] = Segment("free", "hole", 1)
	edit_fh(memo, fh)

def deallocate(index, memo, fh):
	if memo[index].process_name == "NULL":
		i = index
		while ((i < len(memo)) and (memo[i].process_name == "NULL")):
			memo[i] = Segment("free", "hole", 1)
			i += 1
		i = index - 1
		while ((i >= 0) and (memo[i].process_name == "NULL")):
			memo[i] = Segment("free", "hole", 1)
			i -= 1
		edit_fh(memo, fh)
	else:
		temp = memo[index].process_name
		for i in range(len(memo)):
			if (memo[i].process_name == temp):
				memo[i] = Segment("free", "hole", 1)
		edit_fh(memo, fh)

def prints(k):
	for i in range(len(k)):
		print(k[i].process_name + "\t" + k[i].name + "\n")

def printh(k):
	for i in range(len(k)):
		print("base: " + str(k[i].base) + ", " + "size: " + str(k[i].size))

def organize_memory(memory):
	temp_pn = memory[0].process_name
	temp_n = memory[0].name
	seg_size = 1
	new_memory = []
	for i in range(1, len(memory)):
		if memory[i].process_name == temp_pn and memory[i].name == temp_n:
			seg_size += 1
		else:
			new_memory.append(Segment(temp_pn, temp_n, seg_size))
			temp_pn = memory[i].process_name
			temp_n = memory[i].name
			seg_size = 1
	new_memory.append(Segment(temp_pn, temp_n, seg_size))
	return new_memory
###########################################################################
def draw_memory(memory, canvas):
	canvas.delete(ALL)
	global y_offset
	global x_offset
	global mag_factor
	canvas.create_text(2, 0, text = "Memory Layout", font = "Helvetica 22 bold", anchor = "nw" )
	memory_size = 0
	for i in range (len(memory)):
		memory_size += memory[i].size 
	y_offset = 35
	x_offset = 50
	mag_factor = (canvas_height - y_offset)/memory_size
	acc_size = 0
	canvas.create_text(25, (y_offset - 1), text = str("0"), font = "Times 11")
	for i in range(len(memory)):
		canvas.create_text(25, (y_offset - 3 + mag_factor*(acc_size + memory[i].size)), text = str(acc_size + memory[i].size), font = "Times 11	")
		if (memory[i].name != "UNK" and memory[i].name != "hole"):
			canvas.create_rectangle(x_offset, (y_offset + mag_factor*acc_size), canvas_width, (y_offset + mag_factor*(acc_size + memory[i].size)))
			canvas.create_text(0.5*(canvas_width + x_offset), (y_offset + mag_factor*(acc_size + 0.5*memory[i].size)), text = "Process: " + memory[i].process_name + ", Segment: " + memory[i].name, font = "Times 12 bold")
			# canvas.create_text(0.5*canvas_width + x_offset, (y_offset + mag_factor*(acc_size + 0.5*memory[i].size) + 7), text = "Segment: " + memory[i].name, font = "Times 12 bold")
		elif (memory[i].name == "UNK"):
			canvas.create_rectangle(x_offset, (y_offset + mag_factor*acc_size), canvas_width, (y_offset + mag_factor*(acc_size + memory[i].size)), fill = "red")
			canvas.create_line(x_offset, (y_offset + mag_factor*acc_size), canvas_width, (y_offset + mag_factor*(acc_size + memory[i].size)), fill = "blue")
			canvas.create_line(canvas_width, (y_offset + mag_factor*acc_size), x_offset, (y_offset + mag_factor*(acc_size + memory[i].size)), fill = "blue")
		elif (memory[i].name == "hole"):
			canvas.create_rectangle(x_offset, (y_offset + mag_factor*acc_size), canvas_width, (y_offset + mag_factor*(acc_size + memory[i].size)), fill = "green")
		acc_size += memory[i].size

def draw(): 
	memory.clear()
	if mem_size.isdigit():
		for i in range(int(mem_size)):
			memory.append(Segment(size = 1))
		draw_memory(organize_memory(memory), canvas)
	else:
		messagebox.showerror(title = "Error", message = "Memory Size MUST BE AN INTEGER!\nابعدوا عننا بقى سودتوا عيشتنا ")

def create_hole():
	if (not mem_size.isdigit()):
		messagebox.showerror(title = "Error", message = "Enter Memory Size First!")
	elif hole_address.isdigit() and hole_size.isdigit():
		if (int(hole_address) + int(hole_size)) > int (mem_size):
			messagebox.showerror(title = "Error", message = "Out of Range!\nاحنا هنهرج !")
		else:
			hole(int(hole_address), int(hole_size), memory, fh)
			draw_memory(organize_memory(memory), canvas)
			hole_address_entry.delete(0, END)
			hole_size_entry.delete(0, END)
	else:
		messagebox.showerror(title = "Error", message = "Hole Starting Address and Hole Size Must Be Integers!\nابعدوا عننا بقى سودتوا عيشتنا ")

def allocate_segment(algorithm):
	if (not mem_size.isdigit()):
		messagebox.showerror(title = "Error", message = "Enter Memory Size First!")
	else:
		if (not segment_size.isdigit()):
			messagebox.showerror(title = "Error", message = "Segment Size Must Be an Integer!\nهو حضرتك بتعمل ايه ؟")
		else:
			done = Allocate(Segment(process_text, segment_text, int(segment_size)), algorithm, memory, fh)
			if not done:
				messagebox.showerror("Error", "Segment Can't Fit!")
			else:
				draw_memory(organize_memory(memory), canvas)
				segment_name_entry.delete(0, END)
				segment_size_entry.delete(0, END)

def deallocate_segment(event):
	if event.x > x_offset and event.y > y_offset:
		y_true = (event.y - y_offset)/mag_factor
		deallocate(int(y_true), memory, fh)
		draw_memory(organize_memory(memory), canvas)
	#print ("x = " + str(event.x) + ", y = " + str(event.y))

def show_seg_table():
	dict_memory = organize_memory(memory)
	f = 0
	for i in range (len(dict_memory)):
		if dict_memory[i].process_name == process_seg:
			f = 1
			break
	if f == 0:
		messagebox.showerror("Error", "Process Doesn't Exist!\nهو حضرتك بتعمل ايه ؟")
	else:
		seg_window = Toplevel(root)
		Label(seg_window, text = "Segment Table for " + process_seg, font = "Times 20").pack()
		seg_table = ttk.Treeview(seg_window)
		seg_table["columns"] = ("one", "two")
		seg_table.column("#0", width = 100, minwidth = 80, stretch = "no")
		seg_table.column("one", width = 100, minwidth = 80, stretch = "no")
		seg_table.column("two", width = 100, minwidth = 80, stretch = "no")
		seg_table.heading("#0", text = "Segment", anchor = "w")
		seg_table.heading("one", text = "Starting Address", anchor = "w")
		seg_table.heading("two", text = "Size", anchor = "w")
		acc_size = 0
		for i in range (len(dict_memory)):
			if dict_memory[i].process_name == process_seg:
				seg_table.insert("", "end", text = dict_memory[i].name, values = (str(acc_size), str(dict_memory[i].size)))
			acc_size += dict_memory[i].size
		seg_table.pack()

def pretext(event, entry):
	global mem_size
	global hole_address
	global hole_size
	global process_text
	global segment_text
	global segment_size
	global process_seg

	if (event == '<Enter>'):
		# print("I've entered")
		if entry.get() == "Memory Size" or entry.get() == "Hole Starting Address" or entry.get() == "Hole Size" or entry.get() == "Process Name" or entry.get() == "Segment Size" or entry.get() == "Segment Name" or entry.get() == "Process to Get Table":
			entry.delete(0, END)
	elif (event == '<Leave>'):
		# print("I've left")
		if entry is mem_size_entry:
			mem_size = entry.get()
		elif entry is hole_address_entry:
			hole_address = entry.get()
		elif entry is hole_size_entry:
			hole_size = entry.get()
		elif entry is process_name_entry:
			process_text = entry.get()
		elif entry is segment_name_entry:
			segment_text = entry.get()
		elif entry is segment_size_entry:
			segment_size = entry.get()
		elif entry is segment_table_entry:
			process_seg = entry.get()

		if entry.get() == "" and entry is mem_size_entry:
			entry.insert(0, "Memory Size")
		elif entry.get() == "" and entry is hole_address_entry:
			entry.insert(0, "Hole Starting Address")
		elif entry.get() == "" and entry is hole_size_entry:
			entry.insert(0, "Hole Size")
		elif entry.get() == "" and entry is process_name_entry:
			entry.insert(0, "Process Name")
		elif entry.get() == "" and entry is segment_name_entry:
			entry.insert(0, "Segment Name")
		elif entry.get() == "" and entry is segment_size_entry:
			entry.insert(0, "Segment Size")
		elif entry.get() == "" and entry is segment_table_entry:
			entry.insert(0, "Process to Get Table")

def create_label(text = "", y = 0, x = 0):
	label = Label(root, text = text, anchor = "nw")
	label.place(y = y, x = x)
	return label

def create_entry(text = "", y = 0, x = 0):
	Ent = Entry(root)
	Ent.insert(0, text)
	Ent.bind(sequence = '<Enter>', func = lambda entry: pretext('<Enter>', Ent))
	Ent.bind(sequence = '<Leave>', func = lambda entry: pretext('<Leave>', Ent))
	Ent.place(y = y, x = x)
	return Ent

def create_button(text = "", y = 0, x = 0, command = None):
	btn = Button(root, text = text, command = command)
	btn.place(y = y, x = x, width = 125)
	return btn
###########################################################################
root = Tk()
root.title("Memory Mangement Project")
root.geometry("1005x705")

memory = []
fh = []

mem_size = ""
hole_address = ""
hole_size = ""
process_text = ""
segment_text = ""
segment_size = ""
process_seg = ""

radio_choice = StringVar()
radio_choice.set("FF")

canvas_width = 400
canvas_height = 700
canvas = Canvas(root, height = canvas_height, width = canvas_width)

canvas.bind(sequence = "<Double-Button-1>", func = deallocate_segment)
canvas.create_text(2, 0, text = "Memory Layout", font = "Helvetica 22 bold", anchor = "nw")
canvas.place(y = 0, x = 1000 - canvas_width)

close_btn = create_button("Close", 120, 290, root.destroy)

mem_size_label = create_label("Memory Size:", 1, 0)

mem_size_entry = create_entry("Memory Size", 3, 125)

mem_size_btn = create_button("Enter", 0, 290, draw)

hole_address_label = create_label("Hole Starting Address:", 31, 0)

hole_address_entry = create_entry("Hole Starting Address", 33, 125)

hole_size_label = create_label("Hole Size:", 61, 0)

hole_size_entry = create_entry("Hole Size", 63, 125)

hole_btn = create_button("Enter Hole", 30, 290, create_hole)

process_name_label = create_label("Process Name:", 91, 0)

process_name_entry = create_entry("Process Name", 93, 125)

process_btn = create_button("Enter Segment", 87, 290, command = lambda: allocate_segment(radio_choice.get()))

segment_name_label = create_label("Segment Name:", 121, 0)

segment_name_entry = create_entry("Segment Name", 123, 125)

segment_size_label = create_label("Segment Size:", 151, 0)

segment_size_entry = create_entry("Segment Size", 153, 125)

Radiobutton(root, text = "First Fit", variable = radio_choice, value = "FF").place(y = 183, x = 0)
Radiobutton(root, text = "Best Fit", variable = radio_choice, value = "BF").place(y = 213, x = 0)

segment_table_label = create_label("Segment Table:", 243, 0)

segment_table_entry = create_entry("Process to Get Table", 245, 125)

segment_table_btn = create_button("Show Segment Table", 239, 290, show_seg_table)

root.mainloop()