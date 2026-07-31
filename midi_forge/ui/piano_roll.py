import customtkinter as ctk
from ..models import Project
COLORS={"Melody":"#59d9ff","Chords":"#a979ff","Bass":"#ff9e55","Kick":"#ff4f6d","Snare":"#ffd65a","Closed Hat":"#74e08a"}
class PianoRoll(ctk.CTkCanvas):
    """Read-only, scrollable piano roll prepared for later editing."""
    def __init__(self,master):
        super().__init__(master,bg="#10131a",highlightthickness=0,xscrollincrement=1)
        self.zoom=26; self.project=None; self.configure(xscrollcommand=lambda *_:None)
    def draw(self,project):
        self.project=project; self.delete("all"); width=max(self.winfo_width(),round(project.length_beats*self.zoom)); height=360
        self.configure(scrollregion=(0,0,width,height))
        for beat in range(int(project.length_beats)+1):
            x=beat*self.zoom; self.create_line(x,0,x,height,fill="#3a4050" if beat%4==0 else "#252a35",width=2 if beat%4==0 else 1)
        for name,track in project.tracks.items():
            if track.is_drum: continue
            for note in track.notes:
                y=330-(note.pitch-30)*5
                self.create_rectangle(note.start*self.zoom,y,note.end*self.zoom,y+4,fill=COLORS[name],outline="")
