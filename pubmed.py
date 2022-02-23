import hashlib
import time
import xml.etree.ElementTree as ET
import pandas as pd
from metapub import PubMedFetcher

def props(cls):   
  return [i for i in cls.__dict__.keys() if i[:1] != '_']



query="""(("portugal"[MeSH Terms] OR "portugal"[All Fields] OR "portugal s"[All Fields]) AND (("pubmed books"[Filter] OR "case reports"[Publication Type] OR "classical article"[Publication Type] OR "clinical study"[Publication Type] OR "clinical trial"[Publication Type] OR "clinical trial protocol"[Publication Type] OR "clinical trial, phase i"[Publication Type] OR "clinical trial, phase ii"[Publication Type] OR "clinical trial, phase iii"[Publication Type] OR "clinical trial, phase iv"[Publication Type] OR "comparative study"[Publication Type] OR "controlled clinical trial"[Publication Type] OR "dataset"[Publication Type] OR "evaluation study"[Publication Type] OR "guideline"[Publication Type] OR "meta analysis"[Publication Type] OR "multicenter study"[Publication Type] OR "observational study"[Publication Type] OR "randomized controlled trial"[Publication Type] OR "review"[Publication Type] OR "systematic review"[Filter]) AND "humans"[MeSH Terms] AND 2012/01/01:2022/12/31[Date - Publication])) AND ((booksdocs[Filter] OR casereports[Filter] OR classicalarticle[Filter] OR clinicalstudy[Filter] OR clinicaltrial[Filter] OR clinicaltrialprotocol[Filter] OR clinicaltrialphasei[Filter] OR clinicaltrialphaseii[Filter] OR clinicaltrialphaseiii[Filter] OR clinicaltrialphaseiv[Filter] OR comparativestudy[Filter] OR controlledclinicaltrial[Filter] OR dataset[Filter] OR evaluationstudy[Filter] OR guideline[Filter] OR meta-analysis[Filter] OR multicenterstudy[Filter] OR observationalstudy[Filter] OR randomizedcontrolledtrial[Filter] OR review[Filter] OR systematicreview[Filter]) AND (humans[Filter]) AND (2012:2022[pdat]))"""

dict_for_paper={"pmid":[],"url":[],"journal":[],"title":[],"doi":[],"year":[],"majorMESH":[],"otherMESH":[],"Authors":[],"filliation":[],"article_type":[]}
fetch = PubMedFetcher()
nlist = fetch.pmids_for_query(query, retmax=100)  # default gets 250
for pmid in nlist:

        article = fetch.article_by_pmid(pmid)
        #print(article)
        #print(props(article))
        #print(article.authors)
        doi=article.doi
        title = article.title
        year = article.year
        url = article.url
        authors=article.authors_str
        journal=article.journal
        dict_for_paper["doi"].append(doi)
        dict_for_paper["Authors"].append(authors)
        dict_for_paper["year"].append(year)
        dict_for_paper["title"].append(title)
        dict_for_paper["url"].append(url)
        dict_for_paper["pmid"].append(pmid)
        dict_for_paper["journal"].append(journal)

   #     print(article.author1_last_fm)
    #    print(article.author1_lastfm)
        #print(article.mesh)
        other_l=[]
        mjrMesh=""
        for meshtermid,descr in article.mesh.items():
       #     print( meshtermid,descr )
            if descr["major_topic"]:
                mjrMesh=meshtermid
            else:
                other_l.append(meshtermid)
        
        dict_for_paper["majorMESH"].append(mjrMesh)
        dict_for_paper["otherMESH"].append(";".join(other_l))

        filliation_l=[]
        root = ET.fromstring(article.xml)
        author_list=root[0][0][3][5] #AuthorList
        for author in author_list:
           # print(author)
            filliation = author.find('AffiliationInfo')
            if filliation is not None:
                for f in filliation:
                    filliation_l.append(f.text)
        
        dict_for_paper["filliation"].append(";".join(filliation_l))

        article_type = "|".join(article.publication_types.values())
        dict_for_paper["article_type"].append(article_type)

try:
    df=pd.DataFrame.from_dict(dict_for_paper)
except:
    print(dict_for_paper)

#print(df)
df.to_csv("test.csv",index=False)