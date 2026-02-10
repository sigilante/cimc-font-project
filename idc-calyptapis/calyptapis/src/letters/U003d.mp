% U+003D EQUALS SIGN (=)
beginfig(61) ;
  pickup loz_pen;
  path upper_bar;
  upper_bar := (-(1/2)*x_radius, (1/4)*y_radius)
               -- ((1/2)*x_radius, (1/4)*y_radius);
  draw upper_bar;

  path lower_bar;
  lower_bar := (-(1/2)*x_radius, -(1/4)*y_radius)
               -- ((1/2)*x_radius, -(1/4)*y_radius);
  draw lower_bar;
endfig;
