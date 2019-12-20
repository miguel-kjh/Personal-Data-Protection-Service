from languageBuilder import languageBuilder
from NameSearchByEntities import NameSearchByEntities
from NameSearchByBruteForce import NameSearchByBruteForce
from NameSearchByGenerator import NameSearchByGenerator


lb = languageBuilder()
lb.defineNameEntity()
nlp = lb.getlanguage()
s = NameSearchByBruteForce(nlp)
print("Nombres finales num", s.searchNames("Ángel Javier Eduardo Isidoro de todos los Santos"))
print("Nombres finales 1", s.searchNames("CAROLINA BENITEZ del ROSARIO y juez Daniel Rosas"))
print("Nombres finales 2", s.searchNames("Noelia Real Giménez"))
print("Nombres finales 3", s.searchNames("La señorita Maria Baute"))
print("Nombres finales 3", s.searchNames("La señorita Carla Baute Sanchez"))
print("Nombres finales 4", s.searchNames("Miguel de Montes de Oca estuvo aquí hace 2 minutos"))
print("Nombres finales 5", s.searchNames("Bien, soy el juez Cayo Medina de Lara, voy a nombrar a los representantes de la Asamblea: "
            + "Laura Vega, "
            + "Laura Sebastian Ramírez y "
            + "Joseph Stetter."))