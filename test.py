import stepper.ammo as ammo
import stepper.format as f

for missile in (f.Stpd(ammo.Factory(None))):
    print missile
