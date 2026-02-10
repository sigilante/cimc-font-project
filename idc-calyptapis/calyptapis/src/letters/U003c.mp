% U+003C LESS-THAN SIGN (<)
beginfig(60) ;
  pickup thin_pen;
  path less_than;
  less_than := ((1/2)*x_radius, (1/4)*y_radius)
               -- (-(1/2)*x_radius, Oy)
               -- ((1/2)*x_radius, -(1/4)*y_radius);
  draw less_than;
endfig;
