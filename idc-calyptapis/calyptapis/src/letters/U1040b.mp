% U+1040B DESERET CAPITAL LETTER SHORT OO (𐐋)
beginfig(1035) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  path bar;
  bar := (Ox, -y_radius) -- (Ox, (1/3)*y_radius);

  draw bar;

  pickup loz_pen;

  path serif;
  serif := (-(1/3) * x_radius, y_radius)
          -- ((1/3) * x_radius, y_radius);
  draw serif shifted (0, -2.0 * y_radius);

  pickup thin_pen;

  path outer_circle;
  outer_circle := (Ox, y_radius){left}
                  .. tension 0.9
                  .. (-x_radius, Oy){down}
                  .. tension 0.9
                  .. (Ox, -y_radius){right}
                  .. tension 0.9
                  .. (x_radius, Oy){up}
                  .. tension 0.9
                  .. cycle;

  draw outer_circle scaled (2/3) shifted (2/3*x_radius, 1/3*y_radius);

endfig;
