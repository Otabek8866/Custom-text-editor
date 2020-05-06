import tkinter
from tkinter import messagebox, filedialog
from os.path import split

class MyTextClass(tkinter.Text):
	KEY_WORDS = ['class', 'def', '']
	def high_light(self):
		pass

	def searching_words(self):
		pass


class TextEditor(object):

	def __init__(self):
		# Creating a main window
		self._main_window = tkinter.Tk()
		self._main_window.geometry('800x600+300+100')
		self._main_window.title('Boost Text Editor')
		
		# Creating object variables
		self._filename = None
		self._title = tkinter.StringVar()

		# Creating a title bar
		self._title_bar = tkinter.Label(self._main_window, textvariable=self._title, 
										font=('times new roman', 12, 'italic'), bd=1, relief=tkinter.GROOVE)
		self._title_bar.pack(side=tkinter.TOP, fill=tkinter.BOTH)
		self.settitle()

		# Creating a menu bar
		self._menu_bar = tkinter.Menu(self._main_window, font=('times new roman', 12, 'italic'), 
										activebackground='blue', tearoff=0)
		self._main_window.config(menu=self._menu_bar)

		# Creating a file menu
		self._file_menu = tkinter.Menu(self._menu_bar, font=('times new roman', 12, 'italic'),
										activebackground='blue', tearoff=0)
		self._file_menu.add_command(label='New', accelerator='Ctrl+N', command=self.newfile)
		self._file_menu.add_command(label='Open', accelerator='Ctrl+O', command=self.openfile)
		self._file_menu.add_command(label='Save', accelerator='Ctrl+S', command=self.savefile)
		self._file_menu.add_command(label='Save As', accelerator='Ctrl+A', command=self.saveasfile)
		self._file_menu.add_separator()
		self._file_menu.add_command(label='Exit', accelerator='Ctrl+E', command=self._closing_main_window)

		# Adding file menu to the main menu bar
		self._menu_bar.add_cascade(label="File", menu=self._file_menu)

		# Creating the edit menu
		self._edit_menu = tkinter.Menu(self._menu_bar, font=('times new roman', 12, 'italic'), 
										activebackground='blue', tearoff=0)
		self._edit_menu.add_command(label='Cut', accelerator='Ctrl+C', command=self.cut)
		self._edit_menu.add_command(label='Copy', accelerator='Ctrl+V', command=self.copy)
		self._edit_menu.add_command(label='Paste', accelerator='Ctrl+P', command=self.paste)
		self._edit_menu.add_separator()
		self._edit_menu.add_command(label='Undo', accelerator='Ctrl+Z')
		self._edit_menu.add_command(label='Redo', accelerator='Ctrl+Y')
		
		# Adding file menu to the main menu bar
		self._menu_bar.add_cascade(label="Edit", menu=self._edit_menu)

		# Creating the help menu
		self._help_menu = tkinter.Menu(self._menu_bar, font=('times new roman', 12, 'italic'), 
										activebackground='blue', tearoff=0)
		self._help_menu.add_command(label='About', accelerator='Ctrl+C', command=self.infoabout)
		self._help_menu.add_command(label='Help', accelerator='Ctrl+V', command=self._help_menu)
		
		# Adding help menu to the main menu bar
		self._menu_bar.add_cascade(label="Help", menu=self._help_menu)

		# Creating a scroll bar
		y_scroll_bar = tkinter.Scrollbar(self._main_window, orient=tkinter.VERTICAL)
		x_scroll_bar = tkinter.Scrollbar(self._main_window, orient=tkinter.HORIZONTAL)

		# Creating Text Area
		self._text_area = tkinter.Text(self._main_window, yscrollcommand=y_scroll_bar.set, xscrollcommand=x_scroll_bar.set,
									font=('times new roman', 14), state='normal', relief=tkinter.GROOVE,
									undo=True)
		y_scroll_bar.pack(side='right', fill='y')
		y_scroll_bar.config(command=self._text_area.yview)
		x_scroll_bar.pack(side='bottom', fill='x')
		x_scroll_bar.config(command=self._text_area.xview)

		self._text_area.pack(fill='both', expand=True)

		self.shortcuts()
	
	def settitle(self):
		if self._filename:
			self._title.set(self._filename)
		else:
			self._title.set("Untitled")

	def newfile(self, *args):
		if self._text_area.edit_modified():
			self.savefile()
		self._text_area.delete('1.0', tkinter.END)
		self._filename = None
		self.settitle()

	def openfile(self, *args):
		try:
			self._filename = filedialog.askopenfilename(title="Select file",
							filetypes=(('All Files', '.'), ("Text Files", '*.txt'), ('Python Files','*.py')))

			if self._filename:
				with open(self._filename, 'r') as readfile:
					self._text_area.delete('1.0', tkinter.END)
					for line in readfile.readlines():
						self._text_area.insert(tkinter.END, line)

				self.settitle()

		except Exception as e:
			messagebox.showerror(title="Error", message=str(e))

	def savefile(self, *args):
		try:
			if self._filename:
				data = self._text_area.get('0.1', tkinter.END)

				with open(self._filename, 'w') as outfile:
					outfile.write(data)

				self.settitle()
				return True
			else:
				return self.saveasfile()

		except Exception as e:
			messagebox.showerror(title="Error", message=str(e))

		
	def saveasfile(self, *args):
		try:
			path = filedialog.asksaveasfilename(title='Save File As', defaultextension='.txt',
				initialfile="Untitled.txt", filetypes=(('All Files', '.'), ("Text Files", '*.txt'), ('Python Files','*.py')))
			untitledfile = split(path)[1]

			if not untitledfile:
				return False

			data = self._text_area.get('0.1', tkinter.END)

			with open(untitledfile, 'w') as outfile:
				outfile.write(data)

			self._filename = untitledfile
			self.settitle()
			return True
		except Exception as e:
			messagebox.showerror(title="Error", message=str(e))

	def cut(self, *args):
		self._text_area.event_generate('<<Cut>>')

	def copy(self, *args):
		self._text_area.event_generate('<<Copy>>')

	def paste(self, *args):
		self._text_area.event_generate('<<Paste>>')

	def infoabout(self):
		messagebox.showinfo(title="About Boost Text Editor", message='Just a simple text editor created for fun in python :)')

	def shortcuts(self):
		self._text_area.bind("<Control-n>", self.newfile)
		self._text_area.bind("<Control-o>", self.openfile)
		self._text_area.bind("<Control-s>", self.savefile)
		self._text_area.bind("<Control-a>", self.saveasfile)
		self._text_area.bind("<Control-e>", self._closing_main_window)
		self._text_area.bind("<Control-x>", self.cut)
		self._text_area.bind("<Control-c>", self.copy)
		self._text_area.bind("<Control-v>", self.paste)
		
	def _closing_main_window(self):
		if self._text_area.edit_modified():
			answer = messagebox.askyesno("Do you want to save this file?")
			result = True
			if answer:
				if not self._filename:
					result = self.saveasfile()
				else:
					result = self.savefile()
		if result:
			self._main_window.destroy()
	
	def start(self):
		self._main_window.protocol("WM_DELETE_WINDOW", self._closing_main_window)
		self._main_window.mainloop()
		

if __name__ == "__main__":
	
	text_editor = TextEditor()
	text_editor.start()
