import numpy as np
import matplotlib.pyplot as pl

from fisheye import fisheye

# generate random points in [0,1]^2
# N = 10000
# pos = np.random.random((N,2))


pos = []

for i in range(0, 1080):
    for j in range(0, 1920):
        pos.append([i, j]) 
        
pos = np.array(pos)       

# initialize fisheye with radius R = 0.4 and focus in the center
F = fisheye(R=150,d=3)
F.set_focus([540,960])

fig, axs = pl.subplots(1, 4, figsize=(16,8))

for iax, ax in enumerate(axs):
    
    # iterate through different fisheye mode
    if iax == 0:
        ax.set_title('original')
    elif iax == 1:
        ax.set_title('default fisheye')
        F.set_mode('default')
    elif iax == 2:
        ax.set_title('Sarkar-Brown')
        F.set_mode('Sarkar')
    elif iax == 3:
        ax.set_title('root')
        F.set_mode('root')

    if iax == 0:
        _pos = pos
    else:
        # fisheye transform
        _pos = F.radial_2D(pos) 


    # for i in range(len(pos)):
    #     if( pos[i][0] == _pos[i][0] and pos[i][1] == _pos[i][1]):
    #         continue
    #     print(i, "  ", pos[i], "  ",_pos[i])    

    ax.plot(_pos[:,0],_pos[:,1],'.k', markersize = 1)
    ax.axis('square')
    ax.axis('off')

fig.tight_layout()
fig.savefig('scatter.png')

# pl.show()