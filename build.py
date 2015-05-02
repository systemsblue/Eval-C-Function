#!/usr/bin/env python

import os
import sys

def usage():
	print "Usage : python " + sys.argv[0] + " < C source file: *.c >"
	print "Eval-C Function Header Generator & Code Builder"
	exit(0)

def prn(x): hd.write(x + "\n")

argc = len(sys.argv)
if argc != 2:
	usage()

fname = sys.argv[1]
if fname[-2:] != ".c":
	usage()		

try:
	f = open(fname, 'r')
except:
	print "No such file: " + fname
	exit(1)
	
hf = 0
pf = 0
list = []
for line in f:
	if line.find("/*SO*/") >= 0:
		sp = line[:-1].split()
		if sp[1] == "/*SO*/":
			if sp[0] == "#include":
				if pf == 0:
					print "No parameters for evalc()."
					exit(1)
				header = sp[2].replace("\"", "")
				hf += 1		
			else:
				if hf > 0:
					print "Descript the generated header file name '" + header + "' after all parameters definition."
					exit(1)
				list.append(sp)
				pf += 1
f.close()
if hf == 0:
	print "No generated header file name"
	exit(1)

hd = open(header, 'w')

# Generate header file

prn("char *__eval_fmt = \"#include<stdio.h>\\n\\")
prn("#include<string.h>\\n\\")
prn("typedef struct{\\n\\")

for l in list:
	if l[0] == "char" and l[2].find("[") >= 0:
		sp = l[2].split("[")
		prn(l[0] + " *" + sp[0] + ";\\n\\")
	else:
		prn(l[0] + " " + l[2] + "\\n\\")


prn("} __PSTRC;\\n\\")

prn("void __feval(__PSTRC *ps){\\n\\")

for l in list:
	if l[0] == "char" and l[2].find("[") >= 0:
		sp = l[2].split("[")
		prn("char *" + sp[0] + "; " + sp[0] + " = ps->" + sp[0] + ";\\n\\")
	else:
		p = l[2].replace(';', '')
		prn(l[0] + " " + p + " = ps->" + p + ";\\n\\")


prn("%s;\\n\\")

for l in list:
	if l[0] != "char":	
		p = l[2].replace(';', '')
		prn("ps->" + p + " = " + p + ";\\n\\")


prn("}\";")

prn("typedef struct{")

for l in list:
	if l[0] == "char" and l[2].find("[") >= 0:
		sp = l[2].split("[")
		prn(l[0] + " *" + sp[0] + ";")
	else:
		prn(l[0] + " " + l[2])



prn("} __PSTRC;")

prn("int evalc(char *eval){")
prn("void (*func)(__PSTRC *);")
prn("void *so;")
prn("__PSTRC ps;")

for l in list:
	if l[0] == "char" and l[2].find("[") >= 0:
		sp = l[2].split("[")
		prn("ps." + sp[0] + " = " + sp[0] + ";")
	else:
		p = l[2].replace(';', '')
		prn("ps." + p + " = " + p + ";")

code = """
	FILE *fp;

	strcpy(ps.pstr1, pstr1);

	fp = fopen("./sotemp.c", "w");
	fprintf(fp, __eval_fmt, eval);
	fclose(fp);
	system("cc -w -fPIC --share -o ./sotemp.so ./sotemp.c");

	so = dlopen("./sotemp.so", RTLD_LAZY);
	if(!so){
		fprintf(stderr, "%s\\n", dlerror());
		return -1;
	}

	func = dlsym(so, "__feval");

	if(!func){
		fprintf(stderr, "%s\\n", dlerror());
		return -2;
	}

	(*func)(&ps);
	dlclose(so);
"""[1:-1]

prn(code)

for l in list:
	if l[0] != "char":	
		p = l[2].replace(';', '')
		prn(p + " = ps." + p + ";")

prn("return 0;}")

hd.close()

os.system("export PRELOAD=./sotemp.so")
os.system("cc -o " + fname[:-2] + " " + fname + " -ldl")

