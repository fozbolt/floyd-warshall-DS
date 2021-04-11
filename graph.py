import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
INF = 9999

def create_graph(cvor):
    """
    Kreiranje random direktiranog grafa
    
    Parameters
    ----------
    cvor: int
        Broj čvorova za kreiranje random grafa

    Returns
    -------
    
    Vraća matricu koja sadržava sve vrijednosti novokreiranog grafa
    """

    G = nx.generators.directed.random_k_out_graph(cvor, 3, 0.75,self_loops=False) # networkx naredba za generiranje direktiranog grafa
    

    # postavljanje random weighta na svaki pravac u grafu 
    for (u,v,w) in G.edges(data=True):
        w['weight'] = random.randint(-2,5)


    if nx.negative_edge_cycle(G): print('Warning: created graph contains negative cycles')

    # kreiranje pdf-a prije konvertiranja grafa
    create_pdf(G)

    #konverzija grafa u matricu
    adj_matrix = nx.to_numpy_array(G).astype(int) # pretvorba grafa u numpy array tipa int  
    for i,row in enumerate(adj_matrix): # pretvara sve nule u 2D arrayu u INF za daljnji rad sa njim
            for j,column in enumerate(row):
                if i!=j and adj_matrix[i][j] == 0: adj_matrix[i][j] = INF
        
    return adj_matrix


def create_pdf(graph):
    """
    Kreiranje grafa u pdf obliku

    Parameters
    ----------
    graph: numpy polje 
        Matrica direktiranog grafa

    Returns
    -------
    None

    """

    G = graph
    pos = nx.layout.spring_layout(G) # pozicioniranje čvorova 

    nodes = nx.draw_networkx_nodes(G, pos, node_size=30, node_color="blue") # stvaranje svih čvorova u grafu sa odgovarajućim parametrima
    edges = nx.draw_networkx_edges( #stvaranje rubova grafa odnosno pravaca sa odgovarajućim parametrima 
        G,
        pos,
        node_size=30,
        arrows=True,
        arrowstyle="->",
        arrowsize= 20,
        edge_color='blue',
        edge_cmap=plt.cm.Blues,
        width=1,
    )

    nx.draw_networkx_edge_labels(G,pos) #Postavlja rubne vrijednosti

    #Ove naredbe smo koristili za prikazivanje grafa
    ax = plt.gca() # nabavlja trenutnu instancu osi na slici
    ax.set_axis_off() # isključuje os x i y 
    #plt.show()
    plt.savefig("generatedGraph.pdf") # Spremanje grafa u file


def saveGraph(G, name):
    """
    Spremanje grafa u file

    Parameters
    ---------- 
    G: numpy polje
        Matrica direktiranog grafa
    name: string, 
        Naziv file-a

    Returns
    -------
    None

    """

    if '.txt' in name:
        np.savetxt(name, G, delimiter=',', newline="\n", fmt='%d')
    else:
        np.savetxt(name+'.txt', G, delimiter=',', newline="\n", fmt='%d')

    print('Graph saved successfuly')


def loadGraph(fileName):
    """
    Učitavanje grafa sa file-a

    Parameters
    ----------
    fileName: string 
        Naziv file-a kojeg želimo učitat


    Returns
    -------
    None

    """

    return np.loadtxt(fileName, delimiter=",", dtype= int)

    