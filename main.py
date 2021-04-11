'''
Kolegij: Distribuirani sustavi
Tema: Floyd-Warshallov algoritam (MPI)
Mentori: izv. prof. dr. sc. Božidar Kovačićić i v. pred. dr. sc. Vedran Miletić
Izradili: Kristijan Krulić i Filip Ožbolt
#################################################

main.py za razliku od floydWarshallMPI.py omogućava veći stupanj customizacije(Dinamički odabir broja čvorova u grafu,
    kreiranje vizualnog prikaza tog grafa u pdf formatu, čitljiviji format ispisa te ispis u .txt file)
'''



from mpi4py import MPI
import numpy as np
from graph import create_graph, create_pdf, loadGraph, saveGraph
from file import set_graph

# mpiexec -n 4 python main.py

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

INF = 9999
generatedGraph = None


if rank==0:  
    set_graph()
    generatedGraph = loadGraph('testExample.txt')

    #https://www.quora.com/Are-NumPy-arrays-faster-than-lists
    #bez konvertiranja numpy polja u listu je read i write duplo sporiji
    generatedGraph = generatedGraph.tolist()

'''
generatedGraph = [[0, 5, INF, 10],
        [INF, 0, 3, INF],
        [INF, INF, 0,   1],
        [INF, INF, INF, 0]
        ]
'''

graph = comm.bcast(generatedGraph, root=0)
n = comm.bcast(len(graph), root=0)


if(rank != 0):

    #raspodjela obrade podataka(matrice) po procesima
    #step -> promijenjiva vrijednost za određivanje početka i kraja rada svakog procesa
    #start -> varijabla koja određuje početak rada za pojedini proces
    #end -> varijabla koja određuje kraj rada pojedinog procesa
   
    step = int(len(graph) / size)
    start = (rank - 1)*step
    end = start + step
    if rank == size - 1:
        end = n

    
    #k -> središnji vrh (čvor kroz koji se traži najkraći put do vrha)
    for k in range(start, end):
        #print(k, rank)
        for i in range(0, n):

                for j in range(0, n):
                    if (i == j): continue
                    graph[i][j] = min(graph[i][j],
                                    graph[i][k] + graph[k][j])
    
        #print('rank:', rank, '\n', graph)
   
    sendmsg = comm.send(graph, dest=0)
    
    

else:
    minMatrix = np.full((n, n), 9999)

    for srcc in range(1, size):
        result = comm.recv(source=srcc)
        finalResult = np.minimum(minMatrix,result)
    

    #radi malo čitljivijeg ispisa (potrebno promijeniti format ispisa u '%s' ako želimo umjesto 9999 spremati 'INF)
    #result = [[y if y < 9900 else 'INF' for y in x] for x in result]
    finalResult = np.asarray(finalResult)
    finalResult[finalResult > 9900 ] = 9999
     
    print('result:\n', np.asarray(finalResult))
    

    #create_pdf(generatedGraph) -> vec se prije kreira nakon odabira cvora
    saveGraph(np.asarray(result), 'testExampleResult.txt')
    
    

