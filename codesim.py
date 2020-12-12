import sys, os

def preproduce(path):   #对代码进行编译预处理
    if not os.path.isfile(path):
        sys.stderr.write("No Such File or Directory\n")
        sys.exit()
    order = 'gcc -S ' + path
    os.system(order)
    filename = os.path.basename(path).split('.')[0] + '.s'  #编译得到的汇编文件
    if not os.path.isfile(filename):
        sys.stderr.write("No Such File or Directory\n")
        sys.exit()
    f = open(filename, 'r')
    codes = ''.join(f.readlines())
    string = codes.replace('	',"")
    string = string.replace('\n',"")
    f.close()
    os.remove(filename)
    return string
    

def hash(string):   #求哈希值
    res = 0
    b = 9887
    for i in range(len(string)):
        res = res + ord(string[i])*b 
    return res
   
def get_hashes(string, k):  #求所有k_gram及其哈希值
    hashes = []
    for i in range(len(string)-k+1):
        k_gram = string[i:i+k]
        k_hash = hash(k_gram)
        hashes.append(k_hash)
    return hashes

def get_minimum(nums):  #求一个哈希值数组中的最小值
    res = []
    minimum = sys.maxsize
    index = 0
    for i in range(len(nums)):
        if nums[i] <= minimum:
            minimum = nums[i]
            index = i
    res.append(minimum)
    res.append(index)
    return res

def winnowing(path):
    k,t = 60, 200
    w = t - k + 1
    string = preproduce(path)
    hashes = get_hashes(string, k)
    size = len(hashes)
    fingerprints = []
    minimum_index = get_minimum(hashes[0:w])
    minimum = minimum_index[0]
    index = minimum_index[1]
    fingerprints.append(minimum)
    for i in range(size-w+1):
        if hashes[i+w-1] <= minimum:    #如果窗口最右边的比现在的最小值还小，则更新
            minimum = hashes[i+w-1]
            index = i + w -1
            fingerprints.append(minimum)
        elif index < i:     #如果最小值滑出窗口，则更新整个窗口的最小值和索引
            minimum_index = get_minimum(hashes[i:i+w])
            minimum = minimum_index[0]
            index = minimum_index[1]
            fingerprints.append(minimum)
    return fingerprints


def similarity(finger1, finger2):   #比较两个文件的fingerprint
    count = 0
    length1 = len(finger1)
    length2 = len(finger2)
    for i in range(length1):
        for j in range(length2):
            if finger1[i] == finger2[j]:
                count = count + 1
                break
    if length2 > length1:
        length1 = length2
    res = count / length1
    return res

def main(path1, path2):
    fingerprint1 = winnowing(path1)
    fingerprint2 = winnowing(path2)
    print(similarity(fingerprint1, fingerprint2))


if __name__ == "__main__":
    length = len(sys.argv)
    if length == 2:
        if sys.argv[1] != "-h" and sys.argv[1] != "--help":
            sys.stderr.write("parameter not defined\n") 
            sys.exit()
        print("usage: ./codesim [-h|--help] code1 code2")
    if len(sys.argv) == 3:
    	main(sys.argv[1], sys.argv[2])

