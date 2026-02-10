% U+0030 DIGIT ZERO (0)
beginfig(48) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  path outer_oval;
  outer_oval := (Ox, y_radius){left}
                .. tension 0.9
                .. (-0.75*x_radius, Oy){down}
                .. tension 0.9
                .. (Ox, -y_radius){right}
                .. tension 0.9
                .. (0.75*x_radius, Oy){up}
                .. tension 0.9
                .. cycle;

  draw outer_oval;

endfig;
