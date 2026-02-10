% U+0033 DIGIT THREE (3)
% Construction follows Ue003 (4015) loop vocabulary, mirrored to open left.
beginfig(51) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  % Upper loop opening left (mirrored standard loop)
  path upper_loop;
  upper_loop := (-x_radius, (1/2)*y_radius){up}
                .. tension 0.9
                .. (Ox, y_radius){right}
                .. tension 0.9
                .. (x_radius, Oy){down}
                .. tension 0.9
                .. (Ox, -.5*y_radius){left};
  upper_loop := upper_loop scaled (2/3) shifted (Ox, (1/3)*y_radius);
  draw upper_loop;

  % Lower loop opening left (mirrored standard loop)
  path lower_loop;
  lower_loop := (-x_radius, (-1/2)*y_radius){down}
                .. tension 0.9
                .. (Ox, -y_radius){right}
                .. tension 0.9
                .. (x_radius, Oy){up}
                .. tension 0.9
                .. (Ox, .5*y_radius){left};
  lower_loop := lower_loop scaled (2/3) shifted (Ox, -(1/3)*y_radius);
  draw lower_loop;

endfig;
