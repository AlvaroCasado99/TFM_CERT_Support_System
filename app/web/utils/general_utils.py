""" Aquí se encuntran funciones que no tienen por contexto un lugar determinado"""

def is_sublist(list1: list, list2: list) -> bool:
    ls1 = [elem for elem in list1 if elem in list2]
    ls2 = [elem for elem in list2 if elem in list1]

    return (ls1 == ls2) and (len(ls1)>0 or len(ls2)>0)
