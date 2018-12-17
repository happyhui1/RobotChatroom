from socket import *
import sys,os

def send_msg(s,name,addr):
    while True:
        text=input("发言:")
        #如果输入quit表示退出
        if text.strip()=='quit':
            msg="Q "+name
            s.sendto(msg.encode(),addr)
            sys.exit("退出聊天室")
        msg='C %s %s'%(name,text)
        s.sendto(msg.encode(),addr)
         



def recv_msg(s):
    while True:

        data,addr=s.recvfrom(2048)
        if data.decode()=="EXIT":
            sys.exit(0)
        print(data.decode()+"\n发言",end="")
        


#创建套接字，登录，创建子进程（互不干扰）
def main():
    if len(sys.argv)<3:
        print("argv is error")
        return
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    ADDR=(HOST,PORT)

    #创建套接字
    s=socket(AF_INET,SOCK_DGRAM)
    while  True:
        name=input("请输入你的姓名：")
        msg="L "+name
        #发送登录请求
        s.sendto(msg.encode(),ADDR)

        #等该服务器回复
        data,addr=s.recvfrom(1024)
        if data.decode()=='OK':
            print("登入成功，进入聊天室和你的朋友聊天吧")
            break
        else:
            #不成服务端会回复不成功的原因
            print(data.decode())
    pid=os.fork()
    if pid <0:
        sys.exit("创建子进程失败")
    elif pid==0:
        send_msg(s,name,ADDR)
    else:
        recv_msg(s)
if __name__=="__main__":
    main()
        

        
