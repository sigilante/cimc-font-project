% U+0022 QUOTATION MARK (")
beginfig(34) ;
  pickup loz_pen rotated 90;
  path tick;
  tick := (Ox, y_radius)
          -- (Ox, (2/3)*y_radius);
  draw tick shifted (-(1/4)*x_radius, 0);
  draw tick shifted ((1/4)*x_radius, 0);
endfig;
