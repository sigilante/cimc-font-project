% U+10405 DESERET CAPITAL LETTER LONG OO (𐐅)
beginfig(1029) ;
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

  draw outer_circle;

  pickup thin_pen;

  path bar;
  bar := (Ox, -y_radius) -- (Ox, y_radius);

  draw bar;
endfig;
