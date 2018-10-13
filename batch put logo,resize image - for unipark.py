from PIL import Image
import os
from random import randint

def load():
    folder_list = os.listdir()
    return(folder_list)

def resize(chosen, name):
    img = Image.open('{0}'.format(name)) # image extension *.png,*.jpg
    old_width, old_height = img.size
    new_width  = chosen
    new_height = int((chosen / old_width)* old_height) 
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    if (os.path.isdir('resized')== 0):
        os.mkdir('resized')
    os.chdir('resized')
    img.save('{}_new.jpg'.format(str(name)))
    os.chdir('../')
    print('{} image resized'.format(name))
    
def resize_logos(chosen, name):
    os.chdir('logo')
    logo = Image.open('{0}'.format(name))    
    old_width, old_height = logo.size
    new_width  = int(chosen / 4)
    new_height = int(((chosen/4) / old_width)* old_height) 
    logo = logo.resize((new_width, new_height), Image.ANTIALIAS)
    logo.save('rescaled_{}'.format(name))
    os.chdir('../')
    print('logo resized')

def put_logo(img_name, chosen, lr , bw):
    target_h = 0
    target_w = 0
    if os.path.isdir('resized'):
        os.chdir('resized')
        img = Image.open('{}_new.jpg'.format(img_name))
        os.chdir('../')
    old_width, old_height = img.size
    if  bw == 'b' :
        os.chdir('logo')
        logo = Image.open('rescaled_b.png')
        os.chdir('../')
        logo_width, logo_height = logo.size
        side = 'r'
        if  'l' == lr and target_h == 0 and target_w == 0:
            target_h = old_height - logo_height
            target_w = 0
            side = 'l'
        elif 'r' == lr:
            target_h = old_height - logo_height
            target_w = old_width - logo_width            
        img.paste(logo,(target_w, target_h), logo)
        if (os.path.isdir('b')== 0):
            os.mkdir('b')
        os.chdir('b')
        img.save('{}_b{}.jpg'.format(str(img_name),side))
        os.chdir('../')
        print("{}pasted".format(img_name))
    else:
        os.chdir('logo')
        logo = Image.open('rescaled_w.png')
        os.chdir('../')
        logo_width, logo_height = logo.size
        side = 'r'
        if  'l' == lr:
            target_h = old_height - logo_height
            target_w = 0
            side = 'l'
        elif 'r' == lr:
            target_h = old_height - logo_height
            target_w = old_width - logo_width  
        img.paste(logo,(target_w, target_h), logo)
        if (os.path.isdir('w')== 0):
            os.mkdir('w')
        os.chdir('w')
        img.save('{}_w{}.jpg'.format(str(img_name),side))
        os.chdir('../')
        print("{}pasted".format(img_name))

def choose(img_name, rl, hc, bw, chosen):
    if hc == 1:
        will_do = hard_coded (rl, bw)
        execute(will_do, img_name, chosen, rl, bw)
    
    else:
        avg = [0,0,0]
        for i in range(1000):
            x = randint(0,900)
            y = randint(0,700)
            pix = img.getpixel((x,y))
            avg[0] += pix[0]
            avg[1] += pix[1]
            avg[2] += pix[2]
        mean = 0
        for x in range(3):
            avg[x] = int(avg[x]/1000)
            mean += avg[x]
        if (mean > 350):
            print('FUCK')


def execute(will_do, img_name, chosen, lr , bw):
    if 'r' in will_do:
        if 'w' in will_do:
            put_logo(img_name, chosen, 'r' , 'w')
        if 'b' in will_do:
            put_logo(img_name, chosen, 'r' , 'b')
    if 'l' in will_do:
        if 'w' in will_do:
            put_logo(img_name, chosen, 'l' , 'w')
        if 'b' in will_do:
            put_logo(img_name, chosen, 'l' , 'b')
def hard_coded(rl, bw):
    rl = list(rl)
    bw = list(bw)
    rt = ['','','','']  #[r,l,b,w]
    if 'r' in rl:
        if 'b' in bw:
            rt[0] = 'r'
            rt[2] = 'b'
        if 'b' in bw:
            rt[0] = 'r'
            rt[3] = 'w'
    elif 'l' in rl:
        if 'b' in bw:
            rt[1] = 'l'
            rt[2] = 'b'
        if 'b' in bw:
            rt[1] = 'l'
            rt[3] = 'w'
    return rt
def erase_nonusable(folder):
    for x in folder:
        if 'jpg' in x or 'png' in x:
            continue
            print(x)
        else:
            folder.remove(x)
            print('removed {}'.format(x))
    return folder

def ask_hc ():
    rl = input('r or l : ')
    bw = input('b or w : ')
    return(rl, bw)
            
def main():
    desired_w = int(input("input desired width"))
    hardcode = input('hc? 0 xor 1')
    lr = 'r'
    bw = 'b'
    if hardcode:
        tmp =  ask_hc()
        lr = tmp[0]
        bw = tmp[1]
    folder = load()
    print(folder)
    resize_logos(desired_w, 'b.png')
    resize_logos(desired_w, 'w.png')
    print ('logos resized')
    folder = erase_nonusable(folder)
    print(hardcode)
    for x in folder:
        print (x)
        if x != 'repaired.py' and x != 'logo' and x != 'a' and x != 'b' and x != 'w' and x != 'resized':
            resize (desired_w, x)
    for x in folder:
        print(hardcode)
        print (x)
        if x != 'repaired.py' and x != 'logo' and x != 'a' and x != 'b' and x != 'w' and x != 'resized':
            choose(x, lr, int(hardcode), bw, desired_w)
    print ('DONE')

main()
