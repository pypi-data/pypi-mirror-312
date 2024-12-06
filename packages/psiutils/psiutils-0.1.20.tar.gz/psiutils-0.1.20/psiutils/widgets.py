"""Various Tkinter widgets and methods."""
import tkinter as tk
from tkinter import ttk
import contextlib

from .constants import PAD, COLOURS
HAND = 'hand2'
DIM_TEXT = '#555'


class PsiText(tk.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that reports on internal widget commands."""
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = f"{self._w}_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result


def get_styles() -> ttk.Style:
    style = ttk.Style()
    # Labels - foreground
    style.configure('red-fg.TLabel', foreground='red')
    style.configure('green-fg.TLabel', foreground='green')
    style.configure('blue-fg.TLabel', foreground='blue')
    style.configure('yellow-fg.TLabel', foreground='yellow')
    style.configure('grey-fg.TLabel', foreground='grey')
    style.configure('orange-fg.TLabel', foreground='orange')

    # Labels - background
    style.configure('red-bg.TLabel', background='red')
    style.configure('green-bg.TLabel', background='green')
    style.configure('blue-bg.TLabel', background='blue')
    style.configure('yellow-bg.TLabel', background='yellow')
    style.configure('grey-bg.TLabel', background='grey')
    style.configure('orange-bg.TLabel', background='orange')

    # Entries - background
    style.configure('grey-bg.TEntry', fieldbackground='grey')
    style.configure('pale-grey-bg.TEntry', fieldbackground=COLOURS['pale-grey'])

    style.configure('red-bg.TEntry', fieldbackground='red')
    style.configure('green-bg.TEntry', fieldbackground='green')
    style.configure('orange-bg.TEntry', fieldbackground='orange')
    style.configure(
        'pale-umber-bg.TEntry', fieldbackground=COLOURS['pale-umber'])
    style.configure(
        'pale-red-bg.TEntry', fieldbackground=COLOURS['pale-red'])

    # Entries - foreground
    style.configure('red-fg.TEntry', foreground='red')
    style.configure('green-fg.TEntry', foreground='green')
    style.configure('orange-fg.TEntry', foreground='orange')

    # Frames
    style.configure('red.TFrame', background='red')
    style.configure('green.TFrame', background='green')
    style.configure('blue.TFrame', background='blue')
    style.configure('yellow.TFrame', background='yellow')
    style.configure('grey.TFrame', background='grey ')

    # Tree view
    style.map('Treeview',
              foreground=fixed_map(style, 'foreground'),
              background=fixed_map(style, 'background'))

    return style


def fixed_map(style, option):
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out

    # style.map() returns an empty list for missing options, so this should
    # be future-safe
    return [elm for elm in style.map('Treeview', query_opt=option)
            if elm[:2] != ('!disabled', '!selected')]


def vertical_scroll_bar(
        master: tk.Frame,
        widget: tk.Widget,
        ) -> ttk.Scrollbar:

    v_scroll = ttk.Scrollbar(
        master,
        orient='vertical',
        command=widget.yview
        )
    widget.configure(yscrollcommand=v_scroll.set)
    widget['yscrollcommand'] = v_scroll.set
    return v_scroll


def enter_widget(event: object = None) -> None:
    if tk.DISABLED in event.widget.state():
        return
    event.widget.winfo_toplevel().config(cursor=HAND)


def _leave_widget(event: object = None) -> None:
    event.widget.winfo_toplevel().config(cursor='')


def clickable_widget(widget: object) -> None:
    widget.bind('<Enter>', enter_widget)
    widget.bind('<Leave>', _leave_widget)


def status_bar(master: tk.Frame, textvariable: tk.StringVar,
               colour: str = DIM_TEXT) -> tk.Frame:
    frame = ttk.Frame(master, relief=tk.SUNKEN)
    frame.columnconfigure(1, weight=1)
    label = tk.Label(frame, fg=colour, textvariable=textvariable)
    label.grid(row=0, column=0, sticky=tk.W, padx=PAD, pady=1)
    return frame


@contextlib.contextmanager
def WaitCursor(root):
    root.config(cursor='watch')
    root.update()
    try:
        yield root
    finally:
        root.config(cursor='')


def separator_frame(master: tk.Frame, text: str) -> tk.Frame:
    frame = ttk.Frame(master)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(2, weight=1)

    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=0, column=0, sticky=tk.EW, padx=PAD, pady=PAD*4)

    label = ttk.Label(frame, text=text)
    label.grid(row=0, column=1, sticky=tk.E)

    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=0, column=2, sticky=tk.EW, padx=PAD)
    return frame


class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.grid(row=0, column=1, sticky=tk.NS)

        self.canvas = tk.Canvas(
            self,
            bd=0,
            width=200, height=300,
            yscrollcommand=vscrollbar.set)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        vscrollbar.config(command=self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.interior = ttk.Frame(self.canvas)
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.interior_id = self.canvas.create_window(
            0, 0, window=self.interior, anchor=tk.NW)

    def _configure_interior(self, event):
        # Update the scroll bars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(),
                self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(
                self.interior_id, width=self.canvas.winfo_width())
