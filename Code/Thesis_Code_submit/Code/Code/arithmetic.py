from PIL import Image
import math
import cv2
import numpy as np
#import matplotlib.pyplot as plt
from PyQt5 import  QtGui
from steganography import *

LEN = 0
# %% LSB隐写
class LSB:
    """
    定义 LSB 隐写算法类
    """
    def __init__(self):
        self.im=None
    def plus(self,str):
      #Python zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。
       return str.zfill(8)

    def get_key(self,strr):
 
        #获取要隐藏的文件内容
        str = ""
        s = strr
        global LEN 
        LEN = len(s)
        #print("s is",s)
 
        for i in range(len(s)):
 
             #逐个字节将要隐藏的文件内容转换为二进制，并拼接起来
 
             #1.先用ord()函数将s的内容逐个转换为ascii码
 
             #2.使用bin()函数将十进制的ascii码转换为二进制
 
             #3.由于bin()函数转换二进制后，二进制字符串的前面会有"0b"来表示这个字符串是二进制形式，所以用replace()替换为空
 
             #4.又由于ascii码转换二进制后是七位，而正常情况下每个字符由8位二进制组成，所以使用自定义函数plus将其填充为8位
 
            str = str+self.plus(bin(ord(s[i])).replace('0b',''))
 
            #print str
 
        #f.closed
 
        return str
 
 
 
    def mod(self,x,y):
 
        return x%y;
 
    #str1为载体图片路径，str2为隐写文件，str3为加密图片保存的路径
 
    def write(self,str1,str2):  
 
        im = Image.open(str1)
        #获取图片的宽和高
 
        width = im.size[0]
 
        #print ("width:"+str(width)+"\n")
 
        height = im.size[1]
 
        #print ("height:"+str(height)+"\n")
 
        count = 0
 
        #获取需要隐藏的信息
 
        key = self.get_key(str2)
 
        keylen = len(key)
 
        for h in range(0,height):
 
            for w in range(0,width):
 
                pixel = im.getpixel((w,h))
                print(pixel)
 
                a=pixel[0]
 
                b=pixel[1]
 
                c=pixel[2]
 
                if count == keylen:
 
                    break
 
                #下面的操作是将信息隐藏进去
 
                #分别将每个像素点的RGB值余2，这样可以去掉最低位的值
 
                #再从需要隐藏的信息中取出一位，转换为整型
 
                #两值相加，就把信息隐藏起来了
 
                a= a-self.mod(a,2)+int(key[count])
 
                count+=1
 
                if count == keylen:
 
                    im.putpixel((w,h),(a,b,c))
 
                    break
 
                b =b-self.mod(b,2)+int(key[count])
 
                count+=1
 
                if count == keylen:
 
                    im.putpixel((w,h),(a,b,c))
 
                    break
 
                c= c-self.mod(c,2)+int(key[count])
 
                count+=1
 
                if count == keylen:
 
                    im.putpixel((w,h),(a,b,c))
 
                    break
 
                if count % 3 == 0:
 
                    im.putpixel((w,h),(a,b,c))

        return im


    def toasc(self,strr):
     return int(strr, 2)
 
#le为所要提取的信息的长度，str1为加密载体图片的路径，str2为提取文件的保存路径
 
    def read(self,img):
 
        a=""
 
        b=""

        im = img #Image.open(str1)
        le = LEN
        lenth = le*8
 
        width = im.size[0]
 
        height = im.size[1]
 
        count = 0
 
        for h in range(0, height):
 
            for w in range(0, width):
 
                 #获得(w,h)点像素的值
 
                pixel = im.getpixel((w, h))
 
                #此处余3，依次从R、G、B三个颜色通道获得最低位的隐藏信息
 
                if count%3==0:
 
                    count+=1
 
                    b=b+str((self.mod(int(pixel[0]),2)))
 
                    if count ==lenth:
 
                        break
 
                if count%3==1:
 
                    count+=1
 
                    b=b+str((self.mod(int(pixel[1]),2)))
 
                    if count ==lenth:
 
                        break
 
                if count%3==2:
 
                    count+=1
 
                    b=b+str((self.mod(int(pixel[2]),2)))
 
                    if count ==lenth:
 
                        break
 
            if count == lenth:
 
                break


        str11=""
        for i in range(0,len(b),8):
 
                #以每8位为一组二进制，转换为十进制
 
            stra = self.toasc(b[i:i+8])
 
            #将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
            str11 = str11+chr(stra)
            stra =""
        #print(str11)
        return str11
    
    def new_write(self,input_image_path,output_image_path,text):
        write_new(input_image_path,output_image_path,text)
    def new_read(self,output_image_path):
        return read_new(output_image_path)

if __name__=="__main__":
    lsb=LSB()
    # 写
    lsb.load_bmp('test.bmp')
    info1=[0,1,0,1,1,0,1,0]
    lsb.write(info1)
    lsb.save('lsb.bmp')
    # 读
    lsb.load_bmp('lsb.bmp')
    info2=lsb.read()
    print (info2)


# %% Jsteg隐写

class Jsteg:
    """
    定义 Jsteg 隐写算法类
    """
    def __init__(self):
        LSB.__init__(self)
        self.sequence_after_dct=None
    
    def get_dct(self, filename):
        filename = filename.encode('gbk')
        img = cv2.imread(filename.decode(), cv2.IMREAD_GRAYSCALE)
        #img = cv2.imread(filename.decode(), cv2.IMREAD_COLOR) 
        #plt.imshow(img)
        dct = cv2.dct(img.astype(np.float32))
        dctInt = np.rint(dct).astype(np.int32)
        return dctInt, img
 
    def set_sequence_after_dct(self,sequence_after_dct):
        self.sequence_after_dct=sequence_after_dct
        self.available_info_len=len([i for i in self.sequence_after_dct if i not in (-1,1,0)]) # 不是绝对可靠的
        #print ("Load>> 可嵌入",self.available_info_len,'bits')
     
    def get_sequence_after_dct(self):
        return self.sequence_after_dct
 
    def write(self,info):
        """先嵌入信息的长度，然后嵌入信息"""
        info=self._set_info_len(info)
        info_len=len(info)
        info_index=0
        im_index=0
        while True:
            if info_index>=info_len:
                break
            data=info[info_index]
            if self._write(im_index,data):
                info_index+=1
            im_index+=1
 
 
    def read(self):
        """先读出信息的长度，然后读出信息"""
        _len,sequence_index=self._get_info_len()
        info=[]
        info_index=0
 
        while True:
            if info_index>=_len:
                break
            data=self._read(sequence_index)
            if data!=None:
                info.append(data)
                info_index+=1
            sequence_index+=1
 
        return info
 
    #===============================================================#
 
    def _set_info_len(self,info):
        l=int(math.log(self.available_info_len,2))+1
        info_len=[0]*l
        _len=len(info)
        info_len[-len(bin(_len))+2:]=[int(i) for i in bin(_len)[2:]]
        return info_len+info
 
    def _get_info_len(self):
        l=int(math.log(self.available_info_len,2))+1
        len_list=[]
        _l_index=0
        _seq_index=0
        while True:
            if _l_index>=l:
                break
            _d=self._read(_seq_index)
            if _d!=None:
                len_list.append(str(_d))
                _l_index+=1
            _seq_index+=1
        _len=''.join(len_list)
        _len=int(_len,2)
        return _len,_seq_index
 
    def _write(self,index,data):
        origin=self.sequence_after_dct[index]
        if origin in (-1,1,0):
            return False
 
        lower_bit=origin%2
        if lower_bit==data:
            pass
        elif origin>0:
            if (lower_bit,data) == (0,1):
                self.sequence_after_dct[index]=origin+1
            elif (lower_bit,data) == (1,0):
                self.sequence_after_dct[index]=origin-1
        elif origin<0:
            if (lower_bit,data) == (0,1):
                self.sequence_after_dct[index]=origin-1
            elif (lower_bit,data) == (1,0):
                self.sequence_after_dct[index]=origin+1
 
        return True
 
    def _read(self,index):
        if self.sequence_after_dct[index] not in (-1,1,0):
            return self.sequence_after_dct[index]%2
        else:
            return None
    def new_write(self,str1,str2):
        lsb = LSB()
        newim = lsb.write(str1,str2)
        return newim
    def new_read(self,img):
        lsb = LSB()
        return(lsb.read(img))
        
 
if __name__=="__main__":
    jsteg=Jsteg()
    #print("Attention Here!!!")
    # 写
#    sequence_after_dct=[-1,0,1]*100+[i for i in range(-7,500)]
    sequence_after_dct = jsteg.get_dct(r"d:\Users\LIQIC\Desktop\testTim.jpg")
    shape = sequence_after_dct.shape
    sequence_after_dct = sequence_after_dct.reshape(-1)
    jsteg.set_sequence_after_dct(sequence_after_dct)
    info1=[0,1,0,1,1,0,1,0]
    jsteg.write(info1)
    sequence_after_dct1 = jsteg.get_sequence_after_dct()
    
    img = cv2.idct(
            sequence_after_dct1.reshape(shape).astype(np.float32))
    cv2.imwrite('test.jpg', img)
    # 读
    sequence_after_dct2 = jsteg.get_dct('test.jpg')
    sequence_after_dct2 = sequence_after_dct2.reshape(-1)
    jsteg.set_sequence_after_dct(sequence_after_dct2)
    info2=jsteg.read()
    print (info2)


# %% F3隐写

class F3(Jsteg):
    """
    定义 F3 隐写算法类
    """
    def __init__(self):
        Jsteg.__init__(self)

    def set_sequence_after_dct(self,sequence_after_dct):
        self.sequence_after_dct=sequence_after_dct
        sum_len=len(self.sequence_after_dct)
        zero_len=len([i for i in self.sequence_after_dct if i==0])
        one_len=len([i for i in self.sequence_after_dct if i in (-1,1)])
        self.available_info_len=sum_len-zero_len-one_len # 不是特别可靠
        #print ("Load>> 大约可嵌入",sum_len-zero_len-int(one_len/2),'bits')
        #print ("Load>> 最少可嵌入",self.available_info_len,'bits\n')

    def _write(self,index,data):
        origin=self.sequence_after_dct[index]
        if origin == 0:
            return False
        elif origin in (-1,1) and data==0:
            self.sequence_after_dct[index]=0
            return False
 
        lower_bit=origin%2
 
        if lower_bit==data:
            pass
        elif origin>0:
            self.sequence_after_dct[index]=origin-1
        elif origin<0:
            self.sequence_after_dct[index]=origin+1
        return True
 
    def _read(self,index):
        if self.sequence_after_dct[index] != 0:
            return self.sequence_after_dct[index]%2
        else:
            return None
    def new_write(self,input_image_path,output_image_path,text):
        write_new(input_image_path,output_image_path,text)
    def new_read(self,output_image_path):
        return read_new(output_image_path)
        
 
 
if __name__=="__main__":
    f3=F3()
    # 写
    sequence_after_dct=[-1,0,1]*100+[i for i in range(-7,500)]
    f3.set_sequence_after_dct(sequence_after_dct)
    info1=[0,1,0,1,1,0,1,0]
    f3.write(info1)
    sequence_after_dct2=f3.get_sequence_after_dct()
    # 读
    f3.set_sequence_after_dct(sequence_after_dct2)
    info2=f3.read()
    print (info2)


# %% F5隐写
class F5(Jsteg):
    def __init__(self):
        Jsteg.__init__(self)

    def set_sequence_after_dct(self,sequence_after_dct):
        self.sequence_after_dct=sequence_after_dct
        sum_len=len(self.sequence_after_dct)
        zero_len=len([i for i in self.sequence_after_dct if i==0])
        one_len=len([i for i in self.sequence_after_dct if i in (-1,1)])
        self.available_info_len=sum_len-zero_len-one_len # 不是特别可靠
        #print ("Load>> 大约可嵌入",sum_len-zero_len-int(one_len/2),'bits')
        #print ("Load>> 最少可嵌入",self.available_info_len,'bits\n')
         
    def set_sequence_after_dct(self,sequence_after_dct):
        self.sequence_after_dct=sequence_after_dct
        sum_len=len(self.sequence_after_dct)
        zero_len=len([i for i in self.sequence_after_dct if i==0])
        one_len=len([i for i in self.sequence_after_dct if i in (-1,1)])
        self.available_info_len=sum_len-zero_len-one_len # 不是特别可靠

    def _write(self,index,data):
        origin=self.sequence_after_dct[index]
        if origin == 0:
            return False
        elif origin in (-1,1) and data==0:
            self.sequence_after_dct[index]=0
            return False
 
        lower_bit=origin%2
 
        if lower_bit==data:
            pass
        elif origin>0:
            self.sequence_after_dct[index]=origin-1
        elif origin<0:
            self.sequence_after_dct[index]=origin+1
        return True
 
    def _read(self,index):
        if self.sequence_after_dct[index] != 0:
            return self.sequence_after_dct[index]%2
        else:
            return None
    def new_write(self,input_image_path,output_image_path,text):
        write_new(input_image_path,output_image_path,text)
    def new_read(self,output_image_path):
        return read_new(output_image_path)

# %% EzSteg隐写 
import numpy as np
 

class EzSteg:
    def __init__(self):
         self.im=None
 
    def load_gif(self,gif_file):
        self.im=Image.open(gif_file)
        self._load_palette()
        self._sort_palette()
        self._load_palette_data()
        self.available_info_len=len(self.palette_data)
 
    def write(self,info):
        info=self._set_info_len(info)
        self.palette_data=self._write(self.palette_data,info)
        return self.palette_data
     
 
    def read(self):
        palette_data = np.loadtxt('./EzSteg.dat',dtype=int)
        _len,im_index=self._get_info_len(palette_data)
        #print("Len and im_index",_len,im_index)
        info=self._read(palette_data[im_index:im_index+_len])
        return info
         
    def save(self,filename):
        self.im.save(filename)
 
 
    def _load_palette(self):
        self.palette=[]
        palette=self.im.palette.palette
        for i in range(int(len(palette)/3)):
            self.palette.append((palette[3*i],palette[3*i+1],palette[3*i+2]))
      
    def _sort_palette(self):
        f=lambda t:0.299*t[0]+0.587*t[1]+0.114*t[2]
        Y=[f(t) for t in self.palette]
        self.Y_index=np.argsort(Y)
        self.Y_index_inverse=[0]*256
        for i in range(len(self.Y_index)):
            self.Y_index_inverse[self.Y_index[i]]=i

    def _load_palette_data(self):
        self.palette_data=self.im.getpalette()
 
    def _set_info_len(self,info):
        l=int(math.log(self.available_info_len,2))+1
        info_len=[0]*l
        _len=len(info)
        info_len[-len(bin(_len))+2:]=[int(i) for i in bin(_len)[2:]]
        return info_len+info

    def _get_info_len(self,palette_data):
        l=int(math.log(self.available_info_len,2))+1
        #print("available_info_len and L ",self.available_info_len,l)
        len_list=[]
        for i in range(l):
            _d=self._get_lsb(palette_data[i])
            len_list.append(str(_d))
        _len=''.join(len_list)
        _len=int(_len,2)
        return _len,l
 
    def _write(self,palette_data,info):
        for i in range(len(info)):
            Y_index=self.Y_index_inverse[palette_data[i]]
            np.savetxt('./EzSteg_Y_index_inverse.dat', self.Y_index_inverse,fmt="%d")
            lower_bit=Y_index%2
            if lower_bit==info[i]:
                pass
            elif (lower_bit,info[i])==(0,1):
                palette_data[i]=self.Y_index[Y_index+1]
            elif (lower_bit,info[i])==(1,0):
                palette_data[i]=self.Y_index[Y_index-1]
        return palette_data
 
    def _read(self,palette_data):
        info=[]
        for i in range(len(palette_data)):
            info.append(self._get_lsb_new(palette_data[i]))
        return info
    def _get_lsb(self,_palette_data):
        return self.Y_index_inverse[_palette_data]%2

    def _get_lsb_new(self,_palette_data):
        Y_index_inverse_new=[0]
        Y_index_inverse_new = np.loadtxt('./EzSteg_Y_index_inverse.dat', dtype=int)
        #print('locate',_palette_data,'data ',Y_index_inverse_new[_palette_data])
        return (Y_index_inverse_new[_palette_data])%2

    def plus(self,str):
      #Python zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。
       return str.zfill(8)

    def get_key(self,strr):
 
        #获取要隐藏的文件内容

        str1 = ""
        s = strr
        #global LEN 
        #LEN = len(s)
        length = len(s)
        #print("s is",s)
        f = open("./len.dat","w")
        f.write(str(length))
        f.close()
        for i in range(len(s)):
 
             #逐个字节将要隐藏的文件内容转换为二进制，并拼接起来
 
             #1.先用ord()函数将s的内容逐个转换为ascii码
 
             #2.使用bin()函数将十进制的ascii码转换为二进制
 
             #3.由于bin()函数转换二进制后，二进制字符串的前面会有"0b"来表示这个字符串是二进制形式，所以用replace()替换为空
 
             #4.又由于ascii码转换二进制后是七位，而正常情况下每个字符由8位二进制组成，所以使用自定义函数plus将其填充为8位
 
            str1 = str1+self.plus(bin(ord(s[i])).replace('0b',''))
 
            #print str
 
        #f.closed
 
        return str1
 
 
 
    def mod(self,x,y):
 
        return x%y;
 
    #str1为载体图片路径，str2为隐写文件，str3为加密图片保存的路径
 
    def new_write(self,str1,str2):  
 
        im = Image.open(str1)
        #获取图片的宽和高
 
        width = im.size[0]
 
        #print ("width:"+str(width)+"\n")
 
        height = im.size[1]
 
        #print ("height:"+str(height)+"\n")
 
        count = 0
 
        #获取需要隐藏的信息
 
        key = self.get_key(str2)
        keylen = len(key)
        #global LEN 
        #LEN= keylen
        #f = open("./len.dat","w")
        #f.write(str(keylen))
        #f.close()
        for h in range(0,height):
 
            for w in range(0,width):
 
                pixel = im.getpixel((w,h))
                #print(pixel)
 
                a=pixel[0]
 
                b=pixel[1]
 
                c=pixel[2]
 
                if count == keylen:
 
                    break
 
                #下面的操作是将信息隐藏进去
 
                #分别将每个像素点的RGB值余2，这样可以去掉最低位的值
 
                #再从需要隐藏的信息中取出一位，转换为整型
 
                #两值相加，就把信息隐藏起来了
 
                a= a-self.mod(a,2)+int(key[count])
 
                count+=1
 
                if count == keylen:
 
                    im.putpixel((w,h),(a,b,c))
 
                    break
 
                b =b-self.mod(b,2)+int(key[count])
 
                count+=1
 
                if count == keylen:
 
                    im.putpixel((w,h),(a,b,c))
 
                    break
 
                c= c-self.mod(c,2)+int(key[count])
 
                count+=1
 
                if count == keylen:
 
                    im.putpixel((w,h),(a,b,c))
 
                    break
 
                if count % 3 == 0:
 
                    im.putpixel((w,h),(a,b,c))

        return im


    def toasc(self,strr):
     return int(strr, 2)
 
#le为所要提取的信息的长度，str1为加密载体图片的路径，str2为提取文件的保存路径
 
    def new_read(self,img):
 
        a=""
 
        b=""

        im = img #Image.open(str1)
        f = open("./len.dat","r")
        le = int(f.read())
        #le = LEN
        #print("read Len ",LEN)
        #f.close()
        #print(le)
        #le = LEN
        lenth = le*8
 
        width = im.size[0]
 
        height = im.size[1]
 
        count = 0
 
        for h in range(0, height):
 
            for w in range(0, width):
 
                 #获得(w,h)点像素的值
 
                pixel = im.getpixel((w, h))
 
                #此处余3，依次从R、G、B三个颜色通道获得最低位的隐藏信息
 
                if count%3==0:
 
                    count+=1
 
                    b=b+str((self.mod(int(pixel[0]),2)))
 
                    if count ==lenth:
 
                        break
 
                if count%3==1:
 
                    count+=1
 
                    b=b+str((self.mod(int(pixel[1]),2)))
 
                    if count ==lenth:
 
                        break
 
                if count%3==2:
 
                    count+=1
 
                    b=b+str((self.mod(int(pixel[2]),2)))
 
                    if count ==lenth:
 
                        break
 
            if count == lenth:
 
                break


        str11=""
        for i in range(0,len(b),8):
 
                #以每8位为一组二进制，转换为十进制
 
            stra = self.toasc(b[i:i+8])
 
            #将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
            str11 = str11+chr(stra)
            stra =""
        #print(str11)
        return str11
    
    #def new_write(self,input_image_path,output_image_path,text):
    #    write_new(input_image_path,output_image_path,text)
    #def new_read(self,output_image_path):
    #    return read_new(output_image_path)


# %% blindWaterMark
import random
import cv2


class BlindWaterMark():
    def __init__(self):
        self.im=None
        self.seed = 10
        self.alpha = 1.0
    
    def load_img(self,filename):
        # 导入原始图像
        self.im = cv2.imread(filename)
        dctShape = self.im.shape
        dctInt = self.im.reshape(-1)
        np.savetxt('./im.dat',dctInt,fmt="%f")
    def load_wm(self,filename):
        # 导入水印
        self.wm = cv2.imread(filename)

    def load_img_wm(self,filename):
        # 导入含水印图像
        self.im_wm = cv2.imread(filename)
        return  self.im_wm
    def bgr_to_rgb(self):
        # OpenCV是以(BGR)的顺序存储图像数据的
        b, g, r = cv2.split(self.im)
        self.im = cv2.merge([r, g, b])
    
    def write(self):
        wm = self.wm
        h, w = self.im.shape[0], self.im.shape[1]
        hwm = np.zeros((int(h * 0.5), w, self.im.shape[2]))
        assert hwm.shape[0] > wm.shape[0],"水印尺寸过长"
        assert hwm.shape[1] > wm.shape[1],"水印尺寸过宽"
        hwm2 = np.copy(hwm)
        for i in range(wm.shape[0]):
            for j in range(wm.shape[1]):
                hwm2[i][j] = wm[i][j]
        
        # 水印置乱
        random.seed(self.seed)
        m, n = list(range(hwm.shape[0])), list(range(hwm.shape[1]))
        random.shuffle(m)
        random.shuffle(n)
        for i in range(hwm.shape[0]):
            for j in range(hwm.shape[1]):
                hwm[i][j] = hwm2[m[i]][n[j]]
        
        # 写入水印
        rwm = np.zeros(self.im.shape)
        for i in range(hwm.shape[0]):
            for j in range(hwm.shape[1]):
                rwm[i][j] = hwm[i][j]
                rwm[rwm.shape[0] - i - 1][rwm.shape[1] - j - 1] = hwm[i][j]
        self.f1 = np.fft.fft2(self.im)      # 原始图像的FFT
        self.f2 = self.f1 + self.alpha * rwm          # 原始图像FFT + 水印
        
        # 已添加水印的空域图像
        self.img_wm = np.real(
                np.fft.ifft2(self.f2))
        dctShape = self.img_wm.shape
        dctInt = self.img_wm.reshape(-1)
        np.savetxt('./wave.dat',dctInt,fmt="%f") #because of the pixel is float and cv.imwrite default type is int 
        return self.img_wm

    def read(self,img):
        # 解水印
        dct = np.loadtxt('./im.dat',dtype=float)
        im = dct.reshape(img.shape)
        dctInt = np.loadtxt('./wave.dat',dtype=float)
        img_wm = dctInt.reshape(img.shape)
        #print(self.img_wm.shape,"",im.shape)
        random.seed(self.seed)
        m, n = list(range(int(img.shape[0] * 0.5))), list(range(img.shape[1]))
        #m, n = list(range(int(self.im.shape[0] * 0.5))), list(range(self.im.shape[1]))
        random.shuffle(m)
        random.shuffle(n)
        
        f1 = np.fft.fft2(im)
        f2 = np.fft.fft2(img_wm)
        rwm = (f2 - f1) / self.alpha
        rwm = np.real(rwm)
        
        self.wm1 = np.zeros(rwm.shape)
        for i in range(int(rwm.shape[0] * 0.5)):
            for j in range(rwm.shape[1]):
                self.wm1[m[i]][n[j]] = np.uint8(rwm[i][j])
        for i in range(int(rwm.shape[0] * 0.5)):
            for j in range(rwm.shape[1]):
                self.wm1[rwm.shape[0] - i - 1][rwm.shape[1] - j - 1] = self.wm1[i][j]
        qPixmap =  self.img2pixmap( self.wm1)
        return qPixmap
        #height, width, channel = self.wm1.shape
        #bytesPerLine = 3 * width
        #qImg = QtGui.QImage(self.wm1.data, width, height,QtGui.QImage.Format_RGB888)
        #qpixmap = QtGui.QPixmap.fromImage(qImg)
        #return qpixmap

    def img2pixmap(self, image):
        Y, X = image.shape[:2]
        self._bgra = np.zeros((Y, X, 4), dtype=np.uint8, order='C')
        self._bgra[..., 0] = image[..., 2]
        self._bgra[..., 1] = image[..., 1]
        self._bgra[..., 2] = image[..., 0]
        qimage = QtGui.QImage(self._bgra.data, X, Y, QtGui.QImage.Format_RGB32)
        pixmap = QtGui.QPixmap.fromImage(qimage)
        return pixmap

    def new_write(self,img1,mark1):
        mark = np.array(mark1)
        img = np.array(img1)
        rows,cols,dims=mark.shape
        for i in range(0,dims):
            for j in range(0,rows*2):
                for k in range(0,cols*2):
                    img[j,k,i]=img[j,k,i]&252
        for i in range(0,dims):
            for j in range(0,rows):
                for k in range(0,cols):
                    img[2*j,2*k,i]=img[2*j,2*k,i]+(mark[j,k,i]&192)//64
                    img[2*j,2*k+1,i]=img[2*j,2*k+1,i]+(mark[j,k,i]&48)//16
                    img[2*j+1,2*k,i]=img[2*j+1,2*k,i]+(mark[j,k,i]&12)//4
                    img[2*j+1,2*k+1,i]=img[2*j+1,2*k+1,i]+(mark[j,k,i]&3)
        img=Image.fromarray(img)
        return img
    def new_read(self,mark):
        imgwmark=np.array(mark)
        result=imgwmark
        rows,cols,dims=imgwmark.shape
        rows=rows//2
        cols=cols//2
        for i in range(0,dims):
            for j in range(0,rows*2):
                for k in range(0,cols*2):
                   imgwmark[j,k,i]=imgwmark[j,k,i]&3
        for i in range(0,dims):
            for j in range(0,rows):
                for k in range(0,cols):
                    result[j,k,i]=imgwmark[2*j,2*k,i]*64+imgwmark[2*j,2*k+1,i]*16+imgwmark[2*j+1,2*k,i]*4+imgwmark[2*j+1,2*k+1,i]
        mark_get=Image.fromarray(result)
        mark_get = mark_get.convert("RGB")
        data = mark_get.tobytes("raw","RGB")
        qim = QtGui.QImage(data, mark_get.size[0], mark_get.size[1], QtGui.QImage.Format_RGB888)
        qim = QtGui.QPixmap.fromImage(qim)
        return qim





# %% 文件隐藏
# png: 0000 0000 4945 4e44 ae42 6082
# jpg: ffd9
# gif: 3B
#!/usr/bin/env python
#coding:utf-8

import PIL
from PIL import Image,ImageFont,ImageDraw

from math import sqrt
class attachFile():
    def __init__(self):
      pass
    #Consider the Text charactor numbers per line 
    def handletext(self,pix,text):
        textlist=[]
        font_perline = pix
        hangshu=int(len(text)/font_perline)
        line = int(len(text)/font_perline)
        if line==0:
            textlist.append(text)
        else:
            for i in range(0,line):
                partoftext=text[font_perline*i:(i+1)*font_perline]
                textlist.append(partoftext)
            if text[(i+1)*font_perline:]:
                textlist.append(text[(i+1)*font_perline:])
        return textlist

    def write(self,im,text):
        size = im.size
        text=text.strip('\n') 
        pix=int(sqrt((size[0]*size[1])/len(text)))
        while len(text)>(size[0]/pix)*(size[1]/pix):
            pix-=1
        texttopic=self.handletext(pix,text)
        im2=Image.new('RGB',size,(255,255,255))
        dr=ImageDraw.Draw(im2)
        ny=len(texttopic)
        for i in range(0,ny):
            dr.text((0,pix*i),texttopic[i],fill=(0,0,0))
        #write
        pixim=im.load()
        pixim2=im2.load()
        for x in range(0,size[0]):
            for y in range(0,size[1]):
                if pixim2[x,y]==(255,255,255):
                    if pixim[x,y][0]%2==0:
                        pass
                    else:
                        pixim[x,y]=(pixim[x,y][0]-1,pixim[x,y][1],pixim[x,y][2])

                else:
                    if pixim[x,y][0]%2==0:
                        pixim[x,y]=(pixim[x,y][0]+1,pixim[x,y][1],pixim[x,y][2])
                    else:
                        pass

        return im
    def read(self,im):
       pix=im.load()
       sizex,sizey=im.size
       for x in range(0,sizex):
        for y in range(0,sizey):
            if pix[x,y][0]%2==1:
                pix[x,y]=(0,0,0)
            else:
                pix[x,y]=(255,255,255)
       #PIL image to QImage to QPixmap
       im = im.convert("RGB")
       data = im.tobytes("raw","RGB")
       qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_RGB888)
       qim = QtGui.QPixmap.fromImage(qim)
       return qim