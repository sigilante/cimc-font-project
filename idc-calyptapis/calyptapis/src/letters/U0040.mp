% U+0040 COMMERCIAL AT (@)
beginfig(64) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  % Outer arc — nearly full circle, open at lower-right
  path outer_arc;
  outer_arc := (x_radius, -(1/3)*y_radius){down}
               .. tension 0.9
               .. (Ox, -y_radius){left}
               .. tension 0.9
               .. (-x_radius, Oy){up}
               .. tension 0.9
               .. (Ox, y_radius){right}
               .. tension 0.9
               .. (x_radius, (1/3)*y_radius){down};
  draw outer_arc;

  % Inner circle
  path inner;
  inner := (Ox, y_radius){left}
           .. tension 0.9
           .. (-x_radius, Oy){down}
           .. tension 0.9
           .. (Ox, -y_radius){right}
           .. tension 0.9
           .. (x_radius, Oy){up}
           .. tension 0.9
           .. cycle;
  inner := inner scaled (1/3);
  draw inner;
endfig;
