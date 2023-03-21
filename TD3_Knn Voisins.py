# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:39:58 2022

@author: Thityx
"""

"""LES IMPORTS"""

import csv #va permettre la lecture de fichier csv
import time #va permettre le comptage du temps d'exécution du programme 

#%%

"""EXTRACTION DES DONNEES DES FICHIERS CSV"""

def open_file (nomdufichier):
    # On extrait les données d'entrainement de data.csv
    file = open(r"C:\Users\charl\OneDrive\Desktop\Téléchargements\{}.csv".format(nomdufichier),"r")
    data = []
    reader= csv.reader(file,delimiter=",")
    for row in reader:
        if nomdufichier != "finalTest" :
            data.append({"d0":float(row[0]),"d1":float(row[1]),"d2":float(row[2]),"d3":float(row[3]),"d4":float(row[4]),"d5":float(row[5]),"classe":row[6]})
        else :
            data.append({"d0":float(row[0]),"d1":float(row[1]),"d2":float(row[2]),"d3":float(row[3]),"d4":float(row[4]),"d5":float(row[5])})  
    return data

def unify (data1,data2):
    """
    Paramètre : deux listes d'ensembles dont chaque ensemble est modélisé par un dictionnaire
    Résultat : une liste ayant fusionné les deux listes prises en paramètre
    """
    unify = []
    for row in data1:
        unify.append(row)
    for row in data2:
        unify.append(row)
    return unify
   
    
#%%

"""KNN"""


def distance_manhattan(data1,data2):
    """
    Renvoie la distance de Manhattan entre deux ensembles
    """
    return abs(data1["d0"]-data2["d0"]) + abs(data1["d1"]-data2["d1"]) + abs(data1["d2"]-data2["d2"]) + abs(data1["d3"]-data2["d3"]) + abs(data1["d4"]-data2["d4"]) + abs(data1["d5"]-data2["d5"])

""""""

def frequence_classe (table):
    """
    Paramètre : une liste d'ensembles de 5 variables, chaque ensemble étant modélisé par un dictionnaire
    Résultat : Un dictionnaire dont les clés sont les classes et les valeurs, le nombre de fois où cette classe apparait
    """
    frequence = {}
    for data in table:
        classe = data["classe"] #on prend la classe de chaque ensemble
        if classe in frequence.keys(): #si cette la clé de cette classe est déjà créée
            frequence[classe] = frequence[classe] + 1 #on incrémente de 1 le nombre de fois qu'elle apparait
        else:
            frequence[classe] = 1 #on crée une clé dans le dictionnaire frequence pour chaque classe qu'on initialise à 1
    return frequence

def classe_majoritaire (table):
    """
    Paramètre : une liste d'ensembles de 5 variables, chaque ensemble étant modélisé par un dictionnaire
    Résultat : le nom de la classe la plus représentée dans cette liste
    """
    frequences = frequence_classe(table) #on compte le nombre de fois que chaque classe apparaît
    classe_max = table[0]["classe"] #on initie la classe_max par une valeur par défaut
    for (classe,nombre) in frequences.items():
        if frequences[classe_max] < nombre :
            classe_max = classe #on prend la classe qui appraît le plus de fois
    return classe_max

""""""

def k_plus_proches(k,table,nouveau):
    """
    Paramètre : le meilleur k, les valeurs d'entrainement, un nouvel ensemble dont on doit prédire la classe
    Résultat : une liste des k voisins les plus proches de cette ensemble
    """
    # On trie les données de la table selon la distance croissante avec la donnée cible
    # On définie le critère de trie
    def distance_nouveau(data):
        return distance_manhattan(data,nouveau)
    
    # On trie la table selon le critère choisi
    table_triee = sorted(table,key=distance_nouveau)
    
    # Prendre les k premières valeurs de la table triée
    proches_voisins = []
    for i in range(k): #range(1,k+1) lorsque l'on compare avec le meme dataset sans la colonne des classes
        proches_voisins.append(table_triee[i])
        
    # On renvoie les plus proches voisins
    return proches_voisins

""""""

def attribution (k,table,nouveau):
    """
    Paramètre : le meilleur k, les valeurs d'entrainement, un nouvel ensemble dont on doit prédire la classe
    Résultat : la classe prédite du nouvel ensemble
    """
    voisins = k_plus_proches(k, table, nouveau) #on prend les k voisins les plus proches de l'ensemble
    classe = classe_majoritaire(voisins) #on prend la classe la plus fréquente de ces k voisins pour prédire la classe de l'ensemble
    return classe

""""""

def get_prediction(train,test,k):
    """
    Paramètre : le meilleur k, les valeurs d'entrainement, les nouveaux ensembles dont on doit prédire la classe
    Résultat : une liste des prédictions, chaque prédictions étant modélisé par un dictionnaire
    """
    prediction = [] #création de la liste des prédictions
    for i in range(len(test)): #on parcours les nouveaux ensembles
        dico = {}
        dico["classe"] = attribution(k,train,test[i]) #chaque prédiction est modélisé par un dictionnaire
        prediction.append(dico) #pour pouvoir ensuite utiliser la fonction classe_majoritaire
    return prediction

""""""

def final_prediction(data,preTest,both):
    """
    Paramètre : Les predictions du fichier finalTest avec pour valeur d'entrainement data puis preTest puis data+preTest
    Résultat : Ecrit dans un fichier text le lissage de ces prédictions
    """
    #Creation et ecriture du fichier txt
    myfile = open(r"C:\Users\charl\OneDrive\Desktop\Téléchargements\delemazure_sample.txt", "w+")
    # On parcourt les predictions
    for i in range(len(data)):
        liste = [] # on regroupe les 3 predictions dans une liste pour pouvoir utiliser la fonction classe_majoritaire
        liste.append(data[i])
        liste.append(preTest[i])
        liste.append(both[i])
        classe = classe_majoritaire(liste) # parmis les 3 prédictions faites au dessus on prend la plus fréquente
        if i == 0 : #pas de saut de ligne pour la première prédiction
            myfile.write(classe) #ecriture de la prediction dans le fichier txt
        else:
            myfile.write("\n" + classe) #ecriture de la prediction dans le fichier txt  
    myfile.close() #fermeture du fichier txt
      
    
# %% 

"""ZONE DU MAIN"""

if __name__ == '__main__':
    start_time = time.time()
    
    
    #Ouverture des fichiers
    data = open_file("data") 
    preTest = open_file("preTest")
    both = unify(data,preTest)
    test = open_file("finalTest")
    #Predictions
    pred_data = get_prediction(data,test,5)
    pred_preTest = get_prediction(preTest,test,4)
    pred_both = get_prediction(both,test,4)
    #On choisis la prédiction la plus fréquente parmis les 3
    final_prediction(pred_data,pred_preTest,pred_both) 
    
    
    print("\nTemps d'exécution : %s seconds" % round((time.time() - start_time),4)) 