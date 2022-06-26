import subprocess,sys, logging, tkinter as tk
from tkinter import scrolledtext
from time import sleep



logging.basicConfig(level=logging.DEBUG, filename='.log',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.log(logging.INFO,msg='\n\t\t\t\t[NEW SESSION]\n')

try:
    import requests
    from cefpython3 import cefpython as cef
    
except ImportError:
    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    install('cefpython3')
    install('requests')
    import requests
    from cefpython3 import cefpython as cef
postData={}

def on_browse(browser,frame,request):
    if browser.GetUrl() == 'https://discord.com/channels/@me':
        if not request.GetPostData() == {}:
            global postData
            postData=request.GetHeaderMap()["Authorization"]

sys.excepthook = cef.ExceptHook
cef.Initialize(settings={'cache_path':'./cache'})
browser = cef.CreateBrowserSync(url="https://discord.com/login")
browser.SetClientCallback('OnBeforeResourceLoad',on_browse)

while postData == {}:
    cef.MessageLoopWork()
del browser
cef.Shutdown()
print (postData)
logging.info (postData)

def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
        event.widget.event_generate("<<Cut>>")

    if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
        event.widget.event_generate("<<Paste>>")

    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

root = tk.Tk()
root.resizable(False,False)
root.bind_all("<Key>", _onKeyRelease, "+")


def sendMSG(IDs, msg):
    for id in IDs:
        data = {
        'content':f'{msg}'
        }
        headers = {
        'authorization':f'{postData}'
        }
        r = requests.post(url=f'https://discord.com/api/v9/channels/{id}/messages',data=data, headers=headers)
        if not r.status_code == 200:
            print  (f'{id}:{r}')
            logging.info  (f'{id}:{r}')
            while r.status_code == 429:
                n = 7
                print (f'   >>Response <429>, waiting {n} seconds...')
                logging.info (f'   >>Response <429>, waiting {n} seconds...')
                sleep(n)
                r = requests.post(url=f'https://discord.com/api/v9/channels/{id}/messages',data=data, headers=headers)
        if r.status_code == 200:
            print (f'[OK] {id}')
            logging.info (f'[OK] {id}')
    open('ID каналов.txt', mode='w',encoding='utf-8').write('\n'.join(IDs)) #discod channel IDs



root.geometry('800x200')
txt = scrolledtext.ScrolledText(root, width=40,height=10)
SIDtxt = scrolledtext.ScrolledText(root, width=40,height=10)
sendBtn = tk.Button(root,text='Send', #send
                    command = 
                    lambda: sendMSG(SIDtxt.get("1.0",tk.END).split(),txt.get("1.0",tk.END))
                    )
sendBtn.place(x=680,y=0,height=100,width=120)

sendFileBtn = tk.Button(root,text='Send from \n\"Message.txt\"',
                        command =
                        lambda: sendMSG(SIDtxt.get("1.0",tk.END).split(),open('Message.txt',mode='r', encoding='utf-8').read())
                        )
sendFileBtn.place(x=680,y=100,height=100,width=120)

SIDtxt.insert('1.0',open('Channel IDs.txt', mode='r',encoding='utf-8').read())
SIDtxt.place(x=0,y=0,height=200, width=200)
txt.place(x=200,y=0,height=200, width=480)

if __name__ == '__main__':
    root.mainloop()
