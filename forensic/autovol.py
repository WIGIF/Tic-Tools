#!/usr/bin/python3

from argparse import ArgumentParser
from sys import argv
from datetime import datetime
from random import choices
from time import sleep
from os import mkdir
from threading import Thread
from subprocess import run,PIPE,DEVNULL


class VolThread(Thread):
	def __init__(self,file,profil,cmd,outdir):
		Thread.__init__(self)
		self.file = file
		self.profil = profil
		self.cmd = cmd
		self.outdir = outdir
		self.result = ''
	
	def run(self):
		global done_count
		try:
			self.result = run([VOL2_PATH, f'-f {self.file}',f'--profil={self.profil}',self.cmd],stdout=PIPE,stderr=DEVNULL).stdout.decode()
			if self.result == '': raise Exception()
			with open(self.outdir + self.cmd,'w') as file:
				file.write(self.result)
			print('\x1b[1A\x1b[2K',end='')
			print(f'{self.cmd:12s} : \x1b[32m\x1b[1mDONE\x1b[0m')
		except:
			print('\x1b[1A\x1b[2K',end='')
			print(f'{self.cmd:12s} : \x1b[31m\x1b[1mERROR\x1b[0m')
		done_count += 1
		print(f"[{(done_count*'■' + ' '*len(cmd_list))[:len(cmd_list)]}] {done_count} / {len(cmd_list)}")


def report(file,profil):
	CP_name = run([VOL2_PATH, f'-f {file}',f'--profil={profil}',"printkey -K" ,"ControlSet001\\Control\\ComputerName\\ActiveComputerName"],stdout=PIPE,stderr=DEVNULL).stdout.decode()[39:]
	print(CP_name)
	USR_lst = run([VOL2_PATH, f'-f {file}',f'--profil={profil}',"hashdump"],stdout=PIPE,stderr=DEVNULL).stdout.decode()
	print(USR_lst,end='')

def KDBG(file):
	print('Determining profile ...')
	cmd = run([VOL2_PATH, f'-f {file}','imageinfo'],stdout=PIPE,stderr=DEVNULL)
	pf = cmd.stdout.decode().replace('  ','').split(' ')[3][:-1]
	print(f'Profile FOUND : {pf}')
	return pf

def check_th(thread_list):
	"""
		Check how many threads are alive
	"""
	alive_th = 0
	for th in thread_list:
		if th.is_alive():
			alive_th += 1
	return alive_th

def cmd_menu(all):
	if not all : return ['cmdline','consoles','envars','filescan','hashdump','psscan','pstree']
	return ['clipboard','cmdline','consoles','envars','filescan','hashdump','hivelist','iehistory','lsadump','malfind','mftparser','notepad','psscan','pstree','psxview','sockets','truecryptsummary']

if __name__ == "__main__" :
	
	VOL2_PATH = "vol2"

	parser = ArgumentParser()
	parser.add_argument("-f", help="Input file", type=str, required=True)
	parser.add_argument("-p","--profil", help="OS Profile", type=str, required=('-k' not in argv and '--kdbg' not in argv))
	parser.add_argument("-k","--kdbg", help="Find profile using KDBG", action="store_true")
	parser.add_argument("-a", help="Use all commands",action="store_true")
	parser.add_argument("-t", help="Max threads", type=str, default=3)
	parser.add_argument("-o", help="Output directory", type=str)
	args = parser.parse_args()

	input_file = args.f
	if args.kdbg : profil = KDBG(input_file)
	else : profil = args.profil

	if args.o : 
		outdir = args.o
		if outdir[-1] != '/' : outdir += '/'
	else:
		nonce = ''.join(choices('0123456789abcdef',k=2))
		outdir = f'/tmp/vol_{nonce}_{datetime.now().strftime("%d:%m_%Hh%M")}/'
		mkdir(outdir)
		print(f'Out dir : {outdir}')
	
	if args.a : cmd_list = cmd_menu(True)
	else : cmd_list = cmd_menu(False)
	
	report(input_file,profil)
	
	print("\n----------------------------\nStart scan...\n")
	print(f"[{' '*len(cmd_list)}] 0 / {len(cmd_list)}")

	thread_count = 0
	thread_list = []
	done_count = 0

	for cmd in cmd_list :
		while thread_count > args.t :
			sleep(2)
			thread_count = check_th(thread_list)
		thread_list.append(VolThread(input_file,profil,cmd,outdir))
		thread_list[-1].start()
		thread_count += 1
