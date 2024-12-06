from numba import jit
from numpy import *
from pynndescent import NNDescent
from scipy.spatial import KDTree
import time
import numpy as np
import warnings
from scipy import sparse
from scipy.sparse.csgraph import minimum_spanning_tree
import colorsys

def NaturalNeighbor(nnIndex,N,K):  
    print('Search natural neighbors...')  
    nb=zeros(N)
    supk=0
    count1=0   
    while 1:
        for i in range(N):
            q = nnIndex[i,supk+1] 
            nb[q] = nb[q] + 1  
        count2=sum(nb==0) 
        if (count1==count2) or (supk+1 == K-1):
            K = supk+2
            break
        else:
            supk=supk+1
            count1=count2 
    print('supk = '+str(supk))
    return nb,K 
 
def LDP(X,knnMethod,K):
    N = X.shape[0]
    # Step 1: detemine the natural neighbors
    print('find knn...')
    t0 = time.time() 
    if knnMethod == 'KD-tree':
        tree = KDTree(X) 
        dis, nnIndex = tree.query(X, k=K)
    elif knnMethod == 'NNDescent': 
        # index = NNDescent(X,n_neighbors = K) # initialized by random projection trees; n_neighbors is a parameter in indexing for constructing the searching graph 
        # nnIndex, dis = index.query(X, k=K)
        index = NNDescent(X,n_neighbors = K,random_state = 1)
        nnIndex,dis = index.neighbor_graph # given the fact that here testing dataset is actually the training dataset, there is no need to run index.query, i.e., one can directly use the neighbors of each node on the initially constructed neighbor graph 
        # nnIndex = nnIndex[:,0:K]
        # dis = dis[:,0:K]
    elif knnMethod == 'HNSW':
        # Declaring index
        p = hnswlib.Index(space = 'l2', dim = Dim) # possible options are l2, cosine or ip        
        # Initializing index - the maximum number of elements should be known beforehand
        p.init_index(max_elements = N, ef_construction = 200, M = 16)        
        # Element insertion (can be called several times):
        p.add_items(X, np.arange(N))        
        # Controlling the recall by setting ef:
        p.set_ef(50) # ef should always be > k        
        # Query dataset, k - number of closest elements (returns 2 numpy arrays)
        nnIndex,dis = p.knn_query(X, k = K)
        dis = sqrt(dis)
    else:
        print('No such knn method............................................')
        
    t_knn = time.time()
    
    nb,K = NaturalNeighbor(nnIndex,N,K)
    
    nnIndex = nnIndex[:,0:K]
    dis = dis[:,0:K]
    
    # step 2: compute density 
    f = nb/(sum(dis,1)+np.spacing(1))  
    
    # Step 3: determine the parent node 
    max_ind = np.argmax(f[nnIndex],axis = 1);  
    pr =zeros(N,dtype=int); # Pre-allocate the space for the parent node vector.
    rs = zeros(N,dtype=int)
    t = 0 
    for i in range(N):
        pr[i] = nnIndex[i,max_ind[i]] # pr(i): parent node of node i
        if pr[i] == i:
            rs[t] = i
            t = t + 1
    rs = rs[0:t]
    # Step 4: get initial clustering assignments 
    c = ClusterLabeling(pr,rs)
    
    return nnIndex,f,rs,c

def ClusterLabeling(pr,rs): 
    # first, determine the root label of each node;
    r = pr; # initialize the root label vector r (we will update it in the following loop)
    N = len(pr);
    passed_nodes = zeros(N,dtype=int); # Pre-allocate the maximum space for the passed nodes, since there are maximally N passed nodes.
    # note: the above pre-allocation aims to avoid using concatenation operation 
    # (shown in the pseudocode of Alg.3) to store all the passed nodes;
    # since concatenation operation is inefficient for Matlab.
    for i in range(N):
        if r[i]!=i:
            parent=i;
            t = 0; # a variable to count the number of passed nodes
            passed_nodes[t] = i;
            while r[parent] !=parent: # search root
                parent=r[parent];
                t = t + 1;
                passed_nodes[t] = parent; 
            r[passed_nodes[0:t+1]]=parent; # update root label of all the passed nodes (note that here "parent" stores the index of the reached root).
    # then determine the clustering labeling (cluster label: 1,2,...#roots)
    c=zeros(N,dtype=int); # Preallocate the space for the cluster label vector; c(i): cluster label of node i;
    c[rs] = arange(len(rs)); # first, assign cluster labels to the root nodes;
    c=c[r]; # then, assign cluster labels to non-root nodes based on the root nodes they have reached
    return c    

def EdgeCutting(pr1,EW,c,MinSize,nC):
    # Written by Teng Qiu (UESTC), Chengdu, China, 2022
    # # implementation of Supplementary Alg. S2 
    # Input: 
    #     pr1: i.e., pr' in Alg. S1, which is the parent supernode vector for the supernodes; pr1(i) denotes the parent supernode of supernode i;
    #     EW: i.e., ew' in Alg. S2, denoting the edge weight vector; EW(i) denotes the edge between supernode i and its parent supernode pr1(i);
    #     c: initial cluster label vector (obtained in step 4). 
    #     MinSize: cluster size threshold for the cutting (specifying the minimal cluster size);
    #     nC: expected number of clusters;
    # Output: 
    #     pr2: i.e., pr'' in Alg. S2, denoting the updated parent supernode vector after edge cutting. 
    #     rs2: i.e., rs'' in Alg. S2, denoting the root supernode vector. 
    
    # Note: the input NW is the result (i.e.,initial weight of each supernode) of step 1 of the "ComputeNW" algorithm
    print('  Cut (stage 1): determine node weight in the constructed forest...')
    CS1_st = time.time();
    # determine the initial weight of each supernode (1st step of Alg. S1)
    M = len(EW); N = len(c);
    NW=zeros(M); # NW(i) will store the number of nodes in cluster i.
    for i in range(N):
        NW[c[i]] = NW[c[i]] + 1; 
    
    # Compute inNeighbors (i.e., step 2 of Alg. S1)
    inNei = [[] for i in range(M)]; # note: each cell is not initialized by the array size; this is a problem for speed as the elements are gradually added; but this is not a problem for c++ using advanced data structure; For Matlab, one can also consider to use a vector to count the number of elements of each cell first, based on which each cell can be initialized; 
    
    roots = zeros(M,dtype=int)
    t = 0
    for i in range(M):
        if pr1[i] != i:
            inNei[pr1[i]].append(i) 
        else:
            roots[t] = i
            t = t + 1
    roots = roots[0:t] 
    # linearlize the nodes in the in-tree-based forest such that all the in-neighbors of each
    # node have larger indexes than this node (this is fulfilled based on the
    # Breadth First Search algorithm. (Step 3 of Alg. S1)
    i = 0;      
    Ind = zeros(M,dtype=int);
    ct = 0;
    for j in range(len(roots)):        
        Ind[ct] = roots[j]; 
        ct = ct + 1;
        while i<=ct-1:
            temp = inNei[Ind[i]]
            if len(temp):     
                for m in range(len(temp)):    
                    Ind[ct] = temp[m]; 
                    ct = ct + 1;
            i = i + 1;                     
    # update the weight of each node on the in-tree-based forest (Step 4 of Alg. S1)
    for j in range(M):
        i = Ind[M-1-j];
        if pr1[i]!=i:
            NW[pr1[i]]=NW[pr1[i]]+NW[i];      
    ## cut the edges according to cluster number and MinSize
    ind = np.argsort(-EW); # Step 2 of Alg. S2; 
    # the following is the step 3 of Alg. S2
    cut_edge_num = 0; 
    t = 1;
    num_roots_initial = len(roots);
    num_of_edges_in_graph = M - num_roots_initial;  
    if nC >= num_roots_initial:
        num_of_edges_required_to_remove = nC - num_roots_initial; 
    else:
        num_of_edges_required_to_remove = 0;
        print('there could exist over-partitioning problem; it is suggest to increase the value of parameter k or increase cluster number');
   
    passed_node = zeros(M,dtype=int);
    CS1 = time.time() - CS1_st
    print('  cost time on 1st stage of Cut: '+str(CS1)+'s')
    
    print('  Cut (stage 2): check the edges one by one in decreasing order of edge weight...')
    CS2_st = time.time();
         
    while (cut_edge_num != num_of_edges_required_to_remove) and (t <= num_of_edges_in_graph):
        start_node = ind[t-1];
        end_node = pr1[start_node];
        if NW[start_node] > MinSize:
            # search the root node of end node
            ct = 0; 
            # lines 10 to 15
            passed_node[ct] = end_node; 
            ct = ct + 1;
            while end_node != pr1[end_node]:
                end_node = pr1[end_node];                  
                passed_node[ct] = end_node;
                ct = ct + 1;
                       
            # lines 16 to 24
            root_node_reached = end_node;
            
            if NW[root_node_reached]-NW[start_node] > MinSize:
                NW[passed_node[0:ct]] = NW[passed_node[0:ct]] - NW[start_node];
                pr1[start_node] = start_node;
                cut_edge_num = cut_edge_num + 1; 
                 
        t = t + 1; 
    pr2 = pr1;
    
    r_num = 0
    rs2 = zeros(nC,dtype=int)
    for i in range(M):
        if pr2[i] == i:
            rs2[r_num] = i
            r_num = r_num + 1
    CS2 = time.time() - CS2_st
    print('  time cost on the 2nd stage of Cut: '+str(CS2)+'s')  
    return pr2,rs2

def FastLDPMST(X,nC,MinSize,K,knnMethod):
    N = X.shape[0]
    TotalTime_start = time.time()
    # print('steps 1 to 4...')
    neighborIds,f,rs,c = LDP(X,knnMethod,K); # steps 1 to 4
    steps_1_to_4_time = time.time() - TotalTime_start;
    # print('  Time Cost on Steps 1 to 4: '+str(steps_1_to_4_time)+'s');
    #% Steps 5 to 8
    Rsamples = X[rs,:]; # Rsamples stores the samples corresponding to the root nodes;
    del X; # save some space when processing very large datasets
    M = len(rs); # number of root nodes = the number of initially obtained clusters (i.e.,
    # the number of supernodes)
    if M > nC:
        ## Step 5: compute adjacency (or weight) matrix of a weighted graph
        # step 5 contains the following two sub-steps (step 5.1 and step 5.2).
        step5_time_clusterDistance_start = time.time();
        #% step 5.1
        # print('step 5.1: determine multiple cluster labels of each node...')
        # The lines 4 and 5 of the pseudocodes of Alg. 4 show a nested
        # "for" loop, which should be avoided in Matlab (since Matlab is more efficient on
        # processing vectors than loops). In the following, we first determine the reverse neighbor i of each
        # node j (not that in lines 4 and 5 of Alg. 4, j is a neighbor of node
        # i; conversely, i is a reverse neighbor of node j). The goal of lines
        # 3 to 5 is to union the cluster label of all the reverse neighbors of
        # nodes j (note that the cluster labels of some reverse neighbors could
        # be the same).
        k = neighborIds.shape[1]; 
        Temp = zeros((N*k,2),dtype=int)
        t = 0
        for j in range(k):
            for i in range(N):            
                Temp[t,0] = neighborIds[i,j]
                Temp[t,1] = c[i]
                t = t + 1
        del neighborIds; # free up some space.
        
        # Note that in Alg. 4, ML is a data structure containing N sets (i.e., ML(j),j = 1 to N). 
        # In the following, we will not try to store the information by sets.
        # Insteads, the vectors will be used for storing the information in ML.
        # Specifically, we will use "unique" to remove the repeated row;
        # consequently, the "union" operation (in line 5 of Alg. 4) is not needed.
        # And the output matrix Temp2 (= [I J]) stores all the information associated
        # with ML, where J(t) stores the reverse cluster label of node I(t), t>=1.
        
        Temp2 = unique(Temp,axis = 0); # for the matrix A, this returns the unique rows of A. The rows of the matrix C will be in sorted order.
        del Temp;
        I = Temp2[:,0]; # Note: the values in I have been sorted in ascending order in "unique" function;
        J = Temp2[:,1]; # Note: the values in J have been sorted in ascending order in "unique" function;
        del Temp2;
        
        # Then, we determine the size of ML(j) indirectly based on the repeatedness of the elements j in vector I.
        # Note that the values in I have been sorted in ascending order
        # by "unique" function. In order words, the same values are 
        # adjacent in vector I (e.g., [1,1,1,2,2,3,3]). 
        # Thus, to determine the size of ML(2), we need to determine (from left to right) the 
        # first index (i.e., 4) and last index (i.e., 5) of 2 in vector I, then the size of ML(2) is
        # 5 - 4 + 1 = 2. 
        
        start_idx = zeros(N,dtype=int);
        end_idx = zeros(N,dtype=int);
        ML_size = zeros(N,dtype=int);
        j =  0;
        start_idx[j] = 0;
        for t in range(1,len(I)):
            if I[t] != I[t-1]:
                end_idx[j] = t - 1;
                ML_size[j] = end_idx[j] - start_idx[j] + 1;
                j = j + 1;
                start_idx[j] = t; 
        end_idx[j] = len(I)-1; # in this line, j should be N.  
        ML_size[j] = end_idx[j] - start_idx[j] + 1;
        
        #% step 5.2
        # print('step 5.2: compute a sparse weight matrix of size:'+str(M)+' x '+str(M)+'...');
        Total_Num = int(sum(ML_size*(ML_size - 1))/2); # Total_Num: the total number of pairs of (p,q) that requires to be considered in line 9 of Alg. 4
        Pairs = zeros((Total_Num,2),dtype = int); # Pre-allocate the space. Each row of Pairs will be used to store a pair of elements (p,q) in any set ML(j).
        Pairs_f = zeros(Total_Num); # Pre-allocate the space. Pairs_f(t) will be used to store the density information f(j) corresponding to a pair of (p,q)
        
        # in the following, we first store all the pairs of elements (p,q) in
        # each set ML(j) in matrix Pairs (based on the cluster label vector J) and store the corresponding densities in
        # vector Pairs_f.
        
        tt = 0;
        for j in range(N):
            if ML_size[j] != 1:
                ML_j = J[start_idx[j]:(end_idx[j]+1)]; # note: the values in J has been sorted in ascending order (according to the unique function);
                for s in range(ML_size[j]-1):
                    for t in range(s+1,ML_size[j]):
                        # first store in Pairs(tt,1) and Pari(tt,2) all
                        # different elements p,q in ML(j),respectively. Note:
                        # there could exist repeated rows in Pairs, which will be removed later.
                        Pairs[tt,0] = ML_j[s];
                        Pairs[tt,1] = ML_j[t];
                        Pairs_f[tt] = f[j]; # store the corresponding density f(j);
                        tt = tt + 1; 
        del I,J
            
        # Then, we compute the non-zero elements of matrix F, Count, and D, as well as
        # the set Xi (in line 13) of Alg. 4 in the following way.
        # First, we get all the different pairs of (p,q) from matrix Pairs (using "unique"
        # function in Matlab); the output matrix DiffPairs stores the
        # coordinates of the non-zero elements in the weight matrix D (note that
        # matrix DiffPairs can be viewed as the matrix form of the set Xi
        # in line 13 of Alg. 4, i.e, each row of DiffPairs can be viewed as an element
        # in set Xi); Then, we accumulate the densities of those
        # repeated pairs stored in Pairs so as to get non-zero elements of
        # matrix F in Alg. 4 and we also count the number of those
        # repeated pairs so as to get the non-zero elements of matrix Count in
        # Alg.4. Note that the above goals are fulfilled based on another output of "unique" function,
        # i.e., vector IC in the following. And note that we store the non-zero elements
        # of matrix F and matrix Count in vectors F_v and Count_v, respectively.
        
        DiffPairs,IC = unique(Pairs,axis = 0,return_inverse = True); # get all the different rows of matrix Pairs, each representing the row and column index of a non-zero element in weight matrix D;
        # note: Pairs = DiffPairs[IC,:]
        P = DiffPairs[:,0]; # row index of the non-zero elements of D;
        Q = DiffPairs[:,1]; # column index of the non-zero elements of D;
        # P stores all the values of p, and Q stores all the corresponding
        # values of q in Alg. 4.
        
        Num_nonZeroE = len(P); # Num_nonZeroE: the number of all the non-zero elements in weight matrix D.
        F_v = zeros(Num_nonZeroE); # Pre-allocate the space.
        Count_v = zeros(Num_nonZeroE); # Pre-allocate the space.
        for t in range(len(IC)):
            # note: Pairs = DiffPairs(IC,:);
            # IC(t) specifies which row of DiffParis is the same as the t-th
            # row of Pairs
            # Accordingly, the the following two lines of code can be viewed as the 1-dimensional
            # indexing version of the corresponding 2-dimensional indexing
            # version in lines 10 and 11 of Alg. 4. 
            F_v[IC[t]] = F_v[IC[t]] + Pairs_f[t]; # vector F_v stores all the non-zero elements of matrix F in Alg.4
            Count_v[IC[t]] = Count_v[IC[t]] + 1; # vector Count_v stores all the non-zero elements of matrix Count in Alg.4
     
        D_v = zeros(Num_nonZeroE); # D_v will store the values of all the non-zero values of weight matrix D in Alg.4
        for t in range(Num_nonZeroE):
            d = sqrt(sum((Rsamples[P[t],:]-Rsamples[Q[t],:])**2)); # numerator of Eq. 6
            D_v[t] = d/F_v[t]/Count_v[t];  # compute a non-zero element of weight matrix D according to Eq. 6 (i.e., the non-zero distances between clusters or supernodes);
            # Note: D_v, F_v, Count_v are the three vectors storing all the
            # non-zero elements of matrices D, F, and Count in Alg. 4, respectively.
      
        step5_time_clusterDistance = time.time() - step5_time_clusterDistance_start;
        # print('  Time Cost on Step 5: '+str(step5_time_clusterDistance)+'s');
        
        # Note: an easier and more straight-forward way of determining matrices F, Count, and D of Alg.4 is by virtue of sparse function in Matlab.
        # Specifically, define matrices F, Count, and D as sparse matrices and then do the assignment and query operation
        # based on the pseudocode of Alg.4. However, our experiments show that
        # such easier sparse-matrix-based programming
        # is slightly slower than the above non-sparse-function-based programming in Matlab; for instance,
        # on a dataset with millions of samples, the non-sparse-function-based code spent around 10 second, in contrast to
        # around 30 seconds for the sparse-function-based code (omitted here).
        # This is due to the following limitation for the sparse matrix in Matlab.
        # In Matlab, assigning a value to an element of a sparse matrix is not
        # as efficient as querying an element of a sparse matrix; in Alg. 4, there involves such code (line 10):
        # F(p,q) <- F(p,q) + f(j), which involves the assignment operations on F. Since line 10
        # of Alg. 4 exists in a nested loop, this will amplify the above limitation of sparse matrix.
        
        #% Step 6: Construct MSF
        step6_time_on_MSF_start = time.time();
        # print('step 6: Construct MSF ...');
        G = sparse.coo_matrix((D_v,(P,Q)),shape=(M,M)).tocsr() # construct the sparse weighted graph based on the non-zero elements of the weight matrix D
        ST = minimum_spanning_tree(G) #  This is computed using the Kruskal algorithm.  
        # print('transform MSF to in-tree-based MSF...')      
        pr1 = bfs_search(M, ST)
        
        EW = zeros(M); # Pre-allocate the space for edge weight vector of an in-tree-based MSF.
        for i in range(M):
            EW[i] = max(ST[i,pr1[i]],ST[pr1[i],i]);  # ST is not a symmetric matrix, and thus max is used to get the non-zero element
      
        step6_time_on_MSF = time.time() - step6_time_on_MSF_start;
        # print('  Time Cost on Step 6: '+str(step6_time_on_MSF)+'s');
        
        #% Step 7: Cut the forest
        # print('Step 7: Cut the tree...')
        step7_time_on_cutting_start = time.time();
        pr2,rs2 = EdgeCutting(pr1,EW,c,MinSize,nC); # Supplementary Alg. S2; pr1: pr' in Alg. S1; pr2: pr'' in Alg. S2.
        step7_time_on_cutting = time.time() - step7_time_on_cutting_start
        # print('  Time Cost on Step 7: '+str(step7_time_on_cutting)+'s')
        
        #% Step 8: update cluster labels of all the nodes
        # print('Step 8: final cluster assignment...');
        step8 = time.time();
        sp_c = ClusterLabeling(pr2,rs2); # first, get the cluster labels of all supernodes (line 1 of supplementary Alg. S3); sp_c(i): the cluster label of the supernode i;
        c = sp_c[c]; # then, get the cluster label of all the (normal) nodes (line 2 of supplementary Alg. S3).
        step8_time = time.time() - step8
        # print('  Time Cost on Step 8: '+str(step8_time)+'s')
         
    else:
        # this case is explained in the 2nd footnote of the paper (Section 4.9).
        warnings.warn('  in this case, steps 5 to 8 are not needed')
     
    TotalTime=time.time() - TotalTime_start;
    # print('End of clustering');
    # print('############# summary ###################');
    # print('Time Cost on whole method: '+str(TotalTime)+'s');
    
    return c,f,TotalTime

def bfs_search(N, ST):
    Edges = ST.tocoo()
    st = Edges.row
    en = Edges.col
    
    adj = [[] for i in range(N)]
    for i in range(len(st)):
        v1 = st[i]
        v2 = en[i]
        adj[v1].append(v2)
        adj[v2].append(v1)
        
    pr = arange(N)
    bfs_traversal = zeros(N)
    vis = [False]*N
    t = 0
    for i in range(N):  
        if (vis[i] == False):
            q = []
            vis[i] = True
            q.append(i) 
            # search the component containing node i
            while (len(q) > 0):
                g_node = q.pop(0) 
                bfs_traversal[t] = g_node
                t = t + 1
                for j in adj[g_node]:
                    if (vis[j] == False):
                        vis[j] = True
                        q.append(j)
                        pr[j] = g_node
    return pr

def get_n_hls_colors(num):
   hls_colors = []
   i = 0
   step = 360.0 / num
   while i < 360:
       h = i
       s = 90 + random.random() * 10
       l = 50 + random.random() * 10
       _hlsc = [h / 360.0, l / 100.0, s / 100.0]
       hls_colors.append(_hlsc)
       i += step
   return hls_colors

def ncolors(num):
    rgb_colors = []
    if num < 1:
        return rgb_colors
    hls_colors = get_n_hls_colors(num)
    for hlsc in hls_colors:
        _r, _g, _b = colorsys.hls_to_rgb(hlsc[0], hlsc[1], hlsc[2])
        r, g, b = [int(x * 255.0) for x in (_r, _g, _b)]
        rgb_colors.append([r, g, b]) 
    return rgb_colors