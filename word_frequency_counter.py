import string

fn = input("File to read> ")

count = {}

with open(fn) as fp:
    data = fp.read().lower()

data = data.splitlines()
nd = []
for x in data:
    nd.extend(map(lambda x: ''.join([y for y in x if y in string.ascii_lowercase or y in string.digits]), x.split()))

for x in range(nd.count('')):
    nd.remove('')

for x in nd:
    count.setdefault(x, 0)
    count[x] += 1

# Reverse the frequencies
freq_word = {}
for k, v in count.items():
    freq_word.setdefault(v, [])
    freq_word[v].append(k)

for k in sorted(freq_word, reverse=True):
    for v in freq_word[k]:
        print(f"{v}: {k}")