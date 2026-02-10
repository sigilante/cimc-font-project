% U+1041F DESERET CAPITAL LETTER ESH (𐐟)
beginfig(1055) ;
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
                .. (-x_radius, -1.0*y_radius){down}
                .. tension 0.9
                .. (Ox, -2y_radius){right}
                .. tension 0.9
                .. (x_radius, (-3/2)*y_radius){up}
                ;
  upper_loop := upper_loop scaled (2/3) shifted (2/3*x_radius, 1/3*y_radius);
  draw upper_loop;

  pickup loz_pen rotated 90;
  draw (xpart point 0 of upper_loop, y_radius+0.375*pen_height)
      -- (xpart point 0 of upper_loop, -y_radius-0.375*pen_height);

  pickup loz_pen;
  serif := (xpart point 0 of upper_loop, y_radius)
          -- (xpart point 0 of upper_loop + (1/3)*x_radius, y_radius);
  draw serif;
  draw serif shifted (0, -2*y_radius);


  currentpicture := currentpicture reflectedabout((0,0),(0,y_radius));

  draw currentpicture;

endfig;
