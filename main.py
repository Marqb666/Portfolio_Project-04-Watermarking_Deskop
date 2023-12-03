from tkinter import colorchooser
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import *
from tkinter import ttk
import os
from PIL import ImageTk,Image, ImageFont, ImageDraw


window = tk.Tk()
window.title('Watermark')

window.columnconfigure(1,weight=1,minsize=800)
window.rowconfigure(0,weight=1,minsize=600)

color_red = 255
color_green = 255
color_blue = 255
alpha_text = 150
choosen_color_name = '#ffffff'

txt=Image.new('RGBA',(0,0), (255,255,255,0))
text_orientation = 0


h= ttk.Scrollbar(window, orient=HORIZONTAL)
v = ttk.Scrollbar(window, orient=VERTICAL)
canvas = Canvas(window, scrollregion=(0, 0, 10000, 10000), yscrollcommand=v.set, xscrollcommand=h.set, background='white' )
h['command'] = canvas.xview
v['command'] = canvas.yview

canvas.grid(column=1, row=0, sticky='nsew')
h.grid(column=1, row=1, sticky='ew')
v.grid(column=2, row=0, sticky='ns')

frm_button = tk.Frame(master=window, relief=tk.RAISED,borderwidth=2)
frm_button.grid(row=0,column=0,rowspan=2,sticky='ns')

lbl_warning = tk.Label(canvas,text='Press open to find image',foreground='black',relief=tk.RAISED,width=30, height=12, anchor=CENTER, font=('Times New Roman',30))
lbl_warning.pack(pady=20,padx=10)

def open_to_edit():
    global img_id01, im01, image_main, filepath
    filepath = fd.askopenfilename(
        filetypes=[("All Files", "*.*")])
    if filepath:
        entry_width.delete(0, tk.END)
        entry_higth.delete(0, tk.END)
        image_main = Image.open(filepath,mode='r').convert('RGBA')
        im01 = ImageTk.PhotoImage(image_main)
        img_id01 = canvas.create_image(25,25,image=im01, anchor='nw')
        entry_width.insert(0,str(image_main.size[0]))
        entry_higth.insert(0,str(image_main.size[1]))
        canvas.itemconfig(tagOrId=img_id01)
        btn_resize['state']='active'
        btn_txt['state']='active'
        lbl_warning.destroy()
    else:
        return
    window.title(f"Watermark - {filepath}")

def resize():
    global img_id01,im01, image_main, txt
    width = int(entry_width.get())
    higth = int(entry_higth.get())
    image_main = image_main.resize((width,higth))
    im01 = ImageTk.PhotoImage(image_main)
    img_id01=canvas.create_image(25, 25, image=im01, anchor='nw')
    canvas.itemconfig(tagOrId=img_id01)
    txt = Image.new('RGBA', image_main.size, (255, 255, 255, 0))
    btn_save['state'] = 'active'
def text():
    global draw_text, img_id01, im01,image_main,txt, text_orientation,txt
    try:
        text_to_put = text_window.get('1.0',tk.END)
        font_size=int(combobox_size.get())
        font_type = combobox_font.get() + '.ttf'
        font = ImageFont.truetype(f"Noto_Sans/{font_type}", font_size)
        txt=Image.new('RGBA',image_main.size, (255,255,255,0))
        draw_text = ImageDraw.Draw(txt)

        x = int(ent_x_text.get())
        y = int(ent_y_text.get())

        alpha = int(combbox_alpha.get())
        text_orientation = int(combobox_orientation.get())

        fill = (color_red,color_green,color_blue,alpha)
        draw_text.text((x, y), text=text_to_put, font=font, fill=fill,)
        out= Image.alpha_composite(image_main,txt.rotate(text_orientation, center=(image_main.size[0]/2,image_main.size[1]/2)))
        im01 = ImageTk.PhotoImage(out)
        print(image_main.size[0]/2)
        img_id01 = canvas.create_image(25, 25, image=im01, anchor='nw')
        canvas.itemconfig(tagOrId=img_id01)
        btn_save['state'] = 'active'

    except NameError:
        print('Choose the image')
def choose_color():
    global choosen_color_name,color_red,color_green,color_blue
    choosen_color = colorchooser.askcolor(initialcolor='#000000')
    choosen_color_name = choosen_color[1]
    color_red = choosen_color[0][0]
    color_green = choosen_color[0][1]
    color_blue = choosen_color[0][2]
    lbl_color.configure(background=choosen_color_name)
def close():
    btn_txt['state']='normal'
    btn_txt.config(state='normal')
    windowb.destroy()
def text_edit():
    global out, text_window, combobox_size, combobox_font, lbl_color, windowb, btn_txt, ent_x_text, ent_y_text,combbox_alpha,combobox_orientation
    windowb = Toplevel(window)
    windowb.resizable(False,False)
    windowb.title('Text edition')
    windowb.columnconfigure(0, weight=1, minsize=200)
    windowb.rowconfigure(1, weight=1, minsize=200)
    frm_top = tk.Frame(windowb, relief=tk.RAISED,borderwidth=3)
    frm_middle = tk.Frame(windowb, relief=tk.RAISED, borderwidth=3)
    frm_bottom = tk.Frame(windowb, relief=tk.RAISED, borderwidth=3)


    text_window = tk.Text(frm_middle, background='white', width=65, height=20)
    v = ttk.Scrollbar(frm_middle, orient=VERTICAL,command=text_window.yview)
    text_window.configure(yscrollcommand=v.set)


    combobox_font = ttk.Combobox(frm_top,width=15)
    path = "Noto_Sans"
    list_of_files = os.listdir(path)
    list_of_fonts =[file.split('.')[0] for file in list_of_files]
    combobox_font['values'] = list_of_fonts
    combobox_font.set(list_of_fonts[0])
    combobox_font.state(['readonly'])

    combobox_size = ttk.Combobox(frm_top,width=15)
    list_of_values = [n for n in range(1001)]
    combobox_size['values'] = list_of_values
    combobox_size.set(40)
    combobox_size.state(['readonly'])

    btn_color = tk.Button(frm_top, text='Color', command=choose_color, width=10)
    btn_put_on_picture = tk.Button(frm_bottom, text='Put Watermark', command=text)
    btn_close = tk.Button(frm_bottom, text='Close', command=close)


    ent_x_text = tk.Entry(width=5, master=frm_top)
    ent_x_text.insert(index=0, string='5')
    ent_y_text = tk.Entry(width=5,master=frm_top)
    ent_y_text.insert(index=0,string='5')

    values_alpha = [n for n in range(256)]
    combbox_alpha = ttk.Combobox(master=frm_top, values=values_alpha, state='readonly',width=5)
    combbox_alpha.set(100)

    values_oreintation = [n for n in range(361)]
    combobox_orientation = ttk.Combobox(master=frm_top, values=values_oreintation, state='readonly',width=5)
    combobox_orientation.set(0)

    lbl_x_coordinate = tk.Label(frm_top,text='X:')
    lbl_y_coordinate = tk.Label(frm_top,text='Y:')
    lbl_alpha = tk.Label(frm_top,text='alpha:')
    lbl_orientation = tk.Label(frm_top,text='orientation:')
    lbl_color = tk.Label(frm_top, background=choosen_color_name, relief=tk.RAISED,width=30)
    lbl_font= tk.Label(frm_top, text='font:')
    lbl_size = tk.Label(frm_top, text='size:')
    lbl_where = tk.Label(frm_top, text='Where to put:')

    frm_top.grid(row=0,columnspan=2,sticky='nsew')
    frm_middle.grid(row=1,column=0, sticky='nsew')
    frm_bottom.grid(row=2,columnspan=2, sticky='nsew')


    lbl_font.grid(row=0,column=0, sticky='w', pady=5, padx=5)
    combobox_font.grid(row=0, column=1, sticky='w')
    lbl_size.grid(row=1, column=0, sticky='w', pady=5, padx=5)
    combobox_size.grid(row=1, column=1)
    lbl_alpha.grid(row=0, column=2, sticky='w', pady=5, padx=5)
    combbox_alpha.grid(row=0, column=3)
    lbl_orientation.grid(row=1, column=2, sticky='ew', pady=5, padx=5)
    combobox_orientation.grid(row=1,column=3)
    lbl_where.grid(row=0, column=4,columnspan=5, sticky='nsew')
    lbl_x_coordinate.grid(row=1,column=4, sticky='e', padx=5)
    ent_x_text.grid(row=1, column=5, sticky='w', )
    lbl_y_coordinate.grid(row=1, column=6, sticky='e',padx=5)
    ent_y_text.grid(row=1, column=7,sticky='w')
    btn_color.grid(row=2, column=0, padx=5,pady=5)
    lbl_color.grid(row=2,column=1, columnspan=7, padx=10,pady=5, sticky='nsew')

    v.grid(column=1, row=0, sticky='ns')

    text_window.grid(row=0, column=0, sticky='ns')

    btn_put_on_picture.grid(row=3, column=0, padx=150, pady=10,sticky='e')
    btn_close.grid(row=3, column=5, padx=50,pady=10)

    btn_txt['state']='disabled'
    windowb.protocol("WM_DELETE_WINDOW", close)

def save_as():
    global out
    filepath = fd.asksaveasfilename(
        defaultextension='png',
        filetypes=[("Image Files", "*.png"), ("All Files", "*.*")]
        )
    if filepath:
        out = Image.alpha_composite(image_main, txt.rotate(text_orientation,center=(image_main.size[0] / 2, image_main.size[1] / 2)))
        out.save(filepath)
        window.title(f"Simple Watermark Editor - {filepath}")

    else:
        return


btn_open = tk.Button(master=frm_button,width=10, text='Open', command=open_to_edit, background='red',foreground='black',)
btn_open.grid(row=0,column=0, padx=5,pady=5, sticky='ew')

lbl_width = tk.Label(width=10, master=frm_button, text='Width Px')
lbl_width.grid(row=1,column=0, sticky='ew')

entry_width = tk.Entry(width=10,master=frm_button)
entry_width.grid(row=2,column=0,padx=5, pady=0, sticky='ew')

lbl_width = tk.Label(width=10, master=frm_button, text='Higth Px')
lbl_width.grid(row=3,column=0, sticky='ew')


entry_higth = tk.Entry(width=10, master=frm_button)
entry_higth.grid(row=4, column=0, padx=5, pady=0, sticky='ew')

btn_resize = tk.Button(master=frm_button,width=10, text='Resize', command=resize, state='disabled')
btn_resize.grid(row=5,column=0,padx=5, pady=5, sticky='ew')

btn_txt = tk.Button(master=frm_button,width=10, text='Text on', command=text_edit, state='disabled')
btn_txt.grid(row=6,column=0,padx=5, pady=5, sticky='ew')

btn_save = tk.Button(master=frm_button,width=10, text='Save As...',command=save_as, state='disabled')
btn_save.grid(row=7,column=0,padx=5, pady=5, sticky='ew' )


window.mainloop()







