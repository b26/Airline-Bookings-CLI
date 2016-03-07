drop view available_flights;
create view available_flights(flightno,dep_date, src,dst,dep_time,arr_time,fare,seats,
  price) as
(
  select f.flightno, sf.dep_date, f.src, f.dst, f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)),
  f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24,
  fa.fare, fa.limit-count(tno), fa.price
  from flights f, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2
  where f.flightno=sf.flightno and f.flightno=fa.flightno and f.src=a1.acode and
  f.dst=a2.acode and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) and
  sf.dep_date=b.dep_date(+)
  group by f.flightno, sf.dep_date, f.src, f.dst, f.dep_time, f.est_dur,a2.tzone,
  a1.tzone, fa.fare, fa.limit, fa.price
  having fa.limit-count(tno) > 0
);

drop view good_connections;
create view good_connections (src,dst,dep_date, dep_time, arr_time, flightno1,flightno2, layover,price) as
(
  select a1.src, a2.dst, a1.dep_date, a2.dep_time, a1.arr_time, a1.flightno, a2.flightno, a2.dep_time-a1.arr_time,
  min(a1.price+a2.price)
  from available_flights a1, available_flights a2
  where a1.dst=a2.src and a1.arr_time +1.5/24 <=a2.dep_time and a1.arr_time +5/24 >=a2.dep_time
  group by a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a2.dep_time, a1.arr_time
);


drop view search_flights;
create view search_flights(flightno1, flightno2, src, dst, dep_date, dep_time, arr_time, layover, stops, fare, seats, price) as
(
    select a.flightno, g.flightno2, a.src, nvl(g.dst, a.dst) as dst, a.dep_date, to_char(a.dep_time, 'HH24:MI'), to_char(a.arr_time, 'HH24:MI'), g.layover, count( distinct g.layover), a.fare, a.seats, greatest(a.price, nvl(g.price, 0)) from
available_flights a left outer join good_connections g on g.flightno1 = a.flightno and g.dep_date = a.dep_date
  group by a.flightno, g.flightno2, a.src, a.dst, g.dst, a.dep_date, a.dep_time, a.arr_time, a.fare, g.layover,  a.seats, a.price, g.price
);







