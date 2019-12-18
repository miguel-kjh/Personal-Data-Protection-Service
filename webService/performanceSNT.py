from SearcherNamesTexts import SearchNamesDeepSearch,SearcherNamesProcedure
from time import time
from languageBuilder import languageBuilder
import matplotlib.pyplot as plt

nlp = languageBuilder()
def measuereDeepSearch(data):
    iter = 100
    sn = SearchNamesDeepSearch(nlp.getlanguage())
    summatory = 0
    for _ in range(0,iter):
        st = time()
        sn.searchNames(data)
        summatory += time()-st
    return  summatory / iter

def measuereSearch(data):
    iter = 100
    sn = SearcherNamesProcedure(nlp.getlanguage())
    summatory = 0
    for _ in range(0,iter):
        st = time()
        sn.searchNames(data)
        summatory += time()-st
    return  summatory / iter


if __name__ == "__main__":
    data_name_only = [
        "Miguel", "Miguel Ángel", "Raúl Lopez-Potrillo" , "Miguel Ángel Medina Ramírez","Javier Jaime Medina de Cruz Camino"
        #"Felipe Juan Froilán de todos los Santos", "Gumersindo Javier Eduardo Isidoro de todos los Santos"
    ]
    data_without_name = [
        "", "hola que", "hola que tal","esta en la fiesta", "uno dos tres cuatro cinco", "uno dos tres cuatro cinco seis" , 
        "no me lo creo, en serio", "estos van en serie y aquellos en paralelo"
    ]
    data = [
        "¿Está aquí Maria Ortega?", 
        "El PSOE no camina pues en la dirección de buscar un plan alternativo con el PP y Ciudadanos, sino en la de lograr la investidura alrededor de la mayoría que hizo la moción de censura a Mariano Rajoy en junio de 2018. ",
        "A diferencia de Albert Rivera, al que aspira a sustituir en el congreso de la próxima primavera, Arrimadas es proactiva en la búsqueda de un acuerdo para la investidura, pero la alianza entre las fuerzas constitucionalistas que plantea no se contempla de momento ni por el Gobierno ni por el PP",
        "¿Dónde estaba hace ocho años? Olmo, Mercedes y Adrián atravesaron un día de 2011 la calle Atocha. No iban solos. No se conocían. Llenaron el centro de Madrid cuando nadie se lo esperaba. España estaba inmersa en otra anodina precampaña electoral para las autonómicas y municipales de 2011 y no los vio llegar." 
        + "Aquí está la juventud precaria”, se presentaron. Un mes después nacía el 15-M. Surgió con tanta fuerza y llegó tan en silencio que dejó atónito a un país con poca querencia a la protesta callejera",
        "El genetista estadounidense George Church está ultimando una aplicación de citas, similar a Tinder o Meetic, pero con información genética de sus usuarios para evitar que dos personas portadoras de una misma enfermedad hereditaria grave se conozcan, se enamoren y tengan hijos. La app, bautizada DigiD8, estará disponible “probablemente pronto”, según explica Church en la web de su laboratorio de la Universidad de Harvard.Solo revisamos enfermedades clínicamente muy graves, como la de Tay-Sachs”, subraya el investigador. El cerebro de los niños con este trastorno acumula una sustancia grasienta que destruye sus neuronas. Las criaturas afectadas suelen morir antes de cumplir los cuatro años. Pero, para que surja la enfermedad, es necesario que tanto la madre como el padre presenten una misma mutación en uno de sus 22.000 genes. Si existe esa coincidencia genética entre los progenitores, hay un 25% de probabilidades de que su hijo sufra este trastorno letal."
    ]
    timesDeepSearcher = []
    timesProcedureSearcher = []
    for element in data_name_only:
        timesDeepSearcher.append(measuereDeepSearch(element))
        timesProcedureSearcher.append(measuereSearch(element))
        #print(SearcherNamesProcedure(nlp.getlanguage()).searchNames(element))
    plt.plot(timesDeepSearcher, 'r')
    plt.plot(timesProcedureSearcher, 'g') 
    plt.legend(("Deep","Procedure"))
    plt.show()