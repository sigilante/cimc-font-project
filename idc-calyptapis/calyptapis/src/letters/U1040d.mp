% U+1040D DESERET CAPITAL LETTER OW (𐐍)
beginfig(1037);
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
  draw lower_loop;

  pickup loz_pen rotated 90;
  draw point 0 of upper_loop -- point 0 of lower_loop;

  pickup thin_pen;
  path loop;
  loop := (point 1 of upper_loop){down}
          .. tension 0.9
          .. (x_radius, 0.4*y_radius){right};
  draw loop;

  pickup loz_pen;
  path serif;
  serif := (x_radius, 0.4*y_radius)
          -- ((5/3)*x_radius, 0.4*y_radius);
  draw serif;
endfig;
