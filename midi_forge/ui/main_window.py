from pathlib import Path
import os,random
import customtkinter as ctk
from tkinter import filedialog,messagebox
from ..generators import generate_project
from ..midi import export_all,export_track
from ..models import Project,Settings
from .piano_roll import PianoRoll
class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__(); self.title("MIDI Forge"); self.geometry("1180x760"); self.minsize(980,650); ctk.set_appearance_mode("dark")
        self.project=None; self.export_root=Path.cwd()/"exports"
        self.vars={"project_name":ctk.StringVar(value="My Beat"),"root":ctk.StringVar(value="C"),"scale":ctk.StringVar(value="Minor"),"bpm":ctk.StringVar(value="140"),"bars":ctk.StringVar(value="8"),"seed":ctk.StringVar(value="42"),"melody_complexity":ctk.IntVar(value=55),"melody_density":ctk.IntVar(value=55),"swing":ctk.IntVar(value=0),"humanisation":ctk.IntVar(value=0)}
        self.track_vars={}; self._build()
    def _build(self):
        self.grid_columnconfigure(1,weight=1); self.grid_rowconfigure(0,weight=1); panel=ctk.CTkScrollableFrame(self,width=285); panel.grid(row=0,column=0,sticky="nsew",padx=(12,6),pady=12)
        ctk.CTkLabel(panel,text="MIDI FORGE",font=ctk.CTkFont(size=26,weight="bold")).pack(pady=(8,16))
        self._entry(panel,"Project name","project_name"); self._option(panel,"Root key","root",("C","C#","D","D#","E","F","F#","G","G#","A","A#","B")); self._option(panel,"Scale","scale",("Major","Minor")); self._entry(panel,"BPM (40–240)","bpm"); self._option(panel,"Bars","bars",("4","8")); self._entry(panel,"Seed","seed")
        for label,key in (("Melody complexity","melody_complexity"),("Melody density","melody_density"),("Swing","swing"),("Humanisation","humanisation")): self._slider(panel,label,key)
        ctk.CTkButton(panel,text="Generate",height=40,command=self.generate).pack(fill="x",pady=(14,5)); ctk.CTkButton(panel,text="New seed",command=self.random_seed).pack(fill="x",pady=5); ctk.CTkButton(panel,text="Save preset",command=self.save_preset).pack(fill="x",pady=5); ctk.CTkButton(panel,text="Load preset",command=self.load_preset).pack(fill="x",pady=5)
        main=ctk.CTkFrame(self); main.grid(row=0,column=1,sticky="nsew",padx=(6,12),pady=12); main.grid_rowconfigure(1,weight=1); main.grid_columnconfigure(0,weight=1)
        self.status=ctk.CTkLabel(main,text="Choose settings and generate an idea.",anchor="w"); self.status.grid(row=0,column=0,sticky="ew",padx=14,pady=10)
        self.roll=PianoRoll(main); self.roll.grid(row=1,column=0,sticky="nsew",padx=12); self.checks=ctk.CTkFrame(main); self.checks.grid(row=2,column=0,sticky="ew",padx=12,pady=10)
        buttons=ctk.CTkFrame(main,fg_color="transparent"); buttons.grid(row=3,column=0,sticky="ew",padx=12,pady=(0,12))
        for text,cmd in (("Export selected",self.export_selected),("Export all",self.export_everything),("Open export folder",self.open_exports)): ctk.CTkButton(buttons,text=text,command=cmd).pack(side="left",padx=(0,8))
    def _entry(self,parent,label,key): ctk.CTkLabel(parent,text=label,anchor="w").pack(fill="x"); ctk.CTkEntry(parent,textvariable=self.vars[key]).pack(fill="x",pady=(2,8))
    def _option(self,parent,label,key,values): ctk.CTkLabel(parent,text=label,anchor="w").pack(fill="x"); ctk.CTkOptionMenu(parent,variable=self.vars[key],values=list(values)).pack(fill="x",pady=(2,8))
    def _slider(self,parent,label,key): ctk.CTkLabel(parent,text=label,anchor="w").pack(fill="x"); ctk.CTkSlider(parent,variable=self.vars[key],from_=0,to=100).pack(fill="x",pady=(2,8))
    def settings(self): return Settings(project_name=self.vars["project_name"].get().strip(),root=self.vars["root"].get(),scale=self.vars["scale"].get(),bpm=int(self.vars["bpm"].get()),bars=int(self.vars["bars"].get()),seed=int(self.vars["seed"].get()),melody_complexity=self.vars["melody_complexity"].get(),melody_density=self.vars["melody_density"].get(),swing=self.vars["swing"].get(),humanisation=self.vars["humanisation"].get())
    def generate(self):
        try:
            self.project=generate_project(self.settings()); self.roll.draw(self.project)
            for child in self.checks.winfo_children(): child.destroy()
            self.track_vars.clear()
            for name in self.project.tracks:
                var=ctk.BooleanVar(value=True); self.track_vars[name]=var; ctk.CTkCheckBox(self.checks,text=name,variable=var).pack(side="left",padx=8,pady=8)
            self.status.configure(text=f"Generated {self.project.settings.bars} bars • {sum(len(t.notes) for t in self.project.tracks.values())} notes • seed {self.project.settings.seed}")
        except Exception as exc: messagebox.showerror("Generation error",str(exc))
    def random_seed(self): self.vars["seed"].set(str(random.SystemRandom().randrange(1,2147483647))); self.generate()
    def export_selected(self):
        if not self._require_project(): return
        folder=self.export_root/self.project.settings.project_name.replace(" ","_")
        for name,var in self.track_vars.items():
            if var.get(): export_track(self.project.tracks[name],folder/f"{name.lower().replace(' ','_')}.mid",self.project.settings.bpm)
        self.status.configure(text=f"Selected tracks exported to {folder}")
    def export_everything(self):
        if self._require_project():
            folder=export_all(self.project,self.export_root); self.status.configure(text=f"All MIDI exported to {folder}"); messagebox.showinfo("Export complete",str(folder))
    def open_exports(self): self.export_root.mkdir(parents=True,exist_ok=True); os.startfile(self.export_root)
    def save_preset(self):
        try:
            path=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("JSON","*.json")])
            if path: self.settings().save(Path(path))
        except Exception as exc: messagebox.showerror("Preset error",str(exc))
    def load_preset(self):
        path=filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not path:return
        try:
            settings=Settings.load(Path(path))
            for key in self.vars:self.vars[key].set(getattr(settings,key))
            self.generate()
        except Exception as exc:messagebox.showerror("Preset error",str(exc))
    def _require_project(self):
        if self.project is None: messagebox.showwarning("Nothing generated","Generate a project first."); return False
        return True
