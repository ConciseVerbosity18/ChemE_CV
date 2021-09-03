import os
print(__file__)
print(os.path.dirname(__file__))


# print(file, os.path.isfile(file))
def install(to_dir=os.path.join(os.path.expanduser('~'),'Documents','ol-('), Bat = True, batloc = os.path.join(os.path.expanduser('~'),'Desktop', 'Windows_Bookmark.bat')):
    '''to_dir: folder where the program and bookmark data will be.
    Bat: True if you want a bat file to launch the program (requires python to be path variable)
    batloc: where that bat file will be (default of Desktop) should end with extension .bat'''

    dire = os.path.dirname(__file__)
    file = os.path.join(dire, 'Windows_Bookmark.py')
    if not os.path.isfile(file):
        print('Could not install. Error code: 1')
        return
    with open(file) as f:
        txt = f.read()
    installf = os.path.join(to_dir,'Windows_Bookmark.py')
    with open(installf, 'w') as f:
        f.write(txt)
    print('Installed in', os.path.dirname(installf))
    if Bat:
        print('Creating bat file to execute')
        with open(batloc, 'w') as f:
            f.write(f'python {installf}')
        print('batfile created')

if __name__ == '__main__':
    install()