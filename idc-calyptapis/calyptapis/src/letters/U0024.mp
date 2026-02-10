% U+0024 DOLLAR SIGN ($)
beginfig(36) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  % Vertical bar through center
  path bar;
  bar := (Ox, -y_radius) -- (Ox, y_radius);
  draw bar;

  % S-curve (cf. Es U+1041D figure_eight, using half)
  path s_curve;
  s_curve := ((1/2)*x_radius, (2/3)*y_radius){up}
             .. tension 0.9
             .. (Ox, y_radius){left}
             .. tension 0.9
             .. (-(1/2)*x_radius, (1/2)*y_radius){down}
             .. tension 0.9
             .. (Ox, Oy){right}
             .. tension 0.9
             .. ((1/2)*x_radius, -(1/2)*y_radius){down}
             .. tension 0.9
             .. (Ox, -y_radius){left}
             .. tension 0.9
             .. (-(1/2)*x_radius, -(2/3)*y_radius){up};
  draw s_curve;
endfig;
