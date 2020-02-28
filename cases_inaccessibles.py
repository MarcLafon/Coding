import numpy as np

def get_voisins(i,j,x):
    l,c = x.shape

    if j==0:
        left=(np.NaN,np.NaN),np.inf
    else:
        left=(i,j-1),x[i,j-1]

    if j==(c-1):
        right = (np.NaN,np.NaN),np.inf
    else:
        right = (i,j+1),x[i,j+1]
    
    if i==0:
        up = (np.NaN,np.NaN),np.inf
    else:
        up = (i-1,j),x[i-1,j]

    if i==(l-1):
        down = (np.NaN,np.NaN),np.inf
    else:
        down = (i+1,j),x[i+1,j]
      
    return np.array((left,right,up,down))


def is_unseen(i,j,positions):
    if np.isnan(i) or np.isnan(j):
        return False
    else:
        return positions[i,j]==0

def select_move(i, j, x, voisins, positions):

    possible_moves = np.less_equal([v[1] for v in voisins], x[i,j])
    unseen_moves = np.array([is_unseen(a,b,positions) for (a,b),v in voisins])
    
    moves = np.bitwise_and(possible_moves, unseen_moves)
    selected_voisins = voisins[moves]
    n = selected_voisins.shape[0]
    if n>0:
        return n, selected_voisins[n-1]
    else:
        return n,((np.NaN,np.NaN),np.NaN)

def recherche(checkpoint, x, positions):
    new_checkpoints=[]
    move = True
    i,j=checkpoint
    alpha=1
    while move:
        positions[i,j]+=1
        voisins = get_voisins(i,j,x)
        n,((a,b),v) = select_move(i, j, x, voisins, positions)
        if n==0:
            move=False
        elif n>1:
            new_checkpoints.append((i,j))
        i=a
        j=b  
        alpha+=1
    return new_checkpoints, positions

def clear_checkpoints(checkpoints,positions):
    remaining_checkpoints = []
    for checkpoint in checkpoints:
        neighbors = get_voisins(checkpoint[0],checkpoint[1],positions)
        remaining_positions = np.where(get_voisins(checkpoint[0],checkpoint[1],positions)[:,1]==0)[0].shape[0]
        if remaining_positions>0:
            remaining_checkpoints.append(checkpoint)
    return remaining_checkpoints

def count_unaccessible_points(x):
    positions = np.zeros(x.shape).astype(np.int)
    checkpoints = [(0,0)]
    while len(checkpoints)>0:
        checkpoint = checkpoints.pop(0)
        new_checkpoints, positions = recherche(checkpoint, x, positions)
        checkpoints.extend(new_checkpoints)
        checkpoints = clear_checkpoints(checkpoints,positions)
    
    unaccessible_points = np.where(positions==0)[0].shape[0]
    return unaccessible_points
    
if __name__=="__main__":
    x = np.array([[6,6,5,3,6],[6,4,5,3,1],[4,8,2,4,1],[5,2,2,4,1],[0,1,0,2,0]])
    n = count_unaccessible_points(x)
    print(x)
    print(n)
