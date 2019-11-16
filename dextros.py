#!/usr/bin/env python3

import textwrap
import hashlib
import itertools
import time
import string
import sys
import os
import platform



ver = platform.python_version()

if (ver <= '3'):
	print("\033[91m[!] dextros is not supported below python3\033[00m")
	sys.exit(1)


# import errors
try:
	from mpi4py import MPI
	try:
		from passlib.hash import nthash, lmhash
	except ImportError:
		print("\033[91mHuh..? Always read README before running any new script ;)\033[00m")
		print("\033[91mpasslib not installed! I will install for you\033[00m")
		os.system("pip3 install passlib")
except ImportError:
#	print("\033[91mmpi4py is not installed! I will install for you\033[00m")
#	os.system("pip3 install mpi4py")
#	sys.exit(1)
	print("")


# banner always looks great


print("""\033[91m
       __          __
  ____/ /__  _  __/ /__________  _____
 / __  / _ \| |/_/ __/ ___/ __ \/ ___/
/ /_/ /  __/>  </ /_/ /  / /_/ (__  )
\__,_/\___/_/|_|\__/_/   \____/____/
					V.1.0\033[00m

				\033[93mBy shubham_chaskar and Rohith_rachappale\033[00m

""")

a= input("\033[92mPaste the hash here: ")
b = input("""\033[92mSelect the attack method: 
		    1) Dictionary Attack
		    2) Brute-force attack
		\033[00m""")

c = input("Give full path for dictionary: ")
print("\033[92mCalling other nodes and distributing the task..\033[00m")
# MPI variables

comm = MPI.COMM_WORLD
name = MPI.Get_processor_name()
rank = comm.Get_rank()
size = comm.Get_size()

# functions for generating hash


def md5(guess):
	enc = guess.encode()
	final = (hashlib.md5(enc)).hexdigest()
	return final


def sha1(guess):
	enc = guess.encode()
	final = (hashlib.sha1(enc)).hexdigest()
	return final


def sha224(guess):
	enc = guess.encode()
	final = (hashlib.sha224(enc)).hexdigest()
	return final


def sha256(guess):
	enc = guess.encode()
	final = (hashlib.sha256(enc)).hexdigest()
	return final


def sha384(guess):
	enc = guess.encode()
	final = (hashlib.sha384(enc)).hexdigest()
	return final


def sha512(guess):
	enc = guess.encode()
	final = (hashlib.sha512(enc)).hexdigest()
	return final

# this is for windows


def ntlm(guess):
	nt = nthash.hash(guess)
	lm = lmhash.hash(guess)
	final_ntlm = lm + nt
	return final_ntlm


def display(final_pass, node_name):
	print("*" * 150)
	print("\033[92mPASSWORD FOUND : ", final_pass, "by the node", node_name,"\033[00m")
	print("*" * 150)
	print("\033[92mTime taken: ", time.time() - t,"\033[00m")
	print("*" * 150)
	comm.Abort()
	sys.exit(0)


t = time.time()

# master code
if rank == 0:
	global min_length
	global max_length
	pre_user_hash = input("\033[92mEnter Hash to Crack..\033[00m\n")
	user_hash = pre_user_hash.replace(':', '')  # removing ':' from windows hash
	print("")
	if len(user_hash) == 64:
		confirm = input("\033[91mIs This Hash Retrieved From windows SAM Database...(y/n)\033[00m  ")

	length_of_hash = len(user_hash)
	hash_lengths = ['40', '32', '56', '64', '96', '128']
	if str(length_of_hash) in hash_lengths:
		choice_of_attack = int(input("what you want to do with hash..\nEnter your choice:\n 1)Dictionary Attack\n 2)Brute-Force \n"))
		if choice_of_attack == 1:
			min_length = 0
			max_length = 0
			choice_of_characters = ""
			final_node_string = ""
			file_path = input("\033[92mEnter full path for Dictionary :\033[00m")
			print("")
			if os.path.exists(file_path):
				print("\033[92mDictionary File found...Proceeding\033[00m \n")
				num_lines = 0

				with open(file_path, 'r') as f:  # it will count number of lines that will help us to divide file in equal parts
					print("\033[92mcounting number of words to distribute them into node equal number of files: \033[00m\n")
					print("[\033[92mIt will take few minutes........\033[00m \n")
					for line in f:
						num_lines += 1
				print("\033[92mNumber of words are present in dictionary are: ", num_lines, "\033[00m\n")

				count = (num_lines + (size - 1)) // (size - 1)
				lines_per_file = count
				smallfile = None
				final_node = []

				with open(file_path) as bigfile:  # creating new files in master for nodes
					print("\033[92mwriting into new files for distribution to the nodes: \033[00m\n")
					print("\033[92mIt will take some time..........\033[00m\n")
					for lineno, line in enumerate(bigfile):
						if lineno % lines_per_file == 0:
							if smallfile:
								smallfile.close()
							small_filename = 'small_file_{}.txt'.format(lineno + lines_per_file)
							smallfile = open(small_filename, "w")
						smallfile.write(line)
						if lineno % lines_per_file == 0:
							final_node.append(small_filename)

					for node in range(size - 1):  # distributing files to nodes using SCP.
						print("\033[92mdistributing files to the nodes: \033[00m\n")
						print("\033[92mDistribution will take some time......\033[00m\n")
						if final_node[node] in final_node:
							name = "compute-0-" + str(node)
							command = "scp " + final_node[node] + " root@" + name + ":/root"
							process = os.popen(command)
							comm.send((final_node_string, user_hash, min_length, max_length, choice_of_characters, choice_of_attack, final_node[node]), dest=node + 1)
							print("\033[92mTransferring file ", final_node[node], "from node ", name, "\033[00m\n")

					if smallfile:
						smallfile.close()

			else:
				print("\033[91mFile not found, enter correct location...\033[00m")
				sys.exit(0)

		elif choice_of_attack == 2:
			dicn_file = ''

			min_length = int(input("\033[92mEnter expected minimum length :\033[00m\n"))
			print("")
			max_length = int(input("\033[92mEnter expected maximum length :\033[00m\n"))
			print("")
			# choice_of_characters = input("\033[92mEnter the choice of characters: \033[00m")
			# print("")
			# special_characters = input("\033[92mEnter choice of special characters: \033[00m")
			# user_list = list(choice_of_characters)

			default = string.ascii_uppercase+string.ascii_lowercase+string.digits
			default_list = list(default)

			# for char in user_list:
			# 	if char in default_list:
			# 		default_list.remove(char)
			# ref_string_to_join = ''

			# string_after_join = ref_string_to_join.join(default_list)

			# choice_of_characters = choice_of_characters + special_characters

			final_string = default

			length_final_string = len(final_string)

			parts = length_final_string//size

			wrapped = textwrap.wrap(final_string, parts)

			for node in range(size):		# wrapping list for nodes (different starting point for each nodes)
				wrapped_list = list(final_string)
				if wrapped[node] in wrapped:
					sub_wrapped_list = list(wrapped[node])
					for part in sub_wrapped_list:
						if part in sub_wrapped_list:
							wrapped_list.remove(part)
					sub_ref_string_to_join = ""
					sub_string_after_join = sub_ref_string_to_join.join(wrapped_list)
					final_node_string = wrapped[node] + sub_string_after_join

					for k in range(1):					# sending all parameters to nodes
						if sub_wrapped_list[0] in sub_wrapped_list:
							print("\033[92mSending...\033[00m")
							comm.send((final_node_string, user_hash, min_length, max_length, choice_of_attack, dicn_file, confirm), dest=node)
		else:
			print("\033[91mPlease enter either '1' or '2'....exiting\033[00m")
			comm.Abort()
			sys.exit(1)
	else:
		print("\033[91mUnsupported hash format\033[00m")
		comm.Abort()
		sys.exit(1)


else:
	# code for nodes

	my_final, user_hash, min_length, max_length, choice_of_characters, choice_of_attack, dicn_file, confirm = comm.recv(source=0)
	t = time.time()
	attempts = 1
	if choice_of_attack == 1:
		print("\033[92m Received ", dicn_file, "By this node ", name, "\033[00m\n")
		print("\033[92mI need some sleep so Sleeping for 35 seconds....\033[00m")  # sleeping because SCP takes time to transfer files
		time.sleep(35)
		if os.path.exists(dicn_file):
			print("\033[92mLocation seems good.... proceeding\033[00m\n")
		else:
			print("\033[92mpath for dictionary is incorrect\033[00m")
			MPI.Abort()
			sys.exit(1)
		f = open(dicn_file, "r")
		for password in f:
			attempts += 1
			if confirm == 'y':
				hash_generated = ntlm(password[:-1])
				if (attempts % 1000) == 0:
					print("password attempting: ", password, " on node: ", name)

				if user_hash == hash_generated:
					display(password, name)

			elif len(user_hash) == 32:
				hash_generated = md5(password[:-1])
				if (attempts % 1000) == 0:
					print("password attempting: ", password, " on node: ", name)

				if user_hash == hash_generated:
					display(password, name)

			elif len(user_hash) == 40:
				hash_generated = sha1(password[:-1])
				if (attempts % 1000) == 0:
					print("password attempting: ", password, " on node: ", name)

				if user_hash == hash_generated:
					display(password, name)

			elif len(user_hash) == 56:
				hash_generated = sha224(password[:-1])
				if (attempts % 1000) == 0:
					print("password attempting: ", password, " on node: ", name)

				if user_hash == hash_generated:
					display(password, name)

			elif len(user_hash) == 64:
				hash_generated = sha256(password[:-1])
				if (attempts % 1000) == 0:
					print("password attempting: ", password, " on node: ", name)

				if user_hash == hash_generated:
					display(password, name)

			elif len(user_hash) == 96:
				hash_generated = sha384(password[:-1])
				if (attempts % 1000) == 0:
					print("password attempting: ", password, " on node: ", name)

				if user_hash == hash_generated:
					display(password, name)

			elif len(user_hash) == 128:
				hash_generated = sha512(password[:-1])
				if (attempts % 1000) == 0:
					print("password attempting: ", password, " on node: ", name)

				if user_hash == hash_generated:
					display(password, name)

			else:
				print("Unsupported hash format")
				sys.exit(1)

	elif choice_of_attack == 2:
		print("\033[92mReceiving string from Master to make combinations  \033[00m")
		# brute-force for nodes
		attempts = 0
		for length in range(min_length, max_length + 1):

			for password in itertools.product(my_final, repeat=length):
				attempts += 1
				password = "".join(password)
				if confirm == 'y':
					hash_generated = ntlm(password)
					if (attempts % 1000) == 0:
						print("password attempting: ", password, " on node: ", name)

					if user_hash == hash_generated:
						display(password, name)

				elif len(user_hash) == 32:
					hash_generated = md5(password)
					if (attempts % 1000) == 0:
						print("password attempting: ", password, " on node: ", name)

					if user_hash == hash_generated:
						display(password, name)

				elif len(user_hash) == 40:
					hash_generated = sha1(password)
					if (attempts % 1000) == 0:
						print("password attempting: ", password, " on node: ", name)

					if user_hash == hash_generated:
						display(password, name)

				elif len(user_hash) == 56:
					hash_generated = sha224(password)
					if (attempts % 1000) == 0:
						print("password attempting: ", password, " on node: ", name)

					if user_hash == hash_generated:
						display(password, name)

				elif len(user_hash) == 64:
					hash_generated = sha256(password)
					if (attempts % 1000) == 0:
						print("password attempting: ", password, " on node: ", name)

					if user_hash == hash_generated:
						display(password, name)

				elif len(user_hash) == 96:
					hash_generated = sha384(password)
					if (attempts % 1000) == 0:
						print("password attempting: ", password, " on node: ", name)

					if user_hash == hash_generated:
						display(password, name)

				elif len(user_hash) == 128:
					hash_generated = sha512(password)
					if (attempts % 1000) == 0:
						print("password attempting: ", password, " on node: ", name)

					if user_hash == hash_generated:
						display(password, name)

				else:
					print("unsupported hash format")
					sys.exit(1)
