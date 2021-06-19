cpdef  bt_for(bytes bufer,list result):
	for i in range(len(bufer) // 4):
		result.append(str(int.from_bytes(bufer[i*4 : (i+1)*4], 'big', signed=False,)))