% U+10403 DESERET CAPITAL LETTER LONG AH (𐐃)
beginfig(1027) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

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

  path loop;
  loop = fullcircle xscaled x_radius yscaled y_radius shifted (0.1*x_radius, 0.5 * y_radius);
  draw (outer_circle cutbefore point 0.55 of outer_circle cutafter point 4 of outer_circle)
       .. (loop cutbefore point 3 of loop cutafter point 5 of loop)
       .. point 3 of outer_circle
       ;

  pickup loz_pen rotated 45;
  path serif;
  serif := subpath(0.45, 0.55) of outer_circle;
  draw serif;

endfig;
