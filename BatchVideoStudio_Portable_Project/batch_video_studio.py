import os, sys, shutil, subprocess, threading, queue
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def home(): return Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).parent
def tool(n):
 p=home()/'ffmpeg'/'bin'/f'{n}.exe'
 return str(p) if p.exists() else shutil.which(n)
def duration(fp,p):
 r=subprocess.run([fp,'-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(p)],capture_output=True,text=True,check=True)
 return float(r.stdout.strip())
def esc(p): return str(p.resolve()).replace('\\','/').replace(':',r'\\:').replace("'",r"\\'")
class App:
 def __init__(self,r):
  self.r=r;r.title('Batch Video Studio');r.geometry('850x690');r.minsize(760,620);self.q=queue.Queue();self.stopflag=threading.Event();self.busy=False
  self.d={k:tk.StringVar() for k in ('video','image','srt','out')};self.font=tk.StringVar(value='Arial');self.size=tk.IntVar(value=30);self.color=tk.StringVar(value='white');self.outline=tk.IntVar(value=2);self.pos=tk.StringVar(value='bottom');self.margin=tk.IntVar(value=48);self.effect=tk.StringVar(value='Khói + Radio/VHS');self.cq=tk.IntVar(value=23)
  self.ui();r.after(120,self.poll)
 def ui(self):
  m=ttk.Frame(self.r,padding=14);m.pack(fill='both',expand=True);ttk.Label(m,text='BATCH VIDEO STUDIO',font=('Segoe UI',20,'bold')).pack(anchor='w');ttk.Label(m,text='Ghép video + ảnh tĩnh + phụ đề SRT theo tên file trùng nhau').pack(anchor='w',pady=(0,10))
  f=ttk.LabelFrame(m,text='Thư mục',padding=8);f.pack(fill='x',pady=5)
  for k,label in [('video','Video'),('image','Ảnh'),('srt','Phụ đề SRT'),('out','Thư mục xuất')]:
   row=ttk.Frame(f);row.pack(fill='x',pady=3);ttk.Label(row,text=label,width=14).pack(side='left');ttk.Entry(row,textvariable=self.d[k]).pack(side='left',fill='x',expand=True,padx=5);ttk.Button(row,text='Chọn...',command=lambda x=k:self.pick(x)).pack(side='right')
  o=ttk.LabelFrame(m,text='Phụ đề và hiệu ứng',padding=8);o.pack(fill='x',pady=5)
  row=ttk.Frame(o);row.pack(fill='x',pady=3)
  for label,w,widget in [('Font',None,ttk.Combobox),('Cỡ chữ',None,ttk.Spinbox),('Màu',None,ttk.Combobox)]: ttk.Label(row,text=label).pack(side='left',padx=(0,3))
  ttk.Combobox(row,textvariable=self.font,values=['Arial','Roboto','Montserrat','Verdana','Georgia','Tahoma'],width=13,state='readonly').pack(side='left',padx=4);ttk.Spinbox(row,from_=14,to=64,textvariable=self.size,width=5).pack(side='left',padx=4);ttk.Combobox(row,textvariable=self.color,values=['white','yellow','cyan','lime'],width=8,state='readonly').pack(side='left',padx=4)
  row=ttk.Frame(o);row.pack(fill='x',pady=3);ttk.Label(row,text='Viền').pack(side='left');ttk.Spinbox(row,from_=0,to=6,textvariable=self.outline,width=5).pack(side='left',padx=4);ttk.Label(row,text='Vị trí').pack(side='left',padx=(10,3));ttk.Combobox(row,textvariable=self.pos,values=['bottom','center','top'],width=9,state='readonly').pack(side='left',padx=4);ttk.Label(row,text='Lề').pack(side='left');ttk.Spinbox(row,from_=0,to=200,textvariable=self.margin,width=5).pack(side='left',padx=4);ttk.Label(row,text='Hiệu ứng').pack(side='left',padx=(10,3));ttk.Combobox(row,textvariable=self.effect,values=['Không hiệu ứng','Khói','Radio/VHS','Khói + Radio/VHS'],width=18,state='readonly').pack(side='left',padx=4)
  row=ttk.Frame(o);row.pack(fill='x',pady=3);ttk.Label(row,text='Chất lượng CQ').pack(side='left');ttk.Spinbox(row,from_=16,to=30,textvariable=self.cq,width=5).pack(side='left',padx=4)
  bar=ttk.Frame(m);bar.pack(fill='x',pady=8);self.start=ttk.Button(bar,text='BẮT ĐẦU',command=self.run);self.start.pack(side='left');self.stop=ttk.Button(bar,text='Dừng sau video hiện tại',command=self.stopjob,state='disabled');self.stop.pack(side='left',padx=8);self.status=tk.StringVar(value='Sẵn sàng');ttk.Label(bar,textvariable=self.status).pack(side='right');self.pb=ttk.Progressbar(m,mode='determinate');self.pb.pack(fill='x',pady=4)
  lf=ttk.LabelFrame(m,text='Nhật ký',padding=6);lf.pack(fill='both',expand=True,pady=5);self.log=tk.Text(lf,state='disabled',wrap='word');self.log.pack(side='left',fill='both',expand=True);sb=ttk.Scrollbar(lf,command=self.log.yview);sb.pack(side='right',fill='y');self.log.configure(yscrollcommand=sb.set);ttk.Label(m,text='Chỉ xử lý video, âm thanh và phụ đề bạn sở hữu hoặc được cấp phép.',foreground='#8a4b08').pack(anchor='w')
 def pick(self,k):
  p=filedialog.askdirectory()
  if p:self.d[k].set(p)
 def msg(self,s):self.q.put(('log',s))
 def run(self):
  if self.busy:return
  ds={k:Path(v.get()) for k,v in self.d.items()}
  for k in ('video','image','srt'):
   if not ds[k].is_dir():messagebox.showerror('Thiếu thư mục',f'Chọn thư mục {k}.');return
  ds['out'].mkdir(parents=True,exist_ok=True);ff,fp=tool('ffmpeg'),tool('ffprobe')
  if not ff or not fp:messagebox.showerror('Thiếu FFmpeg','Không tìm thấy ffmpeg.exe / ffprobe.exe trong ffmpeg\\bin cạnh ứng dụng.');return
  videos=sorted(p for p in ds['video'].iterdir() if p.suffix.lower() in ('.mp4','.mov','.mkv','.avi','.webm'));jobs=[]
  for v in videos:
   im=next((p for p in ds['image'].iterdir() if p.stem.casefold()==v.stem.casefold() and p.suffix.lower() in ('.jpg','.jpeg','.png','.webp','.bmp')),None);s=next((p for p in ds['srt'].iterdir() if p.stem.casefold()==v.stem.casefold() and p.suffix.lower()=='.srt'),None)
   if im and s:jobs.append((v,im,s))
   else:self.msg(f'BỎ QUA {v.name}: thiếu ảnh hoặc SRT cùng tên.')
  if not jobs:self.msg('Không có bộ file trùng tên.');return
  self.stopflag.clear();self.busy=True;self.start.configure(state='disabled');self.stop.configure(state='normal');self.pb.configure(maximum=len(jobs),value=0);threading.Thread(target=self.worker,args=(jobs,ds['out'],ff,fp),daemon=True).start()
 def worker(self,jobs,out,ff,fp):
  good=bad=0
  for i,(v,img,srt) in enumerate(jobs,1):
   if self.stopflag.is_set():break
   self.q.put(('status',f'Đang xử lý {i}/{len(jobs)}: {v.name}'));dest=out/f'{v.stem}_edited.mp4'
   try:
    dur=duration(fp,v);wh=subprocess.run([fp,'-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','csv=s=x:p=0',str(v)],capture_output=True,text=True,check=True).stdout.strip();w,h=map(int,wh.split('x'))
    col={'white':'&H00FFFFFF','yellow':'&H0000FFFF','cyan':'&H00FFFF00','lime':'&H0000FF00'}[self.color.get()];align={'bottom':2,'center':5,'top':8}[self.pos.get()];style=f"FontName={self.font.get()},FontSize={self.size.get()},PrimaryColour={col},OutlineColour=&H00000000,BorderStyle=1,Outline={self.outline.get()},Shadow=0,Alignment={align},MarginV={self.margin.get()}"
    chain=f'scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1';eff=self.effect.get()
    if 'Radio/VHS' in eff:chain+=',noise=alls=12:allf=t+u,eq=contrast=1.08:saturation=0.78,vignette'
    sub=esc(srt);smoke=eff in ('Khói','Khói + Radio/VHS')
    if smoke:graph=f"[0:v]{chain}[base];[base]subtitles='{sub}':force_style='{style}'[cap];nullsrc=s=320x180:r=30,geq=lum='random(1)*255',gblur=sigma=18,eq=contrast=2.1:brightness=-0.28,scale={w}:{h},format=rgba,colorchannelmixer=aa=0.13[smoke];[cap][smoke]overlay=shortest=1:format=auto[v]"
    else:graph=f"[0:v]{chain},subtitles='{sub}':force_style='{style}'[v]"
    args=[ff,'-y','-loop','1','-framerate','30','-i',str(img),'-i',str(v),'-filter_complex',graph,'-map','[v]','-map','1:a?','-t',str(dur),'-c:v','h264_nvenc','-preset','p5','-rc','vbr','-cq',str(self.cq.get()),'-b:v','0','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(dest)]
    p=subprocess.run(args,capture_output=True,text=True)
    if p.returncode:
     cpu=args.copy();cpu[cpu.index('h264_nvenc')]='libx264';cpu[cpu.index('-preset')+1]='medium';ix=cpu.index('-rc');del cpu[ix:ix+4];cpu[cpu.index('-cq')]='-crf';p=subprocess.run(cpu,capture_output=True,text=True)
    if p.returncode:raise RuntimeError((p.stderr or 'FFmpeg error')[-1500:])
    good+=1;self.msg(f'THÀNH CÔNG: {v.name} → {dest.name}')
   except Exception as e:bad+=1;self.msg(f'LỖI: {v.name} — {e}')
   self.q.put(('progress',i))
  self.q.put(('done',f'Hoàn tất. Thành công {good}; lỗi {bad}.'))
 def stopjob(self):self.stopflag.set();self.status.set('Sẽ dừng sau video hiện tại...')
 def poll(self):
  try:
   while True:
    k,v=self.q.get_nowait()
    if k=='log':self.log.configure(state='normal');self.log.insert('end',v+'\n');self.log.see('end');self.log.configure(state='disabled')
    elif k=='status':self.status.set(v)
    elif k=='progress':self.pb['value']=v
    elif k=='done':self.busy=False;self.status.set(v);self.start.configure(state='normal');self.stop.configure(state='disabled');messagebox.showinfo('Hoàn tất',v)
  except queue.Empty:pass
  self.r.after(120,self.poll)
if __name__=='__main__':
 r=tk.Tk()
 try:ttk.Style().theme_use('vista')
 except:pass
 App(r);r.mainloop()
