import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm


#Definer enhetskvadratet vi ønsker å løse varmelikningen på
tot_x1 = 1 #lengde i x1-retning
tot_x2 = 1 #lengde i x2-retning
tot_tid = 0.1  #lengde i tidsretning

#Antall grid points i x1 og x2 -retning og tidssteg
pkt_x1 = 10
pkt_x2 = 10
pkt_tid = 1000

#Steglengde i hver retning og tidssteg
steg_x1 = tot_x1 / pkt_x1
steg_x2 = tot_x2 / pkt_x2
steg_tid = tot_tid / pkt_tid

#Gridpunkter i hver retning
x1 = np.linspace(0, tot_x1, pkt_x1)
x2 = np.linspace(0, tot_x2, pkt_x2)
tid = np.linspace(0, tot_tid, pkt_tid)

#Lager et array for varmen tar inn initialkrav
u = np.zeros((pkt_x1, pkt_x2, pkt_tid))

#Lager en initialverdifunksjon
def initialkrav(x1, x2):
    return np.sin(3*np.pi*np.sqrt((x1-.5)**2 + (x2-.5)**2))

#Beregner varmen med ved å iterere gjenneom initialkravfunksjonen
def verdiberegning():
    verdi = np.zeros((pkt_x1, pkt_x2))
    for i, x1_val in enumerate(x1):
        for j, x2_val in enumerate(x2):
            verdi[i, j] = initialkrav(x1_val, x2_val)
    return verdi

u[:,:,0] = verdiberegning() #Alle varmeverdier når tid = 0

#Euler eksplisitt
def neste_verdiberegning(u):
    neste_verdiberegning = np.zeros((pkt_x1, pkt_x2))
    for i in range(1, pkt_x1-1):
        for j in range(1, pkt_x2-1):
            #Diskretisert versjon av varmelikningen
            neste_verdiberegning[i,j] = steg_tid/(steg_x1**2)*(u[i-1,j]-2*u[i,j]+u[i+1,j]) + steg_tid/(steg_x2**2)*(u[i,j-1] - 2*u[i,j] + u[i,j+1]) + u[i,j]
    return neste_verdiberegning

#Itererer gjennom tidsintervallet. Finner løsningene på varmelikningen ved ulik tid.
for i in range(pkt_tid-1):
    u[:,:,i+1] = neste_verdiberegning(u[:,:,i])

#Greier for å få animasjonen til å virke
T_ani = 2 #Varighet på animasjonen i sekunder
framespersecond = 30 #Frames per sekund
tot_frames = T_ani * framespersecond #Totalt antall frames

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}) #Plotter
meshX, meshY = np.meshgrid(x1, x2)

def clear(frame):
    ax.clear()
    #Clearer plottet for hver gang
    overflate = ax.plot_surface(meshX, meshY, u[:,:,frame], cmap = cm.coolwarm)
    ax.set_title("Simulering av varmeoverføring, u,  fra enhetsflaten")
    ax.set_xlabel("$x1$")
    ax.set_ylabel("$x2$")
    ax.set_zlabel("$u - Varme$")
    ax.set_xlim((0,tot_x1))
    ax.set_ylim((0,tot_x2))
    ax.set_zlim((-1,1))
    return overflate

#Funksjon for animasjon
ani = animation.FuncAnimation(fig, clear,
                              frames=np.linspace(0, pkt_tid-1, tot_frames).astype(int), interval = 1000/framespersecond)
plt.show()