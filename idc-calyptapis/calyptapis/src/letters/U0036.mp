% U+0036 DIGIT SIX (6)
beginfig(54) ;
  numeric x_diam, y_diam;
  x_diam := 2 * x_radius;
  y_diam := 2 * y_radius;

  pickup thin_pen;

  % Lower bowl — closed circle scaled 2/3, shifted down
  path bowl;
  bowl := (Ox, y_radius){left}
          .. tension 0.9
          .. (-x_radius, Oy){down}
          .. tension 0.9
          .. (Ox, -y_radius){right}
          .. tension 0.9
          .. (x_radius, Oy){up}
          .. tension 0.9
          .. cycle;
  bowl := bowl scaled (2/3) shifted (Ox, -(1/3)*y_radius);
  draw bowl;

  % Ascending tail from the LEFT side of the bowl, sweeping up and right.
  % Overlaps with the bowl's left edge and extends to the top of the glyph.
  path tail;
  tail := (-(2/3)*x_radius, -(1/3)*y_radius){up}
          .. tension 0.9
          .. (Ox, y_radius){right};
  draw tail;

  pickup thin_pen;
  path upper_loop;
  upper_loop := (x_radius, (1/2)*y_radius){up}
                .. tension 0.9
                .. (Ox, y_radius){left}
                ;
  upper_loop := upper_loop scaled (2/3) shifted (0/3*x_radius, 1/3*y_radius);
  draw upper_loop;

endfig;
