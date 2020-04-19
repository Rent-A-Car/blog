import os
import poster.markdown as markdown2
os.system("""cd posts;sha256sum `find -type f` > ../new""")


old=[]
new=[]



def newfile(fn):
    fn = (fn.split())[1]
    if fn != './1':
        fn = fn.replace('./','')
        with open("posts/"+fn,"r") as f:
            md = markdown2.markdown(f.read())
        """
        md = markdown2.markdown_path("posts/"+fn,extras=["metadata", "tables","fenced-code-blocks","strike","smarty-pants"])
        """
        with open('n/'+fn.replace(".md",".html"),"w") as f:
            with open("templates/posts.html","r") as ff:
                f.write((ff.read()).format(md))
        
        #print(md)
        print(fn)




with open('old','r') as f:
    for x in f.readlines():
        old.append(x.strip())

with open('new','r') as f:
    for x in f.readlines():
        new.append(x.strip())


for x in range(0,len(new)):
    if (new[x] in old):
        pass
    else:
       newfile(new[x]) 



os.system("""mv new old""")


