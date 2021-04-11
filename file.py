'''
file.py služi kao posrednik između graph.py i skripta kojima trebaju neke funkcije iz graph.py. 
Namjena je kreiranje grafa odnosno matrice težine(adjacency matrix) i zapisivanje/čitanje te matrice
'''

from graph import create_graph, saveGraph, loadGraph

def set_graph():
    """
    sekvencijalno kreira graf, sprema ga na disk, učitava i ispisuje radi provjere
   
    Parameters 
    ----------
    None
    
    Returns:
    -------
    None
    
    """

    nodes = int(input("Enter number of nodes: "))
    generatedGraph = create_graph(nodes)

    saveGraph(generatedGraph, 'testExample.txt')
    loadedGraph = loadGraph('testExample.txt')

    print('Initial graph:\n', loadedGraph, '\nNote: initial graph visualization is stored in pdf file')



def write_graph(graph):
    """
    sprema izračunati rezultat u file -> korisno kod velikog broja čvorova
   
    Parameters 
    ----------
    graph: numpy array
        Numpy matrica veličine n*n koja predstavlja rješenje algoritma 

    
    Returns:
    -------
    None
    
    """
    
    saveGraph(graph, 'testExampleResult.txt')


if __name__ == "__main__":
    set_graph()


