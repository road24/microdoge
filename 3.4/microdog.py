import os,sys,socket,struct,binascii


GOLD_SALT = 0x646C6F47

login_packet = [
0xDE, 0x9B, 0x0F, 0x00, 
0x74, 0x01, 0x00, 0x00, #THIS IS WHERE OUR RETCODE GOES

0xBB, 0x70, 
0xB3, 0x70, 
# FUCK MY LIFE THE GODDAMNED ID IS ENDIAN SWAPPED HIGH LOW
0xB0, 0x49, 0x28, 0xBB, 
0xE6, 0x09, 0x87, 0x04, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0xbb, 0x70, 0x6c, 0x64, 0x00, 0x00, 0x00, 0x00,
  
]

enable_share = [
0xDE, 0x9B, 0x0F, 0x00, # Dog Serial
0x00, 0x00, 0x00, 0x00, # Mask Key
0xBB, 0x70,  # Length of response I guess
0xBA, 0x70,  # No idea - Maybe Return Code

#Payload and I guess thats it because any more bytes gets into the request memory.
0x70, 0x00, 0x00, 0x00, 0xCE, 0x35, 0x6E, 0xB7, 0xCD, 0x31, 0x6F, 0xB7, 0x00, 0x40, 0x70, 0xB7, 
0x00, 0x40, 0x70, 0xB7, 0x07, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0xBE, 0xCC, 0x52, 0xB7, 
0x02, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x80, 0x00, 0x40, 0x70, 0xB7, 0x3E, 0xDE, 0x6E, 0xB7, 
0x00, 0x30, 0x70, 0xB7, 0x00, 0x10, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x40, 0x70, 0xB7, 
0x07, 0x00, 0x00, 0x00, 0x00, 0x40, 0x70, 0xB7, 0xA8, 0x69, 0xF9, 0xBF, 0x86, 0xE3, 0x6E, 0xB7, 
0xF0, 0x4A, 0x70, 0xB7, 0xF8, 0x1D, 0x6E, 0xB7, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x88, 0x00, 0x00, 0x00, 0x53, 0x8B, 0x6F, 0xB7, 
0x08, 0x00, 0x00, 0x00, 0x88, 0x00, 0x00, 0x00, 0xD8, 0x1D, 0x6E, 0xB7, 0xD8, 0x1D, 0x6E, 0xB7, 
0x00, 0x00, 0x00, 0x00, 0x06, 0xCC, 0x6F, 0xB7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x06, 0xCC, 0x6F, 0xB7, 0x5C, 0x45, 0x70, 0xB7, 0x94, 0x34, 0x6E, 0xB7, 0xA8, 0x69, 0xF9, 0xBF, 
0xD4, 0x32, 0x6E, 0xB7, 0x12, 0x36, 0x6E, 0xB7, 0xD4, 0x32, 0x6E, 0xB7, 0x00, 0x00, 0x00, 0x00, 
0x34, 0x33, 0x6E, 0xB7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x6E, 0xB7, 0xA8, 0x69, 0xF9, 0xBF, 
0x00, 0x40, 0x70, 0xB7, 0x00, 0x29, 0x51, 0xB7, 0xC0, 0x2D, 0x51, 0xB7, 0x08, 0x4B, 0x6F, 0xB7, 
0x40, 0x00, 0x00, 0x00, 0x18, 0x03, 0x52, 0xB7, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 
0x14, 0x37, 0x6E, 0xB7, 0xAD, 0xBF, 0x6E, 0xB7, 0x59, 0x5F, 0x52, 0xB7, 0x28, 0x83, 0x04, 0x08, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0xbb, 0x70, 0x6c, 0x64, 0x00, 0x00, 0x00, 0x00
]





class Microdog:
	def __init__(self):
		self.node_name = "/var/run/microdog/u.daemon"
		self.dog_id = ""
		self.dog_key = 0xBADDDEAD
		self.dog_serial = 0xDEADBEEF
		self.dog_platform = "Linux"
		self.dog_table = {}
		self.md_version = "4.0"
		if not os.path.exists("/var/run/microdog"):
			os.makedirs("/var/run/microdog")
		self.load_info()
		
	#Reads dongle data from descriptor table.
	def load_info(self):
		with open(sys.argv[1]) as f:
			lines = f.readlines()
			for line in lines:
				line = line.strip()
				if(not "#" in line):
					elements = line.split(" ")
					if(len(elements) == 3):
						if(elements[0] == "i"):
							self.dog_id = elements[2]
							self.dog_key = int(elements[1],16)
						if(elements[0] == "c"):
							self.dog_table[elements[2]] = int(elements[1], 16)
						if(elements[0] == "s"):
							self.dog_serial = int(elements[1],16)
						if(elements[0] == "v"):
							self.md_version = elements[1]
							self.dog_platform = elements[2]

		print("Loaded Microdog Version %s" % self.md_version)
		print("Dog Name: %s" % self.dog_platform)
		print("Dog Key: %04X" % self.dog_key)
		print("DogID: %s\nDogSerial:%04x" % (self.dog_id,self.dog_serial))
		print("Loaded %d Keys\n" % len(self.dog_table))	
	
	def login(self,request):
		#TODO - actually DO the request decrypt logic.
		login_response = bytearray(280)
		login_response[0:4] = struct.pack("<I",self.dog_key)
		login_response[4:8] = struct.pack("<I",0)
		tmp_mask = (struct.unpack("<I",request[8:12])[0] + GOLD_SALT) & 0xFFFFFFFF
		#
		cascade = 0
		login_response[8:10] = struct.pack("<H",cascade ^ (tmp_mask & 0xFFFF))
		dogbytes = 8
		login_response[10:12] = struct.pack("<H",dogbytes^ (tmp_mask & 0xFFFF)) 
		#Now we have to cut the dogid up (yes yes cutting up the dog)...
		#AND ENDIAN SWAP
		
		
		payload1 = struct.unpack("<I",binascii.unhexlify(self.dog_id[0:8]))[0] ^ tmp_mask
		
		payload2 = struct.unpack("<I",binascii.unhexlify(self.dog_id[8:16]))[0] ^ tmp_mask
		print("%04X %04X" % (payload1,payload2))
		login_response[8:12] = struct.pack("<I",payload1)
		login_response[12:16] = struct.pack("<I",payload2)
		#print(binascii.hexlify(login_response))
		return login_response
	
	def enable_share(self,request):
		#Todo - actually DO the transaction...
		share_response = bytearray(enable_share)
		
		return share_response
	
	def process(self,request):
		magic =  struct.unpack("<H",request[0:2])[0]
		if(magic != 0x484D):
			print("Error - Unsupported Packet Type")
		opcode = struct.unpack("<H",request[2:4])[0]
		
		tmp_mask = (struct.unpack("<I",request[8:12])[0] + GOLD_SALT) & 0xFFFFFFFF
		
		tmb_mask = bytearray(struct.pack("<I",tmp_mask))
		#We can just decrypt all this shit in place... why not.
		request[12:14] = struct.pack("<H",struct.unpack("<H",request[12:14])[0] ^ (tmp_mask & 0xFFFF))
		request[14:16] = struct.pack("<H",struct.unpack("<H",request[14:16])[0] ^ (tmp_mask & 0xFFFF))
		for i in range(0,256):
			request[16+i] = request[16+i] ^ tmb_mask[i % 4]

		if(opcode == 0x14):
			print("Login Request")
			return self.login(request)
		elif(opcode == 0x08):
			print("EnableShare Request")
			return self.enable_share(request)
		elif(opcode == 0x04):
			print("DogConvert Request")
			return self.convert(request)
			
	def convert(self,request):
		
	
		dogbytes = struct.unpack("<H",request[14:16])[0] 
		rq_str = binascii.hexlify(request[16:16+dogbytes])
		print(dogbytes)

		try:
			response = self.dog_table[rq_str]
			print("%s -> %#x" % (rq_str,response))
		except:
			print("ERR: %s not found in rainbow table!" % rq_str)
			print("Request length is %d" % dogbytes)
			response = 0xBADF00D
		convert_response = bytearray(280)
		convert_response[0:4] = struct.pack("<I",self.dog_key)
		convert_response[4:8] = struct.pack("<I",0)
		tmp_mask = (struct.unpack("<I",request[8:12])[0] + GOLD_SALT) & 0xFFFFFFFF
				#
		cascade = 0
		convert_response[8:10] = struct.pack("<H",cascade ^ (tmp_mask & 0xFFFF))
		dogbytes = 4
		convert_response[10:12] = struct.pack("<H",dogbytes^ (tmp_mask & 0xFFFF)) 
		#Now we have to cut the dogid up (yes yes cutting up the dog)...
		#AND ENDIAN SWAP
		convert_response[8:12] = struct.pack("<I",response ^ tmp_mask)		
				
		#print(binascii.hexlify(convert_response))		
	
		return bytearray(convert_response)