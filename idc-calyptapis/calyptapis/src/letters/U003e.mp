% U+003E GREATER-THAN SIGN (>)
beginfig(62) ;
  pickup thin_pen;
  path greater_than;
  greater_than := (-(1/2)*x_radius, (1/4)*y_radius)
                  -- ((1/2)*x_radius, Oy)
                  -- (-(1/2)*x_radius, -(1/4)*y_radius);
  draw greater_than;
endfig;
