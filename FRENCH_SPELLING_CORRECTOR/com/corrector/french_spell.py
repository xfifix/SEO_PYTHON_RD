#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 29 janv. 2015

@author: stefan.duprey
'''
import re, collections

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

#training_path = 'D:\\My_Data\\My_Spelling_Corrector_Data\\titres_produits.csv'
training_path = '/home/sduprey/My_Data/My_Spelling_Corrector_Data/titres_produits.csv'
NWORDS = train(words(file(training_path).read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in s if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
   inserts    = [a + c + b     for a, b in s for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

################ Testing code from here on ################

def spelltest(tests, bias=None, verbose=False):
    import time
    n, bad, unknown, start = 0, 0, 0, time.clock()
    if bias:
        for target in tests: NWORDS[target] += bias
    for target,wrongs in tests.items():
        for wrong in wrongs.split():
            n += 1
            w = correct(wrong)
            if w!=target:
                bad += 1
                unknown += (target not in NWORDS)
                if verbose:
                    print 'correct(%r) => %r (%d); expected %r (%d)' % (
                        wrong, w, NWORDS[w], target, NWORDS[target])
    return dict(bad=bad, n=n, bias=bias, pct=int(100. - 100.*bad/n), 
                unknown=unknown, secs=int(time.clock()-start) )



french_test = {'tutoriel':'tutorial','manger':'menger',
               'accueil' : 'acceuil','inclue' : 'incluse','accompte' : 'acompte',
               'acoustique' : 'accoustique', 'abattre' : 'abbattre','aberration':'abberration',
               'addiction' : 'adiction', 'adresse' : 'addresse','appara�tre':'apara�tre apparaitre',
               'ascenseur' : 'acenseur', 'ba�onnette' : 'bayonnette', 'bayer' : 'bailler',
               'bancaire' : 'banquaire', 'bissextile' : 'bisextile', 'bizarre' : 'bizard',
               'blanchiment':'blanchiement', 'blizzard' : 'blizard','carrousel':'carroussel',
               'cat�chisme' : 'cath�chisme', 'cueillir' : 'ceuillir','ch�tain' : 'chatain',
               'chert�':'ch�ret�','coalition' : 'coallition','concurrence':'concurent',
               'conjugaison':'conjuguaison','controverse':'contreverse','courir':'courrir',
               'cigogne' : 'cygogne', 'd�connexion' : 'd�connection','d�dicace' : 'd�dicasse',
               'desservir' : 'd�servir','dilemme' : 'dilemne', 'diluvien' : 'dilluvien',
               'emm�nager' : 'em�nager', 'enivr�':'ennivr�', 'ermite':'hermite','exsangue':'exangue',
               'exaucer':'exhaucer', 'exorbitant' : 'exhorbitant','exciter':'exiter',
               'ferroviaire' : 'ferrovi�re', 'filigrane' : 'filligrane','gaufre' : 'gauffre',
               'gen�se':'genn�se','groseillier':'groseiller','guyane':'guyanne',
               'hasard' : 'hazard', 'imb�cilit�' : 'imb�cillit�', 'inclus':'inclu',
               'inclura' : 'incluera', 'ingrat' : 'ingras','installation' : 'instalation',
               'japonais':'japonnais','journaux' : 'journeaux','litt�ralement':'litt�rallement',
               'magazine' : 'magasine', 'maligne' : 'maline','mn�motechnique':'m�motechnique',
               'ob�dience' : 'ob�diance', 'obnubiler':'obnibubiler','oculaire' : 'occulaire',
               'occurence' : 'occurrence', 'ornithorynque': 'ornythorinque', 'p�cuniaire':'p�cunier',
               'permanence':'permannence','pertinemment' : 'pertinament','philharmonique':'phillharmonnique',
               'pilule':'pillule','planification':'plannification', 'pourrir' : 'pourir','puissamment':'puissament', 
               'quatuor':'quattuor','r�sonance' : 'r�sonnance','r�bellion' : 'rebellion','recueillir':'receuillir',
               'rec�le' : 'recelle', 'recommandation' : 'recommendation', 'r�compense' : 'r�compence', 'r��dition':'r�dition',
               'r�sorption' : 'r�sorbtion', 'r�sous' :'r�souds','r�sout':'r�soud', 'r�le' : 'role',
               'rh�torique' : 'rh�toric','s�ance' : 'sc�ance', 'soubresaut':'soubressaut','spatial' : 'spacial',
               'succ�dan�' : 'succ�dann�', 'synchrone' : 'sinchrone',  'syphilis' : 'Syphillis', 'th��tre' : 'th�atre',
               'souffrir' : 'soufrir', 'th�me' : 't�me', 'tonnerre' : 'tonn�re', 'toponymie':'toponomie',
               'trafic' : 'traffic', 'tranquillit�':'tranquillit�e','vaillamment' :'vaillemment',
               'voirie' : 'voierie', 'vraisemblable':'vraissemblable','waggon':'wagon'}  
                
               
                
        



if __name__ == '__main__':
    print spelltest(french_test)

