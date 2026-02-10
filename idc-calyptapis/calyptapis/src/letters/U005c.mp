% U+005C REVERSE SOLIDUS (\)
beginfig(92) ;
  pickup loz_pen rotated angle(x_radius, -2*y_radius);
  path backslash;
  backslash := (-(1/2)*x_radius, y_radius)
               -- ((1/2)*x_radius, -y_radius);
  draw backslash;
endfig;
