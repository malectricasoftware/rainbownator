from sqlalchemy import create_engine, ForeignKey, Column, String, event
from sqlalchemy.orm import sessionmaker, declarative_base
import threading
import hashlib
from os.path import exists
from os import mkdir
import numpy as np
import argparse
import warnings

warnings.filterwarnings('ignore')

if not exists("dbs"):
	print("test")
	mkdir("dbs")
	
def parser():
	parser = argparse.ArgumentParser(description="rainbownator args")
	parser.add_argument("--hash",required=True)
	parser.add_argument("--algo",required=True)
	parser.add_argument("--wlist",required=True)
	parser.add_argument("--threads",default="40")
	args = parser.parse_args()
	return args

Base=declarative_base()

class Pass(Base):
	__tablename__ = "Pass"
	plain = Column("plain", String, primary_key=True)
	md5 = Column("md5", String)
	sha1 = Column("sha1", String)
	sha224 = Column("sha224", String)
	sha256 = Column("sha256", String)
	sha384 = Column("sha384", String)
	sha512 = Column("sha512", String)

	def __init__(self,plain,md5,sha1,sha224,sha256,sha384,sha512):
		self.plain = plain
		self.md5 = md5
		self.sha1 = sha1
		self.sha224 = sha224
		self.sha256 = sha256
		self.sha384 = sha384
		self.sha512 = sha512

	def __repr__(self):
		return f"plaintext: {self.plain} - md5: {self.md5} - shad1: {self.sha1} - sha224: {self.sha224} - sha256: {self.sha256} - sha384: {self.sha384} - sha512: {self.sha512}"

args=parser()
dbname=args.wlist.split("/")[-1].rsplit(".",1)[0]
engine = create_engine(f"sqlite:///dbs/{dbname}.db")
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

def dbcrack(algo,hashin):
	hashtype=getattr(Pass, algo)
	result = session.query(Pass.plain).filter(hashtype == hashin)
	try:
		print(f"{hashin} : {result[0][0]}")
		return True
	except IndexError:
		print("hash not present. trying wordlist")
		return False

def crack(algo, hashin, passcompl):
	hashtype=getattr(hashlib, algo)

	for passcomp in passcompl:
		passcomp=passcomp.replace("\n","")
		result = session.query(Pass).filter(Pass.plain==passcomp)
		if len(result.all()) == 0:
			p=Pass(passcomp, hashlib.md5(passcomp.encode()).hexdigest(), hashlib.sha1(passcomp.encode()).hexdigest(),hashlib.sha224(passcomp.encode()).hexdigest(),hashlib.sha256(passcomp.encode()).hexdigest(),hashlib.sha384(passcomp.encode()).hexdigest(),hashlib.sha512(passcomp.encode()).hexdigest())
			session.add(p)

		if hashtype(passcomp.encode("utf-8")).hexdigest() == hashin:
			print(f"{hashin} : {passcomp}")

def split(a,n):
	return(np.array_split(a, n))

print('''\033[49m                                                                                                              \033[m
\033[49m                                                                                                              \033[m
\033[49m                        \033[48;5;102m \033[38;5;102;49m▄\033[49m                                                                                    \033[m
\033[49m                        \033[49;38;5;102m▀\033[48;5;102m \033[38;5;102;48;5;102m▄\033[38;5;102;49m▄\033[49m    \033[38;5;145;49m▄▄\033[49m  \033[38;5;145;49m▄▄▄▄▄▄▄\033[49m                                                                   \033[m
\033[49m                         \033[48;5;102m   \033[38;5;145;48;5;102m▄\033[48;5;145m    \033[38;5;102;48;5;145m▄\033[48;5;102m \033[48;5;145m          \033[38;5;145;48;5;145m▄\033[38;5;145;49m▄▄▄\033[49m                                                             \033[m
\033[49m                         \033[49;38;5;102m▀\033[38;5;145;48;5;102m▄\033[48;5;145m      \033[49m \033[38;5;145;48;5;145m▄\033[48;5;145m              \033[49m \033[38;5;145;49m▄▄\033[49m                                                          \033[m
\033[49m                         \033[48;5;145m       \033[49;38;5;145m▀\033[38;5;248;49m▄\033[48;5;145m              \033[38;5;102;48;5;245m▄\033[38;5;102;48;5;102m▄\033[48;5;145m     \033[38;5;145;49m▄▄▄▄\033[49m                          \033[38;5;167;49m▄▄▄▄▄▄▄▄\033[49m                 \033[m
\033[49m                    \033[38;5;145;49m▄\033[49m   \033[38;5;145;49m▄\033[48;5;145m       \033[49m \033[48;5;145m               \033[48;5;102m \033[48;5;145m             \033[38;5;145;49m▄▄▄▄\033[49m       \033[38;5;167;49m▄▄▄▄▄\033[48;5;167m                    \033[38;5;167;48;5;167m▄\033[38;5;167;49m▄▄▄\033[49m        \033[m
\033[49m             \033[38;5;145;49m▄▄\033[48;5;145m       \033[48;5;102m  \033[48;5;145m       \033[38;5;145;48;5;145m▄\033[49m \033[38;5;246;48;5;145m▄\033[48;5;145m             \033[49m  \033[38;5;102;48;5;145m▄\033[38;5;247;48;5;145m▄\033[48;5;145m                  \033[38;5;145;49m▄\033[49m \033[38;5;167;48;5;167m▄\033[48;5;167m                               \033[38;5;167;48;5;167m▄\033[38;5;167;49m▄\033[49m     \033[m
\033[49m          \033[38;5;145;49m▄\033[48;5;145m           \033[48;5;102m  \033[38;5;102;48;5;145m▄\033[48;5;145m       \033[38;5;102;48;5;102m▄▄\033[49;38;5;145m▀▀\033[48;5;145m          \033[38;5;145;48;5;145m▄\033[49m \033[48;5;145m   \033[38;5;145;48;5;102m▄▄▄\033[38;5;248;48;5;145m▄\033[38;5;102;48;5;145m▄▄\033[38;5;245;48;5;145m▄\033[48;5;145m            \033[49m \033[38;5;167;49m▄\033[48;5;167m    \033[38;5;173;48;5;167m▄▄▄▄▄\033[48;5;173m                \033[38;5;173;48;5;167m▄▄▄\033[48;5;167m      \033[38;5;167;49m▄\033[49m   \033[m
\033[49m       \033[38;5;145;49m▄\033[38;5;145;48;5;145m▄\033[48;5;145m             \033[38;5;145;48;5;247m▄\033[48;5;102m  \033[38;5;102;48;5;145m▄\033[48;5;145m        \033[38;5;145;49m▄▄▄▄\033[49m \033[49;38;5;145m▀▀▀▀\033[48;5;145m   \033[49m \033[38;5;145;49m▄\033[48;5;145m    \033[49;38;5;145m▀▀\033[48;5;145m    \033[38;5;145;48;5;246m▄\033[38;5;145;48;5;102m▄▄\033[49;38;5;145m▀▀▀▀\033[48;5;145m    \033[49m  \033[38;5;215;48;5;167m▄\033[38;5;221;48;5;167m▄\033[38;5;221;48;5;173m▄▄▄▄▄▄▄\033[38;5;221;48;5;215m▄▄\033[38;5;221;48;5;221m▄▄\033[38;5;221;48;5;215m▄▄\033[38;5;221;48;5;173m▄▄▄▄▄▄▄\033[38;5;173;48;5;173m▄\033[48;5;173m        \033[38;5;173;48;5;167m▄\033[48;5;167m     \033[49m  \033[m
\033[49m      \033[38;5;145;49m▄\033[48;5;145m             \033[38;5;248;48;5;145m▄\033[48;5;145m \033[38;5;145;48;5;145m▄▄\033[38;5;145;48;5;102m▄\033[48;5;102m  \033[38;5;102;48;5;145m▄▄\033[48;5;145m            \033[38;5;145;49m▄▄▄▄\033[38;5;102;48;5;102m▄\033[48;5;102m \033[48;5;145m    \033[49m       \033[49;38;5;145m▀▀\033[49m         \033[38;5;96;49m▄\033[38;5;96;48;5;65m▄\033[38;5;60;48;5;65m▄▄▄▄▄\033[48;5;65m    \033[38;5;65;48;5;71m▄\033[38;5;65;48;5;221m▄▄▄▄▄▄\033[38;5;185;48;5;221m▄\033[48;5;221m        \033[38;5;221;48;5;173m▄▄\033[38;5;215;48;5;173m▄\033[48;5;173m     \033[38;5;173;48;5;167m▄\033[38;5;167;48;5;167m▄▄\033[49;38;5;167m▀\033[49m  \033[m
\033[49m    \033[38;5;145;49m▄\033[48;5;145m           \033[38;5;243;48;5;145m▄▄\033[49;38;5;243m▀\033[49;38;5;145m▀\033[48;5;145m \033[38;5;145;48;5;145m▄\033[49m     \033[49;38;5;243m▀\033[48;5;243m \033[38;5;243;48;5;243m▄\033[38;5;243;48;5;102m▄\033[49;38;5;247m▀\033[49;38;5;145m▀▀▀▀\033[48;5;145m              \033[49;38;5;145m▀\033[49m                    \033[49;38;5;96m▀▀▀\033[38;5;96;48;5;96m▄\033[38;5;96;48;5;60m▄▄▄\033[48;5;60m  \033[38;5;60;48;5;60m▄\033[38;5;60;48;5;65m▄▄▄\033[38;5;242;48;5;65m▄\033[48;5;65m      \033[38;5;65;48;5;221m▄▄\033[38;5;71;48;5;221m▄\033[48;5;221m      \033[38;5;221;48;5;173m▄\033[48;5;173m     \033[38;5;173;49m▄\033[49m   \033[m
\033[49m   \033[38;5;145;49m▄\033[48;5;145m           \033[38;5;246;48;5;243m▄\033[38;5;145;48;5;243m▄\033[48;5;145m \033[49m  \033[49;38;5;145m▀\033[38;5;145;48;5;249m▄\033[49m      \033[48;5;145m  \033[38;5;145;48;5;243m▄\033[49m             \033[49;38;5;145m▀▀▀▀▀\033[49m                            \033[49;38;5;96m▀▀\033[48;5;96m  \033[38;5;96;48;5;60m▄▄\033[38;5;60;48;5;60m▄\033[48;5;60m   \033[38;5;60;48;5;242m▄\033[38;5;60;48;5;65m▄▄\033[48;5;65m      \033[38;5;65;48;5;221m▄\033[48;5;221m     \033[38;5;221;48;5;173m▄\033[48;5;173m   \033[49;38;5;173m▀\033[49m   \033[m
\033[49m  \033[38;5;145;49m▄\033[48;5;145m          \033[49;38;5;145m▀\033[49m  \033[38;5;145;48;5;145m▄\033[48;5;145m  \033[38;5;145;49m▄▄\033[49m     \033[38;5;145;49m▄▄\033[48;5;145m  \033[49;38;5;145m▀\033[49m                                                  \033[49;38;5;96m▀▀\033[48;5;96m  \033[38;5;96;48;5;60m▄▄\033[38;5;60;48;5;60m▄\033[48;5;60m    \033[38;5;60;48;5;65m▄▄\033[48;5;65m    \033[38;5;65;48;5;143m▄\033[48;5;221m     \033[38;5;221;49m▄\033[49m     \033[m
\033[49m  \033[49;38;5;145m▀\033[48;5;145m         \033[49;38;5;145m▀\033[49m    \033[49;38;5;145m▀▀\033[48;5;145m         \033[49;38;5;145m▀▀\033[49m                                                      \033[49;38;5;96m▀▀\033[48;5;96m   \033[38;5;96;48;5;60m▄▄\033[48;5;60m    \033[38;5;60;48;5;65m▄\033[48;5;65m    \033[48;5;221m     \033[49m     \033[m
\033[49m     \033[49;38;5;145m▀▀▀\033[38;5;145;48;5;145m▄\033[48;5;145m  \033[38;5;145;48;5;145m▄\033[49m         \033[49;38;5;145m▀▀▀▀▀\033[49m                                                             \033[49;38;5;96m▀▀\033[48;5;96m   \033[38;5;96;48;5;60m▄\033[48;5;60m    \033[38;5;60;48;5;65m▄\033[48;5;65m   \033[38;5;65;48;5;65m▄\033[38;5;65;48;5;221m▄\033[49;38;5;221m▀\033[49m      \033[m
\033[49m                                                                                          \033[49;38;5;96m▀\033[48;5;96m   \033[38;5;96;48;5;60m▄\033[48;5;60m   \033[48;5;65m     \033[49m       \033[m
\033[49m                                                                                            \033[49;38;5;96m▀\033[48;5;96m   \033[48;5;60m   \033[38;5;60;48;5;65m▄▄\033[49;38;5;65m▀▀\033[49m       \033[m
\033[49m                                                                                             \033[49;38;5;96m▀\033[48;5;96m  \033[38;5;96;48;5;60m▄\033[48;5;60m    \033[38;5;60;49m▄\033[49m        \033[m
\033[49m                                                                                               \033[48;5;96m  \033[38;5;96;48;5;60m▄\033[48;5;60m  \033[38;5;60;48;5;60m▄\033[49m         \033[m
\033[49m                                                                                               \033[48;5;96m     \033[49m          \033[m
\033[49m                                                                                               \033[38;5;96;48;5;96m▄\033[48;5;96m   \033[38;5;96;48;5;96m▄\033[49m          \033[m
\033[49m                                                                                                              \033[m
\033[49m                                                                                                              \033[m
''')

with open("banner.txt","r") as banner:
	print(banner.read())

if not dbcrack(args.algo,args.hash):
	#file read and threading stuff
	with open(args.wlist, "r") as wf:
		lines=wf.readlines()
	if(len(lines)) > int(args.threads):
		number=int(len(lines)/int(args.threads))
	else:
		number=int(len(lines))
	chunks=split(lines,number)
	threads=[]
	for chunk in chunks:
		t=threading.Thread(target=crack, args=(args.algo,args.hash,chunk))
		t.start()
		threads.append(t)
	for t in threads:
		t.join()
session.commit()
