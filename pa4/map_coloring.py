
from CSPProblem import *
from typing import Dict, Iterable, List, Tuple

Country = str
Border = Tuple[Country, Country]

def _make_countrylist(borders: List[Border], other_countries: List[Country]):
        countries = set(other_countries)

        for country1, country2 in borders:
            countries.add(country1)
            countries.add(country2)
        
        countries = list(countries)
        countries.sort()
        return countries

def _make_constraints(borders: List[Border], country_ids: Dict[Country, int], color_options: int) -> Iterable[BinaryConstraint]:

    for country1, country2 in borders:
        id_1 = country_ids[country1]
        id_2 = country_ids[country2]
        assert id_1 != id_2
        
        variable_pair: VariablePair = (id_1, id_2)
        allowed_combinations: BinaryConstraintOptions = list(_make_allowed_combinations(color_options))
        constraint: BinaryConstraint = (variable_pair, allowed_combinations)
        yield constraint

def _make_allowed_combinations(color_options: int):
    for c1 in range(color_options):
        for c2 in range(color_options):
            if c1 != c2:
                yield (c1, c2)


def create_mapcoloring_csp(borders: List[Border], other_countries: List[Country]=[], color_options: int=4) -> CSPProblem:
    
    countries = _make_countrylist(borders, other_countries)
    
    country_name_dict = dict(enumerate(countries))
    country_ids = dict([(n,i) for i,n in enumerate(countries)])        

    border_constraints = _make_constraints(borders, country_ids, color_options)

    map_color_dict = dict([
        (i, chr(ord("a") + i)) for i in range(color_options)
    ])

    initial_color_options = [set(range(color_options)) for _ in range(len(countries))]

    return CSPProblem(
        domains = initial_color_options, 
        binary_constraints = border_constraints,
        variable_label_str = lambda i: country_name_dict[i],
        variable_value_str = lambda v: map_color_dict[v],
        max_varlabel_len = max(map(lambda x: len(x), countries))
    )