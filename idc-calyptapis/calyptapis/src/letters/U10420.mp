% U+10420 DESERET CAPITAL LETTER ZHEE (𐐠)
beginfig(1056);
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  path upper_loop;
  upper_loop := (x_radius, (1/2)*y_radius){up}
                .. tension 0.9
                .. (Ox, y_radius){left}
                .. tension 0.9
                .. (-x_radius, Oy){down}
                .. tension 0.9
                .. (Ox, -.5*y_radius){right}
                ;
  upper_loop := upper_loop scaled (2/3) shifted (2/3*x_radius, 1/3*y_radius);
  draw upper_loop;

  path lower_loop;
  lower_loop := (x_radius, (-1/2)*y_radius){down}
                .. tension 0.9
                .. (Ox, -y_radius){left}
                .. tension 0.9
                .. (-x_radius, Oy){up}
                .. tension 0.9
                .. (Ox, .5*y_radius){right}
                ;
  lower_loop := lower_loop scaled (2/3) shifted (2/3*x_radius, -1/3*y_radius);
  draw lower_loop reflectedabout ((0,0), (0,1)) shifted (4/3*x_radius, 0);

  pickup loz_pen rotated 90;
  path serif;
  serif := (xpart point 0 of upper_loop, y_radius+0.5*pen_height)
           -- (xpart point 0 of upper_loop, (2/3)*y_radius);
  draw serif;
  serif := (xpart point 0 of lower_loop, -y_radius-0.5*pen_height)
           -- (xpart point 0 of lower_loop, -(2/3)*y_radius);
  draw serif reflectedabout ((0,0), (0,1)) shifted (4/3*x_radius, 0);
endfig;
