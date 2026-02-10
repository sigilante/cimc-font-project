% U+10427 DESERET CAPITAL LETTER EW (𐐧)
beginfig(1063) ;
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

  pickup loz_pen rotated -15;
  path beam;
  beam := (-0.5 * x_radius, Oy)
          -- (0.5 * x_radius, Oy);
  draw beam rotated -15;

endfig;
