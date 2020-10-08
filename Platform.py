def getPlatform():
    Platform = os.popen("uname -a 2> NUL").read()
    if 'Android' in Platform:
        return('Android')
    elif 'Linux' in Platform:
        return('Linux')
    else:
        return('Windows')
