input = """
Ah! que l’hiver tarde à passer
Quand on le passe à la fenêtre
Avec des si et des peut-être
Et des vaut mieux pas y penser
L’homme est parti pour travailler
La femme est seule, seule, seule
L’homme est parti pour travailler
La femme est seule, à s’ennuyer

Ah! que le jour tarde à venir
Quand on se lève avec l’étoile
Et on a beau lever la toile
La nuit s’étire à plus finir
L’homme est parti, c’est au chantier
La femme est seule, seule, seule
L’homme est parti, c’est au chantier
La femme est seule, à s’ennuyer

Ah! que le jour est donc pas long
Que la noirceur vient donc d’avance
Quand l’homme est loin, c’est pas la danse
Il faut rester à la maison
L’homme à bûcher et charroyer
Le femme seule, seule, seule
L’homme à bûcher et charroyer
La femme seule, à s’ennuyer

C’est du dedans, c’est du dehors
La femme attend, l’homme voyage
Il y a beau temps, il y a bel âge
Depuis la vie jusqu’à la mort
L’homme est porté à voyager
La femme est seule, seule, seule
L’homme est porté à voyager
La femme reste à s’ennuyer

Excuse les fautes et le papier
Mais j’étais pas maîtresse d’école
J’tiens la maison, j’tiens ma parole
Tit-Jean est arrivé premier
J’sais qu’t’es parti pour travailler
J’tiens la maison, j’fais pas la folle
J’sais qu’t’es parti pour travailler
Mon désennui c’est d’m’ennuyer

Ils ont parlé d’un gros moulin
Au lac d’En-haut, ça f ’rait d’la gagne
C’est p’t-être des plages sur les montagnes
Mais j’t’aurai du soir au matin
T’auras fini de t’éloigner
C’est p’t-être des plages sur les montagnes
T’auras fini de t’éloigner
J’aurai fini de m’ennuyer

Avant d’donner ma lettre à Jean
J’aimerais te dire en post-scriptum
Que la maison, quand y a pas d’homme
C’est comme un poêle éteint tout l’temps
J’t’embrasse encore, avant d’signer
Ta talle d’amour, ta Rose, ta Jeanne
J’t’embrasse encore, avant d’signer
Ta Rose-Jeanne bien-aimée"""

count = 0

for line in input.split():
    for cha in line:
        if "a" == cha:
            count += 1

print(f"Number of 'a' characters in the input: {count}")
