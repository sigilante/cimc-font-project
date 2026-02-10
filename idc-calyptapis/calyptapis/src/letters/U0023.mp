% U+0023 NUMBER SIGN (#)
beginfig(35) ;
  pickup loz_pen;
  path upper_bar, lower_bar;
  upper_bar := (-(1/2)*x_radius, (1/4)*y_radius)
               -- ((1/2)*x_radius, (1/4)*y_radius);
  draw upper_bar;

  lower_bar := (-(1/2)*x_radius, -(1/4)*y_radius)
               -- ((1/2)*x_radius, -(1/4)*y_radius);
  draw lower_bar;

  pickup loz_pen rotated 90;
  path left_bar, right_bar;
  left_bar := (-(1/4)*x_radius, (1/2)*y_radius)
              -- (-(1/4)*x_radius, -(1/2)*y_radius);
  draw left_bar;

  right_bar := ((1/4)*x_radius, (1/2)*y_radius)
               -- ((1/4)*x_radius, -(1/2)*y_radius);
  draw right_bar;
endfig;
