MOD = 256

def getLfsr(key):
# Generate keystream using LFSR
  res = []
  for i in range(2 ** len(key) - 1):
    res.append(key[-1])
    f = key[0] ^ key[-1]
    key = key[:len(key)-1]
    key.insert(0, f)

  return res

def getKeystreamRc4(key):
# Generate keystream using RC4 algorithm and LFSR
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
# Encrypt or Decrypt textInput with key using RC4 algorithm
  keystream = getKeystreamRc4(key)
  textInput = [ord(val) for val in textInput]

  res = ''
  for val in textInput:
    res += chr(val ^ next(keystream))

  return res