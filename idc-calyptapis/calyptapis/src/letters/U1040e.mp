% U+1040E DESERET CAPITAL LETTER WU (𐐎)
beginfig(1038);
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  path lower_circle;
  lower_circle := (Ox, y_radius){left}
                  .. tension 0.9
                  .. (-x_radius, Oy){down}
                  .. tension 0.9
                  .. (Ox, -y_radius){right}
                  .. tension 0.9
                  .. (x_radius, Oy){up}
                  .. tension 0.9
                  .. cycle;

  lower_circle := lower_circle scaled (2/3) shifted (2/3*x_radius, -1/3*y_radius);
  draw subpath (1, 3) of lower_circle;
  draw subpath (1, 3) of lower_circle shifted ((4/3)*x_radius,0);

  pickup thin_pen;

  pickup loz_pen rotated 90;
  path bar;
  bar := (Ox, y_radius)
         -- (point 1 of lower_circle);
  draw bar;
  draw bar shifted ((4/3)*x_radius,0);
  draw bar shifted ((8/3)*x_radius,0);

  pickup loz_pen;
  path serif;
  serif := (-(1/3) * x_radius, y_radius)
          -- ((1/3) * x_radius, y_radius);
  draw serif;
  draw serif shifted ((4/3)*x_radius,0);
  draw serif shifted ((8/3)*x_radius,0);
endfig;
