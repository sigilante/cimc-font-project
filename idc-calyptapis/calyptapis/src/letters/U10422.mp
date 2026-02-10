% U+10422 DESERET CAPITAL LETTER EL (𐐢)
beginfig(1058) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  path upper_loop;
  upper_loop := (x_radius, (1/2)*y_radius){up}
                .. tension 0.9
                .. (Ox, y_radius){left}
                .. tension 0.9
                .. (-x_radius, Oy){down}
                .. tension 0.9
                .. (-x_radius, -2y_radius){down}

                ;
  upper_loop := upper_loop scaled (2/3) shifted (2/3*x_radius, 1/3*y_radius);
  draw upper_loop;

  pickup loz_pen rotated 90;
  path serif;
  serif := point 0 of upper_loop - (0, 0.5*pen_height)
          -- point 0 of upper_loop;
  draw serif;

  pickup loz_pen;
  path lower_serif;
  lower_serif := (-(1/3) * x_radius, -y_radius)
                -- ((1/3) * x_radius, -y_radius);
  draw lower_serif;

  currentpicture := currentpicture reflectedabout((0,0),(x_radius,0));

  draw currentpicture;

endfig;
