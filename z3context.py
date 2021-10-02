from z3 import *

ctx1, ctx2, ctx3, ctx4 = BitVecs('ctx1 ctx2 ctx3 ctx4', 32)
context = [
	ctx1,
	ctx2,
	ctx3,
	ctx4,
]

tmpcnt = 0

def sym_u32(context):
	n = context[0] ^ (context[0] << 11)
	context[0] = context[1]
	context[1] = context[2]
	context[2] = context[3]
	context[3] = n ^ LShR(n, 8) ^ context[3] ^ LShR(context[3], 19)
	return context[3]

def sym_rand_bool(context):
	return sym_u32 & 0x80000000

def sym_rand_int(context, low, high):
	tmp = Bitvecs('tmp{}'.format(tmpcnt), 64)
	tmpcnt += 1
	tmp *= 0
	rand = sym_u32(context)
	tmp |= rand
	return  LShR(tmp * (high - low + 1), 32) + low

def sym_rand_float(context, af, bf):
	val = 0x3F800000 | LShR(sym_u32(context), 9)
	fval = fpBVToFP(val, Float32())
	# 
	# TODO: check RNE vs RNA in docs
	rm = RNE()
	return fpAdd(rm, a, fpMul(rm, fpSub(rm, fval, 1.0), b-a))

def sym_calc(context):
	base = sym_rand_int(context, 90, 110)
	chance = sym_rand_int(0, 99)
	# TODO: the rest of the fucking owl
