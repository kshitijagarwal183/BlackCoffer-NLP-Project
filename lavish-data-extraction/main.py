import requests
import csv
from bs4 import BeautifulSoup
file = open('Inputsheet.csv')
csvreader = csv.reader(file)
links = []
for link in csvreader:
  links.append(link)
l=[]
for link in range(1,len(links)):
  l.append(links[link][1])
#l=list of urls
output=[]
c=1 #c= count of loop 
for url in l:
  data_url=url
  response=requests.get(data_url)
  t=response.text
  l=len(t)
  soup = BeautifulSoup(t,'html.parser')
  tt=[]# tt is list of each paragraph
  p_tags=soup.find_all('p',{'class':''})
  for p in p_tags:
    tt.append(p.text)
  pp=' '.join(tt) #pp is list of all the paragrphs as one element
  ptp=[]#ptp is list of all the words
  ptp=pp.split(' ')
  with open('positive-words.txt', 'r') as p:
    pos = p.readlines()
  p_list = [p.strip() for p in pos]
  with open('negative-words.txt', 'r', encoding='utf-8', errors='ignore') as n:
    neg = n.readlines()
  n_list = [n.strip() for n in neg]
  positive_score=0
  negative_score=0
  for w in ptp:
    if w in p_list:
      positive_score+=1
    else:
      continue
  for w in ptp:
    if w in n_list:
      negative_score+=1
    else:
      continue
  Total_Words_after_cleaning=len(ptp)
  
  polarity_score = (positive_score - negative_score)/ ((positive_score + negative_score) + 0.000001)
  
  subjectivity_score = (positive_score + negative_score)/ ((Total_Words_after_cleaning) + 0.000001)
  
  pts=[]
  pts=pp.split('.')
  
  Average_Sentence_Length = len(ptp) / len(pts)
  
  #cw= no. of difficult/complex words
  cw = 0
  for myword in ptp:
      d = {}.fromkeys('aeiou',0)
      haslotsvowels = False
      for x in myword.lower():
          if x in d:
              d[x] += 1
      for q in d.values():
          if q > 2:
              haslotsvowels = True
      if haslotsvowels:
          cw += 1
  
  Percentage_of_Complex_words =cw /len(ptp)
  
  Fog_Index = 0.4*(Average_Sentence_Length+Percentage_of_Complex_words)
  
  Average_Number_of_Words_Per_Sentence= Average_Sentence_Length
  
  Complex_word_count=cw
  
  Word_count= len(ptp)
  
  #sc=syllable count
  sc=0
  for myword in ptp:
    d = {}.fromkeys('aeiou',0)
    for x in myword.lower():
      if x in d and x!='es' and x!='ed':
        sc += 1
  Syllable_count=sc
  
  ppn=['I','we','We','My','my','Ours','ours','us']
  nppn=sum(x in ppn for x in ptp )
  Personal_Pronouns=nppn

  #j = sum of character length of each word
  j=0
  for i in range(len(ptp)-1):
    j+=len(ptp[i])
  
  Average_word_length=j/len(ptp)
  output.append([links[c][0],url,positive_score,negative_score,polarity_score,subjectivity_score,Average_Sentence_Length,Percentage_of_Complex_words,Fog_Index,Average_Number_of_Words_Per_Sentence,Complex_word_count,Word_count,Syllable_count,Personal_Pronouns,Average_word_length,])
  c+=1
fields=['URL_ID','URL','POSITIVE SCORE','NEGATIVE SCORE','POLARITY SCORE','SUBJECTIVITY SCORE','AVG SENTENCE LENGTH','PERCENTAGE OF COMPLEX WORDS','FOG INDEX','AVG NUMBER OF WORDS PER SENTENCE','COMPLEX WORD COUNT','WORD COUNT','SYLLABLE PER WORD','PERSONAL PRONOUNS','AVG WORD LENGTH']
with open('Output_result.csv', 'w', newline='') as f:
  write = csv.writer(f)
  write.writerow(fields)
  write.writerows(output)