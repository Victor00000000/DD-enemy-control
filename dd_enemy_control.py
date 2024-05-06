import tkinter as tk
from tkinter import filedialog as fd
from tkinter import colorchooser
import re
import math
from easysettings import EasySettings

root = tk.Tk()
root.title('Encounter Controller')
root.geometry('1000x700')
# root.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}')
# root.state('zoomed')
#root.attributes('-fullscreen', True)
menubar = tk.Menu(root)
root.config(menu=menubar)
file_menu = tk.Menu(menubar, tearoff=False)
edit_menu = tk.Menu(menubar, tearoff=False)

settings = EasySettings('EncController.conf')
franesizes = {'framewidth': 234, 'frameheight': 242}
current_frame = None
click_callback = None
enemies = []
framenum = 0
if settings.has_option('column_num'):
    columns = settings.get('column_num')
else:
    columns = 3
    settings.set('column_num', 3)


def apply_damage():
    currdam = root.nametowidget(
        f'{current_frame.winfo_name()}.dam').cget('text')
    if currdam == '':
        return
    else:
        currdam = int(currdam)
        if current_frame.quartervar.get():
            currdam = math.ceil(currdam / 4)
        elif current_frame.checkvar.get():
            currdam = math.ceil(currdam / 2)
    hptext = root.nametowidget(
        f'{current_frame.winfo_name()}.hist').cget('text')
    left = hptext.split('=')[0]
    damage = re.split('([-\+])', left)
    orighp = int(damage.pop(0))

    intdam = 0
    sdam = ''
    for i in range(0, len(damage), 2):
        if damage[i] == '-':
            intdam += int(damage[i+1])
            sdam += f'-{damage[i+1]}'
        else:
            intdam -= int(damage[i+1])
            sdam += f'+{damage[i+1]}'
    intdam += currdam
    sdam += f'-{currdam}'

    root.nametowidget(f'{current_frame.winfo_name()}.hist').config(
        text=f'{orighp}{sdam}={orighp-intdam}')
    root.nametowidget(f'{current_frame.winfo_name()}.dam').config(text='')
    root.nametowidget(f'{current_frame.winfo_name()}.hp').config(
        text=f'{orighp-intdam}')


def apply_heal():
    currdam = root.nametowidget(
        f'{current_frame.winfo_name()}.dam').cget('text')
    if currdam == '':
        return
    else:
        currdam = int(currdam)
    hptext = root.nametowidget(
        f'{current_frame.winfo_name()}.hist').cget('text')
    left = hptext.split('=')[0]
    #damage = left.split('-|+')
    damage = re.split('([-\+])', left)
    orighp = int(damage.pop(0))

    intdam = 0
    sdam = ''
    for i in range(0, len(damage), 2):
        if damage[i] == '-':
            intdam += int(damage[i+1])
            sdam += f'-{damage[i+1]}'
        else:
            intdam -= int(damage[i+1])
            sdam += f'+{damage[i+1]}'
    intdam -= currdam
    sdam += f'+{currdam}'

    root.nametowidget(f'{current_frame.winfo_name()}.hist').config(
        text=f'{orighp}{sdam}={orighp-intdam}')
    root.nametowidget(f'{current_frame.winfo_name()}.dam').config(text='')
    root.nametowidget(f'{current_frame.winfo_name()}.hp').config(
        text=f'{orighp-intdam}')


def button_number(num):
    curr = root.nametowidget(f'{current_frame.winfo_name()}.dam').cget('text')
    if curr == '' and num == 0:
        return
    root.nametowidget(f'{current_frame.winfo_name()}.dam').config(
        text=f'{curr}{num}')


def button_clr():
    root.nametowidget(f'{current_frame.winfo_name()}.dam').config(text='')


def button_undo():
    hptext = root.nametowidget(
        f'{current_frame.winfo_name()}.hist').cget('text')
    left = hptext.split('=')[0]
    damage = re.split('([-\+])', left)
    orighp = int(damage.pop(0))
    if len(damage) <= 1:
        root.nametowidget(f'{current_frame.winfo_name()}.hist').config(
            text=f'{orighp}')
        root.nametowidget(f'{current_frame.winfo_name()}.hp').config(
            text=f'{orighp}')
        return

    damage.pop(-1)
    damage.pop(-1)
    intdam = 0
    sdam = ''
    for i in range(0, len(damage), 2):
        if damage[i] == '-':
            intdam += int(damage[i+1])
            sdam += f'-{damage[i+1]}'
        else:
            intdam -= int(damage[i+1])
            sdam += f'+{damage[i+1]}'

    root.nametowidget(f'{current_frame.winfo_name()}.hist').config(
        text=f'{orighp}{sdam}={orighp-intdam}')
    root.nametowidget(f'{current_frame.winfo_name()}.hp').config(
        text=f'{orighp-intdam}')


def create_frame(name, HP, color='#FFFFFF'):
    frame = tk.Frame(root, relief=tk.RAISED, borderwidth=3)
    global framenum

    def change_current_frame(event):
        global current_frame
        current_frame = frame

    def click(event):
        global click_callback
        if click_callback is not None:
            click_callback(frame)

    label = tk.Label(frame, text=name, width=10, anchor='w')
    label.grid(column=1, row=0, padx=5, pady=5)
    col = tk.Frame(frame, bg=color, width=50, height=30)
    col.grid(column=2, row=0)
    lbl_HP = tk.Label(frame, text='HP')
    lbl_HP.grid(column=0, row=1)
    lbl_HP_hist = tk.Label(
        frame, text=f'{HP}', name='hist', width=10, anchor='e')
    lbl_HP_hist.grid(column=1, row=1)
    lbl_HP_curr = tk.Label(
        frame, text=f'{HP}', name='hp', font=('Helvetica', 14))
    lbl_HP_curr.grid(column=2, row=1)
    lbl_Dam = tk.Label(frame, text='Damage')
    lbl_Dam.grid(column=0, row=2)
    lbl_Dam_curr = tk.Label(frame, text='', name='dam', width=10)
    lbl_Dam_curr.grid(column=1, row=2)
    btn_1 = tk.Button(frame, text='1', name=f'1', width=4,
                      command=lambda: button_number(1))
    btn_1.grid(column=0, row=3)
    btn_2 = tk.Button(frame, text='2', name=f'2', width=4,
                      command=lambda: button_number(2))
    btn_2.grid(column=1, row=3)
    btn_3 = tk.Button(frame, text='3', name=f'3', width=4,
                      command=lambda: button_number(3))
    btn_3.grid(column=2, row=3)
    btn_4 = tk.Button(frame, text='4', name=f'4', width=4,
                      command=lambda: button_number(4))
    btn_4.grid(column=0, row=4)
    btn_5 = tk.Button(frame, text='5', name=f'5', width=4,
                      command=lambda: button_number(5))
    btn_5.grid(column=1, row=4)
    btn_6 = tk.Button(frame, text='6', name=f'6', width=4,
                      command=lambda: button_number(6))
    btn_6.grid(column=2, row=4)
    btn_7 = tk.Button(frame, text='7', name=f'7', width=4,
                      command=lambda: button_number(7))
    btn_7.grid(column=0, row=5)
    btn_8 = tk.Button(frame, text='8', name=f'8', width=4,
                      command=lambda: button_number(8))
    btn_8.grid(column=1, row=5)
    btn_9 = tk.Button(frame, text='9', name=f'9', width=4,
                      command=lambda: button_number(9))
    btn_9.grid(column=2, row=5)
    btn_0 = tk.Button(frame, text='0', name=f'0', width=4,
                      command=lambda: button_number(0))
    btn_0.grid(column=0, row=6)
    btn_clr = tk.Button(frame, text='Clear', name=f'clr', command=button_clr)
    btn_clr.grid(column=1, row=6)
    btn_undo = tk.Button(frame, text='Undo', name=f'un', command=button_undo)
    btn_undo.grid(column=2, row=6)
    checkvar = tk.IntVar()
    quartervar = tk.IntVar()
    btn_res = tk.Checkbutton(frame, text='1/2 Damage',
                             variable=checkvar, name=f'{framenum}check')
    btn_quarter = tk.Checkbutton(
        frame, text='1/4 Damage', variable=quartervar, name=f'{framenum}quarter')
    frame.framenum = framenum
    frame.checkvar = checkvar
    frame.quartervar = quartervar
    framenum += 1
    btn_res.grid(column=0, row=7)
    btn_quarter.grid(column=0, row=8)
    btn_dam = tk.Button(frame, text='Apply damage',
                        name=f'apply', command=apply_damage)
    btn_dam.grid(column=1, row=7, columnspan=2)

    btn_heal = tk.Button(frame, text='Apply heal',
                         name=f'heal', command=apply_heal)
    btn_heal.grid(column=1, row=8, columnspan=2)

    if settings.get('show_notes'):
        nn = tk.Text(frame, name='notes', width=28, height=4)
        nn.grid(column=0, row=9, columnspan=3)

    frame.bind('<Enter>', change_current_frame)
    frame.bind('<Button-1>', click)

    return frame


def add_new():
    wind = tk.Toplevel(root)
    na = tk.StringVar()
    n = tk.Label(wind, text='Name:')
    n.grid(column=0, row=0)
    name_entry = tk.Entry(wind, textvariable=na)
    na.set('Monster')
    name_entry.grid(column=1, row=0)
    h = tk.Label(wind, text='HP:')
    h.grid(column=0, row=1)
    hp = tk.StringVar()
    hp_entry = tk.Entry(wind, textvariable=hp)
    hp.set('10')
    hp_entry.grid(column=1, row=1)
    c = tk.Label(wind, text='Color:')
    c.grid(column=0, row=2)
    color_sh = tk.Frame(wind, bg='#FFFFFF', width=50, height=30)
    color_sh.grid(column=1, row=2)

    def change_color():
        color_code = colorchooser.askcolor(title='Pick new Color')
        color_sh.config(bg=color_code[1])
        wind.focus()

    color_btn = tk.Button(wind, text='Pick new Color', command=change_color)
    color_btn.grid(column=2, row=2)

    def add_card():
        card = create_frame(na.get(), hp.get(), color_sh.cget('bg'))
        enemies.append(card)
        pack_creatures()
        wind.destroy()

    submit_btn = tk.Button(wind, text='Add Card', command=add_card)
    submit_btn.grid(column=0, row=4)
    wind.focus()


def pack_creatures():
    # print(f'{columns = }')
    # print(f'{len(enemies) = }')
    # print(f'{columns * enemies[0].winfo_width() = }')
    # print(
    #     f'{math.ceil(len(enemies) / columns) * enemies[0].winfo_height() = }')
    w = franesizes["framewidth"]
    h = franesizes["frameheight"]
    if settings.get('show_notes'):
        h += 70
    for i, e in enumerate(enemies):
        e.grid(column=i % columns, row=i // columns)
    root.geometry(
        f'{columns * w}x{math.ceil(len(enemies) / columns) * h}')


def read_file(fn):
    with open(fn, 'r') as f:
        creatures = []
        for row in f:
            if row[0:3] == '---':
                creatures.append(creature)
                continue
            if row[0] == '#':
                continue
            ssrow = row.split(':')
            if ssrow[0].lower() == 'name':
                creature = {'name': ssrow[1].strip(
                ), 'hp': 10, 'color': '#FFFFFF'}
            elif ssrow[0].lower() == 'hp':
                creature['hp'] = ssrow[1].strip()
            elif ssrow[0].lower() == 'color':
                creature['color'] = ssrow[1].strip()
        for c in creatures:
            fr = create_frame(c['name'], c['hp'], color=c['color'])
            enemies.append(fr)
    pack_creatures()


def open_file():
    filetypes = (('text files', '*.txt'), ('all files', '*.*'))
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )
    read_file(filename)


def close_file():
    global enemies
    for e in enemies:
        e.destroy()
    enemies = []


def set_close_card():
    global click_callback

    def close_card(fr):
        global click_callback
        for e in enemies:
            if e == fr:
                fr.destroy()
                enemies.remove(e)
        click_callback = None

    click_callback = close_card


def open_options():
    wind = tk.Toplevel(root)
    relief = tk.Label(wind, text='Relief:')
    n = tk.StringVar()
    if settings.has_option('relief'):
        n.set(settings.get('relief'))
    else:
        settings.set('relief', 'Raised')
        n.set('Raised')

    def applyrelief(val):
        for e in enemies:
            if val == 'Flat':
                e.config(relief=tk.FLAT)
            elif val == 'Raised':
                e.config(relief=tk.RAISED)
            elif val == 'Sunken':
                e.config(relief=tk.SUNKEN)
            elif val == 'Groove':
                e.config(relief=tk.GROOVE)
            elif val == 'Ridge':
                e.config(relief=tk.RIDGE)

    def addNotes():
        settings.set('show_notes', True)
        for f in enemies:
            nn = tk.Text(f, name='notes', width=28, height=4)
            nn.grid(column=0, row=9, columnspan=3)
        pack_creatures()

    def deleteNotes():
        settings.set('show_notes', False)
        for e in enemies:
            e.nametowidget('notes').destroy()
        pack_creatures()

    relief_select = tk.OptionMenu(
        wind, n, 'Flat', 'Raised', 'Sunken', 'Groove', 'Ridge', command=applyrelief)

    relief.grid(column=0, row=0)
    relief_select.grid(column=1, row=0)

    cols = tk.Label(wind, text='Number of columns:')
    cols.grid(column=0, row=1)
    ent = tk.Entry(wind)
    ent.grid(column=1, row=1)

    def applycols():
        n = int(ent.get())
        global columns
        columns = n
        pack_creatures()
    colbtn = tk.Button(wind, text='Apply', command=applycols)
    colbtn.grid(column=2, row=1)

    add_notes_btn = tk.Button(wind, text='Add Notes', command=addNotes)
    add_notes_btn.grid(column=1, row=2)

    del_notes_btn = tk.Button(wind, text='Remove Notes', command=deleteNotes)
    del_notes_btn.grid(column=2, row=2)


# enemy1 = create_frame('goblin 1', '10', 'gold')
# enemy2 = create_frame('goblin 2', 11, 'grey35')
# enemies = [enemy1, enemy2]
# pack_creatures()


file_menu.add_command(label='Open...', command=open_file)
file_menu.add_command(label='Close', command=close_file)
file_menu.add_command(label='New Card', command=add_new)
file_menu.add_command(label='Close Card', command=set_close_card)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.destroy)
menubar.add_cascade(label='File', menu=file_menu)

edit_menu.add_command(label='Options', command=open_options)
menubar.add_cascade(label='Edit', menu=edit_menu)

root.mainloop()
