% U+10416 DESERET CAPITAL LETTER JEE (𐐖)
beginfig(1046) ;
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
                .. (Ox, -y_radius){right}
                .. tension 0.9
                .. (x_radius, (-1/2)*y_radius){up}
                ;
  upper_loop := upper_loop scaled (2/3) shifted (2/3*x_radius, 1/3*y_radius);
  draw upper_loop;

  pickup thin_pen;
  path bar;
  bar := (xpart point 4 of upper_loop, -y_radius)
         -- point 4 of upper_loop;
  draw bar;

  pickup loz_pen;
  path serif;
  serif := (-(1/3) * x_radius, y_radius)
          -- ((1/3) * x_radius, y_radius);
  draw serif shifted (xpart point 4 of upper_loop, -2.0 * y_radius);

  pickup loz_pen rotated 90;
  path serif;
  serif := (xpart point 0 of upper_loop, y_radius+0.5*pen_height)
           -- (xpart point 0 of upper_loop, (2/3)*y_radius);
  draw serif;

endfig;
