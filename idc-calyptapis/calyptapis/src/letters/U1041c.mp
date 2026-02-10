% U+1041C DESERET CAPITAL LETTER THEE (𐐜)
beginfig(1052);
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;
  path barl, barr;
  barr := (0.5x_radius, y_radius) -- (-0.5x_radius, -y_radius);
  draw subpath(0,0.5) of barr;
  barl := (-0.5x_radius, y_radius) -- (0.5x_radius, -y_radius);
  draw subpath(0,0.5) of barl;

  pickup loz_pen;
  path serif;
  serif := ((1/6) * x_radius, y_radius)
          -- ((5/6) * x_radius, y_radius);
  draw serif;
  draw serif shifted (-x_radius, 0);

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

  draw outer_circle scaled (1/2) shifted (0, -1/2*y_radius);

endfig;
