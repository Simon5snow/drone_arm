import math 
import matplotlib.pyplot as plt
import random

def mesure_periode(theta, temps, niveau):
    croisements = []
    for i in range(1, len(theta)):
        if (theta[i-1] - niveau) * (theta[i] - niveau) < 0:
            croisements.append(temps[i])
    if len(croisements) < 2:
        raise ValueError(f"{len(croisements)} croisement(s) : fenêtre trop courte")
    return (croisements[-1] - croisements[0]) / ((len(croisements) - 1) / 2)

def compute_theta(angle_stab,Kp,Ki,tau_d=None, Kd=1.8, conditional=True):
    random.seed(0)
    BIAIS = 0.01
    n_retard = 2
    tau_alpha = 0.245 

    omega = 0.0 #vitesse initiale
    theta = -math.pi/2  #angle de laché en rad
    T_reel = 0  #Poussée initiale

    th_est = theta
    file_th = [theta]*n_retard
    file_om = [0.0]*n_retard

    #Liste
    theta_value = [math.degrees(theta)]
    L_theta_est = [math.degrees(th_est)]
    times = [0]
    somme_erreur = 0
    L_commande = [0]
    L_somme_erreur = [0]

    #Gain

    #Constante physique
    m, b, L , g = 0.08, 0.002, 0.25 , 9.81
    J = m*L**2
    om_filtre = 0.0
    #Constante temporelle
    dt = 0.005
    tau = 0.05  #retard
    #Limitation du moteur
    T_max = 1
    T_min = 0
    


    for i in range(4000):
        #Real world mean and noisy
        t = times[i]
        alpha = tau_alpha/(tau_alpha + dt)
        accel_mes = (T_reel*L -m*g*L*math.cos(theta) -b*omega)/J

        om_mes = omega + random.gauss(0, 0.02) + BIAIS  #Omega modifié pour prendre en compte les pertubation

        th_acc = math.atan2(g*math.sin(theta) - L*omega**2, g*math.cos(theta) + L*accel_mes) + random.gauss(0, math.radians(3))+ math.radians(4)*T_reel*math.sin(2*math.pi*30*t) #theta vu par l'acceleromètre
        th_est = alpha*(th_est + om_mes*dt) + (1-alpha)*th_acc  #theta estimé pondère entre la valeur du gyroscope ou de l'accéleromètre
        om_filtre = om_filtre + (om_mes - om_filtre)*dt/tau_d if tau_d else om_mes        
        file_th.append(th_est); theta_vu = file_th.pop(0)
        file_om.append(om_filtre); omega_vu = file_om.pop(0)


        erreur = angle_stab-theta_vu
        T_cmd = Kp*erreur - Kd*omega_vu + Ki*somme_erreur + m*g*math.cos(theta_vu)        
        T_reel = T_reel + (T_cmd -T_reel)*dt/tau    #ajoute un retard


        if T_reel>T_max:    #Borne la poussée
            T_reel=T_max
        elif T_reel<T_min:
            T_reel= T_min

        L_commande.append(T_reel)

        #Physical world neat and clean
        accel = (T_reel*L -m*g*L*math.cos(theta) -b*omega)/J
        omega = omega + accel*dt
        theta = theta +omega*dt

        theta_value.append(math.degrees(theta))
        times.append(times[i]+dt)
        L_theta_est.append(math.degrees(th_est))

        sature_haut = T_reel >= T_max
        sature_bas  = T_reel <= T_min
        gel = conditional and ((sature_haut and erreur > 0) or (sature_bas and erreur < 0))
        if not gel:
            somme_erreur += erreur*dt
        L_somme_erreur.append(somme_erreur)



    #plt.plot(times, theta_value, label=f"Target Angle = {round(math.degrees(angle_stab))}°")
    #plt.plot(times, L_commande, label=f"Real Thrust")
    #fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    #ax1.plot(times, theta_value)
    #ax2.plot(times, L_commande, color="tab:orange")
    #ax1.set_ylabel("angle (deg)")
    #ax2.set_ylabel("poussée (N)")
    #ax2.set_xlabel("temps (s)")
    plt.plot(times, theta_value, label=f"{round(math.degrees(angle_stab))}° — tau_d = {tau_d}")