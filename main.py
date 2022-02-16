import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt

def importTxt():
    with open('C:\\Users\\Jake\\Downloads\\run3-input.txt') as f:
        lines = f.readlines()
    NFRs = []
    FRs = []
    for l in lines:
        if l[0:3] == 'NFR':
            NFRs.append(l)
        elif l[0:2] == 'FR':
            FRs.append(l)
        elif l[0] == '\n':
            x=1
        else:
            print("BADBADBAD")
    return NFRs,FRs

def parseFRs(NFRs,FRs):
    pNFRs = []
    pFRs = []
    for NFR in NFRs:
        for i in range(len(NFR)):
            if NFR[i] == ':':
                pNFRs.append(NFR[i+2:len(NFR)-2])
                break
    for FR in FRs:
        for i in range(len(FR)):
            if FR[i] == ':':
                pFRs.append(FR[i+2:len(FR)-2])
                break

    for i in range(len(pNFRs)):
        pNFRs[i]=pNFRs[i].replace(".","")
        pNFRs[i]=pNFRs[i].lower()
    for i in range(len(pFRs)):
        pFRs[i]=pFRs[i].replace(".","")
        pFRs[i]=pFRs[i].lower()
    return pNFRs,pFRs

def jaccard(A,B):
    words_doc1 = set(A.lower().split())
    words_doc2 = set(B.lower().split())

    intersection = words_doc1.intersection(words_doc2)

    union = words_doc1.union(words_doc2)

    return float(len(intersection)) / len(union)

def jaccardMatrix(FRs):
    rows, cols = (len(FRs), len(FRs))
    df = [[0] * cols] * rows

    jac = 0.0
    for i in range(len(FRs)):
        for j in range(len(FRs)):
            jac = jaccard(FRs[i],FRs[j])
            df[i][j] = jac
    dfi = pd.DataFrame(df)
    return df

def jaccardMatrix2(FRs,NFRs):
    rows, cols = (len(FRs), len(NFRs)+1)

    df = pd.DataFrame({'FR': [0], 'NFR1': [0.0],'NFR2':[0.0],'NFR3':[0.0]})
    jaccd = 0.0
    if len(NFRs) == 4:
        for i in range(len(FRs)):
            # df = df.append([i+1,jac(FRs[i],NFRs[0]),jac(FRs[i],NFRs[1]),jac(FRs[i],NFRs[2])])
            df = df.append({'FR': (i + 1), 'NFR1': jaccard(FRs[i], NFRs[0]), 'NFR2': jaccard(FRs[i], NFRs[1]),
                            'NFR3': jaccard(FRs[i], NFRs[2]),'NFR4': jaccard(FRs[i], NFRs[3])}, ignore_index=True)

        df = df.iloc[1:, :]
        df = pd.DataFrame(df)
        return df

    for i in range(len(FRs)):
        #df = df.append([i+1,jac(FRs[i],NFRs[0]),jac(FRs[i],NFRs[1]),jac(FRs[i],NFRs[2])])
        df = df.append({'FR':(i+1),'NFR1': jaccard(FRs[i],NFRs[0]),'NFR2':jaccard(FRs[i],NFRs[1]),'NFR3':jaccard(FRs[i],NFRs[2])},ignore_index=True)

    df = df.iloc[1:, :]
    df = pd.DataFrame(df)
    return df

def runagglo(matrix):

    df = pd.DataFrame(matrix)
    df2 = df
    num = len(matrix)
    Z = [0]*num
    df.insert(1,"Z",[0]*num,True)
    k = AgglomerativeClustering(n_clusters=8,linkage="single")
    kl = k.fit_predict(df)
    n0,n1,n2,n3,n4,n5,n6,n6,n7,j0,j1,j2,j3,j4,j5,j6,j7 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    i = 1
    for c in kl:
        if c == 0:
            n0 = n0 + 1
            j0 = j0 + matrix[i]
        elif c == 1:
            n1 = n1 + 1
            j1 = j1 + matrix[i]
        elif c == 2:
            n2 = n2 + 1
            j2 = j2 + matrix[i]
        elif c == 3:
            n3 = n3 + 1
            j3 = j3 + matrix[i]
        elif c == 4:
            n4 = n4 + 1
            j4 = j4 + matrix[i]
        elif c == 5:
            n5 = n5 + 1
            j5 = j5 + matrix[i]
        elif c == 6:
            n6 = n6 + 1
            j6 = j6 + matrix[i]
        elif c == 7:
            n7 = n7 + 1
            j7 = j7 + matrix[i]
        i = i+1
    a0 = j0/n0
    a1 = j1 / n1
    a2 = j2 / n2
    a3 = j3 / n3
    a4 = j4 / n4
    a5 = j5 / n5
    a6 = j6 / n6
    a7 = j7 / n7
    list = [a0,a1,a2,a3,a4,a5,a6,a7]
    loser1 = min(list)
    loser1i = list.index(loser1)
    list[loser1i] = 100.00
    loser2 = min(list)
    loser2i = list.index(loser2)
    list[loser2i] = 100.00
    #loser3 = min(list)
    #loser3i = list.index(loser3)
    #list[loser3i] = 100.00

    sendBack = matrix
    i = 1
    for c in kl:
        if list[c] == 100:
            sendBack[i] = int(0)
        elif list[c] == 50:   #fuck around and find out, future Jake
            if i%2 == 0:
                sendBack[i] = int(0)
            else:
                sendBack[i] = int(1)
        else:
            sendBack[i] = int(1)
        i = i+1
    return sendBack

def exporter(m1,m2,m3):
    m1 = list(map(int,m1))
    m2 = list(map(int, m2))
    m3 = list(map(int, m3))
    string = ""
    for i in range(len(m1)):
        string = string + "FR" + str(i+1) +","+ str(m1[i])+","+str(m2[i])+","+str(m3[i])+"\n"
    with open('C:\\Users\\Jake\\Downloads\\JacobKroger-run2-output.txt','w') as f:
        f.write(string)

def exporter4(m1,m2,m3,m4):
    m1 = list(map(int,m1))
    m2 = list(map(int, m2))
    m3 = list(map(int, m3))
    m4 = list(map(int, m4))
    string = ""
    for i in range(len(m1)):
        string = string + "FR" + str(i+1) +","+ str(m1[i])+","+str(m2[i])+","+str(m3[i])+","+str(m4[i])+"\n"
    with open('C:\\Users\\Jake\\Downloads\\JacobKroger-run3-output.txt','w') as f:
        f.write(string)


if __name__ == '__main__':
    # Hey future Jake!
    # 1) Hey
    # 2) I'm pretty sure I fixed what I needed to so that
    # you don't have to worry about the number 4
    # Who knows? I don't
    #
    # 3) I doooo know you need to change the paths at
    # lines 172,161,and 6 depending on what you're doing
    #
    # Functions that actually do meaningful things:
    #
    # importTxt(): reads txt file from path and separates NFRs from FRs
    #   don't tinker with this for performance
    #
    # parseFRs(): interesting little thing that cuts out useless stuff like periods
    #   and colons and makes everything lowercase
    #   you could probably improve performance if you spent some time in here
    #
    # jaccard(): takes two strings, splits them into words, computes jaccard similarity
    #   if you mess with this future Jake I will be slightly annoyed
    #
    # jaccardMatrix2(): BREAD AND BUTTER OF THIS  DO NOT TOUCH.
    #   Takes each FR and computes their JS with each NFR
    #
    # runagglo(): single link clustering, calcs average JS, cuts out the bottom couple
    #   clusters, spits back which FRs are traced to the passed NFR
    #   messing with this will get you significant performance results
    #   specifically how many clusters are cut in the end
    #
    # exporter(): puts the links in a nice little (big) string and spits in to a .txt
    # exporter4(): same thing but with 4 NFRs
    #
    #
    # One last thing: to run the grader program I finagled->
    # open cmd in downloads
    # >javac Bop.java
    # >java Bop
    # suffer!
    ###########################################################################################

    NFRs, FRs = importTxt()
    NFRs, FRs = parseFRs(NFRs, FRs)
    #print(NFRs)
    #print(FRs)
    matrix = jaccardMatrix2(FRs, NFRs)

    matrix1 = runagglo(matrix['NFR1'])
    matrix2 = runagglo(matrix['NFR2'])
    matrix3 = runagglo(matrix['NFR3'])
    if len(NFRs) == 4:
        matrix4 = runagglo(matrix['NFR4'])
        exporter4(matrix1, matrix2, matrix3,matrix4)
    else:
        exporter(matrix1,matrix2,matrix3)





















