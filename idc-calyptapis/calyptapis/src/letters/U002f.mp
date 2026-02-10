% U+002F SOLIDUS (/)
beginfig(47) ;
  pickup loz_pen rotated angle(x_radius, 2*y_radius);
  path slash;
  slash := (-(1/2)*x_radius, -y_radius)
           -- ((1/2)*x_radius, y_radius);
  draw slash;
endfig;
