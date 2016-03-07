select s1.flightno1, s1.flightno2, s2.flightno1, s2.flightno2, s1.src, s1.dst, s1.dep_date as departure, s2.dep_date as return, (s1.price + s2.price) as price
from search_flights s1, search_flights s2
where s1.dst = 'YYZ' and s1.src = s2.dst and s2.src = 'YYZ';

