import sha3

def calc_hash(value):
    return sha3.sha3_256(value.encode("utf8")).hexdigest()

def alloc_hash_tree(root, tree, chunks):
    return { 'root_hash': root, 'hash_tree': tree, 'chunks': chunks }

def calc_root_hash(left, right):
    return calc_hash(left + right)

def chunk(data, size):
    return [data[i:i+size] for i in range(0, len(data), size)]

def make_hash_list(lst):
    l = [calc_root_hash(l, r) for l, r in zip(lst[0::2], lst[1::2])]
    if len(lst) % 2 != 0:
        l.append(calc_root_hash(lst[-1], lst[-1]))
    return l

def make_tree(lst, tree):
    tree.append(lst)
    if len(lst) < 2:
        tree.reverse()
        return tree
    return make_tree(make_hash_list(lst), tree)

def make_hash_tree(data, chunk_size):
    chunks = chunk(data, chunk_size)
    lst = [calc_hash(c) for c in chunks]
    tree = make_tree(lst, [])
    return alloc_hash_tree(tree[0][0], tree, chunks)

def get_root_hash(tree):
    return tree['root_hash']

def get_hash_tree(tree):
    return tree['hash_tree']
    
def get_hash_list(tree, n):
    return tree['hash_tree'][n]

def get_data_chunk(tree, n):
    return tree['chunks'][n]

def get_data(tree):
    return ''.join(tree['chunks'])

# 以下はハッシュツリーのテストコード
message1 = "aaabbbcccdddeee"
hash_tree1 = make_hash_tree(message1, 3)
print("-" * 64)
print(hash_tree1)

message2 = "aaabbbcccdddeez"
hash_tree2 = make_hash_tree(message2, 3)
print("-" * 64)
print(hash_tree2)

# Verify
trusted_root_hash = get_root_hash(hash_tree1)
trusted_hash = get_hash_list(hash_tree1, 1)[0]
untrusted_root_hash = get_root_hash(hash_tree2)
untrusted_hash = get_hash_list(hash_tree2, 1)[0]
print("-" * 64)
print("%s - trusted: 0x%s..., untrusted: 0x%s..." %
        (trusted_root_hash == untrusted_root_hash,
        trusted_root_hash[:8], untrusted_root_hash[:8]))
print("%s - trusted: 0x%s..., untrusted: 0x%s..." %
        (trusted_hash == untrusted_hash,
        untrusted_hash[:8], untrusted_hash[:8]))
