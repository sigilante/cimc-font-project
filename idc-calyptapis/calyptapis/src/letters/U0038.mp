% U+0038 DIGIT EIGHT (8)
beginfig(56) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  % Upper loop — slightly smaller for optical balance
  path upper_loop;
  upper_loop := (Ox, y_radius){left}
                .. tension 0.9
                .. (-0.65*x_radius, (1/2)*y_radius){down}
                .. tension 0.9
                .. (Ox, Oy){right}
                .. tension 0.9
                .. (0.65*x_radius, (1/2)*y_radius){up}
                .. tension 0.9
                .. cycle;
  draw upper_loop;

  % Lower loop — slightly wider for stability
  path lower_loop;
  lower_loop := (Ox, Oy){left}
                .. tension 0.9
                .. (-0.75*x_radius, -(1/2)*y_radius){down}
                .. tension 0.9
                .. (Ox, -y_radius){right}
                .. tension 0.9
                .. (0.75*x_radius, -(1/2)*y_radius){up}
                .. tension 0.9
                .. cycle;
  draw lower_loop;

endfig;
