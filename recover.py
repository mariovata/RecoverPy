from hashlib import md5, sha1, sha256, sha512
import sys
import xml.etree.ElementTree as ET
import time
import os

password_found = False


def writeToXML(password):
    root = ET.Element("password")
    root.text = password
    tree = ET.ElementTree(root)
    tree.write("passwords.xml", encoding="latin-1", xml_declaration=True)


def crack_password(hash_type, h, password):
    hash_func = {"md5": md5, "sha1": sha1, "sha256": sha256, "sha512": sha512}  # dictionary of hash functions
    if hash_type in hash_func:
        if hash_func[hash_type](password).hexdigest() == h:                     # check if password is correct
            return True
    return False


def guess_password(hash_type, h, wordlist):
    global password_found
    for password in wordlist:   # iterate through wordlist
        if password_found:      # if password is found,
            break
        if crack_password(hash_type, h, password):                  # check if password is correct
            print(f"Password found: {password.decode('latin-1')}")  # print password
            password_found = True                                   # set password_found to True
            writeToXML(password.decode('latin-1'))                  # write password to xml file
            break


def main():
    start_time = time.time()  # start timer to calculate time taken to crack password

    # take arguments from command line
    if len(sys.argv) == 4:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]

    if len(sys.argv) == 3:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = "wordlist1.txt"

    else:
        print("Usage: python recover.py <hash_type> <hash> <wordlist>")
        sys.exit(1)

    if not os.path.isfile("passwords.xml"):  # create xml file if it doesn't exist
        root = ET.Element("passwords")       # create root element
        tree = ET.ElementTree(root)          # create tree
        tree.write("passwords.xml", encoding="utf-8", xml_declaration=True)  # write tree to xml file

    with open(arg3, "r", encoding='latin-1') as f:                      # open wordlist
        wordlist = [line.strip("\n").encode('latin-1') for line in f]   # read wordlist and encode to latin-1

    guess_password(arg1, arg2, wordlist)                        # call function to guess password
    print("--- %s seconds ---" % (time.time() - start_time))    # print time taken to crack password
    if not password_found:
        print("Password not found")
        sys.exit(-1)
    else:
        print("Password Saved to XML")
        sys.exit(0)


if __name__ == "__main__":
    main()
