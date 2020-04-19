"""

# Paragrf

Text
====


*italic* italic
**bold** bold
***bold and italic***

++inserted++

==Marked=[color]=  /no



(^|r>)((\>)+\ ){0,}((.|\n)*?)(<b|(?=\n$)\n)






regex = r"(\>\ (.*?)$\n){1,}"








"""
import re
from urllib.parse import quote_plus 
def write_new(text,codeblocks):
    for repl in reversed(codeblocks):
        text = text[:repl[0]] + repl[1] + text[repl[2]:]
    return text


def parse_meta(meta):
    return meta


def get_meta(text):
    regex = r"^-{3,}((.|\n)*?)-{3,}"
    codeblocks=[]
    match = re.search(regex, text)
    try:
        codeblocks.append((match.start(0),"",match.end(0)))
    except:
        return {},text
    meta=parse_meta(match.group(1))
    text=write_new(text,codeblocks)


    return meta,text


def get_varibles(text):
    comm = r"\[\/\/]\:(.*?)$"
    cm = []
    matches = re.finditer(comm, text, re.MULTILINE)
    for match in matches:
        cm.append((match.start(0)," \n ",match.end(0)))
    text = write_new(text,cm)


    regex = r"\[(.*?)\]\:\s(.*?)\n"
    varibles = {}
    vr=[]
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        vr.append((match.start(0)," \n ",match.end(0)))
    text = write_new(text,vr)


    return varibles,text






def all_to_pargph(text):
    regex = r"(?!(<br|<hr))(?!(br|hr))(?!r)(?!>)(((.|\n)*?)(^\n))"
    pargr=[]
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        pargr.append((match.start(0)," <p>"+match.group(4)+"</p> ",match.end(0)))
    text = write_new(text,pargr)
    text = re.sub("<p></p>","\n",text)
    return text




def do_inline_code(text):
    regex = r"(?!\`\`)\`(.*?)\`(?!\`\`)"
    codeblocks=[]
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        mcode = ''
        for x in match.group(1):
            try:
                if int(quote_plus(str(x),encoding="utf-8").replace('%','0x'),16) in range(33,48) or int(quote_plus(str(x),encoding="utf-8").replace('%','0x'),16) in range(58,65) or int(quote_plus(str(x),encoding="utf-8").replace('%','0x'),16) in range(91,97) or int(quote_plus(str(x),encoding="utf-8").replace('%','0x'),16) in range(123,127):
                    
                    mcode=mcode+'&#'+str(int(quote_plus(str(x),encoding="utf-8").replace('%','0x'),16))+';'
                else:
                    mcode=mcode+str(x)
            except:
                mcode=mcode+x

        codeblocks.append((match.start(0),"<code>"+mcode+"</code>",match.end(0)))
    text = write_new(text,codeblocks)
    return text




def do_code_block(text):
    regex = r"\`\`\`(.*)\n((.|\n)*?)\`\`\`"
    codeblocks=[]
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        mcode = ''
        for x in match.group(2):
            try:
                if int(quote_plus(str(x),encoding="utf-8").replace('%','0x'),16) in range(33,48) or int(quote_plus(str(x),encoding="utf-8").replace('%','0x'),16) in range(58,65) or int(quote_plus(str(x),encoding="utf-8").replace('%','0x'),16) in range(91,97) or int(quote_plus(str(x),encoding="utf-8").replace('%','0x'),16) in range(123,127):
                    
                    mcode=mcode+'&#'+str(int(quote_plus(str(x),encoding="utf-8").replace('%','0x'),16))+';'
                else:
                    mcode=mcode+str(x)
            except:
                mcode=mcode+x

        codeblocks.append((match.start(0),"<pre><code>"+mcode+"</code></pre>",match.end(0)))
    text = write_new(text,codeblocks)

    return text









def do_headers(text):
    regexO= r"^(?=#)\#{0,6}(?!\#)(\s)(.*?)$"
    regexT = r"(^)(?=\S+)(.*?)\n((-|=){3,})"
    # ## Синтаксес
    headers=[]
    matches = re.finditer(regexO, text, re.MULTILINE)
    for match in matches:
        hn = str(match.start(1)-match.start(0))
        headers.append((match.start(0),"<h"+hn+">"+match.group(2)+"</h"+hn+">",match.end(0)))
    text = write_new(text,headers)

    # Заголовок
    # ========
    headers=[]
    matches = re.finditer(regexT, text, re.MULTILINE)
    for match in matches:
        if match.group(3)[0] == "=":
            hn="1"
        elif match.group(3)[0] == "-":
            hn="2"
        headers.append((match.start(0),"<h"+hn+">"+match.group(2)+"</h"+hn+">",match.end(0)))
    text = write_new(text,headers)



    return text
     


def do_hr(text):
    regex = r"^(\*\s\*\s\*|\*{3,}|\-\s\-\s\-|\-{3,})"
    matches = re.finditer(regex, text, re.MULTILINE)
    hrs=[]
    for match in matches:
        hrs.append((match.start(0),"<hr>",match.end(0)))
    text = write_new(text,hrs)


    return text




def do_image(text,varibles):
    regexA = r"\[!\[(.*?)\]\((.*?)\)\]\((.*?)((?=\{)\{(.*?)\}\)|\))"
    regexT = r"\!\[(.*?)\]\((.*?)((?=\{)\{(.*?)\}\)|\))"
    images=[]
    matches = re.finditer(regexA, text, re.MULTILINE)
    for match in matches:
        if (match.group(5)) == None:
            style=''
        else:
            style=match.group(5)
        if (match.group(1)) == None:
            title=''
        else:
            title=match.group(1)
        images.append((match.start(0),'<a href="'+str(match.group(3))+'" title="'+str(title)+'"><img src="'+str(match.group(2))+'" alt="'+str(match.group(1))+'" style="'+style+'" ></a>',match.end(0)))
    text = write_new(text,images)





    images=[]
    matches = re.finditer(regexT, text, re.MULTILINE)
    for match in matches:
        if (match.group(4)) == None:
            style=''
        else:
            style=match.group(4)
        if (match.group(1)) == None:
            title=''
        else:
            title=match.group(1)
        #print(style)
        images.append((match.start(0),'<img src="'+str(match.group(2))+'" alt="'+str(match.group(1))+'" style="'+style+'" >',match.end(0)))
    text = write_new(text,images)






    return text

def do_url(text,varibles):
    regex = r"\[(.*?)\]\((.*?)\)"
    url=[]
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        if (match.group(1)) == None:
            title=match.group(2)
        else:
            title=match.group(1)
        url.append((match.start(0),'<a href="'+match.group(2)+'">'+title+'</a>',match.end(0)))
    text = write_new(text,url)


    return text

def do_bold_italic(text):
    regex = r"(?!\s)(\*\*\*((.|\n)*?)\*\*\*|\_\_\_((.|\n)*?)\_\_\_)"
    bld=[]
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        if match.group(2) == None:
            texti = match.group(4)
        else:
            texti = match.group(2)
        bld.append((match.start(0),' <strong><em>'+texti+'</em></strong> ',match.end(0)))
    text = write_new(text,bld)

    return text




def do_bold(text):
    regex = r"(?!\s)(\*\*((.|\n)*?)\*\*|\_\_((.|\n)*?)\_\_)"
    bld=[]
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        if match.group(2) == None:
            texti = match.group(4)
        else:
            texti = match.group(2)
        bld.append((match.start(0),' <strong>'+texti+'</strong> ',match.end(0)))
    text = write_new(text,bld)

    return text

def do_italic(text):
    regex = r"(?!\s)(\*((.|\n)*?)\*|\_((.|\n)*?)\_)"
    bld=[]
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        if match.group(2) == None:
            texti = match.group(4)
        else:
            texti = match.group(2)
        bld.append((match.start(0),' <em>'+texti+'</em> ',match.end(0)))
    text = write_new(text,bld)

    return text

def do_strike(text):
    regex = r"(?!\s)\~\~((.|\n)*?)\~\~"
    bld=[]
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        bld.append((match.start(0),' <del>'+match.group(1)+'</del> ',match.end(0)))
    text = write_new(text,bld)

    return text

def do_ins(text):
    regex = r"(?!\s)\+\+((.|\n)*?)\+\+"
    bld=[]
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        bld.append((match.start(0),' <ins>'+match.group(1)+'</ins> ',match.end(0)))
    text = write_new(text,bld)

    return text





def do_blockquote(text):
    regex = r"(^\>(\ |\n)(.*?)\n){1,}"
    bcq=[]
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        bcqt = match.group(0)
        bcqt = re.sub("^>\ ","",bcqt, 1, re.MULTILINE)
        bcqt = re.sub("^\>(\s)*$","<br>",bcqt,0, re.MULTILINE)
        bcqt = re.sub("\n^>\ ","<br>",bcqt,0, re.MULTILINE)
        bcqt = re.sub("\n",'',bcqt,0,re.MULTILINE)


        #print(bcqt.encode())
        bcq.append((match.start(0),' <blockquote>'+bcqt+'</blockquote> \n',match.end(0)))
    text = write_new(text,bcq)

    return text



def table_get_data(ttext,tp):
    regex= r"(?<=\|)(.*?)(?=\|)"
    data=[]
    matches = re.finditer(regex, ttext, re.MULTILINE)
    for match in matches:
        data.append(match.group(0))
    if tp == 'data':
        print(data)
        return data
    elif tp == 'align':
        y = 0
        for x in data:
            
            regex = r"((\:\-{3,}\:)|(\:\-{3,})|(\-{3,}\:)|(\-{3,}))"
            m = re.search(regex, data[y])
            if m:
                if m.group(2) == None:
                    if m.group(3) == None:
                        if m.group(4) == None:
                            if m.group(5) == None:
                                return 'e'
                            else:
                                data[y]= 'n'
                        else:
                            data[y] = 'r'
                    else:
                        data[y] = 'l'
                else:
                    data[y] ='c'
            else:
                return 'e'
            y = y+1
        return data    





def do_table(text):
    regex=r"(\|(.*)\|)(\n|\s\n)(\|(.*)\|)(\n|\s\n)(((\|(.*)\|)(\n|\s\n)){1,})"
    tbl=[]
    trs=[]
    tblt=''
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        th = match.group(1)
        ta = match.group(4)
        td = match.group(1)
        
        align = table_get_data(ta,'align')
        if align != 'e':
            y = 0
            for x in align:
                if x == 'n':
                    align[y] = ''
                elif x == 'l':
                    align[y] = ' style="text-align:left;" '
                elif x == 'r':
                    align[y] = ' style="text-align:right;" '
                elif x == 'c':
                    align[y] = ' style="text-align:center;" '
                else:
                    return text
                y=y+1
        else:
            return text


        #print(align)



        tblt='<table><thead><tr>'
        y = 0
        for x in table_get_data(th,'data'):
            tblt= tblt +'<th '+align[y]+' >'+x+'</th>\n'
            y = y+1
        tblt+='</tr></thead><tbody>'

        for x in td.split('\n'):
            tblt+='<tr>'
            y = 0
            for x in table_get_data(th,'data'):
                tblt= tblt +'<td '+align[y]+' >'+x+'</td>\n'
                y = y+1
            tblt+='</tr>'
        tblt+='</tbody></table>'


        print(tblt)



        tbl.append((match.start(0),' '+tblt+'',match.end(0)))
    text = write_new(text,tbl)


    return text



def markdown(text):
    text=str(text)
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    meta,text = get_meta(text)
    varibles,text = get_varibles(text)
    text = "\n"+text+"\n"
    text = do_headers(text)
    text = do_code_block(text)
    text = do_inline_code(text)
    text = do_image(text,varibles)
    text = do_url(text,varibles)
    text = do_bold_italic(text)
    text = do_bold(text)
    text = do_italic(text)
    text = do_strike(text)
    text = do_ins(text)
    text = do_blockquote(text)
    text = do_table(text)
    text = do_hr(text)



    text = all_to_pargph(text)
    return text
