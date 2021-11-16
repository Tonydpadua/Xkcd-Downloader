#! python3
# multidownloadXkcd.py – Faz download das tirinhas XKCD usando várias threads.
import requests, os, bs4, threading

os.makedirs('xkcd',exist_ok=True) #armazena as tirinhas em ./xkcd

def downloadXkcd(StartComic,endComic):
    for urlNumber in range(StartComic,endComic):

        #Faz download da página
        print('Downloading page http://xkcd.com/%s...' % (urlNumber))
        res = requests.get('http://xkcd.com/%s'%(urlNumber))
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text)

        #Encontra o URL da imagem da tirinha
        comicElem = soup.select('#comic img')
        if comicElem == []:
            print("Could not find comic images")
        else:
            comicUrl = comicElem[0].get('src')

            #Faz download da imagem
            print('Downloading image %s...'%(comicUrl))
            res = requests.get('http:'+comicUrl)
            res.raise_for_status()

            #Salva a imagem em :/xkcd
            imageFile = open(os.path.join("xkcd",os.path.basename(comicUrl)),"wb")
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

#Cria e inicia os objetos Thread
downloadThreads = [] #uma lista com todos os objetos Thread
for i in range(0,1400,100): #executa o loop 14 vezes e cria 14 threads
    downloadThread = threading.Thread(target=downloadXkcd,args=(i, i+99))
    downloadThreads.append(downloadThread)
    downloadThread.start()

#Espera todas as threads terminarem
for downloadThread in downloadThreads:
    downloadThread.join()
print('Done')
