Šis projektas leidžia nuskaityti produktų informaciją (pavadinimą ir kainą) iš `https://www.gintarine.lt/asmens-higiena-3`.

Naudojimas

from karolis_s_mod1_atsikaitymas.main import *

Nuskaitymas iš Gintarines vaistines puslapio

from karolis_s_mod1_atsiskaitymas.main import *
products = crawl_gintarine ()

    for product in products:
        print (f"Pavadinimas: {product['title']}")
        print (f"Kaina: {product['price']}")