import tkinter as tk
from dsmEFlash_monitor import runDSMEFlashMonitor



def testButton():
	print("Button pressed")


def runMonitor():
	runDSMEFlashMonitor()


def main():
	window = tk.Tk()
	frame = tk.Frame(window)
	frame.pack()
	run_button = tk.Button(frame, text="Run",command=runMonitor())

	run_button.pack()

	window.mainloop()

if __name__ == "__main__":
	main()