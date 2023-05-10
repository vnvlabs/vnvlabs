#Converts all of the ssn submodule urls to https. You should run this before calling
#submodule init.
   # ssh is nice because you can push without passwords
   # https is nice because you can pull without a key.



with open('.gitmodules','r') as f:
    a = f.readlines()
    res = []
    for line in a:
        res.append(line.replace("git@github.com:","https://github.com/"))

with open('.gitmodules', 'w') as f:
    for line in res:
        f.write(line)

