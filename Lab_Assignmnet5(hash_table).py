#Implement a hash table of size 10 and use the division method as a hash function. In case of a collision, use chaining. Implement the following operations:
#Insert(key): Insert key-value pairs into the hash table. 
#Search(key): Search for the value associated with a given key.
#Delete(key): Delete a key-value pair from the hash table


class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]  # List of empty lists (chaining)

    def _hash_function(self, key):
        return key % self.size

    def insert(self, key, value):
        index = self._hash_function(key)
        # Check if key already exists and update
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                print(f"Updated key {key} with value {value}")
                return
        # Else insert new key-value pair
        self.table[index].append([key, value])
        print(f"Inserted key {key} with value {value}")

    def search(self, key):
        index = self._hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None  # Not found

    def delete(self, key):
        index = self._hash_function(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                print(f"Deleted key {key}")
                return
        print(f"Key {key} not found for deletion.")

    def display(self):
        print("Hash Table:")
        for i, bucket in enumerate(self.table):
            print(f"Index {i}: {bucket}")

ht = HashTable()

ht.insert(15, "apple")
ht.insert(25, "banana")  # Collision with 15
ht.insert(35, "cherry")  # Collision again

print("Search 25:", ht.search(25))  # Output: banana
ht.delete(25)
print("Search 25 after deletion:", ht.search(25))  # Output: None

ht.display()
Output
Inserted key 15 with value apple
Inserted key 25 with value banana
Inserted key 35 with value cherry
Search 25: banana
Deleted key 25
Search 25 after deletion: None
Hash Table:
Index 0: []
Index 1: []
Index 2: []
Index 3: []
Index 4: []
Index 5: [[15, 'apple'], [35, 'cherry']]
Index 6: []
Index 7: []
Index 8: []
Index 9: []











#Design and implement a hash table of fixed size. Use the division method for the hash function and resolve collisions using linear probing. Allow the user to perform the following operations:
#Insert a key
#Search for a key 
#Delete a key 
#Display the table

class LinearProbingHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size
        self.DELETED = "<DELETED>"

    def _hash_function(self, key):
        return key % self.size

    def insert(self, key):
        index = self._hash_function(key)
        original_index = index
        while self.table[index] not in (None, self.DELETED):
            if self.table[index] == key:
                print(f"Key {key} already exists at index {index}.")
                return
            index = (index + 1) % self.size
            if index == original_index:
                print("Hash table is full. Cannot insert.")
                return
        self.table[index] = key
        print(f"Inserted key {key} at index {index}.")

    def search(self, key):
        index = self._hash_function(key)
        original_index = index
        while self.table[index] is not None:
            if self.table[index] == key:
                print(f"Key {key} found at index {index}.")
                return index
            index = (index + 1) % self.size
            if index == original_index:
                break
        print(f"Key {key} not found.")
        return None

    def delete(self, key):
        index = self.search(key)
        if index is not None:
            self.table[index] = self.DELETED
            print(f"Key {key} deleted from index {index}.")

    def display(self):
        print("Hash Table:")
        for i, key in enumerate(self.table):
            print(f"Index {i}: {key}")
ht = LinearProbingHashTable()

ht.insert(10)
ht.insert(20)
ht.insert(30)  # Should go to different slots
ht.insert(20)  # Duplicate

ht.display()

ht.search(20)
ht.search(99)

ht.delete(20)
ht.search(20)

ht.display()

output
Inserted key 10 at index 0.
Inserted key 20 at index 1.
Inserted key 30 at index 2.
Key 20 already exists at index 1.
Hash Table:
Index 0: 10
Index 1: 20
Index 2: 30
Index 3: None
Index 4: None
Index 5: None
Index 6: None
Index 7: None
Index 8: None
Index 9: None
Key 20 found at index 1.
Key 99 not found.
Key 20 found at index 1.
Key 20 deleted from index 1.
Key 20 not found.
Hash Table:
Index 0: 10
Index 1: <DELETED>
Index 2: 30
Index 3: None
Index 4: None
Index 5: None
Index 6: None
Index 7: None
Index 8: None
Index 9: None










#Implement a hash table with extendible hashing. The hash table should dynamically expand when the number of keys in a bucket exceeds a certain threshold. Perform the following operations: 
#Insert(key): Insert key-value pairs into the hash table 
#Search(key): Search for the value associated with a given key 
#Delete(key): Delete a key-value pair from the hash table



class Bucket:
    def __init__(self, depth, size):
        self.depth = depth
        self.size = size
        self.items = {}  # Dictionary for storing key-value pairs

    def is_full(self):
        return len(self.items) >= self.size

    def insert(self, key, value):
        self.items[key] = value

    def delete(self, key):
        if key in self.items:
            del self.items[key]

    def search(self, key):
        return self.items.get(key, None)

class ExtendibleHashTable:
    def __init__(self, bucket_size=2):
        self.global_depth = 1
        self.bucket_size = bucket_size
        self.directory = [Bucket(self.global_depth, bucket_size) for _ in range(2)]

    def _hash(self, key):
        return hash(key) & ((1 << self.global_depth) - 1)

    def insert(self, key, value):
        index = self._hash(key)
        bucket = self.directory[index]

        if key in bucket.items or not bucket.is_full():
            bucket.insert(key, value)
            print(f"Inserted ({key}, {value}) into bucket {index}")
            return

        # Bucket is full, need to split
        print(f"Bucket {index} is full. Splitting...")
        self._split_bucket(index)
        # Re-insert the key
        self.insert(key, value)

    def _split_bucket(self, index):
        old_bucket = self.directory[index]
        local_depth = old_bucket.depth
        old_bucket.depth += 1

        if old_bucket.depth > self.global_depth:
            self._double_directory()

        new_bucket = Bucket(old_bucket.depth, self.bucket_size)

        # Update directory to point to new buckets
        for i in range(len(self.directory)):
            if self.directory[i] is old_bucket and ((i >> local_depth) & 1):
                self.directory[i] = new_bucket

        # Rehash the keys in the old bucket
        all_items = list(old_bucket.items.items())
        old_bucket.items.clear()

        for k, v in all_items:
            self.insert(k, v)  # Will hash and reinsert into appropriate bucket

    def _double_directory(self):
        print("Doubling directory size.")
        self.directory += self.directory
        self.global_depth += 1

    def search(self, key):
        index = self._hash(key)
        value = self.directory[index].search(key)
        if value is not None:
            print(f"Found key {key} with value {value} in bucket {index}")
        else:
            print(f"Key {key} not found.")
        return value

    def delete(self, key):
        index = self._hash(key)
        bucket = self.directory[index]
        if key in bucket.items:
            bucket.delete(key)
            print(f"Key {key} deleted from bucket {index}")
        else:
            print(f"Key {key} not found for deletion.")

    def display(self):
        seen = set()
        print("\nDirectory:")
        for i, bucket in enumerate(self.directory):
            if id(bucket) not in seen:
                seen.add(id(bucket))
                print(f"Bucket {i} (depth={bucket.depth}): {bucket.items}")
                
ht = ExtendibleHashTable(bucket_size=2)

ht.insert(1, "One")
ht.insert(2, "Two")
ht.insert(3, "Three")
ht.insert(4, "Four")
ht.insert(5, "Five")

ht.display()

ht.search(3)
ht.delete(3)
ht.search(3)

ht.display()
