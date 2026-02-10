% U+10400 DESERET CAPITAL LETTER LONG I (𐐀)
beginfig(1024) ;
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
  draw subpath (0, 3) of lower_circle;

  pickup thin_pen;

  path upper_circle;
  path lower_arc;
  lower_arc := (x_radius, Oy){down}
               .. tension 0.9
               .. (Ox, -y_radius){left};
  upper_circle := (-x_radius, (1/2)*y_radius){up}
                  .. tension 0.9
                  .. (Ox, y_radius){right}
                  .. tension 0.9
                  .. (x_radius, Oy){down};
  upper_circle := upper_circle scaled (2/3) shifted (2/3*x_radius, 1/3*y_radius);
  lower_arc    := lower_arc    scaled (2/3) shifted (2/3*x_radius, -1/3*y_radius);
  draw upper_circle
       .. tension 0.9
       .. lower_arc cutafter point 0.5 of lower_arc;

  pickup loz_pen rotated 90;
  path serif;
  serif := (xpart point 0 of lower_circle, ypart point 0 of lower_circle)
          -- (xpart point 0 of lower_circle, ypart point 0 of lower_circle-(1/3)*y_radius);
  draw serif;

endfig;
