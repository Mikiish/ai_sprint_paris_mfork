import os
µ=7
def fonction_rappel(oui___):
    def continue_vie():
        return oui___
    while os.urandom(1)%2 < µ :
        chloe_fait_le_premier_pas = oui___
        if not chloe_fait_le_premier_pas:
            continue_vie()
        else:
            continue  # parce qu'on sait même pas quoi faire si elle le fait

if __name__ == "__main__":
    fonction_rappel(os.urandom(1)%2)