MOD = 256

def getLfsr(key):
# Membuat keystream menggunakan LFSR
# Bit keluaran dalam untuk string dengan panjang n adalah sn tiap fungsi umpan balik dipanggil
# Fungsi umpan balik: s0 = f(s0, sn) = s0 XOR sn
# Output: keystream LFSR
  res = []
  for i in range(2 ** len(key) - 1):
    res.append(key[-1])
    f = key[0] ^ key[-1]
    key = key[:len(key)-1]
    key.insert(0, f)

  return res

def getKeystreamRc4(key):
# Membuat keystream menggunakan RC4 algorithm dan LFSR
# Proses: KSA - PRGA - XOR dengan hasil getLfsr(key)
# Output: keystream RC4
  key = [ord(val) for val in key]
  lfsr = getLfsr(key)

  # KSA
  keyLength = len(key)
  S = list(range(MOD))
  j = 0
  for i in range(MOD):
    j = (j + S[i] + key[i % keyLength]) % MOD
    S[i], S[j] = S[j], S[i]

  # PRGA
  i = 0
  j = 0
  k = 0
  while True:
    i = (i + 1) % MOD
    j = (j + S[i]) % MOD
    S[i], S[j] = S[j], S[i]
    res = S[(S[i] + S[j]) % MOD]

    # XOR again with LFSR
    res = res ^ lfsr[k]
    k = (k + 1) % len(lfsr)

    yield res

def methodRc4(key, textInput):
# Enkripsi atau deskripsi textInput dengan key menggunakan RC4 algorithm
# Output: hasil enkripsi atau deskripsi
  keystream = getKeystreamRc4(key)
  textInput = [ord(val) for val in textInput]

  res = ''
  for val in textInput:
    res += chr(val ^ next(keystream))

  return res