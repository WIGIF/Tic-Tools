
import subprocess
import threading
from os import system,mkdir
from datetime import datetime
from random import choices
from time import sleep


class VolThread(threading.Thread):
	def __init__(self,file,profil,cmd,outdir):
		threading.Thread.__init__(self)
		self.file = file
		self.profil = profil
		self.cmd = cmd
		self.outdir = outdir
		self.result = ''
	
	def run(self):
		try:
			self.result = subprocess.run(['vol2', f'-f {self.file}',f'--profil={self.profil}',self.cmd],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL).stdout.decode()
			if self.result == '': raise Exception()
			with open(self.outdir + self.cmd,'w') as file:
				file.write(self.result)
			print(self.cmd + ' : \x1b[32m\x1b[1mDONE\x1b[0m')
		except:
			print(self.cmd + ' : \x1b[31m\x1b[1mERROR\x1b[0m')


def main(argv):

	print("""	
.-.   .-.,---.  ,---.    .---.  .--.  _______ ,-.,-.    ,-. _______.-.   .-.
 \ \ / / | .-'  | .-.\  ( .-._)/ /\ \|__   __||(|| |    |(||__   __|\ \_/ )/
  \ V /  | `-.  | `-'/ (_) \  / /__\ \ )| |   (_)| |    (_)  )| |    \   (_)
   ) /   | .-'  |   (  _  \ \ |  __  |(_) |   | || |    | | (_) |     ) (   
  (_)    |  `--.| |\ \( `-'  )| |  |)|  | |   | || `--. | |   | |     | |   
         /( __.'|_| \)\`----' |_|  (_)  `-'   `-'|( __.'`-'   `-'    /(_|   
        (__)        (__)                         (_)                (__)    

	""")


	input_file = '/home/axonarage/test/ch2.dmp'
	profil = KDBG(input_file)

	nonce = ''.join(choices('0123456789abcdef',k=2))
	outdir = f'/tmp/vol_{nonce}_{datetime.now().strftime("%d:%m_%Hh%M")}/'
	mkdir(outdir)
	print(f'Out : \x1b[1m{outdir}\x1b[0m')

	th_list = []
	cmd_list = cmd_menu()

	th_count = 0
	max_thread = 2
	for cmd in cmd_list :
		while th_count > max_thread :
			sleep(2)
			th_count = check_th(th_list)
		th_list.append(VolThread(input_file,profil,cmd,outdir))
		th_list[-1].start()
		th_count += 1


def KDBG(file):
	print('Determining profile ...')
	cmd = subprocess.run(['vol2', f'-f {file}','imageinfo'],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
	pf = cmd.stdout.decode().replace('  ','').split(' ')[3][:-1]
	print(f'Profile FOUND : \x1b[34m\x1b[1m{pf}\x1b[0m')
	return pf

def check_th(th_list):
	alive_th = 0
	for th in th_list:
		if th.is_alive():
			alive_th += 1
	return alive_th

def cmd_menu():
	return ['clipboard','cmdline','consoles','envars','filescan','hashdump','hivelist','iehistory','mftparser','notepad','psscan','pstree','psxview','truecryptsummary']

main('ts')